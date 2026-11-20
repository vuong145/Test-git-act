#!/usr/bin/env python3
"""Read-only Instacart audit. Python 3.9+, standard library only."""
import argparse
import csv
import json
import re
import sqlite3
import sys
import tempfile
import time
from pathlib import Path
from collections import Counter
from functools import lru_cache

SCHEMAS = {
    'aisles': ['aisle_id', 'aisle'],
    'departments': ['department_id', 'department'],
    'products': ['product_id', 'product_name', 'aisle_id', 'department_id'],
    'orders': ['order_id', 'user_id', 'eval_set', 'order_number', 'order_dow',
               'order_hour_of_day', 'days_since_prior_order'],
    'order_products__prior': ['order_id', 'product_id', 'add_to_cart_order', 'reordered'],
    'order_products__train': ['order_id', 'product_id', 'add_to_cart_order', 'reordered'],
}
NUMBER = {'aisles': 1, 'departments': 2, 'order_products__prior': 3,
          'order_products__train': 4, 'orders': 5, 'products': 6}
MISSING = {'', 'nan', 'null', 'none', 'n/a', '?', 'unknown', 'chưa rõ', '-'}

def integer(value):
    value = value.strip()
    if not re.fullmatch(r'[+-]?[0-9]+', value):
        return None
    n = int(value)
    return n if -(2**63) <= n < 2**63 else None

def positive(value):
    n = integer(value)
    return n if n is not None and n > 0 else None

def resolve(folder, name):
    exact = folder / (name + '.csv')
    if exact.is_file():
        return exact
    candidates = []
    for p in folder.glob('*.csv'):
        if re.fullmatch(re.escape(name) + r'\(\d+\)', p.stem) or p.stem.endswith('Vương' + str(NUMBER[name])):
            candidates.append(p)
    if len(candidates) != 1:
        raise ValueError(f'{name}: need one CSV, found {len(candidates)} alternatives. '
                         'Keep only ONE dataset version in this folder, or use original filenames.')
    return candidates[0]


from decimal import Decimal, InvalidOperation
from itertools import zip_longest

TEXT_COLUMNS = {'aisle', 'department', 'product_name', 'eval_set'}

def records(folder, name):
    path = resolve(folder, name)
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != SCHEMAS[name]:
            raise ValueError(f'{path.name}: header mismatch: {reader.fieldnames}')
        for i, row in enumerate(reader, 1):
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f'{path.name}: malformed CSV record {i}')
            yield row

def decimal_value(value):
    try:
        number = Decimal(value.strip())
        return number if number.is_finite() else None
    except InvalidOperation:
        return None

def outside_domain(col, value):
    if col == 'eval_set':
        return value not in {'prior', 'train', 'test'}
    if col in TEXT_COLUMNS:
        return False
    n = decimal_value(value)
    if n is None:
        return True
    if col == 'days_since_prior_order':
        return not 0 <= n <= 30
    if n != n.to_integral_value():
        return True
    limits = {'reordered': (0, 1), 'order_dow': (0, 6),
              'order_hour_of_day': (0, 23), 'order_number': (1, 100)}
    if col in limits:
        lo, hi = limits[col]
        return not lo <= n <= hi
    return n <= 0

def category(col, before, after):
    a, b = before.strip(), after.strip()
    if a == b:
        return 'outer_whitespace_only'
    if a.lower() in MISSING and b.lower() in MISSING:
        return 'missing_token_representation'
    if b.lower() in MISSING and a.lower() not in MISSING:
        return 'information_replaced_by_missing'
    if a.lower() in MISSING and b.lower() not in MISSING:
        return 'missing_replaced_by_value'
    if col in TEXT_COLUMNS:
        if a.casefold() == b.casefold():
            return 'case_only_review_display_or_category'
        if col == 'eval_set' and b not in {'prior', 'train', 'test'}:
            return 'invalid_eval_label'
        return 'changed_text_or_category'
    x, y = decimal_value(a), decimal_value(b)
    if x is not None and y is not None and x == y:
        return 'numeric_value_preserved_format_changed'
    if x is not None and y is None:
        match = re.fullmatch(r'([+-]?(?:\d+(?:\.\d*)?|\.\d+))\s*(kg|USD|VND|đ|%)', b, re.IGNORECASE)
        if match and decimal_value(match.group(1)) == x:
            return 'original_number_plus_suffix_NOT_auto_repair'
    if outside_domain(col, b):
        return 'changed_to_invalid_value'
    return 'changed_to_plausible_but_different_value'

def compare(clean_dir, dirty_dir):
    result = {}
    for name in SCHEMAS:
        clean_path, dirty_path = resolve(clean_dir, name), resolve(dirty_dir, name)
        if clean_path.resolve() == dirty_path.resolve():
            raise ValueError('Clean and dirty inputs resolve to the SAME file: ' + name)
        keys = ['order_id', 'product_id'] if name.startswith('order_products') else [SCHEMAS[name][0]]
        counts, by_column, examples = Counter(), {}, []
        print('Comparing: ' + name, file=sys.stderr, flush=True)
        for index, (a, b) in enumerate(zip_longest(records(clean_dir, name), records(dirty_dir, name)), 1):
            if index % 2000000 == 0:
                print(f'  {index:,} paired record positions', file=sys.stderr, flush=True)
            if a is not None:
                counts['clean_rows'] += 1
            if b is not None:
                counts['dirty_rows'] += 1
            if a is None or b is None:
                counts['unpaired_record_positions'] += 1
                continue
            aligned = all(positive(a[k]) is not None and positive(a[k]) == positive(b[k]) for k in keys)
            if not aligned:
                counts['key_alignment_mismatch_positions'] += 1
                if len(examples) < 5:
                    examples.append({'record_position': index, 'kind': 'key_mismatch_or_reordered_rows',
                                     'clean_key': {k: a[k] for k in keys},
                                     'dirty_key': {k: b[k] for k in keys}})
                # Do NOT compare non-key fields belonging to potentially different entities.
                continue
            counts['aligned_rows'] += 1
            changed = False
            for col in SCHEMAS[name]:
                if a[col] == b[col]:
                    continue
                changed = True
                counts['changed_cells_on_aligned_rows'] += 1
                kind = category(col, a[col], b[col])
                entry = by_column.setdefault(col, {'changed_cells': 0, 'categories': Counter(), 'examples': []})
                entry['changed_cells'] += 1
                entry['categories'][kind] += 1
                if len(entry['examples']) < 2:
                    entry['examples'].append({'key': {k: a[k] for k in keys}, 'before': a[col], 'after': b[col], 'kind': kind})
            counts['changed_aligned_rows' if changed else 'identical_aligned_rows'] += 1
        result[name] = {
            'clean_file': clean_path.name, 'dirty_file': dirty_path.name,
            'clean_bytes': clean_path.stat().st_size, 'dirty_bytes': dirty_path.stat().st_size,
            'counts': dict(counts), 'by_column': by_column, 'alignment_examples': examples,
            'alignment_complete': not counts['key_alignment_mismatch_positions'] and not counts['unpaired_record_positions']}
    return result

def main():
    parser = argparse.ArgumentParser(description='Read-only comparison against original Instacart CSVs. No automatic cleaning.')
    parser.add_argument('--clean-dir', required=True, type=Path)
    parser.add_argument('--dirty-dir', required=True, type=Path)
    parser.add_argument('--out-dir', type=Path, default=Path(__file__).resolve().parent / 'dirty_audit_results')
    args = parser.parse_args()
    started = time.time()
    report = {'check': '06_compare_original', 'status': 'completed', 'scope': 'all rows; paired original versus dirty',
              'interpretation': [
                  'Original is a reference, not proof of real-world truth.',
                  'Comparison pairs record positions and verifies numeric primary/composite key equality BEFORE comparing other fields.',
                  'On mismatched positions, non-key fields are NOT compared. Mismatches may be key edits, inserted/deleted rows, or sorting; no inference of exact cause.',
                  'If alignment_complete is false, change counts cover aligned rows ONLY. Do not use as a complete difference audit.',
                  'Plausible-but-different values passed a local domain check; relational/history checks may still detect them.',
                  'Numeric suffix removal is NOT automatically safe. No repair is performed.',
                  'Unknown/missing-like text may need domain review; literal category name missing is preserved.' ]}
    code = 0
    try:
        report['results'] = compare(args.clean_dir, args.dirty_dir)
    except Exception as exc:
        report['status'] = 'ERROR_INCOMPLETE'
        report['error'] = str(exc)
        code = 1
    report['seconds'] = round(time.time() - started, 2)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    path = args.out_dir / '06_compare_original.txt'
    text = json.dumps(report, ensure_ascii=False, indent=2)
    path.write_text(text + '\n', encoding='utf-8')
    print(text)
    print('Report: ' + str(path), file=sys.stderr)
    return code

if __name__ == '__main__':
    raise SystemExit(main())
