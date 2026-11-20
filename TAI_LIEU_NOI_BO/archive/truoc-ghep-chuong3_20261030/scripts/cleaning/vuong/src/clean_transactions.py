"""Chunked cleaning; quality information belongs only to separate reports."""
from collections import Counter
import hashlib
from pathlib import Path
import sqlite3

import pandas as pd

from .reconstruction import RowSequence

from .cleaning_rules import (
    append_csv, chunks, clean_frame, export_query, key_digest,
)


def clean_orders(files: dict, headers: dict, folder: Path,
                 db: sqlite3.Connection, audit, size: int) -> pd.Index:
    db.execute('CREATE TABLE orders (order_id INTEGER PRIMARY KEY, '
               'user_id INTEGER NOT NULL, order_number INTEGER)')
    count = 0
    digest = hashlib.sha256()
    sequence = RowSequence(db, 'orders', 'user_id', 'order_number', audit, maximum=100)
    for raw in chunks(files['orders'], size, headers['orders']):
        frame = clean_frame(raw, 'orders', audit)
        sequence.apply(frame)
        rows = frame[['order_id', 'user_id', 'order_number']]
        with db:
            db.executemany(
                'INSERT INTO orders VALUES (?,?,?)',
                rows.astype(object).where(rows.notna(), None)
                .itertuples(index=False, name=None),
            )
        append_csv(frame, folder / 'orders.pending')
        key_digest(digest, frame, 'orders')
        count += len(frame)
        print(f'orders: {count:,}', flush=True)
    audit.checks['orders'] = {
        'input_rows': count, 'input_columns': headers['orders'],
        'input_key_sha256': digest.hexdigest(), 'primary_key_unique': True,
    }
    sequence.finish()
    print('Kiểm tra cấu trúc thứ tự đơn theo khách...', flush=True)
    db.execute('CREATE INDEX orders_user ON orders(user_id)')
    db.execute('''CREATE TEMP TABLE histories AS
        SELECT user_id, COUNT(*) AS n, COUNT(order_number) AS known,
               COUNT(DISTINCT order_number) AS distinct_n,
               MIN(order_number) AS min_n, MAX(order_number) AS max_n
        FROM orders GROUP BY user_id''')
    good = '(known=n AND distinct_n=n AND min_n=1 AND max_n=n)'
    audit.checks['orders']['users'] = db.execute(
        'SELECT COUNT(*) FROM histories').fetchone()[0]
    audit.checks['orders']['users_needing_sequence_review'] = db.execute(
        f'SELECT COUNT(*) FROM histories WHERE NOT {good}').fetchone()[0]
    export_query(db, f'''SELECT * FROM histories WHERE NOT {good}
                     ORDER BY user_id LIMIT 20''',
                 audit.folder / 'history_issue_examples.csv')
    db.execute('DROP TABLE histories')
    return pd.Index(pd.read_sql_query(
        'SELECT order_id FROM orders', db)['order_id'])


def clean_detail(table: str, files: dict, headers: dict, folder: Path,
                 db: sqlite3.Connection, audit, size: int,
                 order_ids: pd.Index, product_ids: pd.Index) -> None:
    if not audit.config.get('reconstruct_sequences_from_preserved_row_order'):
        raise ValueError('Chưa xác nhận giả định thứ tự dòng')
    source = table.rsplit('__', 1)[1]
    db.execute('CREATE TABLE detail (order_id INTEGER, product_id INTEGER, '
               'pos INTEGER, PRIMARY KEY(order_id,product_id)) WITHOUT ROWID')
    count = 0
    digest = hashlib.sha256()
    sequence = RowSequence(db, table, 'order_id', 'add_to_cart_order', audit)
    temporary = folder / (table + '.pending')
    for raw in chunks(files[table], size, headers[table]):
        frame = clean_frame(raw, table, audit)
        if not frame['order_id'].isin(order_ids).all():
            raise ValueError(f'{table}: order_id mồ côi')
        if not frame['product_id'].isin(product_ids).all():
            raise ValueError(f'{table}: product_id mồ côi')
        sequence.apply(frame)
        rows = frame[['order_id', 'product_id', 'add_to_cart_order']]
        with db:
            db.executemany(
                'INSERT INTO detail VALUES (?,?,?)',
                rows.astype(object).where(rows.notna(), None)
                .itertuples(index=False, name=None),
            )
        append_csv(frame, temporary)
        key_digest(digest, frame, table)
        count += len(frame)
        print(f'{table}: {count:,}', flush=True)
    print(f'{table}: kiểm tra giỏ toàn bảng trên đĩa...', flush=True)
    db.execute('''CREATE TABLE basket AS
        SELECT order_id, COUNT(*) AS n, COUNT(pos) AS known,
               COUNT(DISTINCT pos) AS distinct_pos, MIN(pos) AS min_pos,
               MAX(pos) AS max_pos FROM detail GROUP BY order_id''')
    # PK order_id also rejects orders shared by prior and train.
    with db:
        db.execute('INSERT INTO sources SELECT order_id, ? FROM basket',
                   (source,))
    good = '(known=n AND distinct_pos=n AND min_pos=1 AND max_pos=n)'
    basket_count, largest = db.execute(
        'SELECT COUNT(*), MAX(n) FROM basket').fetchone()
    needs_review = db.execute(
        f'SELECT COUNT(*) FROM basket WHERE NOT {good}').fetchone()[0]
    duplicate_extra = db.execute(
        'SELECT COALESCE(SUM(known-distinct_pos),0) FROM basket').fetchone()[0]
    export_query(db, f'''SELECT order_id, n AS basket_size,
                     known AS parsed_positions,
                     known-distinct_pos AS duplicate_position_extra,
                     min_pos, max_pos FROM basket WHERE NOT {good}
                     ORDER BY order_id LIMIT 20''',
                 audit.folder / (source + '_basket_issue_examples.csv'))
    sizes = pd.read_sql_query('SELECT order_id, n FROM basket', db)
    sizes = sizes.set_index('order_id')['n']
    for frame in chunks(temporary, size, headers[table]):
        orders = frame['order_id'].astype('int64')
        position = pd.to_numeric(frame['add_to_cart_order'], errors='coerce')
        outside = position.gt(orders.map(sizes))
        audit.relational_counts[(table, 'position_exceeds_basket_size')] += int(
            outside.sum())
        frame.loc[outside, 'add_to_cart_order'] = ''
        # No status/display/source columns are ever written to this CSV.
        append_csv(frame, folder / files[table].name)
    audit.checks[table] = {
        'input_rows': count, 'input_columns': headers[table],
        'input_key_sha256': digest.hexdigest(), 'baskets': basket_count,
        'largest_basket': largest, 'primary_key_unique': True,
        'foreign_keys_valid': True,
        'baskets_needing_position_review': needs_review,
        'duplicate_position_extra': duplicate_extra,
        'positions_exceeding_basket_size_set_missing':
            audit.relational_counts[(table, 'position_exceeds_basket_size')],
    }
    sequence.finish()
    if needs_review != 0:
        raise ValueError(f'{table}: kiểm tra thứ tự sau tái dựng không đạt')
    temporary.unlink()
    db.execute('DROP TABLE detail')
    db.execute('DROP TABLE basket')
    db.commit()


def finalize_orders(files: dict, headers: dict, folder: Path,
                    db: sqlite3.Connection, audit, size: int) -> None:
    if not audit.config.get('infer_test_from_complete_partition'):
        raise ValueError('Chưa bật suy luận test từ phân chia đầy đủ')
    if not db.execute("SELECT COUNT(*) FROM sources WHERE source='prior'").fetchone()[0]:
        raise ValueError('Thiếu đơn prior trong sources; không suy luận test')
    # One and only one nonprior order per user, at reconstructed final position.
    db.execute("""CREATE TEMP TABLE partition_check AS
        SELECT o.user_id, COUNT(*) AS n,
               SUM(CASE WHEN s.source='prior' THEN 0 ELSE 1 END) AS nonprior,
               MAX(CASE WHEN s.source='prior' THEN NULL ELSE o.order_number END) AS final_n
        FROM orders o LEFT JOIN sources s ON o.order_id=s.order_id
        GROUP BY o.user_id""")
    bad = db.execute('SELECT COUNT(*) FROM partition_check WHERE nonprior<>1 OR final_n<>n').fetchone()[0]
    users = db.execute('SELECT COUNT(*) FROM partition_check').fetchone()[0]
    if bad:
        raise ValueError(f'{bad} khách không có đúng một đơn cuối ngoài prior; không suy ra test')
    expected_users = audit.config.get('expected_users')
    if expected_users is not None and users != expected_users:
        raise ValueError('Số khách khác báo cáo kiểm tra')
    n_test = db.execute('SELECT COUNT(*) FROM orders o LEFT JOIN sources s ON o.order_id=s.order_id WHERE s.order_id IS NULL').fetchone()[0]
    expected_test = audit.config.get('expected_test_orders')
    if expected_test is not None and n_test != expected_test:
        raise ValueError('Số đơn test suy luận khác báo cáo kiểm tra')
    sources = pd.read_sql_query('SELECT order_id, source FROM sources', db)
    sources = sources.set_index('order_id')['source']
    source_counts = Counter()
    for frame in chunks(folder / 'orders.pending', size, headers['orders']):
        source = frame['order_id'].astype('int64').map(sources)
        target = source.fillna('test')
        old = frame['eval_set'].copy()
        conflicts = old.ne('') & old.ne(target)
        if conflicts.any():
            raise ValueError('Nhãn eval_set quan sát được mâu thuẫn phân chia; cần kiểm tra lại nguồn')
        known = source.notna()
        counters = {
            'eval_recovered_prior': source.eq('prior') & old.eq(''),
            'eval_recovered_train': source.eq('train') & old.eq(''),
            'eval_inferred_test': ~known & old.eq(''),
            'eval_observed_consistent': old.eq(target),
        }
        for rule, mask in counters.items():
            audit.relational_counts[('orders', rule)] += int(mask.sum())
        frame['eval_set'] = target
        source_counts.update(target.value_counts().to_dict())
        append_csv(frame, folder / files['orders'].name)
    audit.checks['orders'].update(
        final_eval_set_counts=dict(source_counts), prior_train_disjoint=True,
        users_with_invalid_final_partition=bad, test_orders=n_test,
        test_inference='complete audited files, neither source, exactly one final order per user')
    (folder / 'orders.pending').unlink()
