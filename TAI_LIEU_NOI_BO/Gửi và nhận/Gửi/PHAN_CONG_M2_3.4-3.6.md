# HƯỚNG DẪN PHỐI HỢP HAI THÀNH VIÊN — MỤC 3.4 ĐẾN 3.6

Ngày thiết kế: 29/10/2026. Tài liệu này cụ thể hóa phân công từ `3.4-3.6.md` cùng thư mục; không thay đổi phương pháp thống kê đã chốt trong roadmap. **G0 hiện đã có code, chia tập và nghiệm thu tự động**: reference 39.363 người/giỏ, 415.053 dòng; 18 kiểm thử nền/evidence đạt (sau sửa cơ chế acceptance). Xem `scripts/README_M2.md` và `BAO CAO/Bao cao EDA/common/` trong thư mục bài để nhận gói. Cập nhật 30/10: Vương xác nhận là Bạn 1. Nhánh Bạn 1 đã triển khai thống kê, hai hình và bản thảo riêng; xem scripts/README_M2_BAN1.md. Nhánh Bạn 2, kiểm tra chéo và tích hợp vẫn để lại; không thay thế xác nhận đã đọc hợp đồng của hai bạn. G0 hiện tại đã đổi đường dẫn DATA/ và BAO CAO/ so với ZIP gửi trước; phải xác nhận cấu trúc/hash chung trước tích hợp.

## 1. Nguyên tắc chia việc và điểm phụ thuộc

Giữ phương án: Bạn 1 làm toàn bộ 3.4 và hai hình đầu; Bạn 2 làm ba hình sau, tổng hợp năm insight và toàn bộ 3.6. Tuy nhiên, không thể khẳng định khối lượng chính xác 50/50 khi chưa triển khai. Bạn 2 có nhiều việc kiểm định/diễn giải; Bạn 1 nhận thêm phần dựng nền kỹ thuật và tích hợp QMD/PDF để hướng tới cân bằng.

**Điểm cần giải quyết trước:** nếu `basket_summary.parquet` chỉ được tạo khi Bạn 1 làm xong toàn bộ 3.4 thì Bạn 2 phải chờ. Vì vậy tách bước tạo bảng cấp giỏ khỏi thống kê mô tả thành bước chuẩn bị chung. Sau bước này, cả hai có dữ liệu đầy đủ để code/chạy riêng; Bạn 2 chỉ cần đợi bảng của Bạn 1 khi chốt insight I1–I3.

```text
Khóa config, giả thuyết, schema và phong cách hình
                     ↓
Master → split_manifest → reference → basket_summary
                     ↓
             Nghiệm thu gói nền G0
                ↙              ↘
Bạn 1: bảng 3.4 + hình 1–2    Bạn 2: hình 3–5 + kiểm định 3.6
                ↘              ↓
          Bằng chứng I1–I3 → chốt insight I1–I5
                     ↓
         Kiểm tra chéo → tích hợp QMD → render
```

“Song song” áp dụng sau G0; không đồng nghĩa hai người cùng sửa một script hoặc cùng xuất một tệp. Trước G0, Bạn 2 vẫn có thể chuẩn bị cấu hình giả thuyết, fixture kiểm định và khung văn bản.

## 2. Phần chung phải làm đầu tiên — gói G0

### G0.1. Chốt phương pháp và quy ước

Cả hai đọc Chương 2 hiện hành và mục 6–12 của roadmap. Thống nhất các điểm sau trước khi xem kết quả EDA:

- Chỉ EDA hành vi trên reference; giữ nguyên toàn bộ sản phẩm và singleton. Không dùng fit/validation/test để lựa chọn phân tích.
- Seed 42, PCG64; ID được sắp trước shuffle; quy tắc làm tròn và thứ tự lấy tập giữ đúng mục 7.2 roadmap. Với N=131.209, số giỏ dự kiến là 39.363/39.363/26.241/26.242. Không chép số dự kiến vào kết quả nghiệm thu.
- N giỏ, N dòng sản phẩm–đơn, N hợp lệ là ba mẫu số khác nhau. Không lấy số dòng thay số giỏ trong kiểm định.
- Std ddof=1, phân vị linear, kurtosis excess; giờ chia [0,6), [6,12), [12,18), [18,24); mã ngày giữ 0–6; thiếu giữ riêng.
- Khóa ba cặp kiểm định (3,16), (9,13), (4,12) và lý do kinh doanh trước xem heatmap. Nếu đã xem dữ liệu liên quan từ trước, ghi rõ tính khám phá, không giả vờ đăng ký trước.
- Alpha 0,05; Chi-square không Yates nếu mọi kỳ vọng ≥5, Fisher hai phía nếu bảng thưa, biến hằng không test; Holm trên họ ba cặp theo roadmap.
- Top-N mô tả [10,50,100,500,1000]; chưa chọn N cuối cùng của mô hình. Không dùng tỷ trọng tích lũy để khẳng định quy luật 80–20 nếu chưa đo.
- Thống nhất chữ, màu, đơn vị và caption: nội dung/bảng 12 pt theo bài; hình PNG 300 DPI và PDF vector; kiểm tra chữ hình ở kích thước chèn thực tế.

### G0.2. Phân vai trong công việc chung

| Công việc | Người thực hiện chính | Người kiểm tra |
|---|---|---|
| Đọc Master, xác minh hash/schema/khóa | Bạn 1 | Bạn 2 đối chiếu số dòng, giỏ và ánh xạ user |
| `configs/m2_eda.json`: cấu hình chia, thống kê, đường dẫn | Bạn 1 | Bạn 2 đọc toàn bộ trước khóa |
| `configs/hypotheses_config.json`: cặp, H0/H1, phương pháp | Bạn 2 | Bạn 1 kiểm tra ID–tên và thời điểm khóa |
| `m2_common.py`: đường dẫn, đọc config, kiểm tra metadata | Bạn 1 | Bạn 2 kiểm tra chạy từ cwd khác |
| `m2_split_data.py`: manifest và reference | Bạn 1 | Bạn 2 kiểm tra disjoint/union/tái lập |
| `m2_prepare_reference.py`: bảng giỏ, danh mục ngành | Bạn 1 | Bạn 2 đối chiếu một fixture tính tay |
| Fixture nhỏ cho nhóm/thiếu/giỏ singleton | Bạn 1 | Bạn 2 kiểm tra đáp án thủ công |
| Fixture 2×2, Fisher/Chi-square/Holm | Bạn 2 | Bạn 1 kiểm tra nhánh và mẫu số |
| `configs/m2_plot_style.json`: màu/font/kích thước | Bạn 1 soạn, hai bạn chốt | Bạn 2 thử một hình fixture |

Ba tệp mới `m2_prepare_reference.py`, `m2_plot_style.json` và hướng dẫn phân công này là phần cụ thể hóa tổ chức làm song song, không phải thay đổi thiết kế nghiên cứu. Trong giai đoạn phát triển, config có thể sửa; sau khi hai bên nghiệm thu G0 thì phải lưu hash và trao đổi trước mọi thay đổi.

### G0.3. Gói dữ liệu dùng chung phải bàn giao

Các đường dẫn triển khai dưới đây tính từ **thư mục bài tiểu luận**, không từ thư mục chứa hướng dẫn này. Đường dẫn trong code/config phải tính theo vị trí script/gốc bài, không gắn cứng máy cá nhân.

| Tệp | Nội dung và hợp đồng |
|---|---|
| `DATA/Data phai sinh/M2/split_manifest.parquet` | Một dòng/user; `user_id`, `split`; seed và thuật toán trong metadata. Chỉ một bản có thẩm quyền |
| `DATA/Data phai sinh/M2/reference.parquet` | Toàn bộ cột Master của giỏ reference, giữ nguyên giá trị/schema; dòng sắp theo order/product |
| `DATA/Data phai sinh/M2/basket_summary.parquet` | Một dòng/order; ID người/giỏ, basket_size, n_departments, n_aisles, order_dow, order_hour_of_day, days_since_prior_order, hour_band |
| `DATA/Data phai sinh/M2/department_lookup.csv` | Đủ 21 ngành từ bảng sạch, ID tăng; có cả `other`, `missing`, không lọc chỉ ngành hiện diện trong reference |
| `BAO CAO/Bao cao EDA/common/data_contract.json` | Tên cột, kiểu đọc lại, nullable, đơn vị, mẫu số, quy tắc thiếu và thứ tự phân loại |
| `BAO CAO/Bao cao EDA/common/foundation_manifest.json` | Hash Master, departments nguồn, config, code tạo nền, dữ liệu phái sinh; phiên bản Python/thư viện, số lượng thực đo, thời điểm |
| `BAO CAO/Bao cao EDA/common/foundation_validation.json` | Kết quả kiểm tra G0, lỗi/cảnh báo; chỉ ghi passed sau khi đủ kiểm tra |

Tạo bảng giỏ bằng groupby có kiểm tra nhất quán thuộc tính đơn (`nunique(dropna=False)`), không dùng `first()` trước khi xác minh. `basket_size` phải bằng cả số dòng và số product_id phân biệt; `1 ≤ n_departments ≤ n_aisles ≤ basket_size` sau xác minh quầy→ngành. Tên thiếu không làm mất ID hay nhóm.

Hợp đồng tỷ lệ chung: cột hậu tố `_rate`, `_share`, `_coverage` chứa tỷ lệ [0,1]; hậu tố `_pct` chứa [0,100]; chênh lệch `_pp` tính theo điểm phần trăm. `popularity` và `support_AB` nằm [0,1]; lift không phải phần trăm. CSV lưu số chưa làm tròn, dấu thập phân '.', NA theo quy ước đọc/ghi được ghi trong contract; chỉ làm tròn khi trình bày tiếng Việt.

### G0.4. Điều kiện cho phép tách hai nhánh

- [ ] Hash nguồn đúng; không thay dữ liệu Master/sáu CSV sạch.
- [ ] User không giao tập, hợp bốn tập bằng đầu vào; một order/user đúng một split; một giỏ train/người theo thiết kế hiện hành.
- [ ] Reference giữ nguyên tập cặp khóa/product của giỏ, không mất/nhân dòng, không lọc Top-N.
- [ ] Tổng basket_size bằng dòng reference; số dòng bảng giỏ bằng số order và user reference.
- [ ] Chạy lại cùng input/config cho manifest có cùng nội dung canonical; không lấy timestamp làm một phần hash nội dung tái lập.
- [ ] Danh mục có 21 ID đúng bảng sạch; thiếu tên không bị hiểu nhầm là thiếu ngành.
- [ ] Cả hai đọc được gói nền trong môi trường đã chốt; chạy được từ cwd khác.
- [ ] Hai bạn xác nhận schema/config, hash gói nền và quyền sở hữu tệp.

Nếu G0 chưa đạt, không viết kết luận bằng số thật. Bạn 2 có thể tiếp tục code trên fixture, nhưng hình/kiểm định fixture chỉ để thử, không được đưa vào kết quả bài.

## 3. Phân công Bạn 1 — dữ liệu mô tả, hình 1–2 và tích hợp

### 3.1. Làm toàn bộ mục 3.4

Sở hữu `scripts/m2_eda_summary.py`. Script **đọc** bảng giỏ đã nghiệm thu, không tự tái chia tập hoặc ghi đè bảng giỏ; dùng reference để tổng hợp ngành/quầy/sản phẩm.

Đầu ra trong `BAO CAO/Bao cao EDA/`:

- `sample_overview.csv`, `eda_summary.csv`, `categorical_frequencies.csv`.
- `reference_outliers.json` (IQR reference, khác phạm vi kiểm toán toàn Master ở 3.3).
- `department_summary.csv`, `aisle_summary.csv`.
- `product_popularity.csv`, `top_n_coverage.csv`.

“Toàn bộ CSV của 3.4” thuộc Bạn 1; **không có nghĩa Bạn 1 phải tạo cả CSV tương quan, đồng mua và kiểm định của Bạn 2**. Mỗi cột phải theo schema, công thức và mẫu số trong mục 8 roadmap.

Viết ba tiểu mục 3.4.1–3.4.3 vào `drafts/m2/ban1_3_4.qmd`: phạm vi; thống kê giỏ; cơ cấu/độ tập trung. Bảng dài tách hợp lý, không giảm chữ dưới 12 pt. Chưa sửa QMD chính trong khi hai nhánh đang phát triển.

### 3.2. Hai hình đầu của 3.5

Sở hữu `scripts/m2_plot_univariate.py`:

1. `fig-ref-basket-distribution`: histogram bin theo số nguyên + boxplot; đủ khoảng dữ liệu; không xóa điểm ngoài râu.
2. `fig-ref-category-concentration`: bar tỷ trọng dòng Top-10 ngành + phần còn lại, và đường tỷ trọng dòng tích lũy theo thứ hạng sản phẩm. Độ phủ giỏ của nhóm còn lại phải tính trên hợp order. Dùng tên “đường tích lũy” cho đến khi có bằng chứng về tỷ lệ Pareto cụ thể.

Xuất PNG/PDF vào `BAO CAO/Bao cao EDA/figures/ban1/`, dữ liệu vẽ vào `BAO CAO/Bao cao EDA/plot_data/ban1/`. Viết caption, nguồn và đoạn mô tả ngắn của hình vào `drafts/m2/ban1_3_5_hinh_1_2.qmd`.

### 3.3. Bàn giao sớm bằng chứng insight

Ngay khi bảng 3.4 qua kiểm tra, gửi gói G1 cho Bạn 2; **không cần đợi PDF hay cả hai hình đẹp hoàn chỉnh**. Gói gồm CSV/JSON trên, manifest nhánh và `drafts/m2/ban1_evidence_i1_i3.md`:

| Insight | Bạn 1 cung cấp | Bạn 2 làm tiếp |
|---|---|---|
| I1 | Median/IQR, singleton, số giỏ ngoài hàng rào và mẫu số | Viết diễn giải kinh tế, giới hạn |
| I2 | Tỷ trọng dòng/độ phủ giỏ của ngành, số đếm nguồn | Viết hướng thử nghiệm vị trí ngành |
| I3 | Top-N: tỷ trọng dòng và độ phủ giỏ; phần ngoài danh mục | Viết đánh đổi danh mục dài đuôi, liên kết Chương 4 |

Bạn 1 kiểm chứng lại các con số trong bản insight cuối. Bạn 2 chịu trách nhiệm câu chữ thống nhất của năm insight, không phải tự tính lại toàn bộ 3.4.

### 3.4. Phần tích hợp để cân đối khối lượng

Bạn 1 sở hữu bộ chạy hình chung, README, kiểm thử tích hợp và việc đưa bản đã duyệt vào QMD chính. Kiểm tra caption/nhãn, bảng chữ 12 pt, hình đọc được, nguồn trích dẫn; chạy script render hiện có và kiểm tra PDF. Bạn 2 cùng đọc kết quả, đặc biệt các bảng kiểm định và insight.

## 4. Phân công Bạn 2 — đa biến, năm insight và mục 3.6

### 4.1. Tổng hợp đa biến độc lập với bảng 3.4

Sở hữu `scripts/m2_eda_multivariate.py`, đọc trực tiếp gói G0:

- Từ basket_summary: tạo `time_pivot_median.csv`, `time_pivot_count.csv`, `hour_band_summary.csv`; phân biệt thiếu với 0, ô N<30 đánh dấu theo roadmap.
- Tính `correlation_spearman.csv`, `correlation_pearson.csv`, `correlation_pair_n.csv`; dùng bốn biến định lượng đã chốt, pairwise complete, biến hằng/không đủ dữ liệu là NA.
- Từ reference + danh mục ngành: tạo `department_presence.parquet` tại `DATA/Data phai sinh/M2/` và `department_pair_summary.csv` trong báo cáo. Một dòng/order, đủ 21 cột Boolean theo ID; phải giữ mọi order và cả ngành không hiện diện.

Ma trận ngành `department_presence.parquet` do **Bạn 2 duy nhất** tạo và kiểm chứng để cả heatmap và kiểm định dùng cùng định nghĩa. Khi dùng phép nhân ma trận để đếm đồng xuất hiện, ép sang số nguyên ít nhất int64 trước tính; không nhân Boolean hoặc uint8 rồi hiểu đó là số đếm chính xác. Đối chiếu ba cặp kiểm định bằng crosstab độc lập.

### 4.2. Ba hình sau của 3.5

Sở hữu `scripts/m2_plot_multivariate.py`:

3. `fig-ref-time-patterns`: dashboard tần số giờ/ngày, heatmap median theo ngày×khung giờ, boxplot nhóm giờ; nêu số hợp lệ/thiếu và N nhóm.
4. `fig-ref-correlations`: Spearman là hình chính; Pearson xuất hình/bảng bổ trợ để so sánh, không chọn hệ số lớn hơn làm kết luận. Ghi quan hệ cấu trúc giữa size/ngành/quầy.
5. `fig-ref-department-cooccurrence`: lift đầy đủ **21×21**, thứ tự ID cố định, ẩn đường chéo, ngành có mẫu số 0 hiển thị NA. Có count/support đi kèm; không ghi 441 số lên hình nếu chữ không đọc được. Có thể dùng thang log cho màu nếu công bố rõ, xử lý lift=0 riêng; không cộng epsilon âm thầm để đổi ý nghĩa.

Hình xuất `BAO CAO/Bao cao EDA/figures/ban2/`, dữ liệu vẽ vào `BAO CAO/Bao cao EDA/plot_data/ban2/`; caption/nguồn và mô tả viết vào `drafts/m2/ban2_3_5_hinh_3_5.qmd`. Ma trận 21×21 là đồng mua **ngành**, không phải ma trận sản phẩm hay luật Apriori.

### 4.3. Toàn bộ mục 3.6

Sở hữu `scripts/m2_hypothesis_tests.py`; đọc config giả thuyết đã khóa và gói G0. Có thể dùng ma trận ngành đã kiểm chứng nếu kiểm tra hash reference và danh mục của nó; nếu lệch phải dừng, không dùng bản cũ.

Thực hiện đủ quy trình mục 10 roadmap: crosstab n00/n01/n10/n11 trên tất cả giỏ; bảng kỳ vọng; nhánh Chi-square/Fisher/không test được; Holm; Cramér’s V tính bằng Pearson không Yates; tỷ lệ có điều kiện và chênh lệch điểm phần trăm. Không coi V là chiều liên hệ hay Fisher odds ratio là chi-square.

Xuất `hypotheses.csv`, `hypotheses_details.json`, báo cáo kiểm chứng riêng. Viết `drafts/m2/ban2_3_6.qmd` gồm thiết kế, kết quả và giới hạn. Luôn giữ cả kết quả không có ý nghĩa; p rất nhỏ không hiển thị thành “p=0”. Không kiểm định thêm cả 210 cặp chỉ vì đã vẽ heatmap nếu chưa có thiết kế riêng.

### 4.4. Viết năm insight

Sở hữu `BAO CAO/Bao cao EDA/insights.csv` và `drafts/m2/ban2_3_5_insights.qmd`.

- I1–I3 lấy số từ gói G1 của Bạn 1; I4 lấy dashboard thời gian; I5 lấy đồng mua và đối chiếu 3.6 nếu đúng cặp đã khóa.
- Mỗi insight: **số đo + mẫu số → diễn giải có căn cứ → hành động có thể thử → giới hạn**.
- Không suy doanh thu từ số dòng, sở thích nhân quả từ lift, hoặc chất lượng gợi ý từ p-value. Với khác biệt yếu, viết mức khác biệt nhỏ kèm số đo thay vì cố tạo kết luận mạnh.
- Tránh lặp nguyên văn phần mô tả hình: đoạn cạnh hình giải thích số liệu; đoạn insight tổng hợp ý nghĩa kinh doanh và giới hạn.
- Chỉ chốt I1–I3 khi nhận đúng phiên bản G1 cùng gói nền đang dùng. Trong lúc đợi, hoàn thành I4/I5, kiểm định và khung lập luận.

## 5. Quyền sửa tệp và tránh xung đột

| Nhóm tệp | Chủ sở hữu ghi | Người còn lại |
|---|---|---|
| Gói nền, split, prepare_reference, common, config EDA/style | Bạn 1 | Đọc/review; đề nghị sửa, không ghi song song |
| Config giả thuyết | Bạn 2, khóa trước EDA | Bạn 1 review; thay đổi sau khóa phải báo cả hai |
| Summary 3.4, hình 1–2, bản thảo Bạn 1 | Bạn 1 | Bạn 2 đọc để viết insight |
| Multivariate, presence ngành, hình 3–5, kiểm định, insights, bản thảo Bạn 2 | Bạn 2 | Bạn 1 kiểm tra chéo |
| QMD chính, references.bib, README_M2, bộ chạy hình, manifest tổng | Bạn 1 ở bước tích hợp | Bạn 2 gửi nội dung/nguồn đã kiểm tra và review PDF |
| Nguồn Master, CSV sạch, hồ sơ M1 | Không ai ghi trong M2 | Cả hai chỉ đọc |

Tách script để không cùng sửa `m2_eda_visualize.py`: Bạn 1 làm `m2_plot_univariate.py`, Bạn 2 làm `m2_plot_multivariate.py`; **`m2_eda_visualize.py` chỉ là bộ gọi hai module**, không chứa bản sao công thức thống kê. Bộ gọi không tự sửa config hoặc chạy chia tập. Nó chỉ chạy sau khi các đầu vào summary/multivariate đã sẵn sàng.

Tách kiểm thử: Bạn 1 sở hữu `tests/test_m2_foundation.py`, `tests/test_m2_summary.py`; Bạn 2 sở hữu `tests/test_m2_multivariate.py`, `tests/test_m2_hypotheses.py`. `tests/test_m2_eda.py` do Bạn 1 tích hợp để chạy toàn bộ. Không để hai người cùng ghi báo cáo kiểm thử chung.

Mỗi nhánh ghi metadata riêng: `BAO CAO/Bao cao EDA/ban1/run_manifest.json` và `BAO CAO/Bao cao EDA/ban2/run_manifest.json`; báo cáo từng giai đoạn lưu tên riêng trong thư mục nhánh. Manifest nhánh liên kết hash gói nền, config, input/output/code cần dùng. **Chỉ bước tích hợp** mới ghi `BAO CAO/Bao cao EDA/run_manifest.json` và `m2_validation.json` tổng. Không dùng hai tiến trình cập nhật cùng JSON “latest”.

Mỗi người có thể làm trong bản checkout/workspace riêng, nhưng phải dùng cùng gói G0 có hash khớp; không tự chia lại rồi cho rằng cùng seed là đủ. Nếu cùng thư mục, tuân thủ quyền ghi ở trên. Không đồng bộ bằng cách chép đè toàn bộ thư mục của người kia; bàn giao đúng danh sách tệp sở hữu.

## 6. Các điểm bàn giao và cách làm song song

| Thời điểm | Bạn 1 | Bạn 2 | Kết quả chung |
|---|---|---|---|
| Trước G0 | Code split/prepare/common, kiểm tra nguồn | Khóa giả thuyết, viết fixture kiểm định, review contract | Gói nền qua nghiệm thu |
| Sau G0 | Summary 3.4, fixture mẫu số, bản thảo 3.4 | Multivariate, presence ngành và kiểm định; không đợi summary | Hai nhánh có thể chạy độc lập |
| G1: summary đạt | Bàn giao CSV + bằng chứng I1–I3, tiếp tục hình 1–2 | Nhận G1, viết I1–I3; tiếp tục hình 3–5/I4–I5/3.6 | Thống nhất số liệu cho lời văn |
| G2: hai nhánh đạt | Review bảng đếm/kiểm định và insight của Bạn 2 | Review mẫu số, coverage và hình 1–2 của Bạn 1 | Danh sách lỗi được trả đúng chủ tệp |
| G3: tích hợp | Ghép bản thảo, nguồn, hình vào QMD; chạy kiểm thử/render | Kiểm tra PDF và diễn giải; xác minh mọi insight với nguồn | Chương 3 có số thực, không chỗ chờ |

Gói bàn giao phải nêu: mục đích, danh sách tệp, hash gói nền, config, câu lệnh chạy, kiểm tra đã pass, hạn chế/cảnh báo và việc còn thiếu. Không chỉ gửi ảnh chụp hoặc “code chạy rồi”.

Nếu sửa G0 sau khi đã phân nhánh: giữ hồ sơ phiên cũ, tạo manifest nền mới, báo rõ thay đổi. Cả hai dừng dùng đầu ra chịu ảnh hưởng, chạy lại giai đoạn phụ thuộc, cập nhật số trong bản thảo. Nếu chỉ sửa màu/caption, không cần chạy lại split/kiểm định; chỉ tái tạo hình hoặc PDF liên quan.

## 7. Chạy thử, kiểm tra chéo và tích hợp

Các lệnh sau là **giao diện dự kiến sau khi tạo script**, chưa phải lệnh có sẵn. Chạy từ thư mục bài, đồng thời thử gọi script bằng đường dẫn từ cwd khác để kiểm chứng tính di động.

```powershell
# Gói chung — Xác thực gói nền G0 đã nhận theo README_M2 (môi trường đã khóa)
python scripts/m2_verify_foundation.py
python scripts/m2_check_environment.py

# (Tùy chọn: chỉ chạy nếu cần dựng và nghiệm thu lại toàn bộ nền từ đầu)
# python scripts/m2_run_foundation.py

# Nhánh Bạn 1
python scripts/m2_eda_summary.py
python scripts/m2_plot_univariate.py
python tests/test_m2_summary.py

# Nhánh Bạn 2 — không phụ thuộc summary của Bạn 1
python scripts/m2_eda_multivariate.py
python scripts/m2_plot_multivariate.py
python scripts/m2_hypothesis_tests.py
python tests/test_m2_multivariate.py
python tests/test_m2_hypotheses.py

# Tích hợp sau khi hai nhánh đạt
python tests/test_m2_eda.py
python scripts/m2_eda_visualize.py
python scripts/render_pdf.py --no-open
```

Bạn 2 kiểm tra độc lập ít nhất: tổng basket_size = dòng reference; denominator coverage; nhóm “còn lại” không cộng độ phủ; missing không bị drop khỏi tần số. Bạn 1 kiểm tra độc lập: tổng n00+n01+n10+n11 = N; n11 khớp presence; V đúng công thức; Holm đúng thứ tự gốc; biến hằng/bảng thưa đi đúng nhánh. Fixture tính tay phải bao gồm các trường hợp này, không chỉ kiểm tra tên tệp tồn tại.

Khi tích hợp QMD:

1. Chỉ Bạn 1 chèn bản thảo đã được hai bên duyệt; giữ tên/thứ tự heading chính thức 3.4–3.6.
2. Dùng các nhãn hình roadmap đã chốt, không gõ số hình bằng tay. Tên tệp PNG/PDF trùng stem của nhãn để dễ truy.
3. Đường dẫn hình trong QMD chính tính từ thư mục bài; bản thảo trong drafts không tự render độc lập và không quyết định lại đường dẫn tài nguyên.
4. Loại hình minh họa giả lập cũ của 3.5 khi thay bằng hình thật. Không sửa 3.1–3.3 ngoài thay đổi tham chiếu thực sự cần thiết.
5. Không `resizebox` thu nhỏ bảng; tách bảng kiểm định và bảng chiều liên hệ; 21×21 cần đủ diện tích và nhãn đọc được, có thể không in số từng ô.
6. Kiểm tra PDF toàn bài: dấu Việt, nguồn/caption, tràn lề, cỡ chữ, nhãn, số trang và tính nhất quán số liệu. Không xem render thành công là đã kiểm chứng thống kê.
7. Manifest tổng phải xác minh hai nhánh dùng cùng gói nền, không trộn kết quả cũ/mới. Hai bạn cùng duyệt checklist mục 12 roadmap trước chuyển Chương 4.

## 8. Cân bằng đóng góp và chuẩn bị bảo vệ

Phương án hướng đến cân bằng bằng **sản phẩm và trách nhiệm**, không đo bằng số hình hoặc số dòng code:

| Bạn 1 | Bạn 2 |
|---|---|
| Nền kỹ thuật, split, bảng giỏ, toàn bộ 3.4, hai hình, bằng chứng I1–I3, tích hợp và PDF | Config/fixture kiểm định, ba hình đa biến, ma trận ngành, toàn bộ 3.6, năm insight, review diễn giải/PDF |

Tại G1 và G2, so khối lượng thực tế còn lại; nếu Bạn 2 quá tải phần insight, Bạn 1 chuẩn bị đoạn nháp có số liệu I1–I3, Bạn 2 vẫn là người biên tập cuối. Nếu Bạn 1 quá tải render, Bạn 2 hỗ trợ kiểm tra PDF và lập danh sách lỗi, tránh cùng sửa QMD. Chỉ chuyển quyền sở hữu một tệp sau khi thông báo và người cũ dừng sửa; không suy từ bảng phân công rằng đóng góp thực tế tự động là 50% mỗi người.

Cả hai phải giải thích được: vì sao dùng reference, cấp giỏ khác cấp dòng, split có tái lập, support/coverage/lift khác nhau, giữ missing/singleton, vì sao chọn Chi-square/Fisher, Holm và V nói gì, giới hạn suy luận. Mỗi người trình bày sâu phần mình viết và giải thích được ít nhất một phần code của người kia sau kiểm tra chéo.

**Tiêu chí hoàn thành:** hai nhánh tái lập được trên cùng nền; năm hình và năm insight có nguồn; 3.6 có kiểm tra giả định và kết quả đầy đủ; QMD/PDF đọc được đúng cỡ chữ; không làm thay đổi nguồn/M1; chưa mở test để chọn phương pháp. Việc ghi nhật ký thực hiện riêng theo yêu cầu của người dùng, không tự ghi trong bước lập hướng dẫn này.
