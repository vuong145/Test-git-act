# KẾ HOẠCH HOÀN THÀNH CHƯƠNG 3 VÀ RÚT GỌN CODE — PRJ-08

Cập nhật: 30/10/2026, sau khi chốt các quyết định ở mục 0. Áp dụng cho cả hai thành viên và các công cụ AI hai người dùng.

Tài liệu này là **kế hoạch thực hiện**: làm gì, theo thứ tự nào, ai làm, khi nào coi là xong. Chi tiết kỹ thuật của việc rút gọn (danh sách file, ngân sách dòng, quy tắc viết code, công cụ so sánh đầu ra, danh sách xóa/lưu trữ) nằm ở `HUONG_DAN_RUT_GON_CODE.md` cùng thư mục. Khi hai tài liệu khác nhau về **thứ tự, phân công hoặc quyết định**, theo tài liệu này.

Đường dẫn tính từ thư mục bài `2521001118_Nhom01_TieuLuan/`, trừ khi ghi rõ gốc `TLCK/`.

---

## 0. Các quyết định đã chốt

| # | Vấn đề | Quyết định |
|---|---|---|
| 1 | Lịch | Không đặt mốc ngày. Làm theo thứ tự ở mục 1 |
| 2 | Người hợp nhất | **Vương**. Bản chính là thư mục bài trên máy Vương. Chỉ Vương ghi vào QMD chính, chạy toàn luồng và render bản cuối |
| 3 | Trao đổi giữa hai máy | Tiếp tục gửi gói ZIP, theo quy tắc gói nhỏ ở mục 1.2 |
| 4 | Cấu trúc thư mục | Giữ cấu trúc trên máy Vương (`DATA/…`, `BAO CAO/…`). Phong đồng bộ thư mục trên máy mình cho giống |
| 5 | Kiểm tra trước khi đọc dữ liệu nền G0 | **Chỉ kiểm tra SHA-256 của các file dữ liệu nền.** Không dùng chuỗi manifest G0 bản 1 hay bản 2 để chặn việc đọc dữ liệu |
| 6 | Sửa code Phong cho khớp máy Vương | **Vương sửa khi ghép**; Phong đọc lại phần đã sửa và chạy lại trên máy Phong |
| 7 | I5 và mục 3.6 | Đưa so sánh với mức nền 210 cặp ngành vào I5 và vào phần giới hạn của 3.6 |
| 8 | Kiểm định phân tầng Cochran–Mantel–Haenszel | **Không làm.** Ba kiểm định đã khóa, có Holm, cỡ hiệu ứng và phần giới hạn là đủ yêu cầu kiểm định của đề và rubric |
| 9 | I4 | Giữ cách viết của Phong (so trung vị kích thước giỏ giữa các khung giờ), bổ sung đúng mức độ và giới hạn (mục A4) |
| 10 | Hình Pearson (4 bổ trợ) và bảng 134 quầy | Giữ trong thân bài |
| 11 | Hiệu chỉnh Holm | Giữ bản Phong tự viết (đã có test, kết quả đúng) |
| 12 | `m1_benchmark.py` | Giữ nguyên, không viết lại; số liệu bảng benchmark ở 3.2 giữ nguyên |
| 13 | Kiểm tra lại code làm sạch sau khi tách | Phong tự chạy `clean_phong.py` trên máy Phong |
| 14 | Rút gọn đợt 1 | Làm **sau khi xong Chương 3 và trước Chương 4** |
| 15 | File tiện ích chung `project_io.py` | Chưa chốt người viết; chốt khi bắt đầu rút gọn đợt 1 (bước B1). Bước ghép chỉ cần một hàm kiểm tra hash nhỏ (mục A2) |

---

## 1. Thứ tự tổng và cách trao đổi

### 1.1. Thứ tự

```
A. Hoàn thành Chương 3     A0 → A1 → A2 → A3 → A4 → A5 → A6 → A7
        ↓
B. Rút gọn đợt 1           B0 → B1 → B2 (song song) → B3 → B4
        ↓
C. Chương 4 (viết theo ngân sách dòng và quy tắc code tối thiểu ngay từ đầu)
        ↓
D. Chương 5, tóm tắt, phụ lục
        ↓
B'. Rút gọn đợt 2          M1 build, gộp test, requirements, xóa/lưu trữ
```

Rút gọn đợt 1 đặt trước Chương 4 vì code Chương 4 sẽ đọc dữ liệu qua đúng cổng kiểm tra hash và tiện ích chung dùng lâu dài; viết Chương 4 trên hạ tầng cũ rồi sửa lại là làm hai lần.

### 1.2. Bản chính và quy tắc gói ZIP

- **Bản chính** là thư mục bài trên máy Vương. Mọi thay đổi của Phong đi vào bản chính qua Vương.
- **Phong đồng bộ cấu trúc thư mục** trên máy mình giống máy Vương: `DATA/Data đã làm nhiễu/`, `DATA/Data đã làm sạch/`, `DATA/Data phai sinh/M2/`, `BAO CAO/Bao cao EDA/…`, `BAO CAO/Bao cao lam sach/…`, `scripts/`, `tests/`, `configs/`, `drafts/`. Sau khi đồng bộ, code Phong cũ có thể chưa chạy được trên máy Phong (vì vẫn dùng đường dẫn `Bao cao EDA/…`); bản code đã sửa sẽ đến từ gói của Vương ở bước A3.

**Quy tắc gói ZIP** (áp dụng cho cả hai chiều):

1. Tên gói: `GUI_<nguoi>_<noi-dung>_<YYYYMMDD>.zip`, ví dụ `GUI_VUONG_ghep-chuong3_20261101.zip`.
2. Chỉ chứa **file mới hoặc đã thay đổi** từ lần gửi trước, giữ nguyên đường dẫn tương đối tính từ thư mục bài.
3. **Không đưa vào gói:** `DATA/Data đã làm nhiễu/`, 6 CSV sạch, `master_train.parquet` (hai máy đã có và đối chiếu bằng hash), `.venv-m2/`, `__pycache__/`, `.mplcache/`, `BAO CAO/**/runs/`, PDF/PNG preview, ZIP khác.
4. Kèm file `DANH_SACH.txt` ở gốc gói: mỗi dòng gồm đường dẫn tương đối, SHA-256, một câu mô tả thay đổi.
5. Người nhận: giải nén vào thư mục mới ngoài thư mục bài → đối chiếu SHA-256 với `DANH_SACH.txt` → đọc thay đổi → mới chép vào thư mục bài.
6. Sau khi chép xong, chuyển gói và thư mục giải nén vào `TLCK/Chung/archive/`. Trong `Chung/Gửi và nhận/` chỉ giữ gói mới nhất mỗi chiều.
7. Gói thông thường chỉ vài MB (gói đầy đủ 3.6 của Phong là 1,9 MB). Gói trên 50 MB là dấu hiệu đã đưa nhầm dữ liệu lớn vào.

---

## 2. Giai đoạn A — Hợp nhất code Chương 3

### A0. Chụp mốc (Vương)

1. Tạo `TLCK/Chung/tools/so_sanh_dau_ra.py` theo mục 6.2 của `HUONG_DAN_RUT_GON_CODE.md`; chạy `python so_sanh_dau_ra.py chup` **trước** mọi thay đổi.
2. Lưu bản sao thư mục `scripts/`, `tests/`, `configs/`, `drafts/` và QMD chính vào `TLCK/Chung/archive/truoc-ghep-chuong3/` (không chép `DATA/`).
3. Ghi lại hash các CSV của Phong trong gói `Chung/Gửi và nhận/Nhận/BAN_GIAO_BAN2_DAY_DU_CO_3_6/` (thư mục `Bao cao EDA/ban2/runs/20261030T073707_dfdcac30/` và `hypotheses/hypotheses.csv`) để so ở A3.

### A1. Phong đồng bộ thư mục (Phong)

Theo mục 1.2. Kiểm tra trên máy Phong có đủ 6 CSV nhiễu (cần cho bước B2) và các file nền trong `DATA/Data phai sinh/M2/` có cùng SHA-256 với máy Vương:

| File | 16 ký tự đầu SHA-256 trên máy Vương |
|---|---|
| `DATA/Data phai sinh/M2/split_manifest.parquet` | `2d6106e5c722b509` |
| `DATA/Data phai sinh/M2/reference.parquet` | `708345868d6981cf` |
| `DATA/Data phai sinh/M2/basket_summary.parquet` | `acb8519c6228607b` |
| `DATA/Data phai sinh/M2/department_lookup.csv` | `e6829cea3da95ec2` |

Nếu khác: dừng và báo Vương; không chạy tiếp trên dữ liệu lệch.

### A2. Vương sửa code Phong và ghép vào thư mục bài

**Cổng kiểm tra dữ liệu (quyết định 5).**

1. Thêm vào `scripts/m2_common.py` hiện có một hàm khoảng 10 dòng, `check_data_hashes(json_path)`: đọc file JSON dạng `{đường dẫn tương đối: sha256}`, tính lại SHA-256 từng file, dừng với thông báo rõ nếu thiếu file hoặc lệch hash.
2. Tạo một lần `BAO CAO/Bao cao EDA/common/hashes.json` cho 6 file: 4 file nền ở bảng A1, `DATA/Data đã làm sạch/master_train.parquet`, `configs/hypotheses_config.json`.
3. Mọi script đọc dữ liệu nền gọi `check_data_hashes(...)` thay cho `load_foundation()` / `verified_multivariate()`. Áp dụng cho cả hai script của Vương (`m2_eda_summary.py`, `m2_plot_univariate.py`) để toàn luồng M2 chạy được trên máy Phong mà không cần hồ sơ nghiệm thu nhiều tầng.
4. Không xóa chuỗi manifest–acceptance–`latest.json` cũ ở bước này; chỉ không còn script nào phụ thuộc vào nó. Xóa ở đợt rút gọn.

**Đưa code và đầu ra Phong vào:**

| Từ gói Phong | Vào thư mục bài | Vương sửa gì |
|---|---|---|
| `scripts/m2_eda_multivariate.py` | `scripts/` | Cổng đọc → `check_data_hashes`; đường dẫn `Bao cao EDA/…` → `BAO CAO/Bao cao EDA/…`, `Data phai sinh/…` → `DATA/Data phai sinh/…`; đọc config phẳng `configs/m2_eda.json` thay cho cấu trúc `outputs.ban2.*` lồng nhau; ghi đầu ra vào đường dẫn cố định, **không** thư mục con theo `run_id`; bỏ khối f-string sinh văn bản tóm tắt (dòng ~137–143) |
| `scripts/m2_plot_multivariate.py` | `scripts/` | Như trên; đổi tên 5 hình (bảng dưới); lưu hình **không** dùng `bbox_inches='tight'` |
| `scripts/m2_hypothesis_tests.py` | `scripts/` | Như trên; đọc `department_presence.parquet` từ `DATA/Data phai sinh/M2/`; giữ Holm tự viết; đổi hàm `p_text` để ghi "< 0,001" (bước A4) |
| `scripts/m2_multivariate_io.py` | Không đưa vào | Chỉ phục vụ chuỗi manifest nhánh |
| `scripts/m2_audit_descriptive.py` | Không đưa vào | Kết quả kiểm tra độc lập đã có trong `Chung/Gửi và nhận/Gửi/DOI_CHIEU_BAN1_BAN2_20261030/checks.json`; phần tính lại chuyển vào `tests/` ở đợt rút gọn |
| `tests/test_m2_multivariate.py`, `tests/test_m2_hypotheses.py`, `tests/fixtures/m2_contingency_cases.json` | `tests/` | Sửa import nếu cần |
| `drafts/m2/ban2/*.qmd` | `drafts/m2/ban2/` | Sửa đường dẫn hình theo tên mới |
| Đầu ra CSV, Parquet, hình | Không chép tay | Tạo lại bằng cách chạy script ở A3 |

**Đổi tên hình** (sửa trong biến `filenames` của `m2_plot_multivariate.py`, không đổi tên file bằng tay):

| Tên hiện tại | Tên mới |
|---|---|
| `Hình 3A - Tần số giờ và ngày đặt đơn` | `fig-ref-time-frequency` |
| `Hình 3B - Kích thước giỏ theo ngày và khung giờ` | `fig-ref-time-basket-size` |
| `Hình 4 - Tương quan Spearman giữa các đặc trưng giỏ hàng` | `fig-ref-corr-spearman` |
| `Hình 4 bổ trợ - Tương quan Pearson giữa các đặc trưng giỏ hàng` | `fig-ref-corr-pearson` |
| `Hình 5 - Mức độ đồng mua giữa 21 ngành hàng (Lift)` | `fig-ref-department-lift` |

Tên không dấu, không dấu cách, không ngoặc giải quyết luôn lỗi `render_pdf.py` cắt đường dẫn ở dấu `)`.

**Vị trí đầu ra cố định:**

| Loại | Thư mục |
|---|---|
| Ma trận hiện diện ngành | `DATA/Data phai sinh/M2/department_presence.parquet` |
| CSV đa biến, `insights_i4_i5.csv`, `hypotheses.csv`, `hypotheses_details.json` | `BAO CAO/Bao cao EDA/ban2/` |
| Dữ liệu vẽ | `BAO CAO/Bao cao EDA/plot_data/ban2/` |
| Hình PNG/PDF | `BAO CAO/Bao cao EDA/figures/ban2/` |

Cột `source` của `insights_i4_i5.csv` ghi đường dẫn tương đối từ thư mục bài.

### A3. Chạy toàn luồng và đối chiếu

**Trên máy Vương**, từ thư mục bài:

```powershell
.\.venv-m2\Scripts\python.exe scripts/m2_eda_summary.py
.\.venv-m2\Scripts\python.exe scripts/m2_plot_univariate.py
.\.venv-m2\Scripts\python.exe scripts/m2_eda_multivariate.py
.\.venv-m2\Scripts\python.exe scripts/m2_plot_multivariate.py
.\.venv-m2\Scripts\python.exe scripts/m2_hypothesis_tests.py
.\.venv-m2\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

Test của dự án viết bằng `unittest`; `.venv-m2` không có `pytest`. Chạy lại một lần từ thư mục khác (ví dụ từ `TLCK/`) bằng đường dẫn đầy đủ tới script.

**Đạt khi:**

- `so_sanh_dau_ra.py so` báo khớp toàn bộ phần Bạn 1 (8 CSV 3.4, `reference_outliers.json`, `plot_data/ban1/`).
- Mọi CSV Phong giống từng byte với gói `BAN_GIAO_BAN2_DAY_DU_CO_3_6` (trừ cột `source` đã sửa đường dẫn).
- `hypotheses.csv`: H1 χ² = 1584,256, V = 0,2006; H2 χ² = 910,419, V = 0,1521; H3 χ² = 913,934, V = 0,1524; cả ba bác bỏ H0 sau Holm; tần số kỳ vọng nhỏ nhất 3.612,0 / 2.763,7 / 1.901,0.
- Số mốc khác: reference 415.053 dòng, 39.363 giỏ, 28.742 sản phẩm; trung vị kích thước giỏ 9; pivot ngày × giờ dùng 23.549 giỏ đủ hai biến; tương quan N = 39.363 (ba biến đếm) và 32.787 (cặp có `days_since_prior_order`).
- Test đạt hết.

**Trên máy Phong:** Vương gửi gói ZIP gồm các script, test, config, `hashes.json`, bản thảo đã sửa. Phong chạy đúng chuỗi lệnh trên; kết quả phải khớp từng byte với máy Vương. Phong đọc lại diff code của mình và báo lại nếu có chỗ Vương sửa làm đổi ý nghĩa.

---

## 3. Giai đoạn A — Nội dung Chương 3

### A4. Hoàn thiện năm insight và mục 3.6

> **Cập nhật 30/10 (theo quyết định của Vương):** khi ghép vào QMD chính chỉ chuẩn hóa hình thức, giữ nguyên lời văn bản thảo của Phong (I4, I5, mô tả hình 3–5, mục 3.6) và bằng chứng I1–I3 của Vương. Bảng gợi ý dưới đây là định hướng để **hai bạn tự viết** bản cuối, không phải nội dung để công cụ AI tự điền vào QMD.

**Năm insight.** Phong tổng hợp bản cuối từ `drafts/m2/ban1_evidence_i1_i3.md` và bản I4–I5; Vương kiểm lại mọi con số với CSV. Mỗi insight theo khung: **số đo + mẫu số → cơ chế kinh tế → hành động có thể thử → giới hạn**.

| Insight | Số đo chính (lấy từ CSV) | Hướng diễn giải |
|---|---|---|
| I1 — Giỏ nhỏ, đuôi dài | Trung vị 9, Q1–Q3 = 5–14; 1.578 giỏ (4,01%) vượt rào 27,5; 2.118 giỏ một sản phẩm (5,38%) | Giỏ đủ nhỏ để gợi ý mua kèm còn chỗ; giỏ một sản phẩm không có ngữ cảnh để gợi ý theo giỏ, cần dự phòng theo độ phổ biến. Không suy ra kiểu hộ gia đình |
| I2 — Tập trung ngành | produce 29,52% dòng, có mặt trong 73,95% giỏ; dairy eggs 15,73% / 66,76% | Hai ngành là điểm chạm của đa số giỏ, hợp làm vị trí đặt gợi ý. Lượt xuất hiện không phải doanh thu |
| I3 — Đuôi dài sản phẩm | Top-1.000 chiếm 52,71% dòng nhưng phủ 91,56% giỏ; 47,29% dòng ngoài Top-1.000 | Đánh đổi kích thước danh mục ứng viên ở Chương 4: danh mục nhỏ phủ gần hết giỏ nhưng bỏ sót gần nửa lượt mua, Recall có trần. Phủ giỏ khác với giữ đủ thành phần giỏ |
| I4 — Nhịp thời gian (giữ cách của Phong) | Trung vị kích thước giỏ: 8 ở khung 18–23 (N = 6.077), 9 ở ba khung còn lại (N = 617 / 10.346 / 15.782); Q1–Q3 gần như trùng nhau (5–14, riêng 06–11 là 5–15); 6.541 giỏ (16,6%) thiếu giờ | Viết đúng mức: chênh lệch **một sản phẩm** theo trung vị, các phân phối chồng lấn gần hoàn toàn, nên thời điểm hầu như không đổi quy mô giỏ. Hành động: không cần tách cấu hình gợi ý theo khung giờ dựa trên quy mô giỏ. Giới hạn: thiếu giờ 16,6%, chưa kiểm định, không suy nhân quả |
| I5 — Đồng mua ngành, nối 3.6 | H1: P(dairy eggs khi có bakery) 82,06% so với 60,92% (chênh 21,14 điểm %), V = 0,20. Mức nền: 182/210 cặp ngành có lift > 1, lift trung vị 1,225. Lift H1 = 1,229 (phân vị ~50), H2 = 1,412 (phân vị ~80), H3 = 1,190 (phân vị ~38) | Liên hệ dương giữa các ngành là **hiện tượng chung** do giỏ chứa nhiều ngành, không phải đặc điểm riêng của bakery–dairy eggs. Chỉ dry goods pasta–pantry nổi hơn mặt bằng. Hàm ý: gợi ý liên ngành phải dựa trên luật cấp sản phẩm và so với mức nền (Chương 4), không dựa vào "hai ngành hay đi cùng". Không suy nhân quả, không suy doanh thu |

Tỷ lệ 182/210, lift trung vị và các phân vị được tính từ `department_pair_summary.csv` (210 cặp ngoài đường chéo). Khi đưa vào bài, ghi rõ cách tính và nguồn này; nên tạo bằng code trong `m2_eda_multivariate.py` (vài dòng) để con số có nguồn tái lập, không chép tay.

**Mục 3.6** — sửa bản thảo `drafts/m2/ban2/ban2_3_6.qmd`:

1. **Cách ghi p:** theo APA 7, ghi "p < 0,001" cho cả ba cặp, kèm χ², bậc tự do, N, V. Thêm một câu chú thích: p chính xác của H1 nhỏ hơn mức máy tính biểu diễn được, nên chỉ ghi theo ngưỡng. Bỏ cụm "< 2,23 × 10⁻³⁰⁸" và không giải thích về giới hạn số thực.
2. **Cỡ hiệu ứng:** với N = 39.363, liên hệ rất yếu cũng có p rất nhỏ. Theo mốc thông dụng của Cohen cho bảng 2×2 (0,1 nhỏ; 0,3 vừa), V = 0,15–0,20 là liên hệ **nhỏ**. Có ý nghĩa thống kê không đồng nghĩa với có ý nghĩa kinh doanh.
3. **Giới hạn bắt buộc:** kích thước giỏ là yếu tố gây nhiễu (giỏ lớn có nhiều ngành hơn nên hai ngành bất kỳ dễ cùng xuất hiện); dẫn số 182/210 cặp có lift > 1 và vị trí lift của ba cặp. Đây là liên hệ, không phải nhân quả hay quan hệ bổ trợ.
4. Đoạn "Diễn giải và giới hạn" hiện là ba câu lặp "bác bỏ H0 sau hiệu chỉnh Holm" → viết lại thành đoạn văn có số theo ý 2–3.
5. Đổi nhãn `chi_square` thành "Chi-square"; mọi số theo định dạng Việt.

### A5. Ghép vào QMD chính (Vương ghép; Phong đọc lại)

**Thay đúng ba chỗ giữ chỗ** ở dòng ~776–786 của `2521001118_Nhom01_TieuLuan.qmd`. Không tạo thêm heading cấp 2.

| Mục | Nguồn | Cấp heading |
|---|---|---|
| `## Phân tích thống kê mô tả` (3.4) | `drafts/m2/ban1_3_4.qmd` | Giữ `##` cho mục; `###` cho ba tiểu mục |
| `## Trực quan hóa dữ liệu và Phát hiện Insight kinh doanh` (3.5) | `ban1_3_5_hinh_1_2.qmd` + `ban2_3_5_hinh_3_5.qmd` + năm insight | `ban2_3_5_hinh_3_5.qmd` đang mở đầu bằng `## Trực quan hóa đa biến — phần Bạn 2` → **bỏ dòng này**, chia thành các `###`: phân phối và cơ cấu (hình 1–2); nhịp thời gian (3A–3B); tương quan (4 và 4 bổ trợ); đồng mua ngành (5); năm insight |
| `## Kiểm định giả thuyết thống kê sơ bộ` (3.6) | `ban2_3_6.qmd` đã sửa ở A4 | Bỏ dòng `##` trùng ở đầu bản thảo |

**Quy chuẩn trình bày** (theo đề và cấu hình QMD hiện có `tbl-cap-location: top`, `fig-cap-location: bottom`):

- Bảng: tên ở trên, dòng "Nguồn: …" ngay dưới. Hình: tên ở dưới, có nguồn.
- Nhãn: hình `#fig-ref-…`, bảng `#tbl-ref-…`; trong lời văn gọi bằng `@fig-…`, `@tbl-…`, không viết tay "Hình 3".
- Số: phân cách nghìn bằng dấu chấm, thập phân bằng dấu phẩy, trong bảng lẫn lời văn. CSV giữ nguyên dạng máy.
- Mỗi bảng/hình ghi rõ mẫu số: 39.363 giỏ; 415.053 dòng; 32.822 giỏ có giờ; 23.549 giỏ đủ ngày–giờ; 32.787 giỏ có khoảng cách giữa hai đơn.
- Hình Pearson và bảng 134 quầy ở thân bài (quyết định 10). Bảng 134 quầy dài nhiều trang: dùng bảng dài tự ngắt trang, lặp dòng tiêu đề, giữ chữ 12 pt, không thu nhỏ để ép vừa trang.

### A6. Render và kiểm tra PDF (Vương render; cả hai xem)

1. Hình Phong được xuất lại ở A3 không dùng `bbox_inches='tight'` (đã có `layout='constrained'` với chiều rộng 6,3 inch = 16 cm) và chèn với `width=16cm`, để chữ trong hình giữ đúng 12 pt.
2. `python scripts/render_pdf.py --no-open`.
3. Xem từng trang mới: không mất hình, không tràn lề, bảng không co chữ, mọi `@fig`/`@tbl` hiện số đúng, danh mục bảng/hình cập nhật.
4. Kiểm tra cỡ chữ trong hình và bảng bằng cách đã dùng cho `ban1_preview.pdf` (`BAO CAO/Bao cao EDA/ban1/document_checks.json`).
5. Ghi số trang vào nhật ký.

### A7. Chốt Chương 3 (cả hai)

**Chương 3 được coi là xong khi:**

- [ ] QMD không còn ô chờ ở 3.4–3.6; PDF render thành công trên máy Vương.
- [ ] Toàn luồng M2 chạy được trên cả hai máy, kết quả khớp từng byte.
- [ ] Mọi con số trong 3.4–3.6 khớp CSV (người kia kiểm tra chéo ít nhất 10 số chọn ngẫu nhiên).
- [ ] Đủ năm insight theo khung ở A4; I5 có so sánh với mức nền 210 cặp.
- [ ] 3.6 ghi p theo ngưỡng, có diễn giải V và giới hạn về kích thước giỏ.
- [ ] Không còn đường dẫn tuyệt đối trong `scripts/`, `configs/`, QMD và CSV đầu ra.
- [ ] Test đạt.
- [ ] Lưu bản sao `chuong3-xong` (scripts, tests, configs, drafts, QMD, PDF) vào `TLCK/Chung/archive/`; gửi Phong gói ZIP cuối theo mục 1.2.
- [ ] Cập nhật `roadmap.md` (nhánh Bạn 2 đã xong, Chương 3 đã ghép), `PHAN_CONG_M2_3.4-3.6.md` (đánh dấu hoàn thành), README chạy M2.
- [ ] Ghi phiên nhật ký ghép Chương 3: việc đã làm, số mốc đối chiếu, kết quả test và render, số trang. Số liệu chép từ CSV.

---

## 4. Sở hữu file

| Nhóm file | Chủ sở hữu | Người kiểm tra |
|---|---|---|
| QMD chính, `references.bib`, render cuối, tích hợp | Vương | Phong đọc lại |
| `scripts/cleaning/common.py`, `clean_vuong.py`, `clean_phong.py`, config làm sạch | Vương viết lại cấu trúc | Phong chạy `clean_phong.py` trên máy Phong, kiểm tra phần `orders`, `eval_set`, `order_number` |
| `m1_build_master.py`, `m1_benchmark.py` (giữ nguyên), `summarize_cleaning.py` | Vương | Phong |
| `m2_eda_summary.py`, `m2_plot_univariate.py`, bản thảo 3.4, hình 1–2 | Vương | Phong |
| G0 (`m2_foundation.py` sau khi gộp), `m2_profile_inputs.py` | Phong | Vương (người viết bản G0 gốc, phải giải thích được bản mới) |
| `m2_eda_multivariate.py`, `m2_plot_multivariate.py`, `m2_hypothesis_tests.py`, bản thảo 3.5 đa biến, 3.6, năm insight | Phong (Vương sửa khi ghép ở A2) | Vương |
| `render_pdf.py`, `requirements.txt`, README chạy | Phong | Vương |
| `project_io.py` | Chốt ở bước B1 | |
| `configs/hypotheses_config.json` | Đã khóa; không ai sửa | |

Sửa file của người kia: báo trước; người sở hữu đọc diff trước khi chép vào bản chính.

---

## 5. Giai đoạn B — Rút gọn đợt 1 (sau Chương 3, trước Chương 4)

Chi tiết từng file và ngân sách dòng: `HUONG_DAN_RUT_GON_CODE.md` mục 3. Ở đây quy định thứ tự và điều kiện.

### B0. Mốc trước rút gọn (Vương)

Chạy lại `so_sanh_dau_ra.py chup` trên bản `chuong3-xong` (mốc mới, vì Chương 3 đã thêm đầu ra Bạn 2). Danh sách so sánh trong công cụ đã gồm CSV ở `BAO CAO/Bao cao EDA/ban2/` và `plot_data/`; thêm `DATA/Data phai sinh/M2/department_presence.parquet` vào danh sách `PARQUET` trước khi chụp.

### B1. Tiện ích chung và môi trường

- Chốt người viết `scripts/project_io.py` (≤ 50 dòng, giao diện ở mục 3.5 của `HUONG_DAN_RUT_GON_CODE.md`). Chuyển `check_data_hashes` từ `m2_common.py` sang file này.
- **Trước khi bắt đầu Chương 4:** `.venv-m2` hiện chưa có `scikit-learn`, `mlxtend` (đã kiểm tra thư mục `site-packages`). Cài vào `.venv-m2` trên cả hai máy cùng phiên bản và ghi phiên bản chính xác vào file khóa.

### B2. Làm song song

| Vương | Phong |
|---|---|
| Tách làm sạch thành `common.py` + `clean_vuong.py` + `clean_phong.py` (mục 3.1 hướng dẫn rút gọn). Chạy lại cả hai file trên dữ liệu nhiễu, rồi `summarize_cleaning.py` | Gộp G0 thành `m2_foundation.py` (~110 dòng); file này ghi `BAO CAO/Bao cao EDA/common/hashes.json` đúng định dạng đã dùng ở A2, nên các script phía sau không phải sửa |
| **Đạt khi:** `check_expected` không báo lỗi; 6 CSV sạch khớp hash; báo cáo làm sạch khớp từng byte | **Đạt khi:** 4 file nền khớp nội dung; `canonical_split_sha256` không đổi; toàn luồng M2 chạy không phải sửa |
| Gửi Phong gói ZIP gồm `scripts/cleaning/` mới | Chạy `clean_phong.py` trên máy Phong: `check_expected` không báo lỗi; `orders.csv`, `products.csv`, `order_products__train.csv` khớp hash (`9b52535e…`, `fb88d475…`, `4c8075f0…`); đọc code phần `eval_set`, `order_number` |

### B3. Rút gọn code EDA và kiểm định

| Vương | Phong |
|---|---|
| Bỏ `m2_write_ban1_drafts.py`, `m2_run_ban1.py`; chuyển phần tính lại độc lập của `m2_verify_ban1.py` vào `tests/test_m2_summary.py`; gọn `m2_eda_summary.py`, `m2_plot_univariate.py` | Giữ Holm tự viết; chuyển phần tính lại của `m2_audit_descriptive.py` vào `tests/test_m2_multivariate.py`; gọn hai script đa biến và `m2_hypothesis_tests.py` |

**Đạt khi:** `so_sanh_dau_ra.py so` báo khớp toàn bộ; test đạt.

### B4. Ghép và chạy từ đầu (Vương)

Chạy toàn luồng từ dữ liệu nhiễu tới PDF trên máy Vương, rồi chạy lại từ thư mục làm việc khác. Tìm trong QMD và mọi README tên các file đã bỏ; sửa câu chữ QMD theo mục 4.4 hướng dẫn rút gọn (ví dụ câu nhắc "data contract" ở mục 3.2). Xóa các file đã được thay thế (mục 5.1 hướng dẫn rút gọn). Gửi Phong gói ZIP; Phong chạy lại toàn luồng M2 trên máy Phong. Ghi phiên nhật ký rút gọn: số dòng trước/sau, kết quả so sánh.

Sau B4 mới bắt đầu Chương 4.

---

## 6. Giai đoạn B' — Rút gọn đợt 2 (sau Chương 4–5)

| Việc | Người | Điều kiện |
|---|---|---|
| `m1_build_master.py`: vòng lặp 4 phép ghép, bỏ ghi trùng | Vương | Master khớp nội dung; `join_audit.csv`, schema, dictionary khớp từng byte |
| `m1_benchmark.py` | — | **Giữ nguyên** (quyết định 12) |
| Gộp test, bỏ test của lớp nghiệm thu cũ | Người sở hữu từng test | Test còn lại đạt |
| Gộp `requirements*.txt` thành một file | Phong | Tạo môi trường mới từ file này trong một thư mục trống và chạy được toàn luồng |
| Xóa/lưu trữ theo mục 5 hướng dẫn rút gọn | Cả hai, theo file mình sở hữu | Tìm tên file trong QMD trước khi xóa |

---

## 7. Điều kiện để một phần được coi là rút gọn xong

1. Kết quả không đổi theo đúng mức: CSV tất định so hash, Parquet so nội dung.
2. Các test quan trọng đạt.
3. QMD và hướng dẫn không còn trỏ đến file đã bỏ.
4. Người phụ trách đọc và giải thích được toàn bộ code còn lại.
5. Người kia đã đọc diff và hỏi ít nhất hai câu về trường hợp biên của phần đó.
6. Nhật ký có phiên tương ứng, ghi số dòng trước/sau và kết quả so sánh.

Mục tiêu tham khảo cho phần đến hết Chương 3 sau rút gọn: khoảng 2.900 dòng (đã tính `m1_benchmark.py` giữ nguyên 788 dòng và code 3.6). Không phải con số cứng; không nén một thuật toán rõ ràng thành vài dòng khó đọc để đạt số.

---

## 8. Chuẩn bị vấn đáp: trường hợp biên để hỏi nhau

| Phần | Câu hỏi gợi ý |
|---|---|
| Làm sạch | Vì sao `clean_phong.py` phải đọc `order_id` của prior? Nếu một dòng prior trỏ tới đơn không có trong orders thì sao? `eval_set` được khôi phục theo quy tắc nào? Ranh giới chunk ảnh hưởng gì tới việc khôi phục thứ tự? |
| Master | `validate="many_to_one"` bắt được lỗi gì? Vì sao dùng left join mà vẫn kiểm tra không có `left_only`? |
| Benchmark | Vì sao đo trong tiến trình con? Vì sao Parquet đọc nhanh hơn nhưng RSS đỉnh lại cao hơn CSV? |
| G0 | Với N = 131.209, vì sao số người các tập là 39.363 / 39.363 / 26.241 / 26.242? Đổi thứ tự ID đầu vào thì phép chia có đổi không? Kiểm tra hash chặn được lỗi gì và không chặn được lỗi gì? |
| 3.4 | Độ phủ giỏ của Top-N khác tỷ trọng dòng thế nào? Vì sao độ phủ các ngành cộng lại vượt 100%? |
| 3.5 | Vì sao Spearman là hình chính? Panel thời gian dùng mẫu số nào, giỏ thiếu giờ đi đâu? |
| 3.6 | Khi nào chuyển sang Fisher? Holm khác Bonferroni thế nào, đọc code Holm tự viết từng dòng? V = 0,20 nghĩa là gì khi p gần 0? Vì sao 182/210 cặp có lift > 1? |
