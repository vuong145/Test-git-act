"""Verify published outputs and combine the two member reports."""
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path

import pandas as pd


def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def summarize():
    root = Path(__file__).resolve().parent.parent
    reports = root / 'BAO CAO' / 'Bao cao lam sach'
    data = root / 'DATA' / 'Data đã làm sạch'
    runs = {}
    before_after, actions = [], []
    comparisons = []
    checks = {}
    source_manifest = None
    for member in ['vuong', 'phong']:
        latest = json.loads((reports / member / 'latest.json').read_text('utf-8'))
        folder = reports / member / latest['run_dir']
        report = json.loads((folder / 'run_report.json').read_text('utf-8'))
        if report['status'] != 'completed':
            raise ValueError(f'{member}: chưa hoàn tất')
        if source_manifest is not None and source_manifest != report['inputs']:
            raise ValueError('Hai thành viên dùng nguồn khác nhau')
        source_manifest = report['inputs']
        runs[member] = {'report': str(folder.relative_to(root)),
                        'seconds': report['seconds'],
                        'peak_rss_bytes': report['sampled_process_peak_rss_bytes'],
                        'packages': report['packages'], 'python': report['python'],
                        'finished_at': report['created_at_local']}
        for table in report['tables_cleaned']:
            check = report['checks'][table]
            comparison = report['output_comparison'][table]
            if sha256(data / f'{table}.csv') != comparison['new_sha256']:
                raise ValueError(f'{table}: CSV hiện tại khác đầu ra đã kiểm chứng')
            checks[table] = check
            comparisons.append({'table': table, **comparison})
        before_after.append(pd.read_csv(folder / 'before_after.csv'))
        actions.append(pd.read_csv(folder / 'relational_summary.csv'))
    for table, manifest in source_manifest.items():
        if sha256(root / 'DATA' / 'Data đã làm nhiễu' / manifest['filename']) != manifest['sha256']:
            raise ValueError(f'{table}: nguồn đã thay đổi sau khi chạy')

    # A lightweight integrity join, not an EDA/modeling data product.
    train = pd.read_csv(data / 'order_products__train.csv',
                        usecols=['order_id', 'product_id'])
    orders = pd.read_csv(data / 'orders.csv',
                         usecols=['order_id', 'user_id', 'eval_set'])
    products = pd.read_csv(data / 'products.csv',
                           usecols=['product_id', 'aisle_id', 'department_id'])
    joined = train.merge(orders, on='order_id', how='left', validate='many_to_one')
    if joined.user_id.isna().any() or not joined.eval_set.eq('train').all():
        raise ValueError('Chi tiết train không khớp orders')
    joined = joined.merge(products, on='product_id', how='left', validate='many_to_one')
    for table, key in [('aisles', 'aisle_id'), ('departments', 'department_id')]:
        parent = pd.read_csv(data / f'{table}.csv', usecols=[key])
        joined = joined.merge(parent.assign(_found=True), on=key,
                              how='left', validate='many_to_one')
        if joined['_found'].isna().any():
            raise ValueError(f'Khóa ngoại thiếu trong {table}')
        joined = joined.drop(columns='_found')
    if len(joined) != len(train) or len(joined) < 1000000:
        raise ValueError('Merge làm thay đổi số dòng hoặc không đủ 1 triệu dòng')
    checks['train_merge'] = {
        'rows': len(joined), 'baskets': int(joined.order_id.nunique()),
        'users': int(joined.user_id.nunique()), 'many_to_one_validated': True,
        'at_least_100000': True, 'at_least_1000000': True, 'all_foreign_keys_matched': True,
    }
    before = pd.concat(before_after, ignore_index=True)
    before.to_csv(reports / 'before_after.csv', index=False, encoding='utf-8-sig')
    pd.concat(actions, ignore_index=True).to_csv(
        reports / 'relational_summary.csv', index=False, encoding='utf-8-sig')
    pd.DataFrame(comparisons).to_csv(reports / 'comparison_previous.csv',
                                    index=False, encoding='utf-8-sig')
    result = {'status': 'verified', 'runs': runs, 'checks': checks,
              'source_files_unchanged': True,
              'published_output_hashes_match_runs': True,
              'comparison_previous': comparisons,
              'verified_at': datetime.now(timezone(timedelta(hours=7))).isoformat()}
    (reports / 'verification.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = [
        '# Báo cáo làm sạch và nghiệm thu chung', '',
        f"Thời điểm xác minh: {result['verified_at']}", '',
        '## Kết quả', '',
        '| Bảng | Dòng đầu vào/đầu ra | Cột | Trùng byte với CSV trước chạy |',
        '|---|---:|---:|---|',
    ]
    for comparison in comparisons:
        table = comparison['table']
        check = checks[table]
        lines.append(f"| {table} | {check['output_rows']:,} | "
                     f"{len(check['output_columns'])} | "
                     f"{comparison['byte_identical_to_previous']} |")
    lines += [
        '', 'Đã đọc lại toàn bộ CSV đầu ra để kiểm tra schema, số dòng, '
        'chuỗi khóa, thứ tự tái dựng và thống kê thiếu. SHA-256 xác nhận '
        'nguồn nhiễu không đổi và CSV đã công bố khớp kết quả mỗi lần chạy.', '',
        'Kiểm tra nối train với orders, products, aisles và departments: '
        f"{len(joined):,} dòng, {joined.order_id.nunique():,} giỏ; "
        'mọi phép nối nhiều–một hợp lệ, không mất/nhân dòng. '
        'Đây là kiểm tra toàn vẹn, chưa triển khai EDA hoặc mô hình.', '',
        '## Sửa lỗi và khả năng chạy lại', '',
        '- Phong đọc đầy đủ mã đơn prior trước khi suy luận eval_set; '
        'phát hiện đơn trùng prior/train và kiểm tra một đơn cuối mỗi người.',
        '- Vương kiểm tra khóa ngoại prior theo mã thực trong orders/products.',
        '- Khóa ngoại products được đối chiếu bảng danh mục thực, không chỉ miền ID.',
        '- Cả hai dùng cùng quy tắc, kiểm tra số dòng/giỏ/lượt sửa theo cấu hình '
        'và đọc lại đầu ra trước khi thay CSV. Nếu khác bản cũ, lưu bản cũ trong previous_csv.',
        '- Báo cáo riêng chỉ đếm ba bảng được phân công; bảng tổng hợp nối kết quả hai người.',
        '', '## Số đo lần chạy', '',
        '| Script | Giây | RSS đỉnh lấy mẫu (MiB) |', '|---|---:|---:|',
    ]
    for member, run in runs.items():
        rss = run['peak_rss_bytes']
        lines.append(f"| {member} | {run['seconds']:.2f} | "
                     f"{rss / 1024**2:.2f} |" if rss else
                     f"| {member} | {run['seconds']:.2f} | Không đo được |")
    endings = [datetime.fromisoformat(run['finished_at']) for run in runs.values()]
    beginnings = [datetime.fromisoformat(run['finished_at']) - timedelta(seconds=run['seconds'])
                  for run in runs.values()]
    overlap = max(beginnings) < min(endings)
    execution_note = ('Hai script được chạy đồng thời trong phiên này. ' if overlap
                      else 'Hai script được chạy ở các khoảng thời gian không chồng nhau. ')
    lines += ['', execution_note + 'Số đo bao gồm '
              'hash và kiểm tra; không dùng làm so sánh tốc độ độc lập hoặc '
              'benchmark trước–sau tối ưu. RSS lấy mẫu 0,5 giây có thể bỏ lỡ đỉnh ngắn.',
              '', '## Giá trị còn thiếu', '']
    for row in before.itertuples():
        if row.missing_final:
            lines.append(f'- {row.table}.{row.column}: {row.missing_final:,}.')
    lines += ['', '## Giới hạn', '',
              'Không dùng dữ liệu gốc để điền. Thứ tự mua/thêm giỏ được tái dựng '
              'theo giả định thứ tự dòng đã bảo toàn; đây không phải chứng minh '
              'độc lập về thứ tự thật. Giá trị nằm trong miền hợp lệ vẫn có thể '
              'bị nhiễu. Các thuộc tính thiếu không đủ căn cứ vẫn để thiếu.', '',
              'Số ô thiếu ban đầu, ô không dùng được sau parse và ô thiếu cuối '
              'là ba khái niệm khác nhau; xem before_after.csv. Không cộng '
              'các lượt parse và tái dựng thành số ô duy nhất đã sửa.', '',
              '## Chạy lại', '',
              'Từ thư mục chứa bài tiểu luận: `python scripts/run_cleaning_all.py`. '
              'Hai entry point thành viên cũng chạy độc lập từ bất kỳ thư mục '
              'làm việc nào nhờ đường dẫn tương đối theo config.', '',
              'Kiểm thử: `python tests/test_cleaning.py`. Kiểm thử bao gồm '
              'chunk 1/2/3/100, giỏ qua ranh giới chunk, phân chia prior/train/test, '
              'khóa ngoại mồ côi và nhóm xuất hiện lại.']
    (reports / 'BAO_CAO_LAM_SACH.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return reports


if __name__ == '__main__':
    summarize()
