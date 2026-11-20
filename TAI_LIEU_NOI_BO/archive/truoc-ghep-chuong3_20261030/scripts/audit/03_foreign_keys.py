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
    with tempfile.TemporaryDirectory(prefix='instacart_fk_', dir=ARGS.temp_dir) as tmp:
        conn = database(tmp)
        try:
            parents = {}
            for name, key in [('aisles', 'aisle_id'), ('departments', 'department_id'), ('products', 'product_id')]:
                values = set()
                counts = Counter()
                for row in rows(name):
                    k = positive(row[key])
                    if k is not None:
                        counts['valid_rows'] += 1
                        values.add(k)
                    else:
                        counts['invalid_primary_key'] += 1
                    if name == 'products':
                        for col, parent in [('aisle_id', 'aisles'), ('department_id', 'departments')]:
                            v = positive(row[col])
                            counts[col + '_invalid' if v is None else col + '_unmatched' if v not in parents[parent] else col + '_matched'] += 1
                parents[name] = values
                counts['distinct_ids'] = len(values)
                counts['duplicate_extra_primary_keys'] = counts['valid_rows'] - len(values)
                result[name] = dict(counts)
            conn.execute('CREATE TABLE orders (id INTEGER PRIMARY KEY, eval TEXT)')
            batch = []
            oc = Counter()
            for row in rows('orders'):
                oc['rows'] += 1
                oid = positive(row['order_id'])
                if oid is None:
                    oc['invalid_id'] += 1
                    continue
                batch.append((oid, row['eval_set'].strip()))
                if len(batch) == 50000:
                    conn.executemany('INSERT INTO orders VALUES (?,?)', batch)
                    batch.clear()
                    conn.commit()
            conn.executemany('INSERT INTO orders VALUES (?,?)', batch)
            conn.commit()
            result['orders'] = dict(oc)
            @lru_cache(maxsize=100000)
            def lookup(oid):
                return conn.execute('SELECT eval FROM orders WHERE id=?', (oid,)).fetchone()
            for part in ['prior', 'train']:
                counts = Counter()
                examples = []
                for row in rows('order_products__' + part):
                    counts['rows'] += 1
                    oid, pid = positive(row['order_id']), positive(row['product_id'])
                    order = lookup(oid) if oid is not None else None
                    order_ok = order is not None
                    prod_ok = pid in parents['products']
                    counts['order_id_invalid' if oid is None else 'order_matched' if order_ok else 'order_unmatched'] += 1
                    counts['product_id_invalid' if pid is None else 'product_matched' if prod_ok else 'product_unmatched'] += 1
                    if order_ok and order[0] != part:
                        counts['eval_set_mismatch'] += 1
                    if order_ok and prod_ok:
                        counts['rows_with_both_parents'] += 1
                    elif len(examples) < 3:
                        examples.append({'order_id': row['order_id'], 'product_id': row['product_id']})
                result[part] = dict(counts)
                result[part]['examples_missing_parent'] = examples
        finally:
            conn.close()
    result['note'] = 'Unmatched means absent from supplied files, not necessarily absent from the full source. Duplicate order IDs stop this check; resolve check 02 first. Parent uniqueness is audited in check 02.'
    return result

if __name__ == '__main__':
    run(check, '03_foreign_keys')
