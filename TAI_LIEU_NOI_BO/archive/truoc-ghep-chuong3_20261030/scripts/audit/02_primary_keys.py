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
    with tempfile.TemporaryDirectory(prefix='instacart_keys_', dir=ARGS.temp_dir) as tmp:
        conn = database(tmp)
        try:
            for name in SCHEMAS:
                keys = ['order_id', 'product_id'] if name.startswith('order_products') else [SCHEMAS[name][0]]
                conn.execute('DROP TABLE IF EXISTS keys')
                declaration = ','.join(f'k{i} INTEGER NOT NULL' for i in range(len(keys)))
                pk = ','.join(f'k{i}' for i in range(len(keys)))
                conn.execute(f'CREATE TABLE keys ({declaration}, PRIMARY KEY ({pk})) WITHOUT ROWID')
                sql = 'INSERT OR IGNORE INTO keys VALUES (' + ','.join('?' for _ in keys) + ')'
                n = bad = valid = 0
                batch = []
                for row in rows(name):
                    n += 1
                    key = tuple(positive(row[k]) for k in keys)
                    if None in key:
                        bad += 1
                        continue
                    valid += 1
                    batch.append(key)
                    if len(batch) == 50000:
                        conn.executemany(sql, batch)
                        conn.commit()
                        batch.clear()
                conn.executemany(sql, batch)
                conn.commit()
                unique = conn.execute('SELECT COUNT(*) FROM keys').fetchone()[0]
                result[name] = {'key': keys, 'rows': n, 'invalid_key_rows': bad,
                                'distinct_valid_keys': unique, 'duplicate_extra_rows': valid - unique}
        finally:
            conn.close()
    result['note'] = 'Duplicate keys may have identical OR conflicting non-key values; no records are deleted. Numeric IDs are compared after whitespace/leading-zero normalization.'
    return result

if __name__ == '__main__':
    run(check, '02_primary_keys')
