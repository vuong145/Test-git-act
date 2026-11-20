# Báo cáo kiểm tra dữ liệu nhiễu

Trạng thái: completed_checks_review_required

Chương trình chỉ đọc dữ liệu; các giá trị parse là phục vụ kiểm tra, không được ghi đè vào CSV.

| Bảng | Dòng đã đọc | Cột |
|---|---:|---:|
| aisles | 134 | 2 |
| departments | 21 | 2 |
| products | 49,688 | 4 |
| orders | 3,421,083 | 7 |
| order_products__prior | 32,434,489 | 4 |
| order_products__train | 1,384,617 | 4 |

## Khả năng dùng thứ tự dòng

So sánh theo từng order_id ở bảng chi tiết, theo từng user_id ở orders. Các số dưới đây dùng đoạn nhóm liên tiếp; phải xem thêm số nhóm xuất hiện lại trong JSON.

- orders: 2,182,372 giá trị khớp vị trí dòng; 4,773 không khớp; 1,233,938 ô thứ tự thiếu/không hợp lệ.
- order_products__prior: 25,667,262 giá trị khớp vị trí dòng; 762,067 không khớp; 6,005,160 ô thứ tự thiếu/không hợp lệ.
- order_products__train: 790,964 giá trị khớp vị trí dòng; 67,880 không khớp; 525,773 ô thứ tự thiếu/không hợp lệ.

Không xáo trộn trong bước gây nhiễu không đồng nghĩa dữ liệu ban đầu đã xếp theo thứ tự mua. Khớp trên số còn lại là bằng chứng hỗ trợ, chưa chứng minh mọi ô bị mất. Các giá trị trong miền cũng có thể đã bị thay sai.

## Tên và nhãn nguồn

aisle_id tra được tên quầy, không tra ra tên sản phẩm. Một quầy có nhiều sản phẩm. Báo cáo JSON có ví dụ thực tế. Không dùng dữ liệu gốc và không sửa reordered.

Có trong prior → ứng viên prior; có trong train → ứng viên train; có trong cả hai → lỗi. Không có trong cả hai → cần xác nhận thêm trước khi gán test.

Gửi BAO_CAO_GUI_CHATGPT.zip. Các số ứng viên là chẩn đoán, không phải số ô đã khôi phục.
