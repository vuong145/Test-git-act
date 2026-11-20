# Rà soát phần mô tả Bạn 2 — 30/10/2026

Phạm vi: phân tích đa biến làm độc lập từ G0, bảng thời gian/tương quan/đồng mua, hình 3–5 và insight mô tả I4–I5. Theo phân công, bảng thống kê 3.4 chính thuộc Bạn 1; các đầu ra này hỗ trợ phần 3.4–3.5 của Bạn 2. Không chạy, chỉnh sửa hoặc bàn giao mục 3.6 trong đợt rà soát này.

## Lỗi đã phát hiện và sửa

1. Script vẽ nhập helper từ module kiểm định và bắt buộc có hypotheses.csv. Đã tách helper kiểm chứng sang m2_multivariate_io.py, bỏ phụ thuộc vào kết quả kiểm định. Bản thân việc đếm crosstab để đối soát dữ liệu không phải kiểm định giả thuyết.
2. I5 chứa V/điều chỉnh Holm/kết luận kiểm định ngoài phạm vi. Đã chuyển sang count, support, lift, xác suất có điều kiện và diễn giải mô tả; không nói có ý nghĩa thống kê.
3. Một số median/IQR/số thiếu trong I4 được ghi cố định trong code. Đã lấy động từ bảng đầu ra; thêm mẫu số cụ thể cho pivot và tương quan trong bản thảo.
4. Matplotlib tự raster hóa thanh màu trong một số PDF. Đã buộc toàn bộ thành phần thành vector; kiểm tra 5 PDF không còn ảnh raster nhúng. PNG vẫn 300 DPI.
5. Trục boxplot đặt giới hạn cố định. Đã tính từ giá trị lớn nhất của dữ liệu, giữ toàn bộ giỏ hợp lệ.

## Kết quả kiểm tra

- G0 và hash dữ liệu đầu vào đạt trước/sau; reference 39.363 giỏ, 415.053 dòng.
- Đối chiếu từng giỏ với tập ngành trong reference: 39.363/39.363 đúng, đủ 21 cột Boolean, không đếm lặp nhiều sản phẩm cùng ngành.
- Tính lại toàn bộ 441 ô count/support/lift/xác suất bằng phép Boolean độc lập: khớp. Mẫu số luôn là tất cả giỏ reference khi tính support.
- Tính lại 28 ô median/count ngày × khung giờ và cờ N<30: khớp; kiểm tra N/median/Q1/Q3 của nhóm giờ gồm missing: khớp. Pivot dùng 23.549 giỏ đủ ngày và giờ; 15.814 giỏ thiếu ít nhất một biến không tham gia pivot.
- Tính lại 32 ô Pearson/Spearman bằng NumPy và hạng trung bình: khớp trong sai số 1e-12. N=39.363 cho ba biến đếm; N=32.787 cho cặp có days_since_prior_order.
- 6 tests mô tả đạt: đếm lớn không tràn, ngành vắng, mẫu số/count/lift tính tay, khóa/ngành không hợp lệ, thiếu/biến hằng/không đủ quan sát, ô thời gian rỗng và nhóm missing.
- 5 PNG có DPI 300, 5 PDF không có raster nhúng; liên kết hình trong QMD bản thảo tồn tại. Nhóm hình thời gian tách 3A/3B để không ép chữ.

## Cách dùng và giới hạn nghiệm thu

Chạy trong môi trường M2 đã nghiệm thu: tests/test_m2_multivariate.py; scripts/m2_eda_multivariate.py; scripts/m2_plot_multivariate.py; scripts/m2_audit_descriptive.py. Script kiểm định không cần chạy. Gói yêu cầu G0 version 2 như lần hợp nhất tại Phong; máy nhận phải kiểm tra cùng nguồn/config trước tái lập.

Các file trong ZIP dùng đường dẫn tương đối từ gốc project. QMD bản thảo có đường dẫn ảnh theo gốc để Bạn 1 ghép. Dùng gói BAN_GIAO_BAN2_MO_TA_KHONG_3_6.zip cho phạm vi hiện tại; ZIP BAN_GIAO_BAN2_20261030.zip trước đó có nội dung 3.6, không dùng cho lần gửi này. Các file 3.6 đã tạo từ lượt trước được giữ nguyên tại máy Phong, không tuyên bố chúng chưa từng được chạy.

Đạt các kiểm tra mô tả nêu trên, chưa thể gọi là hoàn hảo hoặc đã nghiệm thu PDF toàn bài. Còn kiểm tra chéo bởi Vương, đặt caption/bảng theo QMD chính và xem PDF ở kích thước in sau tích hợp. Không kết luận nhân quả, hiệu quả gợi ý hoặc tăng doanh thu từ các bảng mô tả. I1–I3 thuộc bằng chứng G1, không phải mục còn thiếu của phân tích đa biến độc lập.
