# Gửi Phong — Kết quả chấm tập test (chính thức), 04/11/2026

Sau khi Phong đồng ý `lock.json` bắt đầu `fe2db0a7`, Vương chạy `m4_lock.py --approve Phong Vuong` lúc **16:10:47** (chỉ `locked_at` và `approvals` đổi so với bản đã duyệt; hash 16 tệp, cấu hình, ngưỡng giữ nguyên), rồi chạy `scripts/m4_test.py test` **một lần** trên máy Vương lúc 16:11:02, xong 16:17:37 (6 phút 35 giây, thoát mã 0, không lỗi). Không chạy lại.

Hash `lock.json` chính thức: `e38b04f22b66438a737597753ef4007cd694adbe809ca62ac9fdfd734dfdb1b7` (ghi cả trong `test_started.json` và `results_test.json`).

## Đã kiểm sau lượt chạy

- Hash 8 đầu ra khớp `results_test.json`; hash `lock.json` trong kết quả khớp tệp hiện có; 16 tệp khóa vẫn nguyên hash sau lượt chạy.
- 24.877 giỏ test đủ điều kiện (trong 26.242 giỏ test), 49.473 sản phẩm che, 24.758.284 cặp ứng viên, 25.958 cặp dương; mỗi phương pháp đủ 24.877 giỏ, không trùng người dùng. Số giỏ và sản phẩm che khớp lúc che giỏ ngày 01/11.
- Mọi lựa chọn (phương pháp chính RF, cấu hình A, ngưỡng F1) lấy từ khóa, không đổi sau khi xem test.

## Số liệu test (chép từ CSV)

**Bảng 4.5 — chỉ số xếp hạng** (`ranking_metrics_test.csv`):

| Phương pháp | P@5 | R@5 | P@10 | R@10 | HR@10 |
|---|---|---|---|---|---|
| Popularity | 0,0199 | 0,0509 | 0,0149 | 0,0755 | 0,1393 |
| Rules | 0,0249 | 0,0650 | 0,0181 | 0,0924 | 0,1655 |
| LR | 0,0235 | 0,0614 | 0,0178 | 0,0910 | 0,1627 |
| RF | 0,0257 | 0,0677 | 0,0187 | **0,0971** | 0,1708 |

Recall@10 trần: 0,5198 (`R@10_ceiling`). Recall@K từ K = 1 đến 10 và đường trần: `recall_at_k_test.csv`; hình: `figures/fig-recall-at-k-test.pdf|png` (hai khung chung trục K).

**Kiểm định chính — bootstrap ghép cặp theo người dùng, 2.000 lần, seed 42** (`paired_bootstrap_test.csv`, n = 24.877):

| So sánh | Chênh lệch Recall@10 | CI 95% | Cải thiện (cận dưới > 0) |
|---|---|---|---|
| RF so với Popularity (chính) | 0,02158 | [0,01923; 0,02386] | Có |
| RF so với Rules (bổ trợ) | 0,00473 | [0,00309; 0,00630] | Có |
| LR so với RF (bổ trợ) | −0,00608 | [−0,00769; −0,00437] | Không |

**Chỉ số phân loại tại ngưỡng F1 đã khóa trên validation** (`classifier_metrics_test.csv`, `confusion_matrix_test.csv`; toàn bộ 24.758.284 cặp):

| Mô hình | Ngưỡng | Accuracy | Precision | Recall | F1 | ROC-AUC | AP | TN | FP | FN | TP |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LR | 0,73128 | 0,99735 | 0,04803 | 0,08113 | 0,06034 | 0,78832 | 0,01401 | 24.690.586 | 41.740 | 23.852 | 2.106 |
| RF | 0,57771 | 0,99738 | 0,05383 | 0,09034 | 0,06746 | 0,81353 | 0,01685 | 24.691.109 | 41.217 | 23.613 | 2.345 |

Tỷ lệ dương 25.958/24.758.284 ≈ 0,105%, nên Accuracy gần 1 chỉ phản ánh lớp âm áp đảo; đọc cùng Precision, Recall, F1, AP.

## Ghi chú để viết

- Số trong bài chép từ các CSV này; Recall trần 0,5198 phải đi kèm Bảng 4.5 và Hình 4.1.
- Kết quả test gần như trùng validation (RF 0,0971 ở cả hai tập; thứ tự Popularity < LR < Rules < RF giữ nguyên); không diễn giải LR kém Rules/RF là "lỗi" khi chưa có số đo riêng, chỉ báo thứ tự và khoảng tin cậy.
- ROC-AUC và AP tái lập từng chữ số trên máy Vương nhờ RF chạy một luồng; báo 4 chữ số thập phân.
- `basket_metrics_test.csv` (99.508 dòng) là bảng theo giỏ làm đầu vào bootstrap.
- Importance, hệ số LR, ablation và hai giỏ ví dụ đã có từ validation (gói A, 04/11); theo thiết kế importance tính trên validation, không cần chạy lại.

## Việc của Phong

- [ ] Đối chiếu ngẫu nhiên 10 số trong bảng trên với CSV.
- [ ] Viết 4.3.2, 4.4, 4.5, 4.6 từ các CSV này và các bảng validation trong gói A; không chạy lại `m4_test.py` (cổng từ chối).
- [ ] Phần chữ trong QMD tính sau theo kế hoạch hai bạn.
