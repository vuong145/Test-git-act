# Hướng dẫn Phong: làm xong mọi việc riêng rồi gửi lại một lần — 04/11/2026

Mục tiêu: Phong hoàn thiện phần của mình trên máy Phong, gửi lại **một gói cuối**; Vương chỉ việc chép nguyên, chạy test và tạo khóa trên máy Vương, rồi chạy kiểm định test một lần. Phần chữ trong tiểu luận tính sau.

Nguyên tắc: Vương chép **nguyên** tệp của Phong, không sửa. Vì vậy mọi thay đổi Phong muốn có đều làm trước khi gửi gói cuối. Không chạy `m4_test.py test` ở bất kỳ giai đoạn nào trên máy Phong.

## A. Đồng bộ máy Phong (làm trước)

Nhận gói `GUI_phong_dong_bo_moi_truong_20261104.zip` (có `NOI_DUNG_THAY_DOI.md`, mục 5), rồi:
1. Kiểm SHA-256 theo `DANH_SACH.txt`.
2. Sao lưu Master và `common/hashes.json` hiện có.
3. Chép Master mới (`master_train.parquet`) **trước**, rồi `common/hashes.json` mới.
4. Chép `scripts/project_io.py`, `tests/test_m2_multivariate.py`, `requirements.txt` mới (thay bản hiện có).
5. Chạy `check_hashes()` cho `common/hashes.json` (kỳ vọng 6/6) và `ban2/hashes.json` (kỳ vọng 10/10).
6. Chạy toàn bộ unittest; ghi kết quả và log.
7. Đọc các chỗ QMD Vương đã sửa (mục 2.5, 3.2, Bảng 3.5); phần chữ tính sau, chỉ cần đọc để biết.

## B. Hoàn thiện `m4_test.py` (làm trước khi gửi lại)

Bắt buộc:
- [ ] Giữ nguyên thiết kế chạy một lần (`test_started.json` tạo độc quyền, từ chối chạy lại).
- [ ] Đặt `n_jobs=1` cho Random Forest ở bước suy luận của `run`, để kết quả tái lập từng chữ số (hiện song song làm xác suất lệch ở chữ số thứ 16, kéo ROC-AUC và AP lệch khoảng 4e-8). Gợi ý một dòng sau khi nạp mô hình: `models["RF"].named_steps["model"].set_params(n_jobs=1)`. Suy luận RF chậm hơn khoảng 9 lần (test thật khoảng 8 đến 10 phút); không đổi tệp mô hình nên không ảnh hưởng hash khóa.

Nên làm:
- [ ] Dời thời điểm tạo `test_started.json` xuống ngay trước lúc nạp giỏ test, sau khi kiểm khóa, nạp hai mô hình và kiểm tra ghi được vào thư mục ra, để lỗi không liên quan đến test không làm kẹt.
- [ ] Thêm ghi chú đầu tệp về cách xử lý nếu máy hỏng giữa lúc chạy: hai bên cùng đồng ý, **đổi tên (không xóa)** `test_started.json` thành `test_started_failed_<ngày giờ>.json`, chỉ khi chưa có tệp kết quả test nào.

Sau khi sửa: chạy lại `tests/test_m4_gate.py` và toàn bộ unittest; chạy thử `python scripts/m4_test.py validation <thư mục thử>` trên dữ liệu gói A và so với kết quả cũ (chỉ số xếp hạng giống hệt; ROC-AUC và AP giống hệt giữa hai lượt chạy khi đã đặt `n_jobs=1`).

## C. Biên bản lần 1

Vương đã gộp biên bản (bản chính ở `Chung/Gửi và nhận/Gửi/THONG_NHAT_CHUONG4_LAN1_20261104.md`, có các dấu `[x]` của Phong). Từ nay chỉ giữ **một bản chính**: Phong không gửi lại cả tệp, chỉ ghi vào tệp gửi lại danh sách ô đã tick hoặc cần sửa. Còn để trống: ô duyệt `lock.json` và ô đã khóa.

## D. Việc Phong cần có trong gói cuối gửi Vương

Giữ nguyên cấu trúc thư mục dự án; gói nhỏ, không nén nếu dưới vài MB:
- `scripts/m4_test.py` (bản cuối), `scripts/m4_common.py` (chỉ nếu có đổi so với bản đã gửi), `tests/test_m4_gate.py` và mọi test thêm hoặc sửa.
- `output/<tên thư mục>/tests.log` (toàn bộ unittest trên máy Phong sau khi đồng bộ), kết quả `check_hashes`, kết quả chạy thử validation.
- `README_GUI_VUONG.md`: đã làm gì, lệnh kiểm, kết quả, kèm `DANH_SACH.txt` có SHA-256.
- Không gửi lại Master hay tệp dữ liệu lớn; không sửa `m4_lock.py` (tệp của Vương, đã mở rộng).

## E. Việc của Vương sau khi nhận gói cuối

1. Kiểm `DANH_SACH.txt`; chép nguyên `m4_test.py`, `m4_common.py`, `test_m4_gate.py` vào dự án; chạy toàn bộ unittest (kỳ vọng 57).
2. Chạy `python scripts/m4_lock.py` (bản nháp, `approvals` đều false). Tệp khóa ghi SHA-256 của mã nguồn bắt buộc, cấu hình, Master và mọi đầu vào M4. Gửi Phong bản `lock.json` này kèm danh sách hash.
3. Phong rà `lock.json` (tên tệp, hash, phương pháp chính, cấu hình A, ngưỡng F1) rồi báo "đồng ý".
4. Khi **cả hai đã đồng ý**: Vương chạy `python scripts/m4_lock.py --approve Phong Vuong`, ghi "đã khóa" kèm ngày vào biên bản. Từ lúc này không sửa code, config hay mô hình.
5. Vương chạy **một lần** trên máy Vương: `.\.venv-m2\Scripts\python.exe scripts/m4_test.py test`, kiểm các tệp `*_test.csv`, `results_test.json` và hình `fig-recall-at-k-test`, rồi gửi Phong gói kết quả để viết 4.3.2 đến 4.6.

Cổng của `m4_test.py` sẽ từ chối chạy nếu thiếu `approvals` đủ hai người hoặc nếu bất kỳ tệp khóa nào đã đổi.

## F. Điều không làm

- Không chạy `m4_test.py test` trên máy Phong.
- Không sửa `lock.json` bằng tay; chỉ `m4_lock.py` ghi.
- Không đặt `approvals` bằng `true` trước khi cả hai đồng ý.
- Không đổi code, cấu hình hay mô hình sau khi đã khóa.
