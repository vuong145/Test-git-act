"""Gộp báo cáo làm sạch của hai thành viên và xác minh sáu CSV đã xuất bản.

Chạy sau clean_vuong.py và clean_phong.py. Đối chiếu SHA-256 của CSV hiện tại với
new_sha256 trong run_report.json của lượt được latest.json trỏ tới; kiểm tra nguồn
nhiễu không đổi; nối thử train với orders/products/aisles/departments.

ĐỌC NHANH: gộp kết quả làm sạch của hai người và CHỨNG MINH sáu CSV sạch đúng là sản phẩm của các lượt đã kiểm chứng.
  Bốn khối: (1) đọc báo cáo mới nhất của từng người, so hash CSV; (2) nguồn nhiễu không đổi;
  (3) nối thử train với orders/products/aisles/departments để chắc khóa ngoại khớp; (4) gộp bảng và ghi verification.json.
  Đầu ra chính: before_after.csv (Bảng 'trước và sau'), relational_summary.csv, comparison_previous.csv, verification.json.
"""
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / 'BAO CAO' / 'Bao cao lam sach'
DATA = ROOT / 'DATA' / 'Data đã làm sạch'


def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    runs, checks, comparisons, before_after, actions, sources = {}, {}, [], [], [], None
    # Khối 1: mỗi người một báo cáo lượt chạy mới nhất; hai người phải dùng cùng nguồn nhiễu; hash CSV hiện tại phải khớp lượt đã kiểm chứng.
    for member in ['vuong', 'phong']:
        latest = json.loads((REPORTS / member / 'latest.json').read_text('utf-8'))
        folder = REPORTS / member / latest['run_dir']
        report = json.loads((folder / 'run_report.json').read_text('utf-8'))
        if report['status'] != 'completed':
            raise ValueError(f'{member}: chưa hoàn tất')
        if sources is not None and sources != report['inputs']:
            raise ValueError('Hai thành viên dùng nguồn khác nhau')
        sources = report['inputs']
        runs[member] = {'report': folder.relative_to(ROOT).as_posix(),
                        'seconds': report['seconds'], 'packages': report['packages'],
                        'python': report['python'], 'finished_at': report['created_at_local']}
        for table in report['tables_cleaned']:
            comparison = report['output_comparison'][table]
            if sha256(DATA / f'{table}.csv') != comparison['new_sha256']:
                raise ValueError(f'{table}: CSV hiện tại khác đầu ra đã kiểm chứng')
            checks[table] = report['checks'][table]
            comparisons.append({'table': table, **comparison})
        before_after.append(pd.read_csv(folder / 'before_after.csv'))
        actions.append(pd.read_csv(folder / 'relational_summary.csv'))
    # Khối 2: file nhiễu gốc không được thay đổi sau khi chạy làm sạch.
    for table, manifest in sources.items():
        if sha256(ROOT / 'DATA' / 'Data đã làm nhiễu' / manifest['filename']) != manifest['sha256']:
            raise ValueError(f'{table}: nguồn đã thay đổi sau khi chạy')

    # Kiểm tra toàn vẹn bằng phép nối nhiều–một; chưa phải bảng Master.
    # Khối 3: nối thử train với các bảng khác (many_to_one): không đổi số dòng, không khóa ngoại thiếu.
    train = pd.read_csv(DATA / 'order_products__train.csv', usecols=['order_id', 'product_id'])
    orders = pd.read_csv(DATA / 'orders.csv', usecols=['order_id', 'user_id', 'eval_set'])
    joined = train.merge(orders, on='order_id', how='left', validate='many_to_one')
    if joined.user_id.isna().any() or not joined.eval_set.eq('train').all():
        raise ValueError('Chi tiết train không khớp orders')
    joined = joined.merge(pd.read_csv(DATA / 'products.csv',
                                      usecols=['product_id', 'aisle_id', 'department_id']),
                          on='product_id', how='left', validate='many_to_one')
    for table, key in [('aisles', 'aisle_id'), ('departments', 'department_id')]:
        parent = pd.read_csv(DATA / f'{table}.csv', usecols=[key]).assign(_found=True)
        joined = joined.merge(parent, on=key, how='left', validate='many_to_one')
        if joined['_found'].isna().any():
            raise ValueError(f'Khóa ngoại thiếu trong {table}')
        joined = joined.drop(columns='_found')
    if len(joined) != len(train) or len(joined) < 1000000:
        raise ValueError('Merge làm thay đổi số dòng hoặc không đủ 1 triệu dòng')
    checks['train_merge'] = {
        'rows': len(joined), 'baskets': int(joined.order_id.nunique()),
        'users': int(joined.user_id.nunique()), 'many_to_one_validated': True,
        'at_least_100000': True, 'at_least_1000000': True, 'all_foreign_keys_matched': True}

    # Khối 4: gộp báo cáo hai người và ghi verification.json (trạng thái 'verified').
    pd.concat(before_after, ignore_index=True).to_csv(
        REPORTS / 'before_after.csv', index=False, encoding='utf-8-sig')
    pd.concat(actions, ignore_index=True).to_csv(
        REPORTS / 'relational_summary.csv', index=False, encoding='utf-8-sig')
    pd.DataFrame(comparisons).to_csv(REPORTS / 'comparison_previous.csv',
                                     index=False, encoding='utf-8-sig')
    result = {'status': 'verified', 'runs': runs, 'checks': checks,
              'source_files_unchanged': True, 'published_output_hashes_match_runs': True,
              'comparison_previous': comparisons,
              'verified_at': datetime.now(timezone(timedelta(hours=7))).isoformat()}
    (REPORTS / 'verification.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"VERIFIED: 6 CSV; train merge {len(joined):,} dòng, "
          f"{joined.order_id.nunique():,} giỏ")


if __name__ == '__main__':
    main()
