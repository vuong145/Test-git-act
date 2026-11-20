# PRJ-08 — Phân tích giỏ hàng và đề xuất bán chéo trên dữ liệu Instacart quy mô lớn

Bài tiểu luận kết thúc học phần **Lập trình Python cho Khoa học Dữ liệu**, Khoa Khoa học Dữ liệu, Trường Đại học Tài chính – Marketing.

| | |
|---|---|
| Giảng viên | Trần Mạnh Tường |
| Lớp học phần | 2631101190501 |
| Nhóm | 01 |
| Thành viên | Lê Văn Vương — 2521001118; Hoàng Thanh Phong — 2521001087 |

**Phân công.** Vương: làm sạch `aisles`, `departments`, `order_products__prior`; bảng Master; benchmark; thống kê mô tả; phần dữ liệu, luật kết hợp và chọn cấu hình của Chương 4. Phong: làm sạch `products`, `orders`, `order_products__train`; phân tích đa biến; kiểm định giả thuyết; Pipeline phân loại; chấm tập test; Chương 5; hợp nhất báo cáo. Hai thành viên rà soát chéo mã và số liệu của nhau.

---

## 1. Hồ sơ nộp

| Thành phần | Vị trí |
|---|---|
| Báo cáo PDF (45 trang; từ bìa đến hết Chương 5 là 43 trang) | [`2521001118_Nhom01_TieuLuan.pdf`](2521001118_Nhom01_TieuLuan.pdf) |
| Mã nguồn báo cáo (Quarto) | [`2521001118_Nhom01_TieuLuan.qmd`](2521001118_Nhom01_TieuLuan.qmd), [`references.bib`](references.bib), [`styles/apa.csl`](styles/apa.csl) |
| Nhật ký làm việc (P-D-M-V, 27 phiên, mới nhất ở trên) | [`nhật ký làm việc.md`](<nhật ký làm việc.md>) — nhật ký của Lê Văn Vương |
| Nhật ký của Hoàng Thanh Phong | Phong nộp riêng |
| Toàn văn mã nguồn có số dòng (48 tệp) | [`toàn bộ mã nguồn.md`](<toàn bộ mã nguồn.md>) |
| Mã chạy được | [`scripts/`](scripts/), [`tests/`](tests/), [`configs/`](configs/), [`requirements.txt`](requirements.txt) |
| Kết quả thực nghiệm (bảng, hình, hồ sơ kiểm tra) | [`BAO CAO/`](<BAO CAO/>) |
| **Dữ liệu** (36 tệp, khoảng 1,46 GiB, không đưa lên GitHub) | **[Google Drive](https://drive.google.com/drive/folders/1rGwQMeVEZPvD4GlIWjp9pco8HCs81gc1)** — hướng dẫn ở mục 4; SHA-256 từng tệp trong [`DATA_SHA256.txt`](DATA_SHA256.txt) |

---

## 2. Kết quả chính

| Nội dung | Kết quả | Tệp nguồn |
|---|---|---|
| Bảng Master | 1.384.617 dòng × 15 cột, 131.209 giỏ; 4 phép ghép khớp 100% | `DATA/Data đã làm sạch/Bảng master TLCK/join_audit.csv`, `master_verification.json` |
| Tối ưu bộ nhớ | DataFrame giảm từ 423,04 xuống 50,10 MiB (−88,16%); đọc Parquet nhanh hơn CSV khoảng 29,59 lần | `DATA/Data đã làm sạch/Bảng master TLCK/data_benchmark.csv` |
| Apriori và FP-Growth | Cùng itemset và support; FP-Growth khai phá nhanh hơn khoảng 4,1 và 14,3 lần ở hai cấu hình | `BAO CAO/Bao cao mo hinh/mining_benchmark_*.csv`, `itemset_equivalence_*.json` |
| Recall@10 trên 24.877 giỏ test | Popularity 0,0755; Rules 0,0924; LR 0,0910; **RF 0,0971**; trần 0,5198 | `BAO CAO/Bao cao mo hinh/ranking_metrics_test.csv` |
| Kiểm định chính (bootstrap ghép cặp, 2.000 lần) | RF − Popularity = 0,0216, khoảng tin cậy 95% [0,0192; 0,0239] | `BAO CAO/Bao cao mo hinh/paired_bootstrap_test.csv` |
| Phân loại (RF) | ROC-AUC 0,8135; Average Precision 0,0169 | `BAO CAO/Bao cao mo hinh/classifier_metrics_test.csv` |

Mọi số trong báo cáo được chép từ các tệp CSV/JSON trong `BAO CAO/` và `DATA/`. Tập test được chấm **đúng một lần** (04/11/2026 16:11) sau khi cấu hình đã khóa; xem mục 6.

---

## 3. Đối chiếu nhanh với barem

| Trụ cột | Nơi xem trong báo cáo | Nơi xem trong mã và kết quả |
|---|---|---|
| I. Vấn đề và dữ liệu lớn | 1.2–1.3 (câu hỏi, mục tiêu), 3.1–3.2 (6 tệp, ghép bảng, kiểu dữ liệu, Parquet, benchmark) | `scripts/m1_build_master.py` (`build`, ghép `merge(..., validate="many_to_one")` dòng 160, ép `category` dòng 178); đọc theo khối 250.000 dòng ở `scripts/cleaning/common.py` (`chunks`, dòng 64) |
| II. Làm sạch và EDA | 3.3 (quy tắc làm sạch, Bảng 3.5–3.6, ngoại lai IQR), 3.4–3.5 (7 hình, insight I1–I5), 3.6 (Chi-square, Holm) | `scripts/cleaning/` (`numeric`, `RowSequence`, `clean_detail`); `scripts/m2_*.py`; `BAO CAO/Bao cao lam sach/before_after.csv`; `BAO CAO/Bao cao EDA/` |
| III. Mô hình và đánh giá | 4.1–4.6 | `scripts/m4_classifier.py` (`build_pipeline`, dòng 25: `Pipeline` + `ColumnTransformer`); `scripts/m4_common.py` (`mask`, `basket_features`, `evaluate`); `scripts/m4_test.py` (`checked_lock` dòng 93, `paired_bootstrap` dòng 60); `scripts/m4_interpret.py` (permutation importance) |
| IV. Khuyến nghị | 5.1 (khuyến nghị, khung hòa vốn), 5.2 (lộ trình 4 bước, KPI), 5.3 (hạn chế, đạo đức dữ liệu) | — |
| V. Hình thức, mã, nhật ký | APA 7 (`references.bib`, `styles/apa.csl`); 57 kiểm thử | `nhật ký làm việc.md`; `toàn bộ mã nguồn.md`; `tests/` |

---

## 4. Lấy dữ liệu từ Google Drive

1. Tải thư mục `DATA` từ Google Drive: <https://drive.google.com/drive/folders/1rGwQMeVEZPvD4GlIWjp9pco8HCs81gc1>.
2. Đặt nó vào **gốc repo**, cạnh tệp `.qmd`, để có `./DATA/...`.
3. **Giữ nguyên tên thư mục có dấu**, vì mã đọc đúng các tên này: `Data đã làm nhiễu`, `Data đã làm sạch`, `Data phai sinh`. Nếu giải nén ZIP, dùng công cụ hỗ trợ tên tệp UTF-8 (7-Zip, hoặc trình giải nén mặc định của Windows 11/macOS).
4. Kiểm dữ liệu tải về (Git Bash, macOS hoặc Linux; chạy từ gốc repo): `sha256sum -c DATA_SHA256.txt`. Đúng thì mỗi dòng in `OK` (36 tệp).

```text
DATA/
├── Data đã làm nhiễu/          6 CSV do giảng viên cung cấp (khoảng 722 MB) — đầu vào bước làm sạch
├── Data đã làm sạch/           6 CSV sạch (khoảng 705 MB) + master_train.parquet (17 MB)
│   └── Bảng master TLCK/       9 hồ sơ của bảng Master (join_audit, master_schema, data_benchmark…)
└── Data phai sinh/
    ├── M2/                     phân hoạch người dùng, tập reference, bảng giỏ (khoảng 7 MB)
    └── M4/                     giỏ đã che, danh mục, luật, đặc trưng, 2 Pipeline đã huấn luyện, hashes.json (khoảng 21 MB)
```

| Muốn làm gì | Cần phần nào của `DATA/` |
|---|---|
| Chạy 57 kiểm thử | Không cần |
| Kiểm hash toàn bộ kết quả (mục 6) | `Data đã làm sạch/master_train.parquet`, `Data phai sinh/M2/`, `Data phai sinh/M4/` (khoảng 45 MB) |
| Chạy lại phân tích Chương 3 (mục 3.4–3.6) | `master_train.parquet` và `Data phai sinh/M2/` |
| Chạy lại Chương 4 | `master_train.parquet`, `Data phai sinh/M2/`, `Data phai sinh/M4/` |
| Làm sạch lại từ đầu và dựng lại Master | `Data đã làm nhiễu/` (các bước sau sinh ra phần còn lại) |

---

## 5. Cài đặt môi trường

- **Python 3.12.** Bài được chạy bằng 3.12.14; bộ 57 kiểm thử cũng đạt trên 3.12.10. Cần Python từ 3.11 trở lên.
- **Phiên bản thư viện** khóa trong `requirements.txt`: pandas 3.0.1, NumPy 2.3.5, PyArrow 26.0.0, SciPy 1.16.3, Matplotlib 3.10.8, Seaborn 0.13.2, scikit-learn 1.9.1, mlxtend 0.25.0, psutil 7.2.2.
- **Font Times New Roman** cần cho các script vẽ hình (`configs/m2_plot_style.json`). Nếu máy không có font này, script vẽ sẽ dừng với thông báo lỗi; các bước còn lại không bị ảnh hưởng.
- Mọi lệnh chạy **từ gốc repo**. Mọi đường dẫn trong mã đều tương đối theo thư mục này; mã không chứa đường dẫn tuyệt đối.

Windows (PowerShell):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS / Linux:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Các lệnh dưới đây viết cho Windows; trên macOS/Linux thay `.\.venv\Scripts\python.exe` bằng `.venv/bin/python`.

---

## 6. Kiểm tra nhanh

**a) 57 kiểm thử, khoảng 15 giây, không cần `DATA/`:**

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p "test_*.py"
```

**b) Kiểm hash, khoảng 1 giây, cần `DATA/` theo mục 4.** Lệnh chỉ đọc, không ghi tệp nào:

```powershell
.\.venv\Scripts\python.exe -B -c "import sys; sys.path.insert(0, 'scripts'); import project_io as p; [print(f, len(p.check_hashes(f)['files']), 'OK') for f in ['BAO CAO/Bao cao EDA/common/hashes.json', 'BAO CAO/Bao cao EDA/ban2/hashes.json', 'DATA/Data phai sinh/M4/hashes.json']]; L = p.read_json(p.path('BAO CAO/Bao cao mo hinh/lock.json')); ok = sum(p.sha256(p.path(n)) == d for n, d in L['files'].items()); print('lock.json', ok, '/', len(L['files'])); print('test_started -> lock', p.read_json(p.path('BAO CAO/Bao cao mo hinh/test_started.json'))['lock_sha256'] == p.sha256(p.path('BAO CAO/Bao cao mo hinh/lock.json')))"
```

Kết quả đúng:

```text
BAO CAO/Bao cao EDA/common/hashes.json 6 OK
BAO CAO/Bao cao EDA/ban2/hashes.json 10 OK
DATA/Data phai sinh/M4/hashes.json 6 OK
lock.json 16 / 16
test_started -> lock True
```

**Chuỗi bằng chứng của tập test:**

1. `BAO CAO/Bao cao mo hinh/test_started.json` ghi SHA-256 của `lock.json`. Tệp này được tạo trước khi nạp tập test.
2. `lock.json` (khóa lúc 04/11/2026 16:10:47, có xác nhận của cả hai thành viên) ghi phương pháp chính, ngưỡng F1 và SHA-256 của 16 tệp: mã nguồn, cấu hình, `requirements.txt`, Master và dữ liệu Chương 4.
3. `results_test.json` ghi SHA-256 của 8 tệp kết quả test.

`scripts/m4_test.py` từ chối chạy nếu bất kỳ tệp nào trong khóa bị đổi. Repo dùng `.gitattributes` (`* -text`) để Git không đổi ký tự xuống dòng, nhờ vậy hash giữ đúng trên mọi hệ điều hành.

---

## 7. Chạy lại toàn bộ quy trình

> **Nên chạy trên một bản sao của repo.** Các script ghi đè kết quả trong `BAO CAO/` và `DATA/`. Nếu chạy lại các bước Chương 4 trước khóa (C4.1–C4.4), các tệp đã khóa sẽ bị ghi lại và `lock.json` sẽ không còn khớp.

| Bước | Lệnh (`.\.venv\Scripts\python.exe` + …) | Mục | Ghi chú |
|---|---|---|---|
| 1 | `scripts/cleaning/clean_vuong.py` | 3.3 | aisles, departments, prior; khoảng 10 phút (prior 32,4 triệu dòng, đọc theo khối) |
| 2 | `scripts/cleaning/clean_phong.py` | 3.3 | products, orders, train |
| 3 | `scripts/summarize_cleaning.py` | 3.3 | Gộp báo cáo, đối chiếu SHA-256 của 6 CSV sạch |
| 4 | `scripts/m1_build_master.py` | 3.2 | Dựng `master_train.parquet`, 13 tiêu chí kiểm tra |
| 5 | `scripts/m1_quality_summary.py` | 3.2–3.3 | Tỷ lệ thiếu, ngoại lai IQR |
| 6 | `scripts/m1_inspect_artifact.py` | 3.2 | `shape`, `info(memory_usage="deep")`, hai chế độ đọc |
| 7 | `scripts/m1_benchmark.py` | 3.2 | **Chạy một mình** để số đo không bị nhiễu; số đo thời gian sẽ khác máy nhóm |
| 8 | `scripts/m2_foundation.py` | 3.4 | Chia 4 tập theo người dùng (PCG64, seed 42) |
| 9 | `scripts/m2_profile_inputs.py`, `scripts/m2_eda_summary.py`, `scripts/m2_plot_univariate.py` | 3.4–3.5 | Thống kê mô tả, Hình 3.2–3.3 |
| 10 | `scripts/m2_eda_multivariate.py`, `scripts/m2_plot_multivariate.py` | 3.5 | Hình 3.4–3.7 |
| 11 | `scripts/m2_hypothesis_tests.py` | 3.6 | Chi-square, Cramér's V, Holm |
| C4.1 | `scripts/m4_prepare.py` | 4.1–4.2 | Che giỏ (seed 42) |
| C4.2 | `scripts/m4_mining.py` | 4.3 | Lưới luật FP-Growth |
| C4.3 | `scripts/m4_benchmark_mining.py 1000 20 2` và `… 2000 20 3` | 4.3 | Apriori và FP-Growth, 3 lượt mỗi thuật toán |
| C4.4 | `scripts/m4_validate.py` | 4.1–4.3 | Chọn cấu hình trên validation; khoảng 30 phút |
| C4.5 | `scripts/m4_lock.py --approve Phong Vuong` | 4.3 | Ghi `lock.json`; từ chối nếu test đã bắt đầu |
| C4.6 | `scripts/m4_report.py` | 4.1, 4.5 | Importance, hệ số LR, mô tả tập; khoảng 17 phút |
| C4.7 | `scripts/m4_test.py test` | 4.4 | **Đã chạy ngày 04/11/2026, cố ý bị chặn nếu chạy lại** (xem dưới) |
| — | `scripts/render_pdf.py --no-open` | — | Xuất PDF; cần Quarto, XeLaTeX, font Times New Roman và Consolas |

Thời gian ghi trên đo ở máy của nhóm: Windows 11, RAM 24 GB, AMD Ryzen 8 nhân/16 luồng.

**Thử nghiệm nhanh, không ảnh hưởng hồ sơ chính thức:**

```powershell
# Chạy toàn bộ Chương 4 trên mẫu nhỏ (pilot_baskets trong configs/m4_model.json; khoảng 2 phút)
# Kết quả ghi vào các thư mục con pilot/, không ghi đè tệp chính thức.
.\.venv\Scripts\python.exe scripts/m4_validate.py --pilot

# Chạy cùng mã chấm test (qua cổng lock.json) nhưng trên validation, ghi ra thư mục riêng; khoảng 11 phút.
# Recall@10 in ra phải trùng số validation trong lock.json:
# Popularity 0,0752; Rules 0,0932; LR 0,0923; RF 0,0971; trần 0,5211.
.\.venv\Scripts\python.exe scripts/m4_test.py validation thu_validation

# Hai bản minh họa trên dữ liệu tự tạo
.\.venv\Scripts\python.exe scripts/m4_classifier.py --demo
.\.venv\Scripts\python.exe scripts/m4_interpret.py --demo
```

**Vì sao `m4_test.py test` không chạy lại được.** Thiết kế cho phép chấm tập test đúng một lần: `test_started.json` được tạo độc quyền trước khi nạp dữ liệu test, và lần chạy sau sẽ bị từ chối. Như vậy tập test không thể được dùng để chọn lại mô hình. Muốn xem cơ chế chấm, dùng chế độ `validation` ở trên.

---

## 8. Cấu trúc thư mục

```text
.
├── 2521001118_Nhom01_TieuLuan.pdf / .qmd   báo cáo và mã nguồn báo cáo
├── nhật ký làm việc.md                     nhật ký P-D-M-V
├── toàn bộ mã nguồn.md                     toàn văn mã có số dòng
├── references.bib, styles/apa.csl          tài liệu tham khảo APA 7
├── requirements.txt                        phiên bản thư viện
├── DATA_SHA256.txt                         SHA-256 của 36 tệp dữ liệu trên Google Drive
├── .gitattributes, .gitignore              giữ nguyên byte mọi tệp; loại DATA/ và tệp sinh tự động
├── assets/                                 logo và hình dùng trong PDF (bản sao byte của hình do mã sinh)
├── configs/                                tham số đã chốt (chia tập, kiểm định, Chương 4, kiểu hình)
├── scripts/                                mã nguồn; thứ tự chạy chi tiết ở scripts/README.md
│   └── cleaning/                           làm sạch 6 bảng (common.py dùng chung, config_*.json)
├── tests/                                  57 kiểm thử (chạy được khi chưa có DATA/)
├── BAO CAO/
│   ├── Bao cao lam sach/                   kiểm tra làm sạch, trước–sau, tỷ lệ thiếu
│   ├── Bao cao kiem tra data rac/          kiểm tra dữ liệu nhiễu ban đầu
│   ├── Bao cao EDA/                        bảng và hình Chương 3; common/ và ban2/ chứa hashes.json
│   └── Bao cao mo hinh/                    bảng, hình, lock.json, kết quả test Chương 4
├── TAI_LIEU_NOI_BO/                        hồ sơ quá trình: trao đổi giữa hai thành viên, thiết kế, bản lưu (xem dưới)
└── DATA/                                   tải từ Google Drive (mục 4)
```

**Về `TAI_LIEU_NOI_BO/` và các đường dẫn `Chung/…` trong nhật ký.** Trong lúc làm bài, nhóm trao đổi qua thư mục chung `Chung/`: thiết kế, gói gửi và nhận giữa hai thành viên, bản sao lưu trước mỗi thay đổi lớn, mã cũ trước đợt rút gọn ngày 31/10. Thư mục này không nộp nguyên vẹn vì có dữ liệu lớn và nhiều bản sao trùng. `TAI_LIEU_NOI_BO/` chép lại, giữ nguyên cấu trúc: các tài liệu nhật ký có liên kết tới, và toàn bộ tài liệu trao đổi giữa hai thành viên trong `Gửi và nhận/` (155 tệp: thư gửi kèm gói, danh sách SHA-256, `.diff`, nhật ký chạy kiểm thử, biên bản đồng ý khóa và xác nhận bản chốt, mã Phong gửi). [`TAI_LIEU_NOI_BO/Gửi và nhận/DANH_MUC_MINH_CHUNG.tsv`](<TAI_LIEU_NOI_BO/Gửi và nhận/DANH_MUC_MINH_CHUNG.tsv>) xếp các tệp này theo ngày sửa gốc, kèm chiều gửi và SHA-256; tiêu chí lược bỏ ghi ở [`TAI_LIEU_NOI_BO/README.md`](TAI_LIEU_NOI_BO/README.md). Các đường dẫn `Chung/…` còn lại trong nhật ký là văn bản ghi chú, không phải liên kết. Mã chạy được không phụ thuộc `TAI_LIEU_NOI_BO/`.

---

## 9. Giới hạn đã biết

- Số liệu trong bài được tạo trên một máy (Windows 11). Thời gian và RAM phụ thuộc phần cứng; các số khác (đếm, chỉ số, hash) tái lập được.
- Kết quả dựa trên **một lần chia** tập theo người dùng (seed 42). Bootstrap đo bất định do mẫu người dùng trong test, không đo biến động khi chia lại.
- PEP 8: chưa đạt tuyệt đối. 7 tệp trong khóa (`scripts/m4_test.py`, `m4_common.py`, `m4_classifier.py`, `project_io.py`, `requirements.txt`, `configs/m2_plot_style.json`, `configs/m4_model.json`) được giữ nguyên byte để không phá chuỗi khóa của tập test.
- Số 189.577 người dùng có chuỗi `order_number` đứt đoạn (mục 3.3) lấy từ lượt kiểm tra dữ liệu nhiễu bằng mã cũ, lưu ở `TAI_LIEU_NOI_BO/archive/code_cu_truoc_rut_gon_20261031/scripts/audit/audit_results/04_order_history.txt`; mã hiện tại không ghi lại số này.
- Dữ liệu không có giá bán và lợi nhuận, nên kết quả là hiệu quả ngoại tuyến, chưa chứng minh tăng doanh thu.

---

## 10. Sử dụng AI và nguồn dữ liệu

- Nhóm dùng Claude Code, Codex và Antigravity để hỗ trợ viết mã, rà soát và biên tập. Cách dùng và cách kiểm chứng ghi trong `nhật ký làm việc.md` và Lời cam đoan của báo cáo.
- Dữ liệu: Instacart Market Basket Analysis (Kaggle, 2017), phiên bản do giảng viên bổ sung nhiễu cho học phần. Nhóm không dùng bản gốc để điền hoặc sửa giá trị. Dữ liệu chỉ dùng cho mục đích học tập.
