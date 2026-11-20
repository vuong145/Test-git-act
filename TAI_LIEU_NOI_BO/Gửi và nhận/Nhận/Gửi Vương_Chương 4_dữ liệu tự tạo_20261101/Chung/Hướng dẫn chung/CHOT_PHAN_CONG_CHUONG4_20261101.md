# Chốt phân công Chương 4 — 01/11/2026

Phong xác nhận trong chat: **“Chốt phương án này”**, đối với mục 11 của `Gửi và Nhận/Nhận/THIET_KE_CHUONG4_20261101.md`, gồm phân công hai máy, **20 mẫu âm/giỏ** và **dung sai hòa Recall@10 = 0,002**. Đây là bản bổ sung cho `THONG_NHAT_PHAN_VIEC_20261031.md`; giữ nguyên bản tài liệu đã nhận. Không coi xác nhận này là bằng chứng một cuộc họp hoặc một xác nhận mới của Vương.

## Phân công đã chốt

| Người | Trách nhiệm |
|---|---|
| Vương | Dữ liệu, che giỏ, danh mục, luật, hàm khớp luật, 7 đặc trưng, lấy mẫu âm, chỉ số xếp hạng, giai đoạn A, benchmark và mọi lượt chạy chính thức trên máy Vương. Viết 4.1, 4.2, 4.3.1. |
| Phong | Pipeline LR/RF, giai đoạn B, ngưỡng F1, bỏ nhóm đặc trưng, chỉ số phân loại, bootstrap ghép cặp, importance, hệ số LR, hình và diễn giải. Viết 4.3.2, 4.4–4.6, hợp nhất QMD. Phát triển trên dữ liệu tự tạo và gói pilot. |
| Cả hai | Duyệt giao diện, giai đoạn C và lock.json trước khi chấm test; đọc chéo kết quả và bài viết. |

Ngoại lệ cho quy tắc cũ chỉ Vương ghi code: Phong sở hữu `scripts/m4_classifier.py`, `scripts/m4_test.py`, `scripts/m4_interpret.py`, `tests/test_m4_model.py`. Test môi trường phụ trợ `tests/test_m4_environment.py` do Phong chuẩn bị. Các tệp dữ liệu/khai phá/khóa, `m4_common.py`, `configs/m4_model.json` và `tests/test_m4_data.py` thuộc Vương theo mục 11.3. Không tự sửa tệp của người kia.

## Quy tắc thực nghiệm giữ nguyên

- Giữ phân hoạch G0; reference chỉ dùng xây danh mục/luật. Không tạo lại Master hoặc đổi phân hoạch.
- Lấy tối đa 20 mẫu âm không hoàn lại trên fit; validation/test chấm toàn bộ ứng viên theo lô. Seed che 42, âm 43, importance 44, bootstrap 42.
- K = 5 và 10; Precision chia K, Recall chia toàn bộ số sản phẩm ẩn kể cả ngoài danh mục; phá hòa điểm bằng product_id tăng. Batch và pilot 2.000 giỏ.
- Giai đoạn A: trong ngưỡng 0,002 so với Recall@10 cao nhất, ưu tiên N nhỏ hơn, support lớn hơn, max_len nhỏ hơn, confidence cao hơn theo thiết kế.
- Lưới B gửi Vương: LR C = 0,01; 0,1; 1; 10. RF max_depth = 10/20 × min_samples_leaf = 20/100; n_estimators = 300; class_weight = None. Các tham số khác theo thiết kế gốc.
- Chưa khóa phương pháp thắng hoặc ngưỡng phân loại. Chỉ duyệt lock.json sau giai đoạn B–C; không dùng test để chọn mô hình.

## Giao diện và bàn giao tiếp theo

Chốt phân công **không đồng nghĩa giao diện đã được triển khai/kiểm thử**. Khi lập bản này, workspace mới có test môi trường M4, chưa có `m4_common.py`, `m4_model.json` hoặc gói pilot.

Vương gửi khung hàm/docstring của `m4_common.py`, cấu hình và schema theo mục 11.4. Cần thống nhất thêm kiểu dữ liệu từng lô trả về từ `iter_features`, cách truyền cấu hình và cách báo thiếu tệp/sai hash. Phong có thể phát triển các thành phần độc lập trên dữ liệu tự tạo ngay, sau đó ghép giao diện này.

Cần làm rõ trước khi chạy trên dữ liệu thật: thiết kế vừa mô tả chuẩn bị giỏ test, vừa giới hạn chỉ `m4_test.py` được đọc test. Đề xuất: bước chuẩn bị phát triển chỉ xử lý fit/validation; phần đọc/che/sinh đặc trưng test chỉ được gọi qua cổng chấm test sau khi kiểm lock. Đây là đề xuất triển khai cần đối chiếu với Vương, chưa phải giao diện đã nghiệm thu.

Gói pilot cần dữ liệu mẫu 2.000 giỏ theo bảng 11.4, schema đặc trưng, cấu hình, code phụ thuộc và manifest SHA-256. Phong kiểm toàn luồng trên pilot, rồi kiểm chéo Recall@10 độc lập trên 50 giỏ validation khi nhận gói A.

Bằng chứng chuẩn bị máy Phong: `output/chuan_bi_chuong4_20261101/KET_QUA_CHUAN_BI.md`. Tài liệu này là quyết định phân công, không phải nhật ký làm việc.
