# Mã nguồn Chương 4 — bản gửi Phong kiểm chứng (04/11/2026)

## Ghi chú quan trọng

- **Toàn bộ mã Chương 4 chạy trên máy Vương** (Windows 11, RAM 24 GB, môi trường `.venv-m2`: Python 3.12.14, pandas 3.0.1, NumPy 2.3.5, scikit-learn 1.9.1, mlxtend 0.25.0, theo `requirements.txt`). Mọi số liệu trong bài lấy từ các lượt chạy trên máy này.
- **Phong là người kiểm chứng**: đọc mã, đối chiếu hash, chạy bộ unittest và kiểm số. Phong **không chạy lại** các lượt chính thức và **không chạy** `m4_test.py test` (cổng khóa từ chối vì tập test đã được chấm một lần).
- Thư mục này chỉ có **mã, cấu hình, test và `requirements.txt`**, giữ đúng cấu trúc dự án (`scripts/`, `tests/`, `configs/`). Không kèm dữ liệu (Master, M2, M4) và đầu ra; các đầu ra đã gửi riêng trong gói A và gói kết quả test.
- Mã đã **khóa** lúc 16:10:47 ngày 04/11/2026 (`lock.json`, hash `e38b04f2…`). Bảy tệp trong thư mục này nằm trong khóa và khớp từng hash: `scripts/m4_test.py`, `m4_common.py`, `m4_classifier.py`, `project_io.py`, `requirements.txt`, `configs/m2_plot_style.json`, `configs/m4_model.json`. Không sửa các tệp này.

## Các tệp và vai trò

| Tệp | Chủ | Việc làm | Dòng* | Trong khóa |
|---|---|---|---|---|
| `scripts/m4_common.py` | Vương | Nền: dựng giỏ và phép che, danh mục C, khai phá, khớp luật và 7 đặc trưng, mẫu âm, chỉ số xếp hạng, nạp lại cấu hình giai đoạn A | 196 | Có |
| `scripts/m4_prepare.py` | Vương | Dựng giỏ fit, validation, test từ Master và che sản phẩm một lần (seed 42) | 38 | Không |
| `scripts/m4_mining.py` | Vương | Danh mục C và luật FP-Growth cho 12 tổ hợp của lưới A | 42 | Không |
| `scripts/m4_benchmark_mining.py` | Vương | So Apriori và FP-Growth (tiến trình con riêng, RAM đỉnh, kiểm tương đương itemset) | 77 | Không |
| `scripts/m4_validate.py` | Vương | Giai đoạn A (24 cấu hình luật) và giai đoạn B (LR, RF), ngưỡng F1, phép bỏ nhóm đặc trưng, trên validation | 141 | Không |
| `scripts/m4_lock.py` | Vương | Giai đoạn C: chọn phương pháp chính, ghi `lock.json` (hash mã, dữ liệu; `approvals` qua `--approve`) | 41 | Không |
| `scripts/m4_report.py` | Vương | Bảng mô tả hai tập, độ phủ luật, importance, hệ số LR, giỏ ví dụ, hình importance (validation) | 91 | Không |
| `scripts/m4_classifier.py` | Phong | `Pipeline`/`ColumnTransformer`, LR và RF, lưới giai đoạn B (`fit_grid`), chế độ `--demo` dữ liệu tự tạo | 103 | Có |
| `scripts/m4_test.py` | Phong | Chỉ số phân loại, bootstrap ghép cặp, cổng khóa và chấm tập test một lần | 171 | Có |
| `scripts/m4_interpret.py` | Phong | Permutation importance bằng AP, hệ số LR, hình mẫu (`--demo`) | 96 | Không |
| `scripts/project_io.py` | Vương | Tiện ích dùng chung: đường dẫn tương đối, ghi nguyên tử, cổng hash, thiết lập hình | 94 | Có |
| `configs/m4_model.json` | Vương | Seed, lưới A và B, dung sai hòa, số mẫu âm, K, bootstrap | — | Có |
| `configs/m2_plot_style.json` | Chung | Phông, cỡ chữ, DPI cho mọi hình | — | Có |
| `tests/test_m4_data.py` | Vương | 13 test: phép che, danh mục, khớp luật, chỉ số tính tay, tương đương Apriori và FP-Growth, mẫu âm | — | Không |
| `tests/test_m4_model.py` | Phong | 7 test: Pipeline, ngưỡng F1, chỉ số phân loại, bootstrap | — | Không |
| `tests/test_m4_interpret.py` | Phong | 4 test: importance và hệ số LR | — | Không |
| `tests/test_m4_environment.py` | Phong | 1 test: phiên bản thư viện | — | Không |
| `tests/test_m4_gate.py` | Phong | 2 test: cổng khóa, chạy một lần, RF một luồng, đầu ra tự tạo | — | Không |

\* Số dòng khác rỗng, gồm docstring và chú thích. Mỗi tệp `.py` có mục "ĐỌC NHANH" ở đầu và chú thích theo khối để đọc theo từng khối lớn.

## Thứ tự chạy và trạng thái (tất cả trên máy Vương)

| Bước | Lệnh (`.\.venv-m2\Scripts\python.exe ...`) | Đã chạy | Đầu ra chính |
|---|---|---|---|
| C4.1 | `scripts/m4_prepare.py` | 01/11 | `M4/masked_baskets.parquet` |
| C4.2 | `scripts/m4_mining.py` | 01/11 (khoảng 24 giây) | `M4/catalog.parquet`, `M4/rules_grid.parquet` |
| C4.3 | `scripts/m4_benchmark_mining.py 1000 20 2` và `2000 20 3` | 01/11 | `mining_benchmark_*.csv`, `itemset_equivalence_*.json` |
| C4.4 | `scripts/m4_validate.py` | 01/11 (xong lúc 23:19) | lưới A, lưới B, `validation_methods.csv`, `basket_metrics_validation.csv`, `classifier_validation.csv`, `ablation.csv`, hai Pipeline |
| C4.5 | `scripts/m4_lock.py --approve Phong Vuong` | 04/11 16:10:47 | `lock.json` chính thức |
| C4.6 | `scripts/m4_report.py` | 01/11 (16 phút 48 giây) | importance, hệ số LR, `dataset_description.csv`, `rule_coverage.json`, giỏ ví dụ, `fig-importance` |
| C4.7 | `scripts/m4_test.py test` | 04/11 16:11:02 đến 16:17:37, **một lần** | `*_test.csv`, `results_test.json`, `fig-recall-at-k-test` |

Ghi chú: `m4_lock.py` chỉ đổi 04/11 (thêm hash mã, `approvals`) sau lượt validation 01/11; `m4_report.py`, `m4_validate.py` và các tệp khác thêm chú thích khối ngày 03/11, cấu trúc code không đổi khi kiểm (so cây cú pháp trước và sau).

## Phong kiểm chứng như thế nào

1. **Hash:** tính SHA-256 `DANH_SACH.txt`; với bảy tệp trong khóa, so với `lock.json` (đã có trong gói kết quả test; hoặc chạy `kiem_lock.py` trong gói khóa nháp).
2. **Chép vào máy Phong** giữ đúng cấu trúc thư mục, chạy `.\.venv-m2\Scripts\python.exe -m unittest discover -s tests -v`; ghi kết quả. Trong thư mục này chỉ có 27 test `m4_*`; toàn bộ dự án trên máy Vương là 57 test.
3. **Đọc mã:** theo mục "ĐỌC NHANH" đầu mỗi tệp, rồi các khối có chú thích. Ghi chỗ nào khó hiểu hoặc nghi sai.
4. **Đối chiếu số:** chọn ngẫu nhiên 10 số trong bài so với CSV nguồn; tính lại độc lập vài số (đã làm cho Rules Recall@10 trên 50 giỏ).
5. **Báo lại** bằng danh sách phát hiện; Phong không sửa tệp trong thư mục này. Đề xuất sửa gửi cho Vương; mọi sửa mã sau khóa phải được hai bên ghi lại.

## Phụ thuộc và quy ước

- Đường dẫn trong mã đều tương đối so với thư mục bài (`ROOT` trong `project_io.py`); không có đường dẫn tuyệt đối.
- Mã cần dữ liệu `DATA/` và `BAO CAO/` của dự án (không kèm). Với `m4_classifier.py --demo` và `m4_interpret.py --demo` chỉ dùng dữ liệu tự tạo, đầu ra có hậu tố `_SYNTHETIC`, không dùng làm kết quả.
- Mọi hạt giống nằm trong `configs/m4_model.json`: che 42, mẫu âm 43, importance 44, bootstrap 42.
