# Phong gửi Vương — rà mã Chương 4, ghép bài và viết Chương 5

Ngày thực hiện: 04/11/2026. Phạm vi: đọc mã, kiểm thử fixture, đối chiếu kết quả đã có, sửa lời văn và viết bài. Không chạy cleaning, tạo Master, khai phá, huấn luyện chính thức, chấm lại test; không thay mã nguồn/config/mô hình/lock của dự án.

## 1. Phiên bản và bằng chứng

- Nguồn chính: `Gửi và Nhận/Nhận/GUI_PHONG_TOAN_BO_20261104/`, gồm thiết kế, CODE_CHUONG4, KET_QUA_TEST và QMD có Chương 4 của Vương.
- Kiểm SHA-256 hai danh sách tệp, tám đầu ra trong `results_test.json`, quan hệ hash lock–dấu chạy–kết quả, bảy tệp mã/config/requirements được khóa có trong gói. Cộng với 24 phép tính lại trung bình chỉ số theo giỏ: **100/100 phép đối chiếu đạt**, chi tiết `verification.json`.
- Lock chính thức nhận được: `e38b04f22b66438a737597753ef4007cd694adbe809ca62ac9fdfd734dfdb1b7`, thời điểm `2026-11-04T16:10:47`. Hồ sơ kết quả ghi split=test, 24.877 giỏ, 24.758.284 cặp. Chỉ đọc đầu ra có sẵn; không mở lại pipeline test.
- Chạy trực tiếp bộ test trong CODE_CHUONG4: **27/27 đạt, 2,190 giây**. Đây là test Chương 4 của gói nhận, không phải tuyên bố đã chạy lại 58 test toàn dự án. Test cổng khóa dùng dữ liệu tự tạo và thư mục tạm; chữ `test` trong fixture không phải lượt chấm test nghiên cứu.
- Đối chiếu riêng 21 giá trị từ CSV nguồn vào bảng `doi_chieu_so_lieu.csv` (8 chỉ số xếp hạng, 9 giá trị bootstrap, 4 thời gian validation). Tính lại từ 99.508 dòng chỉ số theo giỏ: 24.877 giỏ mỗi phương pháp, 49.473 sản phẩm che, 8.449 giỏ không có đáp án trong C. Mọi trung bình xếp hạng khớp sai số dưới 1e-12.
- Đọc trực tiếp các nguồn EDA/validation: `department_summary.csv`, `eda_summary.csv`, `ban2/hypotheses.csv`, `ban2/lift_baseline.csv`, `rule_coverage.json`, `ablation.csv`, hai CSV benchmark khai phá và JSON tương đương. Chương 5 không chép số test từ bản thiết kế.

## 2. Kết quả rà mã

| Nội dung | Kết quả và giới hạn |
|---|---|
| Ma trận giỏ | `basket_matrix` dùng CSR Boolean rồi DataFrame thưa; giữ mọi giỏ reference làm mẫu số support |
| Chọn tham số | FP-Growth tạo 12 tổ hợp; hai ngưỡng confidence tạo 24 cấu hình validation. Pilot chỉ cắt giỏ fit/validation và ghi ra thư mục pilot |
| Đặc trưng | Reference cung cấp danh mục và luật; `basket_features` chỉ nhận phần quan sát; nhãn được tạo riêng từ phần che. Lấy tối đa 20 âm/giỏ fit; validation/test chấm toàn bộ ứng viên |
| LR/RF | Tiền xử lý fit trong Pipeline; OneHotEncoder không bỏ nhóm chuẩn. Dung sai hòa Recall 0,002; xét thời gian trong lưới tương ứng |
| Cổng test | Kiểm hash và hai approvals; dấu chạy tạo độc quyền trước khi nạp test; RF suy luận `n_jobs=1`; kết quả ghi hash đầu ra; bootstrap ghép cặp theo người dùng |
| Tương đương thuật toán | Đối chiếu trực tiếp tập itemset/support. Không có phép đối chiếu độc lập từng confidence/lift |
| `m4_validate.py` | Thực tế đọc toàn bộ `masked_baskets.parquet` rồi mới lọc fit/validation. Chú thích “test không được nạp” không chính xác. Phần test bị loại trước tạo đặc trưng/chọn cấu hình; qua luồng đã đọc chưa thấy sử dụng test để lựa chọn. Ghi nhận để giải thích, không tự sửa mã đã khóa |
| `m4_common.py` | `locked_stage` có bộ lọc Parquet theo split ngay khi đọc; mặc định fit/validation, chỉ bước chấm sau khóa mới truyền test |
| Khác phiên bản hai máy | 9/11 script giống byte. `m4_lock.py` của Vương có bước approvals/chặn sau dấu chạy; `m4_report.py` chỉ đổi chiều cao và khoảng cách hình importance. Không tự thay hai script này; bảy tệp khóa hiện diện trong gói khớp lock chính thức |

Không có kết luận “mã hoàn hảo”: unittest không thay thế chứng minh mọi trường hợp biên. Trong phạm vi lượt chạy và đầu ra nhận được, chưa phát hiện vấn đề buộc chạy lại kết quả nghiên cứu. Mã không được sửa trong phiên này.

## 3. Những chỉnh sửa bài đã thực hiện

| Vị trí trong QMD | Trước / vấn đề | Sau |
|---|---|---|
| 1.2, mục tiêu 3 | Hứa đối chiếu itemset/support/confidence/lift | Nêu phép đối chiếu trực tiếp itemset/support; confidence/lift suy từ cùng support và công thức |
| 1.2, tính khả thi | Pilot chốt Top-N và số âm | Lưới 24 cấu hình validation chọn danh mục/luật; tối đa 20 âm/giỏ cố định; pilot kiểm toàn luồng |
| 2.4, khai phá/benchmark | Nói loại cấu hình vượt ngân sách | Nêu không cấu hình bị loại; phân biệt 12 tổ hợp FP-Growth, 24 cấu hình và hai cấu hình benchmark |
| 2.4, chỉ số | Hứa độ phủ danh mục gợi ý đã đo | Bỏ khỏi kết quả thực nghiệm; chỉ giữ như KPI tương lai trong Chương 5 |
| 2.4, chỉ số | Chỉ K=5,10 | Giữ bảng K=5,10; thêm đường Recall@K từ 1 đến 10 |
| 3.5, I1 | Hẹn phân tích theo cỡ giỏ tại Chương 4 | Chuyển thành hướng phát triển chưa thực hiện |
| Tóm tắt | Ô chờ | Viết 297 từ, dùng số có trong thân bài và CSV/JSON đã đối chiếu |
| Phụ lục và 2.5 | Đưa toàn văn mã/nhật ký vào bài | Bỏ hai phụ lục; nêu nộp riêng; không xóa mã hoặc nhật ký thực tế |
| 4.5 | Gọi hệ số ngành là so với nhóm chuẩn dù OneHot không drop | Đọc hệ số cùng intercept/điều chuẩn; so hai ngành bằng hiệu hệ số; không có nhóm chuẩn bị loại |
| 4.5–4.6 | Giải thích hệ số và gần nhau validation/test hơi chắc | Hạ mức diễn giải: liên hệ của bài toán che giỏ; một lượt chia chưa loại trừ quá khớp |
| Chương 5 | Bốn ô chờ | Viết đủ 5.1–5.4, hai bảng khuyến nghị/KPI, lộ trình, đạo đức, giới hạn và kết luận năm câu hỏi |

Chương 4 được ghép từ QMD Vương gửi; hai hình được chép từ `TIEU_LUAN/assets/chuong4`. Hình Recall giữ nguyên tệp; hình importance là bản bố cục thấp hơn của Vương, khác hash không tự chứng minh khác dữ liệu.

## 4. Việc còn lại ngoài phần viết Chương 5

1. **Rút trang toàn bài:** xem số trang thực tế trong README kèm gói; chưa thể gọi là bản nộp cuối khi vượt 45 trang từ bìa đến hết Chương 5. Giữ chữ 12 pt, không ép lề hoặc thu nhỏ chữ.
2. **Thống nhất Chương 3 và môi trường M1:** Phong giữ nguyên số benchmark lịch sử của QMD hiện hành. Bản Vương nhận có sửa 2.5, 3.2 và benchmark sang lượt 04/11. Diff đã lưu `khac_biet_chuong1_3_voi_vuong.diff`. Đặc biệt câu “hai bản xuất bản” ở 3.2 cần tách kết quả lịch sử khỏi code hiện hành chỉ xuất một Master. Chưa gộp các thay đổi này trong phạm vi sửa tám điểm/Chương 5; cần đối chiếu hồ sơ nguồn của lượt mới trước khi thay đồng loạt bảng và diễn giải. Chương 5 không dùng các tỷ số thời gian M1 còn lệch.
3. **Không coi tệp lock cũ ở thư mục báo cáo của Phong là lock chính thức:** bản e38b04f2 và dấu chạy chính thức vẫn nằm trong gói nhận đã kiểm chứng. Phiên này không thao tác khóa, không thay lock, không chạy lại test.
4. **Rà hình thức toàn bài sau rút gọn:** PDF dựng mới kiểm tra bố cục Chương 5; không tuyên bố đã rà từng trang của Chương 1–4. Không thêm tài liệu tham khảo mới chưa kiểm chứng; các khuyến nghị A/B là thiết kế tương lai của nhóm.

Không tự ghi nhật ký trong phiên này. Có thể dùng báo cáo này làm căn cứ để hai bạn ghi nhật ký khi cần.
