# THIẾT KẾ CHI TIẾT VIẾT CHƯƠNG 4 VÀ CHƯƠNG 5 VÀ PHÂN CÔNG MỚI — PRJ-08

Căn cứ: toàn bộ bài hiện có (Chương 1 đến 3, khung Chương 4 và 5 trong QMD), Chương 2 (cam kết phương pháp), đề bài và barem (`projects.pdf`), `THIET_KE_CHUONG4_20261101.md`, `THONG_NHAT_CHUONG4_LAN1_20261104.md`, kết quả đã chạy trên máy Vương (validation 01/11, khóa và test 04/11).
Đây là bản **Vương đề xuất**, Phong xác nhận ở mục 1. Văn trong bài không nằm ở đây: tệp này chỉ nói viết gì, lấy số ở đâu, tránh gì.

---

## 0. Nguyên tắc chung cho cả hai người

1. **Mọi con số chép từ CSV/JSON, không chép từ tệp này.** Các số trong tệp này đã đối chiếu với nguồn ngày 04/11 để người viết biết mình đang tìm gì; khi viết, mở tệp nguồn ghi ở cột "Nguồn" và chép lại. Số tự tính (tỷ số, phần trăm tương đối) ghi rõ công thức trong bài hoặc chú thích bảng.
2. **Dùng đúng thuật ngữ của Chương 2:** phần quan sát $O_j$, phần che $H_j$, danh mục $C$ (Top-N), ứng viên $C_j=C\setminus O_j$; bốn tập reference, fit, validation, test; "hoàn thiện giỏ hàng" (không phải dự báo đơn kế tiếp); Recall@10 (trung bình vĩ mô theo giỏ) là chỉ số chính.
3. **Nói đúng mức:** hiệu quả ngoại tuyến là căn cứ đề xuất thử nghiệm A/B, không chứng minh tăng doanh thu; liên hệ không phải nhân quả; điểm của classifier chưa hiệu chỉnh nên không gọi là xác suất mua.
4. **Mỗi bảng có số thứ tự và tên đặt ngay phía trên, nguồn ngay phía dưới; mỗi hình có chú thích.** Chữ thân bài và bảng 12 pt, không thu chữ hay lề; hình rộng 16 cm.
5. **Không dùng:** số "Apriori mặc định cần khoảng 14 GB RAM" (chưa đo lại có lưu); số trong lời công cụ AI hay bản tóm tắt; kết quả validation thay cho kết quả test; "mô hình tốt hơn" khi chưa có khoảng tin cậy.
6. **Mọi số của Chương 4 đã khóa.** Mã, cấu hình, mô hình và `lock.json` không đổi nữa; tập test đã chấm một lần (04/11/2026 16:11), không chạy lại. Nếu phát hiện cần số mới, chỉ được tính trên validation hoặc từ các tệp đầu ra đã có, và ghi rõ là phân tích bổ sung.
7. **Dẫn nguồn** theo APA 7 bằng khóa trong `references.bib`; chỉ dẫn những gì tài liệu thật sự nói.

---

## 1. Phân công mới (thay mục 11.2 của bản thiết kế ngày 01/11)

| Người | Viết | Ngoài ra |
|---|---|---|
| **Vương** | **Toàn bộ Chương 4** (4.1 đến 4.6, khoảng 9 trang, bảng và hình nguồn), viết thành một tệp `.qmd` rời để Phong ghép | Giữ mã và số liệu Chương 4 (đã khóa); cắt giảm phần 3.2 đến 3.4 của mình; trả lời mọi câu hỏi về số liệu; đọc chéo Chương 5 |
| **Phong** | **Chương 5** (5.1 đến 5.4, khoảng 4 trang), **Tóm tắt đồ án** (250 đến 350 từ), sửa các điểm lệch ở Chương 1 và 2 (mục 3) | Giữ QMD chính, ghép Chương 4 của Vương, cắt giảm phần 3.5 đến 3.6 của mình, render, đếm trang; kiểm chứng mã Chương 4 (gói `CODE_CHUONG4`); đọc chéo Chương 4 |
| **Cả hai** | Đọc chéo, chốt số trang, kiểm số cuối | Xóa hai phụ lục (mã, nhật ký) khỏi PDF vì nộp riêng; thêm một câu nêu điều này ở mục 2.5 |

Lý do đổi: Chương 4 phụ thuộc chặt vào chi tiết mã và số đo mà Vương nắm; Chương 5 chủ yếu là diễn giải, khuyến nghị và đạo đức, hợp với Phong sau khi đọc kỹ Chương 3 và 4. Thay đổi này bỏ phân công cũ "Phong viết 4.3.2 đến 4.6"; các khung đã soạn (`KHUNG_4_3_2_DEN_4_5.md`, bản thảo 4.1, 4.2, 4.3.1 trong gói A) là tư liệu cho Vương dùng lại, không bỏ phí.

- [ ] Phong xác nhận phân công này (tick ở đây hoặc ghi vào biên bản lần 1).

### Thứ tự làm (không ghi ngày)

1. Vương gửi `CODE_CHUONG4`, Phong kiểm chứng và báo lỗi nếu có.
2. Vương viết Chương 4 theo mục 4; Phong viết Chương 5 theo mục 5. Hai bên làm song song, chỉ phụ thuộc nhau ở "bản đồ bằng chứng" (mục 6) nên không phải chờ.
3. Vương gửi bản Chương 4; Phong gửi bản Chương 5; đọc chéo.
4. Phong ghép vào QMD, cắt Chương 3 xuống ngân sách, viết Tóm tắt, render.
5. Hai bên kiểm số trang, số liệu, tham chiếu và cỡ chữ; xóa ô chờ.

### Ngân sách trang (≤ 45 trang tính từ bìa đến hết Chương 5)

Phần đầu 7; Chương 1 và 2: 6; **Chương 3: 17** (hiện 29 trang, cần cắt 12); **Chương 4: 9**; **Chương 5: 4**; tài liệu tham khảo 1; tổng 44. Chương 4 và 5 viết đúng ngân sách ngay từ đầu, không viết dài rồi cắt.

---

## 2. Cách bài trả lời năm câu hỏi nghiên cứu (khung chung)

| Câu hỏi (Chương 1) | Trả lời ở | Người viết |
|---|---|---|
| 1. Làm sạch và tích hợp sáu bảng, toàn vẹn quan hệ, quy mô, bộ nhớ | 3.1 đến 3.3 (đã có); tổng kết ở 5.4 | Phong (5.4) |
| 2. Cấu trúc giỏ hàng và đồng xuất hiện | 3.4 đến 3.6 (đã có); khuyến nghị ở 5.1 | Phong (5.1) |
| 3. Apriori và FP-Growth: thời gian, RAM, kết quả | **4.3.1** | Vương |
| 4. Luật, LR, RF so với độ phổ biến ngoài mẫu | **4.4, 4.5, 4.6** | Vương |
| 5. Khuyến nghị gợi ý bán chéo và thử nghiệm | **5.1, 5.2** | Phong |

Rubric (barem trụ cột III và IV) cho mức xuất sắc: Pipeline đóng gói hoàn hảo, kiểm định giả thuyết thống kê sâu, Feature Importance thuyết phục (Chương 4); khuyến nghị sắc bén có lộ trình chi tiết, phân tích đạo đức AI và bảo mật dữ liệu (Chương 5). Cấu trúc dưới đây bám các ý này.

---

## 3. Điểm lệch giữa Chương 1 và 2 với thực tế đã làm (cần sửa trước khi viết, Phong sửa)

Các câu dưới đây hứa điều không đúng hoàn toàn với những gì đã làm. Sửa lời văn cho khớp, không sửa mã.

| # | Vị trí | Câu hiện có | Thực tế | Đề xuất |
|---|---|---|---|---|
| 1 | 1.3 (mục tiêu 4) | "Pilot trên máy 24 GB RAM dùng để chốt Top-N, ngưỡng khai phá, độ dài tập và quy mô lấy mẫu âm" | Top-N, ngưỡng và độ dài chọn bằng **lưới 24 cấu hình chấm trên validation đầy đủ** (giai đoạn A); lấy mẫu âm 20/giỏ đặt trước; "pilot" chỉ là lượt thử nhỏ để kiểm luồng | Viết: lưới chọn bằng Recall@10 của phương pháp luật trên validation; pilot chỉ kiểm tính khả thi |
| 2 | 2.4 (Khai phá và benchmark) | "Cấu hình vượt ngân sách pilot được ghi nhận và loại trước khi khóa thiết kế" | Không cấu hình nào bị loại vì ngân sách. FP-Growth chạy đủ 12 tổ hợp; Apriori chỉ benchmark ở hai cấu hình (N=1.000 độ dài 2 và N=2.000 độ dài 3) | Bỏ câu, hoặc viết: Apriori chỉ được so sánh ở hai cấu hình đại diện (nhỏ nhất đã chọn và lớn nhất trong lưới) |
| 3 | 2.4 (Kiểm định và đánh giá) | "Báo riêng ... tỷ lệ giỏ có luật trước dự phòng và **tỷ lệ danh mục được gợi ý**" | Có tỷ lệ đáp án thuộc danh mục (trần Recall) và độ phủ luật trên validation (88,4%); **chưa tính** tỷ lệ danh mục được gợi ý | Bỏ cụm "tỷ lệ danh mục được gợi ý" (khuyến nghị: ít code hơn). Chỉ tính lại nếu cả hai muốn; khi đó tính trên validation, không trên test |
| 4 | 1.3 (mục tiêu 3) | "đối chiếu itemset, support, confidence, lift" | Đã đối chiếu **itemset và support** (lệch lớn nhất 0 ở cả hai cấu hình); confidence và lift suy ra từ support nên giống theo hệ quả | Nói rõ: đối chiếu itemset và support; confidence, lift tính từ support nên không đo riêng |
| 5 | 2.4 | Chỉ số "$K=5,10$" | Hình 4.1 vẽ Recall@K cho K = 1 đến 10 | Thêm: hình mở rộng K từ 1 đến 10 để xem đường cong; chỉ số chính vẫn Recall@10 |
| 6 | 3.5 (I1) | I1 hẹn "so sánh chất lượng gợi ý theo nhóm kích thước giỏ ở Chương 4" | Chưa làm | Hoặc làm phân tích bổ sung nhỏ trên validation (mục 4.4, ô tùy chọn), hoặc đổi I1 thành "có thể kiểm tra ở nghiên cứu sau" |
| 7 | Tóm tắt | Ô chờ | Chưa viết | Phong viết sau khi có đủ Chương 4 và 5 (mục 7) |
| 8 | Phụ lục mã và nhật ký | Còn trong QMD | Nộp riêng theo quy định | Xóa hai phụ lục; thêm một câu ở 2.5 |

---

## 4. CHƯƠNG 4 — Xây dựng mô hình và đánh giá hiệu năng (Vương viết, 9 trang)

Khung tiêu đề theo QMD hiện có. Dưới đây là nội dung từng mục, bảng và hình, nguồn và điều tránh. Sáu bảng và hai hình; nếu vượt ngân sách trang thì giữ hai bảng đầu ở dạng gọn và chuyển phần chi tiết sang CSV.

### 4.1. Kỹ thuật tạo lập và Lựa chọn đặc trưng (khoảng 1,5 trang)

**Trả lời:** nền cho câu hỏi 4. **Có sẵn:** bản thảo 4.1 trong `GUI_vuong_ch4_goiA_20261104/tai_lieu/PHAN_VUONG_CHUONG4.qmd`.

**Ý chính theo thứ tự:**
1. Bài toán phân loại: một dòng là một cặp giỏ–ứng viên; nhãn $y=1$ khi ứng viên thuộc phần che; $y=0$ khi không thuộc giỏ đầy đủ (không phải `reordered`, không phải "không thích").
2. Cách mô phỏng: che $h=\min(k-1,\max(1,\lfloor0{,}2k\rfloor))$ sản phẩm, seed 42 với mã đơn; giỏ một sản phẩm không che.
3. **Bảy đặc trưng** (Bảng 4.1), chỉ dùng thống kê reference và phần quan sát; không dùng phần che, không dùng mã khách, mã sản phẩm, kích thước giỏ đầy đủ (tiết lộ thông tin về phần che).
4. **Kiểm soát rò rỉ:** thống kê học trên reference; tiền xử lý chỉ fit trên fit; test chỉ mở một lần sau khóa.
5. **Tương quan giữa các đặc trưng và lý do giữ:** ba biến luật tương quan Spearman 0,999 đến 1,000 trên mẫu fit sau lấy mẫu âm. Vì vậy đánh giá theo **nhóm** bằng phép bỏ nhóm trên validation (ablation), không đọc riêng từng biến luật.
6. **Kết quả bỏ nhóm** trên validation: bỏ ba biến luật làm Recall@10 giảm rõ (LR 0,0923 xuống 0,0759; RF 0,0971 xuống 0,0788); bỏ nhóm ngành gần như không đổi (LR 0,0925; RF 0,0956). Kết luận mô tả: thông tin luật đóng góp rõ hơn thông tin ngành.

| Bảng 4.1 | Đặc trưng |
|---|---|
| Nội dung | Tên, loại (số hoặc danh nghĩa), nguồn, định nghĩa; bảy dòng |
| Nguồn | `tai_lieu/bang_4_1_dac_trung.csv` (trong gói A); công thức ở `m4_common.py` hàm `basket_features` |

**Số nguồn:** `BAO CAO/Bao cao mo hinh/feature_correlation.csv`, `ablation.csv`.
**Tránh:** nói đặc trưng "quan trọng nhất" ở mục này (để dành 4.5); nói tương quan cao là lỗi (chỉ là hệ quả thiết kế: ba thống kê từ cùng tập luật khớp).

### 4.2. Chuẩn hóa và Phân chia tập dữ liệu (khoảng 1 trang)

**Có sẵn:** bản thảo 4.2 trong gói A; Chương 2 (2.3).

**Ý chính:** (1) phân hoạch theo người dùng, seed 42, bốn tập 30/30/20/20, mỗi người một giỏ nên không giao nhau; (2) vai trò từng tập; (3) lấy mẫu âm không hoàn lại, tối đa 20 âm/giỏ (seed 43), giữ mọi dương, chỉ ở fit; validation và test chấm **toàn bộ** ứng viên; (4) `Pipeline`/`ColumnTransformer`: điền trung vị (số), điền giá trị phổ biến và `OneHotEncoder` bỏ qua mức mới (ngành), `StandardScaler` chỉ cho LR; (5) Precision chia K, Recall chia toàn bộ $|H_j|$ kể cả ngoài danh mục, giỏ không có đáp án trong $C$ vẫn chấm 0; (6) điểm classifier chưa là xác suất đã hiệu chỉnh.

**Bảng 4.2 — Quy mô phân hoạch và mẫu ứng viên (N = 1.000).** Nguồn: `dataset_description.csv`, `bang_4_2_phan_hoach.csv`, và với test `results_test.json`, `classifier_metrics_test.csv`, `masked_baskets.parquet`.

| Chỉ tiêu | Reference | Fit | Validation | Test |
|---|---:|---:|---:|---:|
| Số người dùng/giỏ theo phân hoạch | 39.363 | 39.363 | 26.241 | 26.242 |
| Giỏ một sản phẩm (loại khỏi che) | — | 1.975 | 1.387 | 1.365 |
| Giỏ đủ điều kiện (k ≥ 2) | — | 37.388 | 24.854 | 24.877 |
| Sản phẩm bị che | — | 75.006 | 49.130 | 49.473 |
| Phần che thuộc danh mục, tính gộp | — | 52,30% | 52,48% | 52,47% |
| Phần che thuộc danh mục, trung bình theo giỏ | — | 52,07% | 52,11% | xem ghi chú |
| Cặp ứng viên (trước lấy mẫu) | — | 37.209.316 | 24.736.527 | 24.758.284 |
| Tỷ lệ nhãn dương | — | 0,1054% | 0,1042% | 0,1048% |
| Tỷ lệ dương sau lấy mẫu âm | — | 4,9843% | — | — |

Ghi chú: cột test lấy từ kết quả đã có (số giỏ test đủ điều kiện, sản phẩm che và cặp ứng viên, 25.958 dương) và không gây rò rỉ vì là số mô tả. Giỏ một sản phẩm của test tính bằng 26.242 trừ 24.877. Ô "trung bình theo giỏ" của test chưa có nguồn riêng: bỏ ô này, hoặc tính từ `basket_metrics_test.csv` (trung bình theo giỏ của $|H_j\cap C|/|H_j|$) và ghi nguồn.

**Tránh:** nói "70/30" hay "80/20 stratify" (Chương 2 đã giải thích vì sao tách theo người dùng); nói validation hay test "lấy mẫu âm".

### 4.3. Huấn luyện các mô hình (khoảng 2,5 trang)

#### 4.3.1. Apriori và FP-Growth (khoảng 1,2 trang) — trả lời câu hỏi 3

**Có sẵn:** bản thảo 4.3.1 trong gói A; `tai_lieu/bang_4_3_benchmark.csv`.

**Ý chính:**
1. Ma trận Boolean thưa: 39.363 giỏ reference, cột là sản phẩm trong Top-N; giỏ không có sản phẩm nào của $C$ vẫn nằm trong mẫu số support. Hai thuật toán nhận **cùng** ma trận, ngưỡng support (số giỏ tối thiểu) và độ dài tối đa; Apriori dùng chế độ tiết kiệm bộ nhớ (`low_memory`).
2. Luật hậu đề một sản phẩm, giữ confidence đạt ngưỡng.
3. **Chọn cấu hình luật** (giai đoạn A): 24 cấu hình (N ∈ {500; 1.000; 2.000}, số giỏ tối thiểu ∈ {20; 50}, độ dài ∈ {2; 3}, confidence tối thiểu ∈ {0,05; 0,1}) chấm bằng Recall@10 của phương pháp luật trên validation, dung sai hòa 0,002. Cao nhất tuyệt đối 0,0944 (N=2.000, độ dài 3); chọn N=1.000, 20 giỏ, độ dài 2, confidence 0,05 vì chênh 0,0012 trong dung sai và cấu hình nhỏ hơn: 6.669 luật, Recall@10 0,0932 (Popularity 0,0752). Trần Recall theo N: 0,4104; 0,5211; 0,6363.
4. **Điểm nên nêu:** tăng N từ 1.000 lên 2.000 nâng trần Recall thêm khoảng 0,115 nhưng Recall@10 của luật chỉ tăng khoảng 0,001; ba tham số luật đã chọn đều ở cạnh dưới của lưới, kết luận chỉ áp dụng trong phạm vi lưới.
5. **Benchmark** (Bảng 4.3), ba lượt, tiến trình con riêng, trung vị: tạo ma trận, khai phá, sinh luật, RAM đỉnh. **Kết luận:** hai thuật toán cho cùng tập itemset và support lệch lớn nhất 0; FP-Growth nhanh hơn khoảng 4,1 lần ở cấu hình đã chọn và khoảng 14,3 lần ở cấu hình lớn nhất; RAM đỉnh chênh nhỏ (khoảng 11 MiB và 68 MiB).

**Bảng 4.3.** Nguồn: `mining_benchmark_N1000_c20_l2.csv`, `mining_benchmark_N2000_c20_l3.csv`, `itemset_equivalence_*.json`.

| Danh mục / độ dài | Thuật toán | Itemset / luật | Khai phá (giây) | RAM đỉnh (MiB) |
|---|---|---|---:|---:|
| 1.000 / 2 | Apriori | 7.730 / 6.669 | 3,698 | 199,6 |
| 1.000 / 2 | FP-Growth | 7.730 / 6.669 | 0,903 | 188,8 |
| 2.000 / 3 | Apriori | 11.314 / 13.918 | 19,809 | 280,2 |
| 2.000 / 3 | FP-Growth | 11.314 / 13.918 | 1,389 | 211,9 |

Gợi ý: gộp thêm cột dựng ma trận và sinh luật nếu còn chỗ; có đủ trong CSV nguồn.

**Tránh:** nhắc số "14 GB" của Apriori mặc định; nói FP-Growth "luôn nhanh hơn" (chỉ trên hai cấu hình và máy này); kết luận về chất lượng gợi ý ở mục này (chất lượng nằm ở 4.4).

#### 4.3.2. Logistic Regression và Random Forest (khoảng 1,3 trang)

**Có sẵn:** khung `KHUNG_4_3_2_DEN_4_5.md` của Phong (phần phương pháp) và `m4_classifier.py`.

**Ý chính:** (1) LR: L2, `lbfgs`, tối đa 1.000 vòng, `C` thử 0,01; 0,1; 1; 10. RF: 300 cây, `max_features` căn bậc hai, seed 42, độ sâu 10 hoặc 20, số mẫu tối thiểu tại lá 20 hoặc 100; không dùng `class_weight`. (2) Chọn cấu hình bằng Recall@10 validation; hòa trong dung sai 0,002 thì chọn cấu hình có suy luận nhanh hơn; ngưỡng phân loại chọn riêng bằng F1 validation, không đổi thứ tự xếp hạng. (3) **Giai đoạn C:** phương pháp chính chọn trên validation: RF (0,0971, hơn Rules 0,0932 xa hơn dung sai). (4) **Khóa** trước khi mở test: `lock.json` ghi phương pháp, cấu hình, ngưỡng, hash mã và dữ liệu; hai thành viên duyệt; test chấm một lần.

**Bảng 4.4 — Lưới giai đoạn B và cấu hình chọn.** Nguồn: `validation_grid_B.csv`, `validation_methods.csv`, `lock.json`.

| Mô hình | Cấu hình | Recall@10 validation | Suy luận (giây) | Chọn |
|---|---|---:|---:|---|
| LR | C = 0,01 / 0,1 / 1 / 10 | 0,0923 / 0,0923 / 0,0924 / 0,0924 | 15,86 / 15,31 / 17,45 / 15,56 | C = 0,1 |
| RF | độ sâu 10, lá 20 | 0,0976 | 48,07 | — |
| RF | độ sâu 10, lá 100 | 0,0971 | 47,87 | **Chọn** |
| RF | độ sâu 20, lá 20 | 0,0990 | 86,31 | — |
| RF | độ sâu 20, lá 100 | 0,0983 | 79,42 | — |

Giải thích lựa chọn RF: cấu hình tốt nhất (độ sâu 20, lá 20: 0,0990) hơn cấu hình chọn 0,0019, nằm trong dung sai 0,002, nên chọn cấu hình suy luận nhanh hơn (47,87 giây so với 86,31 giây). Với LR bốn giá trị `C` gần như bằng nhau nên chọn theo thời gian. Ngưỡng F1 validation: LR 0,73128; RF 0,57771.

**Tránh:** nói mô hình "tối ưu" (chỉ tối ưu trong lưới nhỏ); dùng thời gian 63,55 giây của lượt chấm lại ở `validation_methods.csv` để giải thích chọn lưới (phải dùng `validation_grid_B.csv`).

### 4.4. So sánh hiệu năng (khoảng 1,5 trang) — trả lời câu hỏi 4

**Nguồn duy nhất của mục này:** các tệp `*_test.csv` và `results_test.json` (kết quả test chính thức). Validation chỉ nhắc để đối chiếu.

**Ý chính:**
1. Bốn phương pháp trên **cùng giỏ đã che và cùng danh mục**: 24.877 giỏ test đủ điều kiện, 49.473 sản phẩm che.
2. **Bảng 4.5** và đường **trần**: Recall@10 trần 0,5198, nghĩa là khoảng 52% sản phẩm che nằm trong Top-1.000; không phương pháp nào có thể vượt.
3. **Kiểm định chính:** bootstrap ghép cặp theo người dùng, 2.000 lần, seed 42, so RF với Popularity: chênh 0,0216; khoảng tin cậy 95% [0,0192; 0,0239], cận dưới lớn hơn 0 nên có cải thiện. So sánh bổ trợ: RF so với Rules 0,0047 [0,0031; 0,0063]; LR so với RF −0,0061 [−0,0077; −0,0044].
4. **Hình 4.1:** Recall@K cho K = 1 đến 10 của bốn phương pháp kèm đường trần (hai khung chung trục: trần ở trên, bốn phương pháp phóng to ở dưới). Nhận xét: RF và Rules gần nhau ở K nhỏ (K=1 cùng 0,0218), tách dần khi K tăng.
5. **Chỉ số phân loại** (Bảng 4.6) tại ngưỡng đã khóa, trên toàn bộ 24.758.284 cặp, tỷ lệ dương 0,105%: Accuracy gần 1 chỉ phản ánh lớp âm áp đảo; đọc cùng Precision, Recall, F1, ROC-AUC, AP và ma trận nhầm lẫn.
6. **Đối chiếu với validation:** kết quả test gần trùng validation (RF 0,0971 ở cả hai tập; thứ tự Popularity, LR, Rules, RF giữ nguyên), không có dấu hiệu chọn quá khớp trên validation.

**Bảng 4.5 — Chỉ số xếp hạng trên tập test.** Nguồn: `ranking_metrics_test.csv`.

| Phương pháp | P@5 | R@5 | P@10 | R@10 | HR@10 |
|---|---:|---:|---:|---:|---:|
| Popularity | 0,0199 | 0,0509 | 0,0149 | 0,0755 | 0,1393 |
| Rules | 0,0249 | 0,0650 | 0,0181 | 0,0924 | 0,1655 |
| LR | 0,0235 | 0,0614 | 0,0178 | 0,0910 | 0,1627 |
| RF | 0,0257 | 0,0677 | 0,0187 | 0,0971 | 0,1708 |

Dòng cuối bảng: Recall@10 trần 0,5198. Dòng chênh lệch kèm khoảng tin cậy lấy từ `paired_bootstrap_test.csv`.

**Bảng 4.6 — Chỉ số phân loại trên tập test.** Nguồn: `classifier_metrics_test.csv`, `confusion_matrix_test.csv`.

| Mô hình | Ngưỡng | Accuracy | Precision | Recall | F1 | ROC-AUC | AP | TN | FP | FN | TP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LR | 0,73128 | 0,99735 | 0,04803 | 0,08113 | 0,06034 | 0,78832 | 0,01401 | 24.690.586 | 41.740 | 23.852 | 2.106 |
| RF | 0,57771 | 0,99738 | 0,05383 | 0,09034 | 0,06746 | 0,81353 | 0,01685 | 24.691.109 | 41.217 | 23.613 | 2.345 |

**Con số bối cảnh nên đưa (tính từ `basket_metrics_test.csv`, ghi công thức):** RF đạt khoảng 18,7% của trần Recall@10 (0,0971/0,5198); Popularity khoảng 14,5%. 66,0% giỏ có ít nhất một sản phẩm che nằm trong danh mục (33,96%, tức 8.449 giỏ, không thể trúng bất kể phương pháp). HR@10 của RF là 17,1%, nghĩa là 82,9% giỏ không trúng sản phẩm nào trong Top-10.

**Điểm tùy chọn (I1 ở Chương 3):** chất lượng theo nhóm kích thước giỏ. Nếu làm, chỉ làm trên validation (nối `basket_metrics_validation.csv` với `basket_size` trong `masked_baskets.parquet`), ghi rõ là mô tả bổ sung; không làm trên test.

**Tránh:** nói "RF vượt Rules" như cải thiện lớn (chênh 0,0047 nhỏ, có ý nghĩa thống kê nhưng cần xét chi phí, xem 4.6); gọi cải thiện là "tăng doanh thu"; dùng Accuracy làm bằng chứng mô hình tốt; ghi p thay cho khoảng tin cậy.

### 4.5. Độ quan trọng của đặc trưng và Diễn giải (khoảng 1,5 trang)

**Nguồn:** `importance.csv`, `importance_repeats.csv`, `importance_baseline.json`, `lr_coefficients.csv`, `ablation.csv`, `examples.csv`, `figures/fig-importance.pdf`. **Tất cả tính trên validation** (theo thiết kế), không trên test.

**Ý chính:**
1. **Permutation importance** cho LR và RF ở cấu hình đã chọn: 5.000 giỏ validation (seed 44), toàn bộ 4.976.269 cặp ứng viên của các giỏ này, hoán vị mỗi biến 10 lần, đo mức giảm Average Precision; báo trung bình và độ lệch chuẩn qua các lần hoán vị. AP nền: LR 0,01386; RF 0,01649.
2. **Kết quả (Hình 4.2):** LR giảm nhiều nhất khi hoán vị độ phổ biến (0,0037), rồi lift lớn nhất (0,0025); RF giảm nhiều nhất khi hoán vị confidence lớn nhất (0,0048), rồi số luật khớp (0,0024) và lift (0,0021). Ngành ứng viên có tác động nhỏ nhất ở cả hai mô hình (LR 0,00015; RF 0,00057).
3. **Hệ số LR** trên thang chuẩn hóa (một độ lệch chuẩn): lớn nhất là kích thước phần quan sát (0,308), rồi số sản phẩm cùng ngành (0,261), độ phổ biến (0,252), lift (0,193), confidence (0,141), số luật khớp (0,088); mọi hệ số biến số đều dương. Các cột ngành là hiệu so với mức chuẩn của mã hóa một-nóng; so hai ngành bằng hiệu hệ số.
4. **Lưu ý tương quan:** ba biến luật tương quan gần 1, nên tác động riêng từng biến khó tách; đọc cùng phép bỏ nhóm ở 4.1 (bỏ cả nhóm luật làm Recall@10 giảm rõ).
5. **Hai giỏ ví dụ chọn trước theo quy tắc** (giỏ validation có order_id nhỏ nhất có luật khớp và không có luật khớp: đơn 36 và đơn 5858); Top-5 của bốn phương pháp, đánh dấu món che. Cả hai giỏ ví dụ đều không trúng trong Top-5 của cả bốn phương pháp; nói thẳng điều này, vì ví dụ chọn theo quy tắc, không chọn tay cho đẹp. Một số `product_name` trống trong Master (ví dụ mã 13176, 47626): ghi tên khuyết, không bịa tên.

**Tránh:** "đặc trưng X gây ra" (hoán vị đo mức mô hình dựa vào X, không phải nhân quả); coi RF không có hệ số là nhược điểm (RF dùng importance); lấy ví dụ trúng để minh họa (chỉ dùng ví dụ chọn theo quy tắc).

### 4.6. Thảo luận kết quả thực nghiệm (khoảng 1 trang, không bảng)

**Nội dung theo thứ tự:**
1. **Trả lời câu hỏi 3 và 4 bằng một đoạn mỗi câu, kèm số:** FP-Growth nhanh hơn 4,1 đến 14,3 lần và cho cùng kết quả; RF có Recall@10 cao hơn Popularity 0,0216 (khoảng tin cậy 0,0192 đến 0,0239), tương đối khoảng 28,6%; Rules cao hơn Popularity khoảng 22,3% (0,0924 so với 0,0755); LR không vượt Rules.
2. **Cải thiện nhỏ về giá trị tuyệt đối nhưng có ý nghĩa thống kê và ổn định giữa validation và test;** giải thích mức tuyệt đối thấp bằng trần 0,5198 (nửa số sản phẩm che nằm ngoài danh mục) và giỏ nhỏ, không bằng "mô hình kém".
3. **Chi phí và lợi ích:** thời gian suy luận trên validation (24,7 triệu cặp): Popularity 5,77 giây, Rules 6,19 giây, LR 15,59 giây, RF 63,55 giây; RF chậm hơn Rules khoảng 10,3 lần để đổi lấy cải thiện khoảng 5,1% tương đối (0,0971 so với 0,0924). Vì vậy chọn RF hay Rules là quyết định cân bằng chất lượng và chi phí, cơ sở cho thử nghiệm A/B ở Chương 5.
4. **Vai trò của luật:** bỏ nhóm luật làm Recall@10 giảm nhiều nhất; phần lớn năng lực xếp hạng đến từ thông tin đồng mua.
5. **Mở rộng danh mục:** tăng N từ 1.000 lên 2.000 nâng trần nhưng Recall của luật gần như không đổi; lợi ích nằm ở sản phẩm hiếm khó dự đoán.
6. **Giới hạn của thực nghiệm (nối sang 5.3):** giả lập bằng cách che ngẫu nhiên, không có thứ tự thêm hàng thật; nhãn 0 là "chưa mua trong giỏ"; danh mục chung nên so sánh có điều kiện, không tối ưu riêng từng phương pháp; một lượt chia và một seed; không có giá bán, lợi nhuận hay lịch sử hiển thị nên không đo doanh thu; điểm classifier chưa hiệu chỉnh.

**Tránh:** kết luận nhân quả hay lợi ích kinh doanh; lặp lại số bảng thay vì diễn giải; nói "RF tốt nhất" mà không nêu khoảng tin cậy và chi phí.

### Việc code nhỏ còn lại cho Chương 4 (không bắt buộc)

- Không còn mã nào cần viết để có số của Chương 4. Hai phân tích bổ sung tùy chọn: theo nhóm kích thước giỏ (4.4) và độ phủ danh mục được gợi ý (mục 3, điểm 3); cả hai chỉ làm trên validation nếu cả hai muốn, và phải ghi là phân tích bổ sung.

---

## 5. CHƯƠNG 5 — Khuyến nghị quản trị và Kết luận (Phong viết, 4 trang)

Khung tiêu đề theo QMD. Mỗi khuyến nghị phải gắn với một bằng chứng cụ thể (bảng, hình hoặc con số) từ Chương 3 hoặc 4; không có khuyến nghị nào "từ trên trời". Phong đọc kỹ I1 đến I5 (mục 3.5), H1 đến H3 (mục 3.6) và 4.4 đến 4.6 trước khi viết.

### 5.1. Đề xuất giải pháp và Chiến lược kinh doanh (khoảng 1,5 trang) — trả lời câu hỏi 5

**Dạng trình bày gợi ý:** một bảng "Bằng chứng, Khuyến nghị, Điều kiện và giới hạn" (Bảng 5.1) rồi vài đoạn diễn giải. Các khuyến nghị đề xuất (Phong chỉnh lại câu chữ và có thể gộp hoặc bỏ):

| # | Khuyến nghị | Bằng chứng | Giới hạn nêu kèm |
|---|---|---|---|
| R1 | Dùng gợi ý theo **phần giỏ quan sát** thay cho danh sách theo độ phổ biến để hoàn thiện giỏ | 4.4: RF hơn Popularity 0,0216 Recall@10, khoảng tin cậy [0,0192; 0,0239]; Rules hơn Popularity 0,0924 so với 0,0755 | Offline, chưa đo doanh thu |
| R2 | **Lõi là luật đồng mua, thêm tầng xếp hạng RF chỉ khi chi phí chấp nhận được** | 4.4 và 4.6: RF hơn Rules 0,0047 (khoảng tin cậy [0,0031; 0,0063]) nhưng suy luận chậm khoảng 10 lần | Quyết định cân bằng chất lượng và chi phí, kiểm bằng A/B |
| R3 | **Dự phòng theo độ phổ biến** khi ngữ cảnh giỏ quá ít | I1: 5,38% giỏ reference chỉ có một sản phẩm; 4.1 và 4.4: 11,6% giỏ validation không có luật khớp (độ phủ luật 88,4%) | Số phần trăm từ mẫu reference và validation |
| R4 | **Đặt và đo vị trí gợi ý** ở ngành có độ phủ cao (produce, dairy eggs) | I2: produce 29,52% dòng, 73,95% giỏ; dairy eggs 15,73% dòng, 66,76% giỏ | Độ phủ không đo doanh thu; so với phương án phổ biến chung |
| R5 | **Không tách cấu hình theo giờ** chỉ dựa trên quy mô giỏ | I4: chênh trung vị khoảng một sản phẩm, phân phối chồng lấn gần như hoàn toàn | Chưa kiểm định, 16,62% giỏ thiếu giờ |
| R6 | **Thử cặp ngành** như giả thuyết hiển thị: bakery–dairy eggs, dry goods pasta–pantry, produce–meat seafood | 3.6: cả ba bác bỏ giả thuyết độc lập sau Holm, V = 0,201; 0,152; 0,152 (liên hệ nhỏ); lift 1,229; 1,412; 1,190 | Lift trung vị của 210 cặp là 1,225; cặp được chọn không nổi hẳn trên mức nền |
| R7 | **Danh mục ứng viên**: giữ Top-1.000, xem xét chiến lược riêng cho sản phẩm ít phổ biến | 4.3.1 và 4.4: trần Recall 0,5198 vì khoảng một nửa sản phẩm che ngoài Top-1.000; tăng lên 2.000 chỉ nâng Recall@10 của luật khoảng 0,001 | Lợi ích nằm ở sản phẩm hiếm, cần mô hình khác |

**Tránh:** nêu mức tăng doanh thu hay lợi nhuận (không có dữ liệu); gọi cặp ngành là "bổ trợ" chắc chắn; khuyến nghị không có bằng chứng.

### 5.2. Lộ trình triển khai ứng dụng thực tế (khoảng 1 trang)

**Nội dung:**
1. **Giai đoạn 1 (ngoại tuyến, đã làm):** quy trình tái lập, benchmark chi phí, chọn cấu hình, kiểm test một lần. Đầu vào cho giai đoạn sau.
2. **Giai đoạn 2 (thử nghiệm kín):** chạy bóng (shadow) trên lưu lượng thật không hiển thị, so điểm dự đoán với hành vi thật; kiểm tra độ trễ suy luận (RF chậm hơn Rules khoảng 10 lần trong đo của nhóm).
3. **Giai đoạn 3 (A/B):** thiết kế ba nhánh gợi ý: Popularity (đối chứng), Rules, RF; đơn vị ngẫu nhiên hóa là người dùng; thời lượng đủ phủ chu kỳ tuần (dữ liệu có mã ngày, 3.4); mẫu sử dụng ước lượng từ mức nền thật, không bịa số.
4. **Bảng KPI** (Bảng 5.2): chỉ tiêu chính, chỉ tiêu phụ, chỉ tiêu rào chắn:
   - Chính: tỷ lệ thêm sản phẩm gợi ý vào giỏ; giá trị đơn hàng trung bình.
   - Phụ: tỷ lệ nhấp; số sản phẩm mỗi giỏ; độ phủ danh mục được gợi ý.
   - Rào chắn: độ trễ, doanh thu mỗi phiên, tỷ lệ khiếu nại hay bỏ gợi ý, độ đa dạng.
   - Ngoại tuyến để theo dõi: Recall@10 và HR@10 trên bộ giữ lại.
5. **Quy tắc ra quyết định đặt trước:** ví dụ chỉ chuyển sang RF nếu cải thiện chỉ tiêu chính vượt ngưỡng đặt trước và độ trễ trong giới hạn; không nêu con số ngưỡng khi chưa có dữ liệu.
6. **Giám sát sau triển khai:** trôi dữ liệu (thay đổi độ phổ biến, mùa vụ), chất lượng dữ liệu (tỷ lệ thiếu, giả định thứ tự dòng), cập nhật luật và mô hình định kỳ.

**Tài liệu gợi ý thêm vào `references.bib`** (Phong kiểm lại thông tin thật trước khi thêm): Kohavi, Tang và Xu (2020), *Trustworthy Online Controlled Experiments*, Cambridge University Press (thử nghiệm A/B); Efron và Tibshirani (1993), *An Introduction to the Bootstrap*, Chapman & Hall (cho bootstrap ở 4.4).

### 5.3. Hạn chế của nghiên cứu và Đạo đức dữ liệu (khoảng 0,8 trang)

**Hạn chế (mỗi ý một hai câu, kèm bằng chứng):**
- Đánh giá ngoại tuyến bằng che ngẫu nhiên, không tái hiện trình tự thêm hàng thật; thứ tự trong dữ liệu là **giả định** (tái dựng theo thứ tự dòng, đã công bố ở 3.3).
- Nhãn 0 là "chưa mua trong giỏ"; không có giá bán, lợi nhuận, lịch sử hiển thị nên không đo doanh thu hay nhân quả.
- Một nhà bán lẻ, một bộ dữ liệu (đã thêm nhiễu); mỗi người một giỏ train; một lượt chia và một seed.
- Danh mục chung Top-1.000 nên so sánh có điều kiện; khoảng một nửa sản phẩm che nằm ngoài danh mục.
- Điểm classifier chưa hiệu chỉnh; cải thiện Rules sang RF nhỏ.
- Số đo thời gian và RAM phụ thuộc máy và thư viện (một máy, `.venv-m2`).
- Cấu hình luật chọn nằm ở cạnh dưới lưới; không khảo sát ngoài lưới.

**Đạo đức dữ liệu và AI** (barem trụ cột IV yêu cầu rõ):
- **Thiên lệch độ phổ biến:** gợi ý theo độ phổ biến và luật đồng mua khuếch đại sản phẩm đã phổ biến, thu hẹp phơi bày sản phẩm ít phổ biến; kết quả ở 4.4 (trần Recall bị giới hạn bởi danh mục phổ biến) là ví dụ cụ thể. Biện pháp: theo dõi độ phủ và đa dạng, thử nghiệm phơi bày sản phẩm ít phổ biến.
- **Quyền riêng tư:** dữ liệu dùng mã người dùng giả danh, không có thông tin định danh; vẫn có nguy cơ suy ra thông tin nhạy cảm từ giỏ hàng (ví dụ sức khỏe), nên cần tối thiểu hóa dữ liệu, giới hạn thời gian lưu, quyền từ chối và minh bạch với khách hàng.
- **Không suy luận về nhóm người:** nghiên cứu không dùng kích thước giỏ để suy ra thu nhập hay loại hộ gia đình.
- **Trách nhiệm và giám sát của con người:** gợi ý chỉ hỗ trợ, có kiểm soát nội dung; ghi nhận và công khai giới hạn của hệ thống.
- **Tái lập và minh bạch:** mã, cấu hình, hash và khóa lựa chọn trước khi mở test là cam kết minh bạch của nhóm.

**Tài liệu gợi ý** (Phong kiểm lại trước khi thêm): Mehrabi, Morstatter, Saxena, Lerman và Galstyan (2021), "A survey on bias and fairness in machine learning", *ACM Computing Surveys*.

### 5.4. Hướng phát triển và Kết luận (khoảng 0,7 trang)

**Hướng phát triển** (ngắn, gắn với hạn chế):
- Mô hình hóa trình tự thêm hàng và ngữ cảnh người dùng khi có dữ liệu (hướng của @rendle2010, chưa triển khai ở đồ án).
- Mở rộng ứng viên ngoài Top-1.000 và mô hình riêng cho sản phẩm ít phổ biến.
- Hiệu chỉnh điểm xác suất, đánh giá theo nhóm kích thước giỏ.
- Thử nghiệm A/B để đo tác động thật.

**Kết luận: trả lời lần lượt năm câu hỏi nghiên cứu** (mỗi câu một đến hai câu, có số):

| Câu hỏi | Gợi ý nội dung trả lời (chép số từ bài) |
|---|---|
| 1 | Sáu bảng làm sạch và tích hợp thành Master 1.384.617 dòng, 131.209 giỏ; kiểm tra toàn vẹn đạt (13 tiêu chí); bộ nhớ DataFrame giảm từ 423,04 xuống 50,10 MiB (88,16%); Parquet nhỏ hơn CSV 7,75 lần, đọc nhanh hơn khoảng 29,59 lần |
| 2 | Giỏ nhỏ, đuôi dài (trung vị 9 sản phẩm; 5,38% giỏ một sản phẩm); produce và dairy eggs phủ rộng; đồng mua dương phổ biến (182/210 cặp lift > 1), ba cặp đã kiểm có liên hệ nhỏ (V từ 0,152 đến 0,201) |
| 3 | Cùng itemset và support; FP-Growth nhanh hơn khoảng 4,1 lần (N=1.000) và 14,3 lần (N=2.000, độ dài 3), RAM chênh nhỏ |
| 4 | RF cao hơn Popularity 0,0216 Recall@10 (khoảng tin cậy 95% 0,0192 đến 0,0239); cao hơn Rules 0,0047; LR không vượt Rules; trần 0,5198 |
| 5 | Dùng luật làm lõi, thử RF bằng A/B, dự phòng độ phổ biến, đo bằng KPI đã nêu, theo dõi thiên lệch và quyền riêng tư |

Câu cuối của chương: nêu rõ kết quả là hiệu quả ngoại tuyến, cần thử nghiệm thật trước khi kết luận về doanh thu.

**Tránh:** thêm kết quả mới ở Chương 5; lặp lại bảng Chương 4; kết luận mạnh hơn bằng chứng.

---

## 6. Bản đồ bằng chứng (số, nguồn)

Mọi số của Chương 4 và 5 nằm trong các tệp sau; người viết mở tệp để chép. Tất cả trong `BAO CAO/Bao cao mo hinh/` trừ khi ghi khác.

| Nội dung | Tệp |
|---|---|
| Bảng 4.1 đặc trưng | `GUI_vuong_ch4_goiA_20261104/tai_lieu/bang_4_1_dac_trung.csv` |
| Bảng 4.2 phân hoạch | `dataset_description.csv`, `results_test.json`, `classifier_metrics_test.csv` |
| Lưới A (24 cấu hình) | `validation_grid_A.csv` |
| Bảng 4.3 benchmark | `mining_benchmark_N1000_c20_l2.csv`, `mining_benchmark_N2000_c20_l3.csv`, `itemset_equivalence_*.json` |
| Lưới B và chọn | `validation_grid_B.csv`, `validation_methods.csv`, `classifier_validation.csv`, `lock.json` |
| Bảng 4.5, Hình 4.1 (test) | `ranking_metrics_test.csv`, `recall_at_k_test.csv`, `paired_bootstrap_test.csv`, `figures/fig-recall-at-k-test.pdf` |
| Bảng 4.6 (test) | `classifier_metrics_test.csv`, `confusion_matrix_test.csv` |
| Tính theo giỏ (test) | `basket_metrics_test.csv` |
| Importance, hệ số, ablation, ví dụ | `importance.csv`, `importance_repeats.csv`, `importance_baseline.json`, `lr_coefficients.csv`, `ablation.csv`, `examples.csv`, `figures/fig-importance.pdf` |
| Độ phủ luật (validation) | `rule_coverage.json` |
| Tương quan đặc trưng | `feature_correlation.csv` |
| Bằng chứng khóa và chạy một lần | `lock.json`, `test_started.json`, `results_test.json` |
| Số của Chương 3 dùng ở Chương 5 | `BAO CAO/Bao cao EDA/` (tệp `eda_summary.csv`, `department_summary.csv`, `top_n_coverage.csv`, `ban2/hypotheses.csv`, `ban2/lift_baseline.csv`) |

**Quy tắc kiểm số:** trước khi nộp, mỗi người chọn ngẫu nhiên 10 số trong phần mình viết, đối chiếu với tệp nguồn, ghi kết quả vào biên bản.

---

## 7. Tóm tắt đồ án (Phong viết sau khi có Chương 4 và 5, 250 đến 350 từ)

Một đoạn gồm sáu ý theo thứ tự: (1) vấn đề: gợi ý sản phẩm mua kèm khi đang tạo giỏ, dữ liệu đa bảng có nhiễu; (2) dữ liệu: Instacart, sáu bảng, 1.384.617 dòng train, 131.209 giỏ; (3) phương pháp: làm sạch và ghép nối, chia bốn tập theo người dùng, che giỏ, Popularity, luật Apriori/FP-Growth, LR và RF; (4) kết quả định lượng: số của 4.3.1 và 4.4 (benchmark, Recall@10 test, khoảng tin cậy, trần); (5) khuyến nghị: lõi luật, A/B với RF, dự phòng; (6) giới hạn: ngoại tuyến, chưa đo doanh thu. Chỉ dùng số đã có trong thân bài.

---

## 8. Những câu hội đồng có thể hỏi (để cả hai chuẩn bị)

Đề có Live Demo và vấn đáp theo dòng code, kèm thao tác "đổi tham số rồi chạy lại ngay".

- Vì sao tách theo người dùng và vì sao có tập reference? Vì sao che giỏ và vì sao che $h$ sản phẩm?
- Vì sao Recall chia cho cả sản phẩm ngoài danh mục? Trần Recall là gì?
- Vì sao bootstrap ghép cặp thay cho t-test? Vì sao đặc trưng luật phải bằng 0 khi không khớp?
- Vì sao `lock.json` và dấu chạy một lần? Vì sao RF chạy một luồng ở lượt test?
- Đổi `C` của LR hoặc độ sâu RF thì chạy ở đâu và chạy gì? (trên validation hoặc mẫu `--pilot`, không chạy test)
- Vì sao chọn RF mặc dù cấu hình khác Recall cao hơn 0,0019? Vì sao FP-Growth nhanh hơn Apriori?
- Phần việc mỗi người làm là gì? Các số trong bài lấy từ đâu?

Vương trả lời về mã và số Chương 4; Phong trả lời về khuyến nghị, đạo đức và kiểm chứng. Cả hai đều phải hiểu toàn bộ luồng ở mức khối lớn (xem mục "ĐỌC NHANH" ở đầu mỗi tệp mã).

---

## 9. Danh sách kiểm trước khi nộp

- [ ] Ghép Chương 4 và 5 vào QMD, không còn ô chờ ở Chương 4, 5 và Tóm tắt.
- [ ] Cắt Chương 3 xuống khoảng 17 trang; tổng không quá 45 trang từ bìa đến hết Chương 5 (đếm bằng `pdftotext -f N -l N`, không đếm ký tự ngắt trang).
- [ ] Chữ thân bài và bảng 12 pt; hình rộng 16 cm; bảng có tên ở trên và nguồn ở dưới.
- [ ] Mọi số đối chiếu với tệp nguồn (mỗi người 10 số).
- [ ] Sửa các điểm lệch Chương 1 và 2 ở mục 3.
- [ ] Xóa hai phụ lục; thêm một câu ở 2.5 nêu mã và nhật ký nộp riêng.
- [ ] Tham chiếu chéo đủ, không còn "??".
- [ ] Nhật ký làm việc đủ, liên kết còn sống.
