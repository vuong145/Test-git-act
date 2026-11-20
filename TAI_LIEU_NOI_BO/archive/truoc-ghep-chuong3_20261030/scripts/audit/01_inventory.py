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

def rows(name):
    path = resolve(ARGS.data_dir, name)
    FILES[name] = {'name': path.name, 'bytes': path.stat().st_size}
    print('Reading: ' + path.name, file=sys.stderr, flush=True)
    with path.open('r', encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != SCHEMAS[name]:
            raise ValueError(f'{path.name}: wrong header {reader.fieldnames}')
        for i, row in enumerate(reader, 1):
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f'{path.name}: malformed CSV record {i}')
            if i % 2000000 == 0:
                print(f'  {i:,} rows', file=sys.stderr, flush=True)
            yield row

def database(directory):
    conn = sqlite3.connect(str(Path(directory) / 'audit.sqlite'))
    conn.execute('PRAGMA journal_mode=OFF')
    conn.execute('PRAGMA synchronous=OFF')
    conn.execute('PRAGMA cache_size=-32768')
    conn.execute('PRAGMA temp_store=FILE')
    return conn

def run(check, name):
    global ARGS, FILES
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=Path(__file__).resolve().parent,
                        help='Folder containing ONE version of the six CSV files')
    parser.add_argument('--out-dir', type=Path, default=Path(__file__).resolve().parent / 'audit_results')
    parser.add_argument('--temp-dir', type=Path, default=None, help='Disk for temporary SQLite files')
    ARGS = parser.parse_args()
    ARGS.data_dir = ARGS.data_dir.resolve()
    FILES = {}
    started = time.time()
    report = {'check': name, 'status': 'completed', 'scope': 'all CSV records; no sampling'}
    code = 0
    try:
        report['results'] = check()
    except Exception as exc:
        report['status'] = 'ERROR_INCOMPLETE'
        report['error'] = str(exc)
        code = 1
    report['input_files'] = FILES
    report['seconds'] = round(time.time() - started, 2)
    ARGS.out_dir.mkdir(parents=True, exist_ok=True)
    dest = ARGS.out_dir / (name + '.txt')
    text = json.dumps(report, ensure_ascii=False, indent=2)
    dest.write_text(text + '\n', encoding='utf-8')
    print(text)
    print('Report: ' + str(dest), file=sys.stderr)
    raise SystemExit(code)


def check():
    result = {}
    limits = {'order_dow': (0, 6), 'order_hour_of_day': (0, 23),
              'order_number': (1, 100), 'reordered': (0, 1)}
    for name, columns in SCHEMAS.items():
        count = 0
        missing, invalid, spaces = Counter(), Counter(), Counter()
        examples = []
        for row in rows(name):
            count += 1
            for col, raw in row.items():
                value = raw.strip()
                if value != raw:
                    spaces[col] += 1
                if value.lower() in MISSING:
                    missing[col] += 1
                    continue
                bad = False
                if col.endswith('_id') or col in {'order_number', 'add_to_cart_order'}:
                    bad = positive(value) is None
                if col in limits:
                    num = integer(value)
                    low, high = limits[col]
                    bad = num is None or not low <= num <= high
                if col == 'days_since_prior_order':
                    try:
                        bad = not 0 <= float(value) <= 30
                    except ValueError:
                        bad = True
                if col == 'eval_set':
                    bad = value not in {'prior', 'train', 'test'}
                if bad:
                    invalid[col] += 1
                    if len(examples) < 3:
                        examples.append({'record': count, 'column': col, 'value': raw})
        result[name] = {'rows': count, 'columns': len(columns),
                        'missing_tokens': dict(missing), 'invalid_nonmissing': dict(invalid),
                        'outer_spaces': dict(spaces), 'examples': examples}
    result['note'] = 'The literal category name missing is NOT treated as a null. Integer fields reject 1.0; leading zeroes such as 08 are accepted. Missing-token counts are candidates, not deletion instructions.'
    return result

if __name__ == '__main__':
    run(check, '01_inventory')
