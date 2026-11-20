# Gửi Phong — Mã chấm điểm sau khóa (đề xuất cho `m4_test.py`), 04/11/2026

Vương soạn bản `m4_test.py` hoàn chỉnh để Phong rà soát và quyết định dùng. `m4_test.py` là tệp của Phong, nên đây chỉ là đề xuất: Phong so với bản của mình, sửa nếu muốn, rồi chép vào dự án.

**Chưa mở tập test.** Mã đã được chạy thử trên tập validation để kiểm tra đúng; kết quả chạy thử nằm ở `dry_run_validation/` và không dùng cho bài.

## Gồm gì

| Tệp | Nội dung |
|---|---|
| `scripts/m4_test.py` | Bản ghép: giữ nguyên bốn hàm của Phong (`checked_scores`, `best_f1_threshold`, `classification_metrics`, `paired_bootstrap`, đã kiểm so cấu trúc code không đổi) và thêm phần chấm điểm sau khóa (khoảng 90 dòng) |
| `scripts/m4_common.py` | Bản mới của Vương: hàm `locked_stage(cfg, splits=("fit", "validation"))` nhận thêm tham số `splits`; mặc định không đổi, chỉ bước chấm test truyền `("test",)`. Bản này cũng có các chú thích khối mới |
| `dry_run_validation/` | Kết quả chạy thử trên validation: bảng chỉ số xếp hạng, Recall@K (K = 1–10) kèm Recall trần, chỉ số phân loại, ma trận nhầm lẫn, bootstrap, hình Recall@K |
| `DANH_SACH.txt` | SHA-256 từng tệp |

## Phần chấm điểm làm gì

`python scripts/m4_test.py test` thực hiện theo thứ tự:
1. **Cổng khóa:** đọc `BAO CAO/Bao cao mo hinh/lock.json`, kiểm SHA-256 mọi tệp liệt kê; sai một tệp thì dừng. Từ chối chạy nếu `results_test.json` đã tồn tại (chỉ chấm test một lần).
2. Nạp **chỉ** giỏ test đủ điều kiện (qua `locked_stage(cfg, ("test",))`), dùng đúng cấu hình giai đoạn A đã khóa và hai Pipeline đã lưu.
3. Chấm bốn phương pháp (Popularity, Rules, LR, RF) bằng `evaluate` của Vương với K = 1…10; trung bình vĩ mô theo giỏ; Recall trần theo từng K.
4. Chỉ số phân loại của LR và RF tại **ngưỡng F1 đã khóa trên validation**, trên toàn bộ cặp ứng viên (không lấy trung bình theo lô): Accuracy, Precision, Recall, F1, ROC-AUC, AP và ma trận nhầm lẫn.
5. Bootstrap ghép cặp theo người dùng, 2.000 lần, seed 42: phương pháp chính so với Popularity (**kiểm định chính**), cùng hai so sánh bổ trợ (phương pháp chính so với Rules; Rules so với Popularity).
6. Ghi `basket_metrics_test.csv`, `ranking_metrics_test.csv`, `recall_at_k_test.csv`, `classifier_metrics_test.csv`, `confusion_matrix_test.csv`, `paired_bootstrap_test.csv`, `figures/fig-recall-at-k-test.pdf|png` và `results_test.json` (kèm SHA-256 `lock.json` và các đầu ra).

`python scripts/m4_test.py validation <thư mục>` chạy cùng mã trên validation và ghi ra thư mục khác (cổng khóa vẫn kiểm).

## Kiểm tra đã làm trên máy Vương (chạy thử validation, 3 phút)

- **Chỉ số theo giỏ giống hệt** `basket_metrics_validation.csv` cũ ở K = 5 và 10: lệch lớn nhất bằng 0, trên 99.416 dòng.
- **Chỉ số phân loại giống hệt** `classifier_validation.csv`: LR (ngưỡng 0,73128; AP 0,01404; ROC-AUC 0,78526) và RF (ngưỡng 0,57771; AP 0,01710; ROC-AUC 0,81059); 24.736.527 cặp, 25.781 dương.
- 25 test của `m4_model`, `m4_interpret`, `m4_data`, `m4_environment` vẫn đạt khi dùng bản `m4_test.py` ghép; toàn bộ 55 test của dự án đạt với `m4_common.py` mới.
- Bản ghép **không tạo vòng nhập**: `m4_classifier.py` nhập `m4_test`, nên `m4_test` chỉ nhập `m4_classifier` bên trong hàm `run`.

## Hình Recall@K

Hình một khung bị đường trần (khoảng 0,52) kéo trục tung, bốn phương pháp (0,01–0,10) dồn sát nhau. Đã đổi thành hai khung chung trục K: trên là Recall trần, dưới phóng to bốn phương pháp. Rộng 16 cm, cao khoảng 13,7 cm; Phong chỉnh chiều cao nếu cần theo mục 6.6 của THONG_NHAT.

## Việc của Phong

- [ ] Đọc `scripts/m4_test.py` và so với bản hiện tại; sửa nếu cần (ví dụ tên đầu ra, hình, hoặc thêm so sánh bootstrap khác).
- [ ] Chép `m4_test.py` và `m4_common.py` vào dự án; chạy lại toàn bộ unittest và ghi kết quả.
- [ ] **Không chạy lệnh `test`.** Lệnh này chỉ chạy một lần, sau khi Vương và Phong cùng duyệt `lock.json` và ghi vào bảng theo dõi của biên bản lần 1.
- [ ] Viết thêm test cho cổng khóa nếu muốn (ví dụ sửa một byte trong tệp đã khóa thì `run` phải dừng).

## Lưu ý

- `lock.json` hiện khóa dữ liệu và cấu hình, **chưa khóa mã nguồn**; `m4_common.py` và `m4_test.py` mới đổi sau lúc khóa nháp (01/11). Đề nghị trước khi khóa chính thức, Vương mở rộng `m4_lock.py` để ghi thêm hash của các tệp mã dùng cho bước test, rồi chạy lại `m4_lock.py`.
- Kết quả trong `dry_run_validation/` là số validation, chỉ để kiểm tra mã; số đưa vào bài lấy từ lượt chấm test sau khóa.
