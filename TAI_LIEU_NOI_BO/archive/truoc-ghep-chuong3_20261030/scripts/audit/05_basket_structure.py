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
    with tempfile.TemporaryDirectory(prefix='instacart_baskets_', dir=ARGS.temp_dir) as tmp:
        conn = database(tmp)
        try:
            for part in ['prior', 'train']:
                conn.execute('DROP TABLE IF EXISTS positions')
                conn.execute('DROP TABLE IF EXISTS baskets')
                conn.execute('CREATE TABLE positions (oid INTEGER, pos INTEGER, PRIMARY KEY(oid,pos)) WITHOUT ROWID')
                conn.execute('CREATE TABLE baskets (oid INTEGER PRIMARY KEY, n INTEGER)')
                c = Counter()
                batch = []
                basket_counts = Counter()
                def flush():
                    conn.executemany('INSERT OR IGNORE INTO positions VALUES (?,?)', batch)
                    conn.executemany('INSERT INTO baskets VALUES (?,?) ON CONFLICT(oid) DO UPDATE SET n=n+excluded.n', basket_counts.items())
                    conn.commit()
                    batch.clear()
                    basket_counts.clear()
                for row in rows('order_products__' + part):
                    c['rows'] += 1
                    oid, pos = positive(row['order_id']), positive(row['add_to_cart_order'])
                    flag = integer(row['reordered'])
                    c['reordered_' + str(flag) if flag in (0, 1) else 'reordered_invalid_or_missing'] += 1
                    if oid is None:
                        c['invalid_order_id_rows'] += 1
                        continue
                    basket_counts[oid] += 1
                    if pos is None:
                        c['invalid_cart_position_rows'] += 1
                    else:
                        c['valid_position_rows'] += 1
                        batch.append((oid, pos))
                    if c['rows'] % 50000 == 0:
                        flush()
                flush()
                unique_pos = conn.execute('SELECT COUNT(*) FROM positions').fetchone()[0]
                c['duplicate_position_extra_rows'] = c['valid_position_rows'] - unique_pos
                c['baskets'] = conn.execute('SELECT COUNT(*) FROM baskets').fetchone()[0]
                c['max_observed_basket_rows'] = conn.execute('SELECT COALESCE(MAX(n),0) FROM baskets').fetchone()[0]
                sql = """SELECT b.oid,b.n,COUNT(p.pos),MIN(p.pos),MAX(p.pos)
                  FROM baskets b LEFT JOIN positions p ON b.oid=p.oid
                  GROUP BY b.oid
                  HAVING COUNT(p.pos)!=b.n OR MIN(p.pos)!=1 OR MAX(p.pos)!=b.n"""
                examples = []
                for oid, n, distinct, low, high in conn.execute(sql):
                    c['baskets_noncontiguous_or_invalid_positions'] += 1
                    if len(examples) < 5:
                        examples.append({'order_id': oid, 'rows': n, 'distinct_positions': distinct,
                                         'min_position': low, 'max_position': high})
                known = c['reordered_0'] + c['reordered_1']
                result[part] = {'counts': dict(c), 'reorder_rate_valid_rows': round(c['reordered_1']/known, 6) if known else None,
                                'position_examples': examples}
        finally:
            conn.close()
    result['note'] = 'Contiguous positions do NOT prove that the final basket was not truncated. No check can certify completeness without a full-source reference. Reordered is checked for 0/1 only, NOT against customer purchase history. Uses disk-backed SQLite; input row order does not matter.'
    return result

if __name__ == '__main__':
    run(check, '05_basket_structure')
