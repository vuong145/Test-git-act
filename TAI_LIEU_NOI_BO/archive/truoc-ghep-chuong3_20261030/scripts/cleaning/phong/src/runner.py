"""Reproducible member cleaning runs, staged output and explicit validation."""
import argparse
import ctypes
from datetime import datetime, timezone, timedelta
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import sqlite3
import sys
import threading
import time

import numpy as np
import pandas as pd

from .cleaning_rules import (
    Audit, append_csv, chunks, clean_frame, inspect_headers, key_digest,
    resolve_files, verify_outputs,
)
from .clean_transactions import clean_detail, clean_orders, finalize_orders
from .reporting import write_summary


def sha256(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2),
                          encoding='utf-8')


def current_rss():
    """Use psutil when available, otherwise Windows' process memory API."""
    try:
        import psutil
        return psutil.Process().memory_info().rss
    except ImportError:
        if os.name != 'nt':
            return None
        class Counters(ctypes.Structure):
            _fields_ = [('cb', ctypes.c_ulong), ('faults', ctypes.c_ulong)] + [
                (name, ctypes.c_size_t) for name in (
                    'peak_ws', 'ws', 'peak_paged', 'paged', 'peak_nonpaged',
                    'nonpaged', 'pagefile', 'peak_pagefile')]
        counters = Counters()
        counters.cb = ctypes.sizeof(counters)
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        psapi = ctypes.WinDLL('psapi', use_last_error=True)
        psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p,
                                               ctypes.c_void_p,
                                               ctypes.c_ulong]
        if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(),
                                          ctypes.byref(counters), counters.cb):
            raise ctypes.WinError(ctypes.get_last_error())
        return counters.ws


def read_ids(path, column, size, unique=False):
    """Read only keys from noisy input; never use original clean data to fill."""
    pieces = []
    with pd.read_csv(path, usecols=[column], dtype='string',
                     keep_default_na=False, chunksize=size,
                     encoding='utf-8-sig', skip_blank_lines=False) as reader:
        for frame in reader:
            values = frame[column].str.strip()
            if not values.str.fullmatch(r'\d+').all():
                raise ValueError(f'{path.name}.{column}: khóa sai định dạng')
            numbers = pd.to_numeric(values, errors='raise')
            if not numbers.between(1, 2147483647).all():
                raise ValueError(f'{path.name}.{column}: khóa ngoài miền')
            pieces.append(numbers.astype('int64').to_numpy())
    result = pd.Index(np.concatenate(pieces))
    if unique and result.has_duplicates:
        raise ValueError(f'{path.name}: trùng khóa {column}')
    return result if unique else result.unique()


def clean_dimension(table, files, headers, work, audit, references):
    key = {'aisles': 'aisle_id', 'departments': 'department_id',
           'products': 'product_id'}[table]
    raw = pd.concat(list(chunks(files[table], 100000, headers[table])),
                    ignore_index=True)
    frame = clean_frame(raw, table, audit)
    if frame[key].duplicated().any():
        raise ValueError(f'{table}: trùng khóa chính')
    if table == 'products':
        for parent, fk in [('aisles', 'aisle_id'),
                           ('departments', 'department_id')]:
            if not frame[fk].isin(references[parent]).all():
                raise ValueError(f'products: khóa ngoại mồ côi {fk}')
    digest = hashlib.sha256()
    key_digest(digest, frame, table)
    append_csv(frame, work / files[table].name)
    audit.checks[table] = {
        'input_rows': len(frame), 'input_columns': headers[table],
        'input_key_sha256': digest.hexdigest(),
        'primary_key_unique': True, 'foreign_keys_valid': True,
    }


def check_expected(audit):
    """Expected counts are regression checks, never values used to repair data."""
    config = audit.config
    for field, observed in [('expected_rows', 'output_rows'),
                            ('expected_baskets', 'baskets')]:
        for table, expected in config.get(field, {}).items():
            if audit.checks[table][observed] != expected:
                raise ValueError(f'{table}: không khớp {field}')
    for table, rules in config.get('expected_sequence_actions', {}).items():
        for rule, expected in rules.items():
            if audit.relational_counts[(table, rule)] != expected:
                raise ValueError(f'{table}.{rule}: số xử lý khác đối chứng')
    for rule, expected in config.get('expected_eval_recoveries', {}).items():
        if audit.relational_counts[('orders', rule)] != expected:
            raise ValueError(f'orders.{rule}: số khôi phục khác đối chứng')


def run_member(config, config_dir, member):
    started = time.perf_counter()
    config_dir = Path(config_dir).resolve()
    paths = {key: (config_dir / config[key]).resolve()
             for key in ['input_dir', 'output_dir', 'report_dir']}
    if paths['input_dir'] == paths['output_dir']:
        raise ValueError('Thư mục đầu ra phải khác dữ liệu nguồn')
    if not config.get('reconstruct_sequences_from_preserved_row_order'):
        raise ValueError('Cần xác nhận giả định tái dựng thứ tự trong config')
    if member == 'phong' and not config.get('infer_test_from_complete_partition'):
        raise ValueError('Cần bật kiểm chứng phân chia đầy đủ để suy luận test')
    size = int(config.get('chunksize', 250000))
    if size < 1:
        raise ValueError('chunksize phải dương')
    assigned = (['aisles', 'departments', 'order_products__prior']
                if member == 'vuong' else
                ['products', 'orders', 'order_products__train'])
    files = resolve_files(paths['input_dir'])
    headers = inspect_headers(files)
    stamp = datetime.now(timezone(timedelta(hours=7))).strftime('%Y%m%d_%H%M%S_%f')
    reports = paths['report_dir'] / stamp
    work = reports / '_staging'
    work.mkdir(parents=True)
    paths['output_dir'].mkdir(parents=True, exist_ok=True)
    write_json(reports / 'config_used.json', config)
    audit = Audit(reports, config)
    stop = threading.Event()
    memory = {'peak': 0, 'errors': []}

    def monitor():
        while not stop.is_set():
            try:
                rss = current_rss()
                if rss is not None:
                    memory['peak'] = max(memory['peak'], rss)
            except Exception as exc:
                if not memory['errors']:
                    memory['errors'].append(str(exc))
            stop.wait(0.5)

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()
    db = sqlite3.connect(work / 'audit.sqlite')
    try:
        print(f'[{member}] SHA-256: toàn bộ 6 nguồn nhiễu', flush=True)
        inputs = {t: {'sha256': sha256(p), 'bytes': p.stat().st_size,
                      'filename': p.name} for t, p in files.items()}
        for table, expected in config.get('expected_source_sha256', {}).items():
            if inputs[table]['sha256'] != expected:
                raise ValueError(f'{table}: SHA-256 nguồn khác cấu hình')
        references = {t: read_ids(files[t], key, size, unique=True)
                      for t, key in [('aisles', 'aisle_id'),
                                     ('departments', 'department_id'),
                                     ('products', 'product_id'),
                                     ('orders', 'order_id')]}
        db.execute('CREATE TABLE sources '
                   '(order_id INTEGER PRIMARY KEY, source TEXT NOT NULL)')
        if member == 'vuong':
            for table in ['aisles', 'departments']:
                clean_dimension(table, files, headers, work, audit, references)
            clean_detail('order_products__prior', files, headers, work, db,
                         audit, size, references['orders'], references['products'])
        else:
            clean_dimension('products', files, headers, work, audit, references)
            order_ids = clean_orders(files, headers, work, db, audit, size)
            # Prior is a dependency even though Phong exports only three tables.
            # Stream unique order IDs per chunk; no prior attributes are repaired here.
            prior_count = 0
            with pd.read_csv(files['order_products__prior'],
                             usecols=['order_id'], dtype='string',
                             keep_default_na=False, chunksize=size,
                             encoding='utf-8-sig', skip_blank_lines=False) as reader:
                for frame in reader:
                    values = frame['order_id'].str.strip()
                    if not values.str.fullmatch(r'\d+').all():
                        raise ValueError('prior: order_id không hợp lệ')
                    ids = pd.to_numeric(values, errors='raise')
                    if not ids.isin(order_ids).all():
                        raise ValueError('prior: order_id mồ côi')
                    with db:
                        db.executemany('INSERT OR IGNORE INTO sources VALUES (?, ?)',
                                       ((int(x), 'prior') for x in ids.unique()))
                    prior_count += len(frame)
            audit.checks['prior_dependency'] = {
                'rows_read': prior_count,
                'unique_orders': db.execute('SELECT COUNT(*) FROM sources').fetchone()[0],
                'order_foreign_keys_valid': True,
            }
            clean_detail('order_products__train', files, headers, work, db,
                         audit, size, order_ids, references['products'])
            finalize_orders(files, headers, work, db, audit, size)
        selected = {t: files[t] for t in assigned}
        verify_outputs(selected, headers, work, audit, size)
        check_expected(audit)
        # Verify every dependency remained unchanged during execution.
        if any(sha256(files[t]) != inputs[t]['sha256'] for t in files):
            raise ValueError('Dữ liệu nguồn thay đổi trong lúc chạy')
        comparisons = {}
        for table in assigned:
            fresh = work / files[table].name
            previous = paths['output_dir'] / files[table].name
            digest = sha256(fresh)
            old = sha256(previous) if previous.exists() else None
            comparisons[table] = {
                'new_sha256': digest, 'previous_sha256': old,
                'byte_identical_to_previous': old == digest if old else None,
            }
            if previous.exists() and old != digest:
                backup = reports / 'previous_csv'
                backup.mkdir(exist_ok=True)
                shutil.copy2(previous, backup / previous.name)
        audit.save()
        write_summary(reports, audit)
        write_json(reports / 'comparison_previous.json', comparisons)
        # Publish only after all member outputs and source hashes have passed.
        for table in assigned:
            dst = paths['output_dir'] / files[table].name
            src = work / files[table].name
            for attempt in range(5):
                try:
                    if dst.exists():
                        dst.unlink()
                    shutil.move(str(src), str(dst))
                    break
                except OSError:
                    if attempt == 4:
                        raise
                    time.sleep(0.1)
        code_files = list(Path(__file__).parent.glob('*.py'))
        code_root = Path(__file__).resolve().parent.parent
        code_files += list(code_root.glob('run_cleaning_*.py'))
        result = {
            'status': 'completed', 'code_version': '4.0_verified_member_runs',
            'assigned_to': config['assigned_to'], 'tables_cleaned': assigned,
            'created_at_local': datetime.now(timezone(timedelta(hours=7))).isoformat(),
            'seconds': round(time.perf_counter() - started, 2),
            'sampled_process_peak_rss_bytes': memory['peak'] or None,
            'rss_sampling_seconds': 0.5, 'memory_measurement_error': memory['errors'],
            'python': platform.python_version(), 'platform': platform.platform(),
            'packages': {'pandas': pd.__version__, 'numpy': np.__version__},
            'inputs': inputs, 'checks': audit.checks,
            'output_comparison': comparisons,
            'code_sha256': {str(p.relative_to(code_root)): sha256(p) for p in code_files},
            'source_hashes_unchanged': True,
            'assumptions': ['CSV rows preserve original purchase/cart encounter order.'],
            'limitations': ['Sequence semantics are assumed, not independently proven.',
                            'Valid-domain values may still be corrupted.',
                            'Unrecoverable attributes remain missing.',
                            'Sampled RSS may miss brief peaks.'],
        }
        write_json(reports / 'run_report.json', result)
        write_json(paths['report_dir'] / 'latest.json', {'run_dir': stamp})
        print(f'[{member}] HOÀN TẤT: {reports}', flush=True)
        return reports
    except Exception as exc:
        write_json(reports / 'failure.json', {'status': 'failed', 'error': str(exc)})
        raise
    finally:
        stop.set()
        thread.join()
        db.close()
        # Only this run's generated staging directory is removed.
        if work.resolve().parent != reports.resolve():
            raise RuntimeError('Unsafe staging path')
        shutil.rmtree(work)


def cli(member, entry_file):
    for stream in [sys.stdout, sys.stderr]:
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='replace')
    parser = argparse.ArgumentParser(description=f'Làm sạch có kiểm chứng: {member}')
    parser.add_argument('--config', type=Path,
                        default=Path(entry_file).with_name(f'config_{member}.json'))
    args = parser.parse_args()
    path = args.config.resolve()
    run_member(json.loads(path.read_text(encoding='utf-8-sig')), path.parent, member)
