# THIẾT KẾ CHI TIẾT CHƯƠNG 4 — XÂY DỰNG MÔ HÌNH VÀ ĐÁNH GIÁ HIỆU NĂNG

Ngày 01/11/2026. Bản đề xuất của Vương, chờ hai bạn thống nhất. Đây là kế hoạch, không phải kết quả.
Căn cứ: `Chung/archive/projects.pdf` (giai đoạn 5–7, khung 4.1–4.6, rubric trụ cột III–IV), Chương 1–2 của QMD,
`HUONG_DAN_CHUNG_PRJ08.md`, `roadmap.md`, `THONG_NHAT_PHAN_VIEC_20261031.md`.
Đường dẫn tính từ thư mục bài `2521001118_Nhom01_TieuLuan/`.

---

## 0. Kết luận kiểm tra hướng đi hiện có

**Phần phương pháp của `HUONG_DAN_CHUNG_PRJ08.md` (mục 6–10) đúng hướng và khớp Chương 2 của QMD.** Giữ nguyên:
bài toán hoàn thiện giỏ; chia 30/30/20/20 theo người dùng; che giỏ $h=\min(k-1,\max(1,\lfloor0{,}2k\rfloor))$;
danh mục ứng viên C = Top-N của reference; 7 đặc trưng; 4 phương pháp; Recall@10 là chỉ số chính;
bootstrap ghép cặp 2.000 lần; chỉ mở test sau khi khóa cấu hình.

**Chưa đủ để bắt tay vào code**, vì còn 9 chỗ hở:

| # | Chỗ hở | Hậu quả nếu để nguyên | Xử lý trong bản này |
|---|---|---|---|
| 1 | Mục 4.1 của đề tên "Tạo lập **và Lựa chọn** đặc trưng", nhưng hướng dẫn chỉ có danh sách cố định | Thiếu phần "lựa chọn" mà rubric và khung đề đòi | Mục 3.1: lý do giữ/loại từng biến, tương quan trên fit, phân tích bỏ nhóm đặc trưng trên validation |
| 2 | Chưa có lưới tham số cụ thể (Top-N, support, confidence, max_len, LR, RF, số mẫu âm) | Dễ chọn lưới sau khi đã thấy kết quả | Mục 4: lưới cố định, ghi vào config trước khi chạy |
| 3 | Chưa có quy tắc khi hai cấu hình gần bằng nhau | N lớn gần như luôn thắng vì phủ nhiều hơn, chọn N tùy ý | Mục 4.1: dung sai 0,002 Recall@10, ưu tiên cấu hình rẻ hơn |
| 4 | Chưa nói trần Recall do sản phẩm ngoài C | Recall@10 thấp dễ bị đọc là mô hình kém | Mục 3.4: báo thêm "Recall@10 trần" |
| 5 | Chưa có cơ chế kỹ thuật khóa test | Chỉ dựa vào kỷ luật, khó chứng minh khi vấn đáp | Mục 5: `lock.json` + script test từ chối chạy khi thiếu khóa |
| 6 | Permutation importance trên toàn validation với RF quá nặng (khoảng 26 triệu cặp ở N=1.000) | Không chạy nổi hoặc chạy hàng giờ | Mục 3.5: mẫu con cố định 5.000 giỏ validation |
| 7 | Mục 11 (kiến trúc), 13 (lệnh) của hướng dẫn và mục 2, 4, 8 của roadmap còn đường dẫn trước rút gọn (`artifacts/`, `scripts/cleaning/vuong/`, `run_cleaning_all.py`, `src/`) | Viết code theo đường dẫn không còn tồn tại | Mục 6: cấu trúc mới theo quy ước code rút gọn; mục 10: danh sách chỗ cần sửa |
| 8 | `.venv-m2` chưa cài scikit-learn, mlxtend, psutil; môi trường không có pip (tạo bằng uv) | Không chạy được; cài nhầm có thể nâng pandas/numpy làm lệch hash Chương 3 | Mục 9 |
| 9 | Chưa phân công người viết code Chương 4 (THONG_NHAT mục 6.1) | Không ai bắt đầu | Mục 9: đề xuất chia việc |

---

## 1. Đối chiếu rubric và khung đề

| Yêu cầu trong `projects.pdf` | Nơi đáp ứng trong Chương 4 |
|---|---|
| Giai đoạn 5: tạo biến mới, mã hóa danh nghĩa bằng OneHotEncoder, chuẩn hóa StandardScaler trên tập huấn luyện | 4.1: 6 biến số tạo từ reference và phần giỏ quan sát; ngành ứng viên mã hóa OneHot; scaler chỉ fit trên fit |
| Giai đoạn 5: tách train/test, random_state cố định, stratify khi mất cân bằng | 4.2: chia theo người dùng seed 42; giải thích vì sao không stratify theo dòng; báo tỷ lệ lớp từng tập |
| Giai đoạn 6: Logistic Regression, Random Forest bằng Scikit-learn; Pipeline + ColumnTransformer chống rò rỉ | 4.3: hai Pipeline cùng schema; kiểm thử tham số biến đổi chỉ học từ fit |
| Giai đoạn 7: Accuracy, Precision, Recall, F1, ROC-AUC, ma trận nhầm lẫn | 4.4: đủ các chỉ số phân loại trên toàn bộ cặp ứng viên test, cùng chỉ số xếp hạng |
| Giai đoạn 7: Feature Importance hoặc hệ số hồi quy | 4.5: permutation importance + hệ số LR đã chuẩn hóa |
| PRJ-08: ma trận giỏ nhị phân, Apriori/FP-Growth, Support/Confidence/Lift | 4.3: ma trận thưa, benchmark hai thuật toán, bảng luật |
| Rubric III mức Khá: Pipeline chuẩn, không rò rỉ, so sánh 2–3 mô hình đủ metrics | 4 phương pháp trên cùng C và cùng phép che |
| Rubric III mức Xuất sắc: Pipeline hoàn chỉnh, **kiểm định giả thuyết thống kê sâu sắc**, Feature Importance thuyết phục | Bootstrap ghép cặp cho CI chênh lệch Recall@10 (kiểm định chính); importance có mẫu số, số lần lặp, seed |
| Rubric IV (Chương 5) cần căn cứ từ kết quả mô hình | 4.6 chốt 3–4 phát hiện có số đo để Chương 5 dùng lại |
| Vấn đáp: đổi tham số và chạy lại ngay trên IDE | Mọi tham số nằm trong một config; có lệnh chạy nhanh trên mẫu nhỏ (mục 7) |

---

## 2. Số liệu khả thi đã đo (chỉ trên reference và fit)

Đo ngày 01/11 bằng script tạm, không chạm validation/test. Số này dùng để chọn lưới, chưa đưa vào bài.

- Số giỏ theo tập: reference 39.363; fit 39.363; validation 26.241; test 26.242. Mỗi người dùng một giỏ.
- Tập fit: 1.975 giỏ một sản phẩm (loại khỏi đánh giá che giỏ); 37.388 giỏ được che; trung bình h = 2,006 sản phẩm che mỗi giỏ; tổng 75.006 sản phẩm che.
- Support của sản phẩm thứ N trong reference: Top-500 là 121 giỏ (0,3074%); Top-1.000 là 69 giỏ (0,1753%); Top-2.000 là 37 giỏ (0,0940%).
- Tỷ lệ dòng sản phẩm của fit thuộc C: Top-500 41,5%; Top-1.000 52,3%; Top-2.000 64,2%.
  Nghĩa là khoảng một nửa sản phẩm bị che nằm ngoài C với N=1.000, nên Recall@10 có trần thấp. Đây là giới hạn thiết kế, phải báo cùng kết quả.
- Số cặp sản phẩm đồng mua trong reference (Top-1.000): 246.610 cặp xuất hiện ít nhất một lần; 18.453 cặp ≥ 10 giỏ; 6.730 cặp ≥ 20 giỏ; 1.516 cặp ≥ 50 giỏ; 453 cặp ≥ 100 giỏ.
  Tính ma trận đồng xuất hiện thưa mất dưới 0,1 giây, nên khai phá max_len=2 và 3 đều khả thi.
- Ước tính (chưa đo): dữ liệu huấn luyện classifier khoảng 0,8 triệu dòng với 20 mẫu âm/giỏ; chấm validation khoảng 26 triệu cặp ở N=1.000, chạy theo lô 2.000 giỏ.

---

## 3. Thiết kế từng mục 4.1–4.6

### 3.1. Mục 4.1 — Tạo lập và lựa chọn đặc trưng (khoảng 1,5 trang, Bảng 4.1)

**Đơn vị:** cặp (giỏ j, ứng viên c) với c ∈ C_j = C \ O_j.
**Nhãn:** Y=1 nếu c ∈ H_j; Y=0 nếu c không thuộc giỏ đầy đủ.

**Bảy đặc trưng** (giữ đúng Chương 2; tất cả chỉ dùng thống kê reference và O_j, không dùng H_j):

| Đặc trưng | Công thức | Kiểu | Khi không xác định |
|---|---|---|---|
| candidate_popularity | n_ref(c)/N_ref | số | không xảy ra (c ∈ C) |
| matching_rule_count | số luật A→{c} với A ⊆ O_j | số | 0 |
| max_rule_confidence | max confidence các luật khớp | số | 0 |
| max_rule_lift | max lift các luật khớp | số | 0 |
| observed_basket_size | \|O_j\| | số | không xảy ra |
| same_department_count | số sản phẩm trong O_j cùng ngành với c | số | 0 |
| candidate_department_id | ngành của c | danh nghĩa, 21 mức | không xảy ra |

**Phần "lựa chọn" (cần thêm so với hướng dẫn):**
1. *Biến bị loại có lý do*, liệt kê trong bài: `user_id`, `product_id` (mã định danh, không có thứ tự ý nghĩa);
   `reordered`, `days_since_prior_order`, lịch sử prior cá nhân (ngoài phạm vi Chương 2, dễ rò rỉ thông tin hành vi);
   kích thước giỏ đầy đủ (lộ |H_j|, rò rỉ trực tiếp); `aisle_id` của ứng viên (134 mức, trùng vai trò với ngành, tăng chiều OneHot).
2. *Tương quan Spearman giữa 6 biến số* trên dữ liệu fit sau lấy mẫu âm. Dự kiến ba biến luật tương quan mạnh với nhau;
   ghi nhận để diễn giải importance ở 4.5, không loại biến chỉ vì tương quan.
3. *Phân tích bỏ nhóm đặc trưng trên validation* với cấu hình classifier đã chọn: (a) đủ 7 biến; (b) bỏ 3 biến luật; (c) bỏ 2 biến ngành.
   Báo Recall@10 và Average Precision. **Tập đặc trưng cuối giữ nguyên 7 biến như Chương 2**; phép bỏ nhóm dùng để giải thích đóng góp từng nhóm,
   không dùng để đổi thiết kế sau khi đã thấy kết quả.

**Kiểm soát rò rỉ** (viết một đoạn, có kiểm thử đi kèm):
- Luật, độ phổ biến, C chỉ học từ reference (giỏ đầy đủ, không bị che).
- Đặc trưng của giỏ fit/validation/test chỉ dùng O_j. Kiểm thử: đổi H_j mà giữ O_j thì X không đổi.
- Tham số điền thiếu, scaler, encoder chỉ fit trên fit.

### 3.2. Mục 4.2 — Chuẩn hóa và phân chia tập (khoảng 1 trang, Bảng 4.2)

- Dùng lại `split_manifest.parquet` của G0, không chia lại. Nêu lại quy tắc làm tròn và số người dùng từng tập.
- **Vì sao không dùng `train_test_split(stratify=...)` theo dòng:** mỗi giỏ sinh hàng trăm cặp ứng viên; chia theo dòng làm cùng một giỏ, cùng người dùng
  xuất hiện ở cả huấn luyện và kiểm tra. Chia theo người dùng tránh rò rỉ; mất cân bằng lớp xử lý bằng lấy mẫu âm có kiểm soát và chỉ số phù hợp.
- **Bảng 4.2** (một bảng cho cả bốn tập): số giỏ; số giỏ một sản phẩm bị loại; số giỏ đánh giá; tổng |H|; tỷ lệ sản phẩm che thuộc C (vi mô và vĩ mô);
  số cặp ứng viên; tỷ lệ Y=1 trên toàn bộ ứng viên; với fit thêm tỷ lệ Y=1 sau lấy mẫu âm.
- **Che giỏ:** RNG riêng cho từng giỏ, `np.random.default_rng([42, order_id])`, chọn h sản phẩm không hoàn lại. Lưu O, H cho fit/validation/test vào một Parquet;
  mọi phương pháp đọc cùng tệp này.
- **Lấy mẫu âm khi fit:** giữ toàn bộ dương trong C_j; lấy 20 âm/giỏ không hoàn lại từ C_j \ H_j, RNG `default_rng([43, order_id])`; giỏ không có dương vẫn lấy âm;
  thiếu thì lấy hết và ghi số thực tế. Validation/test chấm toàn bộ C_j theo lô.
- **Chuẩn hóa:** `ColumnTransformer` gồm
  - nhánh số: `SimpleImputer(strategy="median")` → `StandardScaler` (chỉ ở LR; RF bỏ bước scale);
  - nhánh danh nghĩa: `SimpleImputer(strategy="most_frequent")` → `OneHotEncoder(handle_unknown="ignore")`.
  Không dùng `drop="first"`: LR có điều chuẩn L2 nên không bị bẫy biến giả, và giữ đủ 21 cột giúp đọc hệ số từng ngành. Ghi câu này trong bài vì đề nhắc bẫy biến giả.

### 3.3. Mục 4.3 — Huấn luyện mô hình (khoảng 2 trang, Bảng 4.3 và 4.4)

**4.3.1. Apriori và FP-Growth**
- Đầu vào: ma trận Boolean thưa, hàng = 39.363 giỏ reference (giữ hàng rỗng sau lọc C trong mẫu số), cột = C.
  Dùng `mlxtend.frequent_patterns.apriori` và `fpgrowth` với cùng `min_support`, `max_len`, cùng DataFrame thưa.
  Apriori chạy với `low_memory=True`: lượt thử 01/11 ở N=500, min_count 50, max_len 2, chế độ mặc định cần khoảng 14 GB RAM
  và 27–42 giây; `low_memory=True` cho cùng 2.016 itemset trong khoảng 1,7 giây, 160 MB. Hồ sơ đo của chế độ mặc định
  không được lưu (bảng đã bị lượt sau ghi đè): muốn đưa số này vào 4.3 phải đo lại có lưu tệp; nếu không thì chỉ nêu định tính.
- Sinh luật bằng `association_rules`, chỉ giữ luật hậu đề một sản phẩm; tính support, confidence, lift, leverage, conviction kèm số giỏ đếm được.
- **Benchmark (Bảng 4.3):** trên cấu hình đã khóa, mỗi thuật toán chạy 3 lần, mỗi lần một tiến trình con mới (theo cách `m1_benchmark.py` đã làm),
  đo riêng thời gian dựng ma trận, khai phá, sinh luật; RAM đỉnh bằng psutil; số itemset, số luật. Báo trung vị và khoảng min–max.
  Kiểm tra tương đương: cùng tập itemset và support lệch không quá 1e-12.
  Thêm một dòng cho cấu hình nặng nhất trong lưới để thấy khác biệt khi dữ liệu lớn hơn.

**4.3.2. Bốn phương pháp xếp hạng**
1. Popularity: popularity giảm dần, `product_id` tăng dần.
2. Association Rules: ứng viên có luật khớp xếp trước theo max confidence giảm dần, rồi popularity giảm dần, rồi `product_id`; không có luật thì xếp sau theo popularity.
3. LR: `LogisticRegression(penalty="l2", solver="lbfgs", max_iter=1000)`, xếp theo `predict_proba` giảm dần, phá hòa bằng `product_id`.
4. RF: `RandomForestClassifier(n_estimators=300, max_features="sqrt", n_jobs=-1, random_state=42)`, cùng quy tắc xếp.

**Bảng 4.4:** cấu hình đã chọn và lưới đã thử của từng phương pháp, kèm Recall@10 validation của cấu hình được chọn.

### 3.4. Mục 4.4 — So sánh hiệu năng (khoảng 2 trang, Bảng 4.5, Hình 4.1)

**Chỉ số xếp hạng**, trung bình theo giỏ, K = 5 và 10: Precision@K (luôn chia K), Recall@K (mẫu số |H_j| gồm cả sản phẩm ngoài C), HitRate@K.
Bổ sung để đọc đúng:
- *Recall@10 trần* = trung bình min(|H_j ∩ C|, 10)/|H_j|: mức cao nhất mọi phương pháp có thể đạt với C đã chọn.
- *Độ phủ:* tỷ lệ sản phẩm che thuộc C (vi mô, vĩ mô); tỷ lệ giỏ có ít nhất một luật khớp; số sản phẩm từng được gợi ý / |C|.

**Chỉ số phân loại** (LR, RF), trên toàn bộ cặp ứng viên test tại ngưỡng tối đa F1 trên validation:
Accuracy, Precision, Recall, F1, ROC-AUC, Average Precision, ma trận nhầm lẫn.
Ghi rõ: tỷ lệ dương rất thấp (ước dưới 1%) nên Accuracy gần 1 không có ý nghĩa; AP và chỉ số xếp hạng là căn cứ chính.

**Kiểm định chính (đáp ứng "kiểm định giả thuyết sâu sắc" của rubric III):**
- Giả thuyết: chênh lệch Recall@10 giữa phương pháp chính (chọn trên validation) và Popularity trên test.
- Bootstrap ghép cặp theo người dùng (một người một giỏ): 2.000 lần, seed 42; CI percentile 2,5%–97,5%.
  Kết luận cải thiện chỉ khi cận dưới > 0.
- So sánh phụ (phương pháp chính với Rules, LR với RF): báo CI cùng cách, ghi là bổ trợ, không dùng để đổi phương pháp chính.

**Bảng 4.5:** 4 hàng phương pháp × cột P@5, R@5, P@10, R@10, HR@10, kèm dòng Recall@10 trần và dòng chênh lệch với CI.
**Hình 4.1:** Recall@K theo K = 1…10 của bốn phương pháp và đường trần (một hình, rộng 16 cm).

### 3.5. Mục 4.5 — Độ quan trọng đặc trưng và diễn giải (khoảng 1,5 trang, Hình 4.2)

- **Đối tượng diễn giải chốt trước, không phụ thuộc phương pháp thắng:** importance và hệ số tính cho **cả LR và RF** ở cấu hình đã chọn trên validation.
  Nếu phương pháp chính là Popularity hoặc Rules (không có Pipeline bảy đặc trưng), 4.5 diễn giải thêm cơ chế của nó bằng số đo
  có sẵn: tỷ lệ giỏ có luật khớp, tỷ lệ gợi ý đến từ luật so với từ độ phổ biến.
- **Permutation importance** của LR và RF trên mẫu con cố định 5.000 giỏ validation (chọn bằng seed 44, chấm toàn bộ ứng viên của các giỏ đó),
  thước đo Average Precision, `n_repeats=10`. Báo trung bình và độ lệch chuẩn. Hoán vị theo cột gốc: 21 cột OneHot của ngành hoán vị cùng nhau như một biến.
- **Hệ số LR** sau chuẩn hóa: dấu và độ lớn của 6 biến số; nhắc tương quan giữa ba biến luật (từ 4.1) làm hệ số khó tách riêng.
- **Hai ví dụ giỏ chọn theo quy tắc, không chọn tay:** giỏ validation có `order_id` nhỏ nhất có ít nhất một luật khớp, và giỏ có `order_id` nhỏ nhất không có luật khớp;
  in Top-5 gợi ý của bốn phương pháp và đánh dấu sản phẩm trúng.
- **Hình 4.2:** biểu đồ thanh permutation importance có thanh sai số.

### 3.6. Mục 4.6 — Thảo luận (khoảng 1 trang, không bảng)

Trả lời RQ3 và RQ4 bằng số đã có ở 4.3–4.5:
- Apriori so với FP-Growth: thời gian, RAM, tương đương kết quả.
- Phương pháp chính có vượt Popularity với CI hay không; nếu không, nêu lý do có số đo (trần Recall, độ phủ luật thấp).
- Đóng góp nhóm đặc trưng (từ phép bỏ nhóm 4.1).
- Giới hạn chỉ nêu những gì riêng của mô hình (danh mục Top-N, che ngẫu nhiên, sản phẩm phổ biến lấn át); các câu "không chứng minh nhân quả" để ở 5.3 theo THONG_NHAT mục 4.2.
- Chốt 3–4 phát hiện làm đầu vào cho Chương 5.

---

## 4. Lưới tham số và quy tắc chọn (ghi vào config trước khi chạy)

### 4.1. Giai đoạn A — danh mục và luật (chọn bằng Recall@10 của phương pháp Rules trên validation)

| Tham số | Giá trị thử | Ghi chú |
|---|---|---|
| N (Top-N) | 500; 1.000; 2.000 | 41,5% / 52,3% / 64,2% dòng fit thuộc C |
| min_support (theo số giỏ) | 20; 50 | 0,0508% / 0,1270% của 39.363 giỏ |
| min_confidence | 0,05; 0,10 | |
| max_len | 2; 3 | |

Tổng 24 cấu hình. Popularity được chấm cùng lúc với mỗi N (không có tham số luật).

**Quy tắc chọn:** lấy cấu hình có Recall@10 lớn nhất; các cấu hình kém hơn mức lớn nhất không quá **0,002** coi là hòa,
khi hòa chọn theo thứ tự: N nhỏ hơn → min_support lớn hơn → max_len nhỏ hơn → min_confidence lớn hơn (ít luật hơn, rẻ hơn).
N và luật cố định từ đây cho cả LR/RF.

### 4.2. Giai đoạn B — classifier (chọn bằng Recall@10 validation; ngưỡng bằng F1 validation)

| Mô hình | Lưới | Số cấu hình |
|---|---|---|
| LR | C ∈ {0,01; 0,1; 1; 10} | 4 |
| RF | max_depth ∈ {10; 20}; min_samples_leaf ∈ {20; 100} | 4 |

Số mẫu âm cố định 20/giỏ (không đưa vào lưới để giới hạn số lần thử). `class_weight=None`: mất cân bằng đã giảm bằng lấy mẫu âm,
và việc xếp hạng không phụ thuộc hiệu chỉnh xác suất. Hòa trong dung sai 0,002 thì chọn mô hình suy luận nhanh hơn (đo trên validation).

### 4.3. Giai đoạn C — phương pháp chính

So Recall@10 validation của 4 phương pháp ở cấu hình tốt nhất; hòa (≤ 0,002) thì chọn chi phí suy luận thấp hơn,
rồi theo thứ tự cố định Popularity → Rules → LR → RF. Ghi kết quả vào `lock.json`.

---

## 5. Khóa trước khi mở test

`lock.json` ghi: cấu hình giai đoạn A, B, C; ngưỡng F1; phương pháp chính; SHA-256 của config, mask, danh mục, luật, hai Pipeline đã lưu;
thời điểm khóa. Script chấm test:
1. Dừng nếu thiếu `lock.json` hoặc bất kỳ hash nào lệch.
2. Chỉ đọc tập test ở script này; các script trước đọc split và lọc bỏ test ngay khi nạp.
3. Ghi kết quả test một lần; chạy lại chỉ cho phép khi `lock.json` không đổi (kết quả phải giống từng byte).

Danh sách kiểm tra mục 6 của roadmap được đánh dấu trong `lock.json` trước khi chạy test.

---

## 6. Cấu trúc code và đầu ra (theo quy ước code rút gọn)

Dùng lại `project_io.py` (đường dẫn tương đối, ghi nguyên tử, `write_hashes`/`check_hashes`, thiết lập hình). Mỗi script gọi `check_hashes()` của G0 trước khi đọc.

Chủ sở hữu từng tệp ở mục 11.3; thứ tự chạy theo thứ tự hàng dưới đây.

| Script | Chủ | Việc | Đầu ra chính | Mục |
|---|---|---|---|---|
| `scripts/m4_common.py` | Vương | Hàm thuần: dựng giỏ, che giỏ, danh mục, sinh C_j, khớp luật, 7 đặc trưng, Popularity/Rules, chỉ số xếp hạng | — | — |
| `scripts/m4_mining.py` | Vương | Danh mục C và luật cho lưới giai đoạn A | `DATA/Data phai sinh/M4/catalog.parquet` (mọi sản phẩm reference đã xếp hạng; C = rank ≤ N), `rules_grid.parquet` (cột `top_n`, `min_count`, `max_len`) | 4.3 |
| `scripts/m4_benchmark_mining.py` | Vương | Benchmark Apriori/FP-Growth, tiến trình con, 3 lần; lượt lỗi/quá giờ vẫn ghi báo cáo | `BAO CAO/Bao cao mo hinh/mining_benchmark_<cấu hình>.csv`, `itemset_equivalence_<cấu hình>.json` (một cặp tệp mỗi cấu hình) | 4.3 |
| `scripts/m4_prepare.py` | Vương | Che giỏ fit/validation/test, giai đoạn A, đặc trưng fit có lấy mẫu âm, tương quan đặc trưng | `M4/masked_baskets.parquet`, `features_fit.parquet`, `feature_schema.json`; `Bao cao mo hinh/validation_grid_A.csv`, `basket_metrics_validation.csv`, `feature_correlation.csv` | 4.1–4.3 |
| `scripts/m4_classifier.py` | Phong | Pipeline, giai đoạn B, ngưỡng F1, phép bỏ nhóm | `M4/pipeline_lr.joblib`, `pipeline_rf.joblib`; `Bao cao mo hinh/validation_grid_B.csv`, `ablation.csv` | 4.1, 4.3 |
| `scripts/m4_lock.py` | Vương | Giai đoạn C, ghi `lock.json` | `Bao cao mo hinh/lock.json` | 4.3 |
| `scripts/m4_test.py` | Phong | Chấm test sau khóa (gọi hàm xếp hạng và chỉ số của `m4_common.py`), chỉ số phân loại, bootstrap | `test_metrics.csv`, `basket_metrics_test.csv`, `classifier_metrics.csv`, `confusion_matrix.csv`, `coverage.csv`, `paired_bootstrap.csv` | 4.4 |
| `scripts/m4_interpret.py` | Phong | Permutation importance, hệ số LR, hai ví dụ giỏ, hình | `importance.csv`, `lr_coefficients.csv`, `examples.csv`; `figures/fig-recall-at-k.pdf`, `fig-importance.pdf` | 4.4–4.5 |
| `configs/m4_model.json` | Vương | Toàn bộ tham số mục 4–5, seed, K, kích thước lô | — | — |

Thư mục báo cáo mới: `BAO CAO/Bao cao mo hinh/` (cùng cấp `Bao cao EDA/`), có `hashes.json` riêng.
Không ghi đè bất kỳ tệp nào Chương 3 đang trích.

---

## 7. Kiểm thử (thêm vào `tests/`, chạy cùng 30 test hiện có)

Hai tệp, dữ liệu nhỏ dựng tay: `tests/test_m4_data.py` (Vương: kiểm thử 1–5, 8) và `tests/test_m4_model.py` (Phong: kiểm thử 6, 7, 9).
1. Che giỏ: O ∩ H = ∅, O ∪ H = giỏ; h đúng công thức với k = 1, 2, 5, 10, 11; cùng seed và `order_id` cho cùng kết quả.
2. Rò rỉ: đổi H mà giữ O thì đặc trưng không đổi.
3. Không có luật: ba đặc trưng luật bằng 0; ứng viên xếp theo popularity.
4. Metrics tính tay: Precision@K chia K khi danh sách ngắn; Recall tính cả đáp án ngoài C; C_j rỗng cho danh sách rỗng và giỏ vẫn được tính.
5. Phá hòa theo `product_id` tăng dần ở cả bốn phương pháp.
6. Pipeline: trung bình của scaler bằng trung bình cột trên dữ liệu fit, không phải validation.
7. Bootstrap ghép cặp: hai phương pháp giống nhau cho CI bằng [0, 0].
8. Apriori và FP-Growth cho cùng itemset/support trên ma trận nhỏ.
9. `m4_test.py` dừng khi thiếu hoặc lệch `lock.json`.

**Chuẩn bị vấn đáp:** `configs/m4_model.json` có cờ `"pilot_baskets": 2000` (chưa script nào đọc; thêm khi viết bước 2, ghi đầu ra pilot vào thư mục riêng, không lẫn kết quả chính thức) để chạy toàn luồng trên mẫu nhỏ trong vài phút,
phục vụ yêu cầu "đổi tham số rồi chạy lại ngay trên IDE" mà không động vào kết quả chính.

---

## 8. Ngân sách 9 trang

| Mục | Trang | Bảng/hình |
|---|---:|---|
| 4.1 | 1,5 | Bảng 4.1 đặc trưng (gộp cột nguồn, kiểu, xử lý) |
| 4.2 | 1 | Bảng 4.2 bốn tập |
| 4.3 | 2 | Bảng 4.3 benchmark; Bảng 4.4 lưới và cấu hình chọn |
| 4.4 | 2 | Bảng 4.5 metrics + CI; Hình 4.1 Recall@K |
| 4.5 | 1,5 | Hình 4.2 importance; ví dụ giỏ viết thành 2–3 câu |
| 4.6 | 1 | Không bảng |
| **Tổng** | **9** | 5 bảng, 2 hình |

Bảng tương quan, kết quả bỏ nhóm, ma trận nhầm lẫn, chỉ số phân loại đầy đủ và toàn bộ lưới: nêu số chính trong lời văn, bảng đầy đủ lưu CSV.
Hình vẽ theo quy cách mục 6.6 THONG_NHAT (rộng 16 cm, chữ 12 pt) ngay từ đầu.

---

## 9. Việc cần chốt trước khi code

1. **Phân công** (THONG_NHAT 6.1): xem mục 11. Mục 11 thay cho cách chia tệp ở mục 6 khi hai bạn đã chốt.
2. **Môi trường — đã xong 01/11 trên máy Vương:** scikit-learn 1.9.1, mlxtend 0.25.0, psutil 7.2.2 (kèm cloudpickle 3.1.2, joblib 1.6.0,
   narwhals 2.28.0, threadpoolctl 3.7.0), khóa trong `requirements.txt`; gói cũ không đổi; 61/61 đầu ra Chương 3 giống từng byte sau khi cài.
   Máy Phong cài cùng phiên bản:
   ```powershell
   uv pip install --python .venv-m2/Scripts/python.exe -r requirements.txt
   ```
3. **Chương 2 không cần sửa** với thiết kế này: Chương 2 đã ghi "lưới tìm kiếm và cấu hình cuối ghi ở chương 4". Nếu hai bạn đổi bất kỳ điểm nào ở mục 0 (đặc trưng, nhãn, chỉ số chính, chia tập), Phong sửa Chương 2 trước khi chạy.
4. Chốt dung sai hòa 0,002 và 20 mẫu âm/giỏ (hoặc đổi) trước khi chạy giai đoạn A.

---

## 10. Chỗ lỗi thời trong hai tài liệu cũ (không sửa; chỉ để biết)

Hai tài liệu cũ là hướng dẫn chung, giữ nguyên. Với Chương 4, tài liệu này là căn cứ; chỗ nào hai bên khác nhau thì theo tài liệu này.

`HUONG_DAN_CHUNG_PRJ08.md`:
- Mục 4 và 13 nhắc `run_cleaning_all.py`, `python tests/test_cleaning.py`: nay là `clean_vuong.py`, `clean_phong.py`, `summarize_cleaning.py`, chạy test bằng `unittest discover`, luôn dùng `.venv-m2`.
- Mục 11: `scripts/cleaning/vuong/`, `scripts/cleaning/phong/`, `src/vi_du_phu_luc.py`, `Data đã làm sạch/`, `Bao cao lam sach/` ở gốc, thư mục `artifacts/`: thay bằng cấu trúc hiện tại (`scripts/cleaning/common.py`…, `DATA/…`, `BAO CAO/…`) và mục 6 của tài liệu này.
- Mục 9 "Pilot có thể bắt đầu N=500/1.000": thay bằng lưới mục 4.

`roadmap.md`:
- Mục 2: dòng "Nhánh Bạn 2 chưa triển khai", "Mục 3.4 trở đi còn khung" đã lỗi thời (Chương 3 đã ghép đủ ngày 01/11); các tệp `pipeline_latest.json`, `README_M2.md`, `README_M2_BAN1.md`, `ban1/validation.json` không còn sau rút gọn.
- Mục 4 "Việc tiếp theo: Bắt đầu M2": nay là M3–M5 theo tài liệu này. Lịch tuần 3 (29/10–04/11) đã qua giữa chừng; ghi lịch mới có lý do, không lùi ngày.
- Mục 8: lệnh chạy cũ, thay bằng `scripts/README.md`.

---

## 11. Phân công và phối hợp hai máy (bản điều chỉnh từ đề xuất chia 50/50)

### 11.1. Đánh giá bản đề xuất chia hai nhánh

Bản đề xuất đúng ở bốn điểm và giữ lại: chia theo nhánh kỹ thuật thay vì mỗi người ba mục; chốt giao diện chung trước khi viết riêng;
làm song song trên dữ liệu nhỏ; một máy chạy lượt cuối. Danh sách "điểm cần tránh" cũng đúng và giữ nguyên ở 11.7.

Có năm chỗ cần sửa:

| # | Vấn đề | Vì sao | Điều chỉnh |
|---|---|---|---|
| 1 | Chưa đều: Phong có đặc trưng, lấy mẫu âm, tiền xử lý, LR/RF, bộ đánh giá, bootstrap, importance, ví dụ giỏ, **cộng hợp nhất QMD**, và viết 4.1, phần LR/RF 4.3, phần chất lượng 4.4, 4.5, 4.6 (khoảng 6,5/9 trang). Vương viết 4.2 và hai phần nhỏ (khoảng 2,5 trang) | Lệch khoảng 60/40 về phía Phong | Chuyển đặc trưng và lấy mẫu âm sang Vương; chuyển mục 4.1 sang Vương |
| 2 | Bộ đánh giá xếp hạng đặt ở Phong, nhưng **Vương là người dùng nó đầu tiên** (chọn danh mục và luật trên validation, bước 3) | Vương phải chờ Phong; nếu không chờ thì Vương dễ tự viết một bộ Recall thứ hai, đúng điều bản đề xuất muốn tránh | Bộ chỉ số xếp hạng (Precision/Recall/HitRate@K, Recall trần, độ phủ) về Vương, vì nó gắn chặt với định nghĩa O, H, C do Vương giữ. Phong giữ chỉ số phân loại, bootstrap và **tự cài lại độc lập** Recall@10 trên 50 giỏ để kiểm tra chéo |
| 3 | Đặc trưng luật (số luật khớp, max confidence, max lift) ở Phong, xếp hạng bằng luật ở Vương | Hai nơi cùng viết phép khớp "tiền đề ⊆ O"; khác một chi tiết là đặc trưng và phương pháp Rules không còn cùng định nghĩa | Một hàm khớp luật duy nhất (Vương) trả về ba thống kê luật cho mỗi cặp (giỏ, ứng viên); Rules và đặc trưng cùng dùng |
| 4 | Không nói máy nào chạy lượt chính thức | Benchmark khai phá và test phải chạy cùng một máy; máy Phong theo QMD mục 2.5 là Python 3.12.10, khác 3.12.14 của `.venv-m2` | Mọi lượt chính thức (validation đầy đủ, benchmark, test) chạy trên **máy Vương**; máy Phong dùng để phát triển và chạy mẫu nhỏ |
| 5 | Không nói ai sở hữu tệp code | CLAUDE.md và THONG_NHAT quy định `scripts/`, `tests/`, `configs/` chỉ Vương ghi; Phong viết code Chương 4 thì phải có ngoại lệ rõ | Mỗi tệp có đúng một chủ (11.3). Phong là chủ các tệp classifier/diễn giải; Vương chỉ chép nguyên vào bài khi nhận gói, không sửa |

### 11.2. Phân công sau điều chỉnh

| Người | Code | Viết (trang dự kiến) |
|---|---|---|
| **Vương** | Dựng giỏ fit/validation/test từ Master + split; phép che cố định; danh mục C; sinh ứng viên C_j; khai phá Apriori/FP-Growth; **hàm khớp luật**; Popularity và Rules; **7 đặc trưng và lấy mẫu âm**; **bộ chỉ số xếp hạng**; chọn danh mục/luật trên validation (giai đoạn A); benchmark khai phá; giữ `configs/m4_model.json`; chạy các lượt chính thức | **4.1** (đặc trưng, lý do giữ/loại, tương quan; phép bỏ nhóm lấy số từ Phong) 1,5; **4.2** 1; **4.3.1** khai phá + benchmark 1 → khoảng **3,5 trang** |
| **Phong** | `Pipeline`/`ColumnTransformer`; LR/RF và lưới giai đoạn B; ngưỡng F1; phép bỏ nhóm đặc trưng; chỉ số phân loại (Accuracy, Precision, Recall, F1, ROC-AUC, AP, ma trận nhầm lẫn); bootstrap ghép cặp; permutation importance, hệ số LR, ví dụ giỏ; hai hình Chương 4 | **4.3.2** LR/RF 1; **4.4** 2; **4.5** 1,5; **4.6** 1 → khoảng **5,5 trang**, cộng hợp nhất QMD |
| **Cùng làm** | Giai đoạn C (chọn phương pháp chính), duyệt `lock.json`, đọc kết quả test | Đọc chéo toàn chương |

Khối lượng: Vương nhiều code nền hơn (dữ liệu, luật, đặc trưng, chỉ số, chạy chính thức); Phong nhiều phần viết hơn và hợp nhất bài.
Như vậy gần 50/50 hơn bản đề xuất, vì phần nặng nhất về code (đặc trưng trên toàn bộ ứng viên) và phần nặng nhất về viết (4.4–4.6) không dồn vào cùng một người.

### 11.3. Chủ sở hữu tệp

| Tệp | Chủ | Người kia được làm |
|---|---|---|
| `scripts/m4_common.py` (che giỏ, C_j, khớp luật, đặc trưng, xếp hạng, chỉ số xếp hạng) | Vương | Đọc, gửi đề xuất sửa |
| `scripts/m4_mining.py`, `scripts/m4_benchmark_mining.py` | Vương | Đọc |
| `scripts/m4_prepare.py` (giỏ, che, đặc trưng, lấy mẫu âm, giai đoạn A) | Vương | Đọc |
| `configs/m4_model.json` | Vương | Gửi giá trị lưới giai đoạn B để Vương ghi vào |
| `scripts/m4_classifier.py` (Pipeline, giai đoạn B, ngưỡng F1, phép bỏ nhóm) | Phong | Chạy lượt chính thức, không sửa |
| `scripts/m4_test.py` (chấm test sau khóa, chỉ số phân loại, bootstrap) | Phong | Chạy lượt chính thức, không sửa |
| `scripts/m4_interpret.py` (importance, hệ số, ví dụ, hình) | Phong | Chạy lượt chính thức, không sửa |
| `scripts/m4_lock.py` (giai đoạn C, ghi `lock.json`) | Vương | Cùng duyệt nội dung `lock.json` |
| `tests/test_m4_data.py` (kiểm thử 1–5, 8 ở mục 7) | Vương | Chạy |
| `tests/test_m4_model.py` (kiểm thử 6, 7, 9 ở mục 7) | Phong | Chạy |

Đây là ngoại lệ có chủ đích với quy tắc "chỉ Vương ghi `scripts/`": cần ghi vào THONG_NHAT khi hai bạn chốt.
Mục 6 đã cập nhật theo bảng này (một tệp gộp trước đây được tách thành `m4_prepare.py`, `m4_classifier.py`, `m4_lock.py` để mỗi tệp một chủ).

### 11.4. Giao diện chung (chốt ở bước 1, không đổi sau đó nếu không có thỏa thuận)

Tất cả Parquet nằm trong `DATA/Data phai sinh/M4/`, ghi kèm `hashes.json`. Kiểu theo từng cột (đúng các tệp đã tạo ngày 01/11): `order_id`, `user_id`, `catalog.product_id` là `int32`; `department_id` là `int8`; `basket_size`, `n_ref`, `rank`, các cột đếm và `consequent` là `int64`; `observed`, `hidden`, `antecedent` là danh sách `int64` đã sắp tăng; chỉ số và `popularity` là `float64`.
`hashes.json` của M4 ghi thêm tham số che (`mask`), hash phân hoạch G0 và lưới A; mọi bước sau gọi `check_mask()` trước khi dùng phép che.

| Bảng | Cột | Ghi chú |
|---|---|---|
| `masked_baskets.parquet` | `order_id`, `user_id`, `split` (fit/validation/test), `basket_size`, `observed` (list), `hidden` (list), `eligible` (bool, k ≥ 2) | Giỏ một sản phẩm có `eligible=False`, `hidden` rỗng |
| `catalog.parquet` | `product_id`, `n_ref`, `department_id`, `popularity`, `rank` | Mọi sản phẩm reference; C với Top-N là `rank <= N`; `rank` từ 1 |
| `rules_grid.parquet` | `antecedent` (list), `consequent`, `n_antecedent`, `n_both`, `support`, `confidence`, `lift`, `leverage`, `conviction`, `top_n`, `min_count`, `max_len` | Hậu đề một sản phẩm; confidence ≥ 0,05 (ngưỡng thấp nhất lưới); `conviction` vô hạn ghi `inf` |
| `features_fit.parquet` | `order_id`, `product_id`, `y`, 7 đặc trưng đúng tên mục 3.1 | Đã lấy mẫu âm; `feature_schema.json` đi kèm |
| Đặc trưng validation/test | Không lưu toàn bộ; hàm `iter_features(split, batch_size)` trong `m4_common.py` sinh theo lô | Tránh tệp hàng chục triệu dòng |
| `rankings_<split>.parquet` | `order_id`, `method`, `rank` (1–10), `product_id`, `score` | Chỉ lưu Top-10 mỗi giỏ mỗi phương pháp |
| `basket_metrics_<split>.csv` | `order_id`, `user_id`, `method`, `n_hidden`, `n_hidden_in_C`, `hits@5`, `hits@10`, `P@5`, `R@5`, `P@10`, `R@10`, `HR@10`, `R@10_ceiling` | Đầu vào của bootstrap; Phong không tính lại chỉ số chính thức |

Quy tắc chung ghi trong `configs/m4_model.json`: seed (che 42, âm 43, mẫu importance 44, bootstrap 42), K = 5 và 10, phá hòa `product_id` tăng,
Precision chia K, Recall chia |H| kể cả ngoài C, giỏ C_j rỗng vẫn tính, dung sai hòa 0,002, 20 âm/giỏ, `batch_size` 2.000 giỏ, `pilot_baskets` 2.000.

### 11.5. Thứ tự làm và điểm bàn giao

Không ghi ngày; mỗi bước xong khi đạt điều kiện ở cột cuối.

| Bước | Vương | Phong | Xong khi |
|---|---|---|---|
| 0. Chuẩn bị | Gửi `requirements.txt` mới | Cài đúng phiên bản bằng uv; chạy `check_hashes()` của G0 và unittest trên máy Phong | Máy Phong báo G0 khớp hash, 30/30 test đạt |
| 1. Chốt giao diện | Viết `configs/m4_model.json` và khung `m4_common.py` có chữ ký hàm, docstring, chưa cần thân hàm | Duyệt bảng 11.4; gửi lưới giai đoạn B | Hai bạn ghi "đã chốt giao diện" vào THONG_NHAT |
| 2. Song song trên dữ liệu nhỏ | Viết che giỏ, C_j, khai phá, khớp luật, đặc trưng, chỉ số xếp hạng; chạy `pilot_baskets=2000`; gửi **gói pilot** (bảng 11.4 trên mẫu nhỏ + code) | Viết Pipeline, LR/RF, chỉ số phân loại, bootstrap, importance trên dữ liệu tự tạo; khi nhận gói pilot thì chạy thử thật | Phong chạy được toàn luồng của mình trên gói pilot; `test_m4_data.py` và `test_m4_model.py` đạt |
| 3. Giai đoạn A | Chạy 24 cấu hình luật trên validation đầy đủ; chọn theo quy tắc mục 4.1; chạy benchmark; gửi **gói A** (catalog, rules, features_fit, masked_baskets, kết quả lưới) | Kiểm tra chéo: tự tính Recall@10 của Rules trên 50 giỏ validation, so với `basket_metrics_validation.csv` | Số Phong tính khớp; danh mục và luật cố định |
| 4. Giai đoạn B | Chạy `m4_classifier.py` của Phong trên máy Vương ở cấu hình chính thức, gửi lại kết quả | Gửi code cuối; đọc kết quả lưới B, chọn LR/RF, ngưỡng F1; chạy phép bỏ nhóm | Có cấu hình B và hai Pipeline đã lưu |
| 5. Khóa | Chạy `m4_lock.py` (giai đoạn C) | Duyệt `lock.json` | Cả hai đồng ý `lock.json`; không sửa code/config sau đó |
| 6. Test | Chạy `m4_test.py` và `m4_interpret.py` một lần trên máy Vương; gửi **gói kết quả** | Đọc kết quả; đối chiếu ngẫu nhiên 10 số giữa CSV và bảng | Có Bảng 4.3–4.5, Hình 4.1–4.2 |
| 7. Viết | Viết 4.1, 4.2, 4.3.1 kèm bảng nguồn, gửi Phong | Viết 4.3.2, 4.4–4.6; hợp nhất QMD; render | Chương 4 ≤ 9 trang, không còn ô chờ; Vương đọc chéo 4.4–4.6, Phong đọc chéo 4.1–4.3.1 |

Lúc chờ nhau: ở bước 2 Phong không phải chờ nhờ dữ liệu tự tạo; ở bước 3 Phong viết khung lời văn 4.3.2–4.5 và hình mẫu; ở bước 4 Vương viết 4.1–4.2.

### 11.6. Gói trao đổi

Theo cách đã dùng cho `m1_inspect_artifact.py` và gói Chương 3:
- Tên `GUI_<người gửi>_ch4_<bước>_<yyyymmdd>.zip`, đặt trong `Chung/Gửi và nhận/Gửi/`.
- Giữ đúng cấu trúc thư mục bài; kèm `README_GUI_*.md` (đã làm gì, lệnh chạy, cần người nhận làm gì) và `DANH_SACH.txt` (đường dẫn, SHA-256, mô tả).
- Chỉ gửi code, config và đầu ra mới. Không gửi Master, Parquet G0, môi trường ảo, `__pycache__`.
- Người nhận kiểm SHA-256, chạy unittest, rồi mới chép vào bài; không sửa tệp không thuộc mình, có sai thì gửi đề xuất.

### 11.7. Điểm cần tránh (giữ từ bản đề xuất, bổ sung)

- Không tạo hai phép chia tập, hai phép che, hai bộ tính Recall hay hai hàm khớp luật.
- Không dùng `basket_summary.parquet` (kích thước giỏ đầy đủ, và chỉ có giỏ reference) làm đặc trưng; `observed_basket_size` tính từ `observed`.
- Không lấy mẫu âm trên validation/test rồi coi là đánh giá đầy đủ.
- Không tính đặc trưng, điểm hay chỉ số trên test ngoài `m4_test.py`. Ngoại lệ duy nhất: `m4_prepare.py` che giỏ test cùng lúc với fit/validation bằng cùng hàm (chỉ dùng seed và `order_id`, không xem kết quả).
- Không sửa code, config hay mô hình sau khi đã xem kết quả test.
- Kết quả chạy trên máy Phong chỉ dùng để phát triển; số đưa vào bài lấy từ lượt chạy chính thức trên máy Vương.
- Mỗi lượt chạy chính thức ghi phiên bản thư viện và hash đầu vào, theo cách `hashes.json` của Chương 3.
