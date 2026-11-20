"""Phong: làm sạch products, orders và order_products__train.

Chạy: python scripts/cleaning/clean_phong.py   (cấu hình: config_phong.json)
Tái dựng order_number theo khách và khôi phục eval_set: đơn có trong prior là 'prior',
trong train là 'train', còn lại là 'test' khi mỗi khách có đúng một đơn cuối ngoài prior.
Chỉ đọc cột order_id của prior nhiễu để làm việc này, không sửa bảng prior.
"""
from collections import Counter
import hashlib

import pandas as pd

from common import (GOOD, RowSequence, append_csv, chunks, clean_detail, clean_dimension,
                    clean_frame, cli, export_query, insert, key_digest, read_ids)

TABLES = ['products', 'orders', 'order_products__train']


def clean_orders(c):
    db, audit = c.db, c.audit
    db.execute('CREATE TABLE orders (order_id INTEGER PRIMARY KEY, '
               'user_id INTEGER NOT NULL, order_number INTEGER)')
    count, digest = 0, hashlib.sha256()
    sequence = RowSequence(db, 'orders', 'user_id', 'order_number', audit, maximum=100)
    for raw in chunks(c.files['orders'], c.size, c.headers['orders']):
        frame = clean_frame(raw, 'orders', audit)
        sequence.apply(frame)
        insert(db, 'orders', frame[['order_id', 'user_id', 'order_number']])
        append_csv(frame, c.work / 'orders.pending')
        key_digest(digest, frame, 'orders')
        count += len(frame)
        print(f'orders: {count:,}', flush=True)
    sequence.finish()
    db.execute('''CREATE TEMP TABLE histories AS SELECT user_id, COUNT(*) AS n,
        COUNT(order_number) AS known, COUNT(DISTINCT order_number) AS distinct_n,
        MIN(order_number) AS min_n, MAX(order_number) AS max_n FROM orders GROUP BY user_id''')
    audit.checks['orders'] = {
        'input_rows': count, 'input_columns': c.headers['orders'],
        'input_key_sha256': digest.hexdigest(), 'primary_key_unique': True,
        **audit.checks.get('orders', {}),
        'users': db.execute('SELECT COUNT(*) FROM histories').fetchone()[0],
        'users_needing_sequence_review': db.execute(
            f'SELECT COUNT(*) FROM histories WHERE NOT {GOOD}').fetchone()[0]}
    export_query(db, f'SELECT * FROM histories WHERE NOT {GOOD} ORDER BY user_id LIMIT 20',
                 audit.folder / 'history_issue_examples.csv')
    return pd.Index(pd.read_sql_query('SELECT order_id FROM orders', db)['order_id'])


def finalize_orders(c):
    """Gán eval_set theo bảng sources; test = đơn cuối không thuộc prior/train."""
    db, audit, config = c.db, c.audit, c.audit.config
    db.execute("""CREATE TEMP TABLE partition_check AS SELECT o.user_id, COUNT(*) AS n,
        SUM(CASE WHEN s.source='prior' THEN 0 ELSE 1 END) AS nonprior,
        MAX(CASE WHEN s.source='prior' THEN NULL ELSE o.order_number END) AS final_n
        FROM orders o LEFT JOIN sources s ON o.order_id=s.order_id GROUP BY o.user_id""")
    bad, users = db.execute('SELECT SUM(nonprior<>1 OR final_n<>n), COUNT(*) '
                            'FROM partition_check').fetchone()
    n_test = db.execute('SELECT COUNT(*) FROM orders o LEFT JOIN sources s '
                        'ON o.order_id=s.order_id WHERE s.order_id IS NULL').fetchone()[0]
    if bad:
        raise ValueError(f'{bad} khách không có đúng một đơn cuối ngoài prior; không suy ra test')
    if config.get('expected_users', users) != users or config.get('expected_test_orders', n_test) != n_test:
        raise ValueError('Số khách hoặc số đơn test khác báo cáo kiểm tra')
    sources = pd.read_sql_query('SELECT order_id, source FROM sources', db).set_index('order_id')['source']
    totals = Counter()
    for frame in chunks(c.work / 'orders.pending', c.size, c.headers['orders']):
        source = frame['order_id'].astype('int64').map(sources)
        target, old = source.fillna('test'), frame['eval_set']
        if (old.ne('') & old.ne(target)).any():
            raise ValueError('Nhãn eval_set quan sát được mâu thuẫn phân chia; cần kiểm tra lại nguồn')
        for rule, mask in {'eval_recovered_prior': source.eq('prior') & old.eq(''),
                           'eval_recovered_train': source.eq('train') & old.eq(''),
                           'eval_inferred_test': source.isna() & old.eq(''),
                           'eval_observed_consistent': old.eq(target)}.items():
            audit.relational_counts[('orders', rule)] += int(mask.sum())
        frame['eval_set'] = target
        totals.update(target.value_counts().to_dict())
        append_csv(frame, c.work / 'orders.csv')
    audit.checks['orders'].update(
        final_eval_set_counts=dict(totals), prior_train_disjoint=True,
        users_with_invalid_final_partition=bad, test_orders=n_test,
        test_inference='complete audited files, neither source, exactly one final order per user')
    (c.work / 'orders.pending').unlink()


def steps(c):
    if not c.audit.config.get('infer_test_from_complete_partition'):
        raise ValueError('Cần bật kiểm chứng phân chia đầy đủ để suy luận test')
    clean_dimension('products', c)
    order_ids = clean_orders(c)
    prior = read_ids(c.files['order_products__prior'], 'order_id', c.size)   # chỉ cột khóa
    if not prior.isin(order_ids).all():
        raise ValueError('prior: order_id mồ côi')
    insert(c.db, 'sources', pd.DataFrame({'order_id': prior, 'source': 'prior'}))
    c.audit.checks['prior_dependency'] = {'unique_orders': len(prior),
                                          'order_foreign_keys_valid': True}
    clean_detail('order_products__train', c, order_ids, c.references['products'])
    finalize_orders(c)


if __name__ == '__main__':
    cli('phong', TABLES, steps)
