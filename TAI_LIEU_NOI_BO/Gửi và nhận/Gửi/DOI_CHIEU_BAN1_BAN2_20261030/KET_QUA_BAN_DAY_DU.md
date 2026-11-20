# Đối chiếu bản bàn giao đầy đủ Bạn 2 — 30/10/2026

## Kết luận

Đủ đầu ra khoa học để tiến hành ghép 3.4–3.6, nhưng CHƯA phải chương 3 đã ghép và nghiệm thu PDF. QMD chính của Vương vẫn có chỗ giữ chỗ ở 3.4–3.6. Không chép đè G0 của Phong vào code Bạn 1 hiện tại.

## Đã kiểm tra

- 57/57 tệp trong PACKAGE_MANIFEST của bản đầy đủ khớp SHA-256. Phần mô tả 3.5 giữ nguyên byte so với gói trước (ngoại trừ tài liệu bàn giao/manifest).
- Đối chiếu trước đó đã xác minh dữ liệu reference/basket/lookup hai bên giống nhau; ma trận hiện diện, 441 ô đồng mua, 28 ô pivot thời gian, các nhóm giờ và tương quan khớp phép tính độc lập (checks.json).
- Tính lại ba bảng 2×2 trực tiếp từ reference của Vương, không lấy bảng đếm của Phong làm đầu vào: số đếm, Pearson không Yates, p, Holm, V, kỳ vọng nhỏ nhất, xác suất có điều kiện, chênh lệch điểm %, support và lift khớp (checks_full_3_6.json).
- H1: chi-square 1584,256013; V=0,200617. H2: 910,418942; V=0,152082. H3: 913,933795; V=0,152375. Cả ba bác bỏ H0 sau Holm ở alpha=0,05. Đây là liên hệ, không phải nhân quả.
- Chạy trực tiếp 4 trường hợp fixture trong gói kiểm định; kiểm tra Holm và từ chối bảng đếm không hợp lệ đều đạt. Chưa chạy toàn bộ pipeline G0 v2 của Phong trên cây G0 v1 của Vương.
- Code có Fisher hai phía cho bảng thưa và xử lý biến hằng; cả ba bảng thực đều đủ tần số kỳ vọng để dùng Chi-square. Không cần tạo kết quả Fisher giả cho dữ liệu thực.

## Việc cần làm lúc ghép, trước khi gọi là hoàn thành

1. **Thống nhất G0/config:** Vương dùng outputs phẳng, Phong dùng outputs theo nhánh lồng nhau; Phong dùng `Bao cao EDA/`, `Data phai sinh/`, Vương dùng `BAO CAO/Bao cao EDA/`, `DATA/Data phai sinh/`. Giữ tổ chức DATA/BAO CAO của Vương. Chọn một hợp đồng và sửa các điểm gọi tương ứng; không chỉ đổi JSON rồi để nguyên code. Nếu chuyển G0 v2, phải chuyển cả consumer Bạn 1 và tạo lại bằng chứng ở môi trường đích. Hash manifest khác không đồng nghĩa dữ liệu khác.
2. **Renderer:** regex ảnh hiện tại ở scripts/render_pdf.py dừng ở dấu `)` đầu tiên. Tên hình `(Lift).png` trong bản thảo Phong sẽ bị cắt mất đường dẫn. Khi tích hợp, đổi tên hình và các tham chiếu đồng bộ hoặc sửa parser; kiểm tra render thật.
3. **Cỡ chữ:** PDF hình Phong rộng khoảng 6,40–6,42 inch do bbox_inches='tight'. Đặt rộng 16 cm sẽ thu font 12 xuống khoảng 11,78–11,80 pt. Cần xuất hình đúng kích thước hoặc điều chỉnh font và kiểm tra PDF cuối; không dùng resizebox để ép bảng. Chưa xác nhận cỡ chữ bản ghép vì chưa có bản ghép.
4. **Nguồn tương đối:** insights_i4_i5.csv còn đường dẫn máy Phong trong cột source. Sửa cách ghi nguồn và cập nhật bằng chứng sau khi chạy lại; đường dẫn này chủ yếu ảnh hưởng truy vết, không phải dữ liệu thống kê.
5. **Lời văn:** gộp I1–I3 từ bằng chứng Bạn 1 với I4–I5 của Phong thành đúng 5 insight; hiện chưa có bản tổng hợp được hai bạn duyệt. Chuẩn hóa dấu thập phân tiếng Việt, heading và nhãn hình/bảng; nối I5 với kết quả 3.6 nhưng giữ giới hạn về nhân quả và kích thước giỏ.
6. **Mẫu số:** ghi riêng reference 39.363 giỏ, tập hợp lệ của từng biến/từng cặp và tập có cả ngày–giờ. Không dùng N=39.363 cho mọi panel nếu panel đã loại thiếu.
7. **p underflow:** H1 p máy bằng 0; bản thảo đã tránh ghi p=0. Cụm “giới hạn số học” với 2,23e-308 nên làm rõ là ngưỡng trình bày, không khẳng định đây là số dương nhỏ nhất float64 (còn số dưới chuẩn). H2/H3 giữ giá trị và Holm hiện tại.
8. **Hoàn thiện PDF:** thay đúng ba chỗ giữ chỗ 3.4–3.6, không tạo thêm mục cấp 2 trùng; kiểm tra mọi tham chiếu, bảng dài, hình, cỡ chữ, phụ lục và ngân sách trang. Chỉ sau đó mới chốt hoàn thành chương 3.

## Rút gọn code — hoãn theo yêu cầu hiện tại

Đã đọc HUONG_DAN_RUT_GON_CODE.md. Thứ tự mới do người dùng chốt là ghép và hoàn thành chương 3 trước, rồi mới rút gọn; ưu tiên này thay cho mốc “trước 3.6” trong tài liệu. Giữ mục tiêu common.py + clean_vuong.py + clean_phong.py, không hai bản cleaning giống nhau; phải bảo toàn kết quả và dấu vết API yêu cầu môn học. Lần này không xóa code, không đổi kiến trúc, không ghi nhật ký. Code sinh QMD và Holm tự viết của bản giao hiện tại được ghi nhận để xử lý trong đợt sau, không dùng lý do đó để bỏ kết quả đúng.
