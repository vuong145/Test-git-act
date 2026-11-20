# Gửi Phong — Khóa nháp `lock.json` để duyệt, 04/11/2026

Vương đã chép nguyên bản cuối của Phong (`m4_test.py`, `m4_common.py`, `tests/test_m4_gate.py`; hash khớp `DANH_SACH.txt` của Phong), chạy lại toàn bộ test (57/57 đạt) và chạy `m4_lock.py` mới để tạo khóa nháp. Tập test **chưa mở**.

SHA-256 của `lock.json` này bắt đầu `fe2db0a7`. `approvals` đang là `false` cho cả hai người, nên cổng của `m4_test.py` vẫn chặn chạy test cho đến khi cả hai duyệt.

## Khóa ghi gì

| Mục | Giá trị |
|---|---|
| Phương pháp chính | RF (Recall@10 validation 0,0971; hơn Rules 0,0932 trên dung sai 0,002 nên không có hòa) |
| Cấu hình A | N = 1.000; min_count 20; max_len 2; min_confidence 0,05 |
| Ngưỡng F1 (validation) | LR 0,73128; RF 0,57771 |
| Mô hình | LR C = 0,1; RF max_depth 10, min_samples_leaf 100 (hai Pipeline đã lưu) |
| Số tệp khóa | 16 tệp, gồm mã (`m4_test.py`, `m4_common.py`, `m4_classifier.py`, `project_io.py`), `requirements.txt`, `m2_plot_style.json`, `m4_model.json`, `M4/hashes.json`, Master (`2741c970…`), các tệp M4 trong `hashes.json` và `validation_methods.csv` |
| Kiểm của Vương | 16/16 tệp khớp hash ngay sau khi khóa; khóa đáp ứng đủ danh sách bắt buộc của cổng; cổng chặn đúng vì thiếu hai xác nhận, không tạo `test_started.json` |

## Phong cần làm

1. Chép `BAO CAO/Bao cao mo hinh/lock.json` và `scripts/kiem_lock.py` vào máy Phong (thay `lock.json` cũ nếu có; sao lưu trước).
2. Chạy kiểm bằng máy Phong (không ghi gì):
   `& .venv-m2/Scripts/python.exe scripts/kiem_lock.py`
   Kỳ vọng: **16/16 tệp khớp**. Nếu có tệp lệch, ghi rõ tên tệp và gửi lại; không sửa tệp để cho khớp. Hai tệp có thể khác nếu máy Phong còn bản cũ: `requirements.txt` (phải bắt đầu `79edb2c0`) và Master (phải bắt đầu `2741c970`); các tệp M4 khớp gói A.
3. Rà nội dung: phương pháp chính, cấu hình A, ngưỡng F1 và danh sách tệp ở bảng trên đúng với `validation_methods.csv`, `validation_grid_A.csv`, `classifier_validation.csv` mà Phong đã đối chiếu ngày 04/11.
4. Nếu đồng ý, báo lại bằng một dòng: "Phong đồng ý lock.json bắt đầu `fe2db0a7`". Không cần gửi lại tệp.

## Sau khi Phong đồng ý

Vương chạy `python scripts/m4_lock.py --approve Phong Vuong` trên máy Vương; lệnh này tạo lại `lock.json` với `approvals` đủ hai người (hash của tệp khóa không đổi, chỉ đổi `locked_at` và `approvals`, nên **hash `lock.json` sẽ khác `fe2db0a7`**), hai bên ghi "đã khóa" kèm ngày vào biên bản, rồi Vương chạy `m4_test.py test` một lần.

Không sửa `lock.json` bằng tay; không đặt `approvals` bằng `true` trước khi cả hai đồng ý.
