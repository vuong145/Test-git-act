"""Human-readable account of observed repairs and unresolved data."""

def write_summary(folder, audit):
    lines = ['# Kết quả làm sạch v4 — đã đọc lại CSV đầu ra', '',
             'Hai cột thứ tự được tái dựng theo GIẢ ĐỊNH thứ tự dòng gốc tương ứng thứ tự mua/thêm giỏ. Đây không phải đối chiếu với giá trị gốc đã biết.', '',
             '| Bảng | Điền ô chưa dùng được | Sửa số lệch vị trí dòng | Số đã khớp |',
             '|---|---:|---:|---:|']
    for table in ['orders', 'order_products__prior', 'order_products__train']:
        if table not in audit.checks:
            continue
        vals = [audit.relational_counts[(table,r)] for r in ['sequence_filled_unusable','sequence_corrected_observed','sequence_observed_consistent']]
        lines.append('| '+table+' | '+' | '.join(f'{n:,}' for n in vals)+' |')
    lines += ['', '## eval_set', '']
    for rule in ['eval_recovered_prior','eval_recovered_train','eval_inferred_test','eval_observed_consistent']:
        if 'orders' not in audit.checks:
            continue
        lines.append(f"- {rule}: {audit.relational_counts[('orders',rule)]:,}")
    lines += ['', '## Các giá trị vẫn thiếu', '']
    for (table,column,state), count in sorted(audit.final_counts.items()):
        if state=='missing' and count:
            lines.append(f'- {table}.{column}: {count:,}')
    lines += ['', 'Tên đã mất không được thay bằng tên quầy hoặc tên phổ biến. reordered không được suy đoán. Giờ, thứ trong tuần và khoảng cách đơn thiếu không được điền trung bình/mode.',
              '', 'Các trạng thái trong cleaning_summary.csv là lượt parse ban đầu. Số ô cuối xem final_column_summary.csv và before_after.csv. Việc sửa thứ tự nằm trong relational_summary.csv, không cộng hai lượt để đếm số ô dữ liệu.',
              '', 'Trong examples.csv, các mục sequence_* có raw là giá trị SAU parse ban đầu; chuỗi trước parse được lấy mẫu riêng theo trạng thái làm sạch. Chỉ lưu tối đa 5 ví dụ mỗi loại để giảm dung lượng.',
              '', 'Không dùng thứ tự đã tái dựng làm bằng chứng độc lập xác nhận giả định tái dựng là đúng. Nếu phân tích hành vi tuần tự, phải công bố giả định và đánh giá độ nhạy.']
    (folder/'SUMMARY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
