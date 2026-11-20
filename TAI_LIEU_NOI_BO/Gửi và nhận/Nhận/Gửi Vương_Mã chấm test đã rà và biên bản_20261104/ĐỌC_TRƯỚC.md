# Gửi Vương — Phong rà mã chấm test, 04/11/2026

Đã kiểm manifest gói GUI_phong_cham_test_20261104, sao lưu mã trước tích hợp tại output/duyet_cham_test_20261104/before và tích hợp hai script. Không mở test nghiên cứu.

## Sửa sau rà soát

1. Cổng test yêu cầu `approvals: {"Phong": true, "Vuong": true}` và hash đầy đủ mã/nguồn. Khóa nháp hiện tại bị chặn. Đây là hợp đồng trường bổ sung cần Vương ghi vào m4_lock khi cả hai thực sự duyệt, không tự đặt True trước đó.
2. Hash bắt buộc: scripts/m4_test.py, m4_common.py, m4_classifier.py, project_io.py, requirements.txt, configs/m2_plot_style.json, configs/m4_model.json, M4/hashes.json, Master và mọi đầu vào liệt kê trong M4/hashes.json. Kiểm stage_A trong M4 khớp lock, kiểm G0 trước test. Mã m4_lock thuộc Vương nên Phong gửi yêu cầu cập nhật thay vì tự sửa tệp này.
3. Test chỉ ghi thư mục báo cáo chính thức; tạo test_started.json bằng chế độ tạo độc quyền trước khi đọc giỏ. Nếu lỗi sau khi bắt đầu, giữ dấu và dừng để hai bên xem log, không tự xóa dấu/chạy lại. Chặn đổi thư mục đầu ra để né dấu. Validation phải ghi thư mục thử riêng.
4. locked_stage dùng bộ lọc Parquet theo split ngay khi nạp thay vì nạp toàn bộ rồi lọc. Đây là một dòng sửa trong m4_common bản Vương gửi, cần Vương tiếp nhận cùng bản m4_test. Không đổi công thức đặc trưng/chấm điểm.
5. Bootstrap giữ so sánh chính phương pháp đã chọn–Popularity, bổ trợ phương pháp chính–Rules và LR–RF đúng thiết kế. Không bỏ so sánh chính khi chính là Popularity: CI tự so bằng [0,0], tránh gắn nhầm primary cho so sánh phụ. Bản đề xuất thay LR–RF bằng Rules–Popularity được đưa lại đúng kế hoạch đã chốt.
6. K=1…10 cho hình Recall, giữ các chỉ số tổng hợp K=5/10. Manifest kết quả chứa cả CSV và PNG/PDF. Bốn hàm checked_scores/best_f1_threshold/classification_metrics/paired_bootstrap giữ nguyên.

## Kiểm chứng

Toàn bộ **57/57 test đạt, 5,754 giây**: 55 test đã có tại máy Phong sau gói A + 2 test mới test_m4_gate. Không ép số test thành 56. Test mới kiểm khóa thiếu phê duyệt, sửa byte đầu vào, thiếu hash code, đổi thư mục ra, dấu chống chạy lại; chạy luồng đánh giá dữ liệu tự tạo và kiểm đầu ra/primary tự so/Recall 1…10. Test hình không render lại, dùng mock; hình trong dry_run_validation của Vương chưa được dùng làm kết quả test.

Lệnh kiểm: `.venv-m2/Scripts/python.exe -m unittest discover -s tests -v`. Không chạy `m4_test.py test` trong giai đoạn rà mã. tests.log kèm theo.

Biên bản phía Phong đã tick phân công, môi trường, giữ tham số, ba thay đổi giao diện và đồng ý Recall@K 1…10. Giữ ô duyệt lock/đã khóa trống vì mã vừa thay đổi và khóa nhận chưa chứa hash code. Xem bản biên bản phía Phong kèm gói.

## Đồng bộ hai file và Master

Gói chấm test chỉ có m4_test.py/m4_common.py và kết quả validation thử; không có project_io.py/test_m2_multivariate.py bản Vương hoặc Master/manifest G0 mới. Không thay chúng bằng bản đoán hoặc đổi manifest để che sai khác.

Theo yêu cầu dùng “bản của bạn”, kèm **bản Phong hiện hành** của project_io.py và test_m2_multivariate.py để Vương có thể chép nguyên và đối chiếu hash. Hai tệp này không đổi trên Phong. Nếu ý định là Phong dùng bản Vương, cần Vương gửi hai bản đó; hiện chưa có đủ nội dung để diff. Không tuyên bố hai máy đã đồng bộ khi chưa có xác nhận hash từ máy nhận.

Chưa thấy gói đồng bộ môi trường chứa Master mới. G0 hiện tại vẫn đạt 6/6. Khi gói mới đến: kiểm manifest gói, sao lưu Master/manifest hiện có, thay Master trước, cập nhật hashes.json sau, rồi check_hashes; không tái tạo Master. Do chưa có gói này, chưa duyệt khóa cuối.

## Vương cần làm trước khóa cuối

- Tiếp nhận bản m4_test.py, thay đổi lọc split m4_common.py và test mới; chạy test trên máy Vương. Đồng bộ hai file phụ thuộc bằng bản thống nhất.
- Hoàn tất đồng bộ Master/môi trường, cập nhật m4_lock để ghi các hash bắt buộc và trạng thái phê duyệt. Không chạy m4_lock cũ rồi coi đã khóa vì nó chưa ghi các trường mới.
- Gửi lock dự thảo cuối và hash mã cho Phong rà. Chỉ ghi approvals đủ hai người và chấm test trên máy Vương sau khi cả hai đã duyệt. lock_review.json là báo cáo rà, không phải lock thay thế.

Không thay QMD và không ghi nhật ký. Gói nhỏ để nguyên thư mục Gửi Vương.
