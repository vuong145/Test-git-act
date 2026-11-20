# Làm sạch dữ liệu — Hoàng Thanh Phong

## Phạm vi

Xuất ba bảng: products, orders, order_products__train. Cần đầy đủ sáu CSV nhiễu để kiểm tra quan hệ.
Không dùng các CSV gốc trong Chung/archive để điền dữ liệu.

## Chạy

Dùng Python 3.11 trở lên. Cài thư viện: `python -m pip install -r requirements.txt`.
Chạy: `python run_cleaning_phong.py`.
Có thể truyền `--config <đường_dẫn_json>`; đường dẫn tương đối được tính từ thư mục chứa config.
Chạy cả hai thành viên và nghiệm thu chung bằng `python scripts/run_cleaning_all.py`
trong thư mục bài tiểu luận.

## Quy tắc và kiểm tra

- Chuẩn hóa khoảng trắng, token thiếu theo từng cột; giữ nhãn danh mục hợp lệ `missing`.
- Kiểm tra định dạng, miền số và khóa; không tự đoán hậu tố đơn vị.
- Tái dựng order_number/add_to_cart_order theo giả định thứ tự dòng còn bảo toàn.
- Kiểm tra nhóm liên tục xuyên chunk, khóa duy nhất và khóa ngoại theo ID thực.
- Phong đọc mã đơn prior từ nguồn nhiễu trước khi kiểm tra phân chia prior/train/test.
- Đọc lại CSV sau xử lý; đối chiếu schema, số dòng, chuỗi khóa và số ô thiếu.
- Kiểm tra SHA-256 của cả sáu nguồn trước/sau; so sánh CSV mới với CSV đang có.
- Chỉ công bố đầu ra sau khi kiểm tra đạt. Bản cũ khác nội dung được sao lưu
  trong previous_csv của báo cáo lần chạy.

## Báo cáo

Báo cáo từng lần chạy nằm ở `Bao cao lam sach/phong/<run_id>` trong thư mục bài.
`latest.json` chỉ tới lần chạy thành công gần nhất. Có run_report.json,
comparison_previous.json, before_after.csv, final_column_summary.csv,
cleaning_summary.csv, relational_summary.csv, examples.csv và SUMMARY.md.
Nếu thất bại, failure.json ghi lỗi và không cập nhật latest.json.

Đầu ra chung là `Data đã làm sạch`; báo cáo tổng hợp do summarize_cleaning.py tạo.
Các module src ở hai gói được đồng bộ; khi sửa quy tắc cần cập nhật cả hai bản.

## Giới hạn

Khôi phục thứ tự dựa trên giả định, không chứng minh lại lịch sử thật.
Các tên, reordered và thời gian thiếu được giữ thiếu khi không đủ căn cứ.
Giá trị qua kiểm tra miền vẫn có thể là giá trị nhiễu hợp lệ về hình thức.
Không dùng số đo một lần chạy để kết luận tỷ lệ cải thiện tài nguyên.
