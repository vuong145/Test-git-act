# Kiểm tra dữ liệu bị làm nhiễu so với bản gốc

## Chạy một lệnh

Cần Python 3.9+; không cần cài thư viện ngoài. Giữ hai thư mục riêng: sáu CSV gốc và sáu CSV bị làm nhiễu. Giải nén bộ code, mở Terminal tại thư mục có RUN_CHECKS.py:

```powershell
python RUN_CHECKS.py --clean-dir "D:\Instacart\data_goc" --dirty-dir "D:\Instacart\data_rac"
```

Thay HAI đường dẫn bằng đường dẫn thật. Nếu máy dùng `py`, thay `python` bằng `py`.

Gửi lại TẤT CẢ file .txt trong `dirty_audit_results` cạnh code, kể cả file báo lỗi. Có 6 báo cáo kiểm tra và 1 file tổng kết chạy. Chạy lại sẽ ghi đè báo cáo cùng tên. Để giữ một lần chạy riêng, thêm `--out-dir "D:\ket_qua_rac_lan_2"`.

Chương trình tự chạy tuần tự, không sửa hoặc xóa CSV. Không cần đặt code cạnh dữ liệu.

## Bảy file Python

- RUN_CHECKS.py: chạy tất cả các kiểm tra tuần tự, tiếp tục các kiểm tra còn lại nếu một kiểm tra lỗi.
- 01_inventory.py đến 05_basket_structure.py: năm kiểm tra đã dùng trên bản gốc, nay áp dụng cho bản nhiễu.
- 06_compare_original.py: kiểm tra mới, đối chiếu toàn bộ bản nhiễu với bản gốc.

Có thể chạy riêng phép đối chiếu:

```powershell
python 06_compare_original.py --clean-dir "D:\Instacart\data_goc" --dirty-dir "D:\Instacart\data_rac"
```

Có thể chạy riêng năm kiểm tra nội bộ, ví dụ:

```powershell
python 03_foreign_keys.py --data-dir "D:\Instacart\data_rac" --out-dir "dirty_audit_results"
```

## Tên CSV

Nhận tên gốc aisles.csv, departments.csv, products.csv, orders.csv, order_products__prior.csv, order_products__train.csv.

Cũng nhận tên nộp bài kết thúc bằng Vương1.csv đến Vương6.csv theo ánh xạ:
1 aisles, 2 departments, 3 prior, 4 train, 5 orders, 6 products.

Nhận một bản hậu tố tải xuống như products(2).csv nếu không có tên gốc. Nếu có tên gốc, tên đó được ưu tiên. Không để lẫn nhiều phiên bản trong cùng thư mục. Mỗi bảng phải là một tệp đầy đủ, không phải hai tệp đã chia đôi.

## Phép kiểm tra mới phân biệt những gì?

| Nhãn | Ý nghĩa |
|---|---|
| outer_whitespace_only | Chỉ thêm/bớt khoảng trắng ngoài |
| case_only_review_display_or_category | Chỉ đổi hoa thường; cần xét cách hiển thị/nhãn |
| numeric_value_preserved_format_changed | Giá trị số không đổi, cách ghi đổi |
| missing_token_representation | Chuyển cách ghi giá trị đã khuyết |
| information_replaced_by_missing | Giá trị có thật trong bản gốc bị thay bằng token khuyết |
| missing_replaced_by_value | Ô khuyết gốc bị gán một giá trị |
| original_number_plus_suffix_NOT_auto_repair | Số gốc còn nhưng bị gắn kg/USD/VND/đ/%; KHÔNG tự coi là sửa an toàn |
| changed_to_invalid_value | Thay đổi sang giá trị sai miền hoặc không đọc được thành số |
| changed_to_plausible_but_different_value | Giá trị mới qua được kiểm tra miền nhưng khác gốc; ví dụ reordered 1 thành 0 |
| invalid_eval_label | Nhãn eval_set không còn thuộc prior/train/test |
| changed_text_or_category | Tên hoặc nhãn thay đổi nội dung |

Báo cáo thống kê theo bảng/cột, chỉ lưu ít ví dụ để dễ gửi. Không xuất hàng triệu dòng khác biệt.

## Không so sánh nhầm khi bị thay đổi thứ tự dòng

06 đọc hai tệp theo vị trí bản ghi, rồi kiểm tra khóa chính (hoặc cặp order_id/product_id) đã chuẩn hóa số và trim có bằng nhau không. Chỉ khi bằng nhau mới so các ô còn lại.

- alignment_complete=true: mọi vị trí đều khớp khóa, không lệch số dòng.
- alignment_complete=false: có đổi khóa, đảo dòng, chèn/xóa dòng hoặc khóa không đọc được. Không thể phân biệt chính xác các nguyên nhân này bằng phép so vị trí.
- Khi false, số ô thay đổi CHỈ áp dụng các dòng khớp khóa; không được kết luận đã liệt kê toàn bộ thay đổi. Gửi báo cáo để thiết kế đối chiếu theo khóa nếu cần.
- Nếu 02 báo khóa trùng, đối chiếu theo thực thể cũng cần xem xét thêm. 06 không thay thế kiểm tra duy nhất của khóa.

## Ý nghĩa và giới hạn kiểm tra logic

01: kiểu, miền, token khuyết. Nhãn danh mục literal `missing` không bị coi là null.
02: khóa trùng và khóa không hợp lệ.
03: quan hệ cha-con, eval_set của đơn so với tệp chi tiết. Nếu orders có khóa trùng, kiểm tra này dừng thay vì tự chọn một dòng cha. Kết quả ERROR_INCOMPLETE là chưa xác minh, không phải đạt.
04: trình tự đơn theo khách, đơn train/test cuối, khuyết khoảng cách mua. Dòng có user/order_number không đọc được bị đếm riêng và loại khỏi tính chuỗi; không coi chuỗi còn lại là minh chứng đầy đủ.
05: vị trí giỏ liên tục, không trùng, cờ reordered có thuộc 0/1. Giỏ bị cắt phần cuối vẫn có thể qua kiểm tra liên tục.
06: thay đổi so với bản gốc, bao gồm thay đổi vẫn hợp lệ về miền. Bản gốc là mốc đối chiếu, chưa phải bằng chứng tuyệt đối về thực tế.

Bộ này KHÔNG tính lại reordered từ lịch sử khách-sản phẩm; phát hiện thay đổi cờ so với bản gốc không đồng nghĩa đã kiểm chứng lịch sử độc lập. Bộ này cũng không tự sửa dữ liệu hoặc chứng nhận mọi quy luật nghiệp vụ có thể nghĩ tới.

## Tài nguyên và báo cáo

Quét toàn bộ các tệp; không lấy mẫu tự động. Chạy tuần tự. 02–05 dùng SQLite trên ổ đĩa cho các phép kiểm tra lớn. Để vài GB trống; có thể thêm `--temp-dir "D:\temp_audit"` vào RUN_CHECKS.py (tạo thư mục trước). Dữ liệu gốc được đọc thêm một lượt bởi 06; năm kiểm tra còn lại chỉ đọc bản nhiễu.

Các phép kiểm tra có thể mất nhiều phút, phụ thuộc máy và ổ đĩa. Tiến độ đọc in mỗi 2 triệu dòng; giai đoạn SQL có thể tạm không in. File tạm tự dọn khi kết thúc bình thường; dừng cưỡng bức có thể để lại file tạm.

status=completed chỉ là chạy xong, không phải dữ liệu sạch. Các counter vắng mặt tương đương 0 nếu kiểm tra đã completed; báo ERROR_INCOMPLETE không được suy diễn như vậy.

Đã kiểm thử trên sáu cặp mẫu gốc/nhiễu của bạn và thử đảo thứ tự bản ghi. Chưa chạy trên toàn bộ bản nhiễu trên máy bạn.
