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
    c = Counter()
    with tempfile.TemporaryDirectory(prefix='instacart_history_', dir=ARGS.temp_dir) as tmp:
        conn = database(tmp)
        try:
            conn.execute('CREATE TABLE history (uid INTEGER, num INTEGER, part TEXT)')
            batch = []
            for row in rows('orders'):
                c['rows'] += 1
                uid, num = positive(row['user_id']), positive(row['order_number'])
                part = row['eval_set'].strip()
                c['eval_' + part if part in {'prior', 'train', 'test'} else 'eval_invalid'] += 1
                raw = row['days_since_prior_order'].strip()
                is_missing = raw.lower() in MISSING
                if num == 1:
                    c['first_order_missing_days' if is_missing else 'first_order_has_days'] += 1
                elif num is not None:
                    c['later_order_missing_days' if is_missing else 'later_order_has_days'] += 1
                else:
                    c['cannot_classify_first_order'] += 1
                if not is_missing:
                    try:
                        valid = 0 <= float(raw) <= 30
                    except ValueError:
                        valid = False
                    if not valid:
                        c['days_invalid'] += 1
                if uid is None or num is None:
                    c['excluded_invalid_user_or_order_number'] += 1
                    continue
                batch.append((uid, num, part))
                if len(batch) == 50000:
                    conn.executemany('INSERT INTO history VALUES (?,?,?)', batch)
                    conn.commit()
                    batch.clear()
            conn.executemany('INSERT INTO history VALUES (?,?,?)', batch)
            conn.commit()
            conn.execute('CREATE INDEX user_idx ON history(uid)')
            query = """SELECT uid, COUNT(*), COUNT(DISTINCT num), MIN(num), MAX(num),
              SUM(CASE WHEN part IN ('train','test') THEN 1 ELSE 0 END),
              MAX(CASE WHEN part IN ('train','test') THEN num ELSE NULL END)
              FROM history GROUP BY uid"""
            examples = []
            for uid, n, unique, low, high, terminal, terminal_num in conn.execute(query):
                c['users'] += 1
                issues = []
                if n != unique:
                    c['users_duplicate_order_number'] += 1
                    issues.append('duplicate_order_number')
                if low != 1 or unique != high:
                    c['users_sequence_gap_or_missing_start'] += 1
                    issues.append('sequence_gap_or_missing_start')
                if terminal != 1:
                    c['users_terminal_count_not_one'] += 1
                    issues.append('terminal_count_not_one')
                if terminal and terminal_num != high:
                    c['users_terminal_not_last'] += 1
                    issues.append('terminal_not_last')
                if high > 100:
                    c['users_order_number_above_100'] += 1
                if issues and len(examples) < 5:
                    examples.append({'user_id': uid, 'issues': issues})
        finally:
            conn.close()
    return {'counts': dict(c), 'examples': examples,
            'note': 'Sequence/terminal failures may be caused by a truncated sample. This check does not reconstruct timestamps or validate purchase histories against product detail.'}

if __name__ == '__main__':
    run(check, '04_order_history')
