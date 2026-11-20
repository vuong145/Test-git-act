# Hướng dẫn hoàn thiện Chương 5 và xử lý `m4_validate.py`

Ngày lập: 04/11/2026. Căn cứ: gói "Gửi Vương_Chương 5 và rà soát Chương 4_20261104" của Phong (kiểm SHA-256 đủ 14 tệp, khớp), đối chiếu với CSV/JSON nguồn trong `BAO CAO/`, `chuong5.qmd` và `thay_doi_qmd.diff`. Tài liệu này chỉ hướng dẫn, chưa sửa tệp nào của bài.

## 0. Nguyên tắc chung (cả hai bạn)

- Không chạy lại `m4_test.py test`, không sửa bảy tệp trong khóa (`m4_test.py`, `m4_common.py`, `m4_classifier.py`, `project_io.py`, `requirements.txt`, `configs/m2_plot_style.json`, `configs/m4_model.json`).
- Mọi con số trong lời văn chép từ CSV/JSON nguồn. Số tính thêm (tỷ số, phần trăm tương đối) phải ghi công thức trong lời văn.
- Giữ chữ 12 pt, không thu chữ hay lề. Việc cắt trang làm sau, khi nội dung đã chốt.
- Không thêm tài liệu tham khảo chưa kiểm chứng. Mỗi mục thêm vào `references.bib` phải mở được nguồn thật và ghi đúng tác giả, năm, nơi xuất bản.
- Chủ tệp: Phong giữ QMD chính và `references.bib`; Vương giữ `scripts/`, `tests/`, `configs/`. Cần sửa tệp của người kia thì gửi đề xuất.

## Phần A. Dành cho Phong: hoàn thiện Chương 5

Vị trí dòng tính theo `chuong5.qmd` trong gói đã gửi (62 dòng). Sửa trong QMD chính rồi cập nhật lại `chuong5.qmd` nếu vẫn giữ bản tách riêng.

### A1. Sáu chỗ phải sửa

**1. Dòng 50 (Giới hạn mô hình): câu "Cấu hình luật được chọn nằm ở cạnh dưới của lưới".**
- Vấn đề: cấu hình chọn là N = 1.000, tối thiểu 20 giỏ, độ dài 2, confidence 0,05. Lưới N là {500; 1.000; 2.000} nên 1.000 là giá trị giữa. Ba tham số còn lại mới nằm ở giá trị thấp nhất.
- Đề xuất viết: "Ba trong bốn tham số của cấu hình luật được chọn (tối thiểu 20 giỏ, độ dài tối đa 2, confidence tối thiểu 0,05) nằm ở giá trị thấp nhất của lưới, còn quy mô danh mục 1.000 nằm ở giữa; nghiên cứu không chứng minh tối ưu ngoài phạm vi đã khảo sát."
- Nguồn kiểm: `validation_grid_A.csv`, `lock.json`, mục 4.3.

**2. Dòng 12 (bảng khuyến nghị) và dòng 21 (đoạn I5): khuyến nghị thử cả ba cặp ngành.**
- Vấn đề: I5 ở Chương 3 nói lift của H1, H2, H3 là 1,229; 1,412; 1,190, ở phân vị 51; 80; 39 của 210 cặp. H3 thấp hơn trung vị 1,225. I5 chỉ nói H2 "nổi hơn tương đối". Chương 5 lại để "thử" cả ba cặp.
- Cách sửa: trong bảng, đổi hàng này thành "Ưu tiên thử cặp dry goods pasta–pantry (lift 1,412, phân vị 80); hai cặp còn lại ở mức trung bình hoặc dưới trung vị nên chỉ thử khi có lý do kinh doanh riêng". Trong đoạn dưới bảng, thêm phân vị 51; 80; 39 để người đọc thấy H3 dưới trung vị.
- Giữ câu "không chọn cặp chỉ vì lift lớn hơn 1" và V từ 0,152 đến 0,201 (đúng nguồn).

**3. Dòng 9 (bảng) và dòng 19 (đoạn sau bảng): "có ý nghĩa thống kê" cho RF so với Rules.**
- Vấn đề: mục 2.4 quy định phép so sánh xác nhận chỉ dành cho phương pháp chính với Popularity. RF so với Rules và LR so với RF là so sánh bổ trợ, không hiệu chỉnh đa so sánh. Chương 5 dùng nó như căn cứ chính cho khuyến nghị.
- Cách sửa: ghi rõ "so sánh bổ trợ" ở dòng 9, và đổi dòng 19 thành "Chênh lệch RF so với Rules (so sánh bổ trợ, chưa hiệu chỉnh đa so sánh) có khoảng tin cậy không chứa 0 nhưng nhỏ về độ lớn". Căn cứ chính cho RF là chênh lệch với Popularity.

**4. Toàn chương: chưa có trích dẫn tài liệu nào.**
- Thêm tối thiểu hai nguồn đã kiểm chứng: một cho thử nghiệm A/B trực tuyến (ví dụ Kohavi, Tang và Xu, 2020, sách *Trustworthy Online Controlled Experiments*, Cambridge University Press; phải kiểm lại thông tin trước khi đưa vào), một cho công bằng hoặc đa dạng trong hệ gợi ý.
- Đặt trích dẫn ở Bước 3 của lộ trình (chọn chỉ tiêu chính, cỡ mẫu, quy tắc dừng) và ở đoạn "Đạo đức và trách nhiệm" (dòng 52). Nếu không kiểm chứng được nguồn, nói rõ trong báo cáo gửi lại là chưa thêm.

**5. Dòng 52 (Đạo đức và trách nhiệm): phần bảo mật còn chung.**
- Barem trụ cột IV yêu cầu đạo đức AI và bảo mật. Hiện chỉ có "tối thiểu hóa dữ liệu, giới hạn truy cập và thời gian lưu".
- Bổ sung cụ thể: ai được truy cập mã người dùng đã giả danh; tách bảng khóa giả danh khỏi bảng giỏ; ghi nhật ký truy cập; không đưa dữ liệu giỏ chưa ẩn danh vào môi trường thử nghiệm; cơ chế người dùng từ chối gợi ý và xóa dữ liệu theo yêu cầu. Chỉ viết những điều nhóm sẽ làm thật, đừng cam kết điều không kiểm soát được.

**6. Dòng 9 (bảng khuyến nghị): chi phí của RF chỉ nằm ở đoạn dưới.**
- Ở cột "Điều kiện áp dụng" của hàng RF so với Rules, ghi thêm "RF chậm hơn Rules khoảng 10,3 lần khi chấm theo lô trên validation (63,55 giây so với 6,19 giây)". Hai số này đã đúng nguồn (`validation_methods.csv`).

### A2. Hai chỗ nên chỉnh nhẹ

- **Kết luận câu hỏi 4 (dòng 60 trở đi):** thêm "so sánh RF với Rules là bổ trợ" cho đồng nhất với mục 2.4.
- **Tóm tắt:** nếu sau khi sửa A1 mà số hoặc ý đổi thì đếm lại từ. Hiện 297 từ, khung cho phép 250–350. Tóm tắt hiện không nhắc mức bổ trợ của so sánh RF–Rules; thêm nửa câu nếu còn chỗ.

### A3. Không đổi (đã kiểm đúng nguồn)

| Nội dung | Giá trị | Nguồn |
|---|---|---|
| Recall@10 test: RF, Popularity, Rules, LR | 0,0971; 0,0755; 0,0924; 0,0910 | `ranking_metrics_test.csv` |
| RF hơn Popularity (khoảng tin cậy 95%) | 0,0216 [0,0192; 0,0239] | `paired_bootstrap_test.csv` |
| RF hơn Rules (khoảng tin cậy 95%) | 0,0047 [0,0031; 0,0063] | `paired_bootstrap_test.csv` |
| HR@10 của RF; trần Recall@10 | 17,08%; 0,5198 | `ranking_metrics_test.csv` |
| Giỏ validation có luật khớp | 88,38% (21.966/24.854) | `rule_coverage.json` |
| Giỏ test không có sản phẩm che trong danh mục | 8.449 | `basket_metrics_test.csv` |
| Phủ giỏ reference: produce; dairy eggs | 73,95%; 66,76% | `department_summary.csv` |
| Cramér's V ba cặp; lift ba cặp; trung vị lift; số cặp lift > 1 | 0,152 đến 0,201; 1,229, 1,412, 1,190; 1,225; 182/210 | `hypotheses.csv`, `lift_baseline.csv` |
| Thời gian suy luận validation: RF; Rules | 63,55 giây; 6,19 giây (10,3 lần) | `validation_methods.csv` |
| RF bỏ ba biến luật (validation) | 0,0971 xuống 0,0788 | `ablation.csv` |
| FP-Growth nhanh hơn Apriori | khoảng 4,1 và 14,3 lần | `mining_benchmark_*.csv` |

### A4. Gộp lại các sửa Chương 1–3 của Vương (bắt buộc trước khi coi QMD là bản chính)

QMD trong gói của Phong dùng bản Chương 1–3 cũ nên đang hoàn lại các sửa ngày 04/11. Xem `khac_biet_chuong1_3_voi_vuong.diff` (66 dòng). Cần gộp ba chỗ:

1. **Mục 2.5:** đổi thành "mọi lượt chạy chính thức dùng cùng môi trường `.venv-m2` trên một máy" (Python 3.12.14, pandas 3.0.1, NumPy 2.3.5, PyArrow 26.0.0, SciPy 1.16.3).
2. **Mục 3.2:** bỏ câu hai vị trí xuất bản và câu "hai bản xuất bản giống nhau"; lượt chạy ngày 04/11 ghi `PASSED`, Master 16.992.331 byte, 13 tiêu chí đạt, nội dung giống bản 20/10 từng ô.
3. **Bảng 3.5 và lời phân tích:** thay bằng số của lượt benchmark ngày 04/11. Không chép số từ diff; mở `DATA/Data đã làm sạch/Bảng master TLCK/data_benchmark.csv` và chép từng ô. Sau khi chép, kiểm lại các tỷ số trong lời văn (ghi nhanh hơn 9,60 lần, đọc nhanh hơn 29,59 lần, tái sử dụng Master nhanh hơn 45,99 lần, giảm RAM 88,16%, nén 7,75 lần là các số lượt 04/11; đối chiếu lại với CSV).

Ghép bằng cách áp diff vào QMD của Phong, không chép đè cả tệp vì QMD chính còn các sửa tám điểm và Chương 5.

### A5. Kiểm tra sau khi sửa

- Render toàn bài, kiểm `??` bằng 0, không thiếu tham chiếu, không thiếu hình.
- Mỗi người đối chiếu 10 số ngẫu nhiên của phần mình viết với CSV nguồn.
- Chương 5 vẫn trả lời đủ năm câu hỏi nghiên cứu ở mục 1.2 và có hai bảng (khuyến nghị, KPI), lộ trình bốn bước, đạo đức, hạn chế.
- Gửi lại Vương theo thư mục không nén, kèm `SHA256.txt` và một báo cáo ngắn liệt kê từng chỗ đã sửa theo A1.

### A6. Nhật ký của Phong (để hai nhật ký khớp nhau)

1. Ghi phiên 04/11 sau 16:09: nhận khóa chính thức, test đã chạy, nhận QMD có Chương 4, rà Chương 4, viết Chương 5 và Tóm tắt, sửa tám điểm, gói "Chương 5 và rà soát Chương 4".
2. Phiên 30/10 (14:37–18:15): dòng nhắc việc nhận gói 3.4 lúc 20:54:26 nằm ngoài khung giờ; sửa giờ hoặc tách sang phiên khác.
3. Phiên 29/10: nêu rõ mục 3.3 đã được Vương tích hợp vào QMD từ 26/10 (năm điểm sửa trùng với bản của Vương) và bản mục 3.1 có sơ đồ Mermaid hiện không còn trong QMD. Dòng 238 "chờ tích hợp mục 3.3" cần sửa theo thực tế.
4. Ghi phiên phản biện kỹ thuật về `render_pdf.py` trước 29/10 (nhật ký Vương nhắc nhưng nhật ký Phong không có).
5. Liên kết trong nhật ký Phong đều là đường dẫn máy Phong (`output/`, `drafts/`, `Gửi và Nhận/`, `Tài liệu/`); khi nộp phải có các thư mục này hoặc đổi đường dẫn.

## Phần B. Dành cho Vương

### B1. `scripts/m4_validate.py`: sửa chú thích "test không được đọc/nạp"

**Sự thật kỹ thuật.**
- Dòng 82: `masked = pd.read_parquet(data / "masked_baskets.parquet")` nạp cả tệp, gồm giỏ test.
- Dòng 84: `masked = masked[masked.eligible & masked.split.isin(["fit", "validation"])]` loại test ngay sau đó.
- Từ dòng 84 trở đi mọi bước (đặc trưng, lấy mẫu âm, chọn cấu hình, ngưỡng F1, bỏ nhóm đặc trưng) chỉ thấy fit và validation. Không có chỗ nào dùng test để chọn. Kết quả validation đã khớp từng byte giữa hai lượt chạy nên không cần chạy lại.
- Vấn đề chỉ là lời nói: ba chỗ ghi "test không được đọc/nạp" là chưa đúng nếu hiểu chặt (test đã nằm trong bộ nhớ trong một dòng lệnh).

**Các chỗ cần sửa (chỉ đổi chữ, không đổi logic).**

| Dòng | Hiện tại | Đề xuất |
|---|---|---|
| 1 | `... trên validation; test không được đọc.` | `... trên validation; giỏ test bị loại ngay sau khi đọc và không tham gia chọn cấu hình.` |
| 9 | `chọn cấu hình bằng VALIDATION, test không được đọc.` | `chọn cấu hình bằng VALIDATION; tệp giỏ che có cả test nhưng bị loại ở dòng lọc đầu tiên, không dùng để chọn.` |
| 83 | `# Khối 1: nạp giỏ fit/validation (test không được nạp).` | `# Khối 1: đọc tệp giỏ che (có cả test), giữ ngay fit/validation.` |
| 84 | `... # test không được nạp` | `... # giỏ test bị loại tại đây` |

**Sau khi sửa.**
1. Chạy `.\.venv-m2\Scripts\python.exe -m py_compile scripts/m4_validate.py` và bộ unittest (`python -m unittest discover -s tests -p "test_*.py"`). Không cần chạy lại `m4_validate.py`.
2. Ghi vào nhật ký: tệp thay đổi, chỉ đổi chú thích và docstring, tệp không nằm trong bảy tệp khóa, `lock.json` và hash khóa không đổi. Xác nhận bằng cách kiểm lại 16 hash của khóa (Phong có `kiem_lock.py`).
3. Gửi tệp mới cho Phong theo thư mục không nén kèm `DANH_SACH.txt`. Từ đó `m4_validate.py` ở máy Phong khác byte với bản cũ; Phong ghi trong báo cáo là "9/11 giống byte" sẽ thành khác ở tệp này, nên báo trước để Phong không tưởng sai.
4. Cập nhật `scripts/README.md` và phần mô tả trong `CODE_CHUONG4` nếu có nhắc câu "test không được đọc" cho tệp này.

**Không nên làm.** Đừng đổi sang đọc có bộ lọc (`filters=[("split","in",[...])]`) cho tệp này nếu chưa chạy lại validation. Đó là đổi mã sau khi kết quả đã chốt; hai lượt validation giống từng byte chỉ chứng minh cho mã hiện tại.

**Các tệp khác có chú thích tương tự, không cần sửa.**
- `m4_common.py` (dòng 11 và 228): `locked_stage` đọc Parquet có `filters=[("split","in",...)]` ở dòng 234, nên fit/validation mới được nạp. Đúng và nằm trong khóa.
- `m4_report.py` (dòng 3 và 6): gọi `locked_stage`, nên đúng.

**Câu trả lời mẫu cho vấn đáp.** "Tệp giỏ che chứa cả bốn tập, em đọc vào rồi lọc ngay ở dòng 84 chỉ giữ fit và validation. Từ đó mọi bước chọn cấu hình chỉ thấy hai tập này. Lúc chấm test, `m4_test.py` mở khóa riêng, kiểm hash và tạo dấu chạy một lần." Nếu hội đồng hỏi vì sao không lọc lúc đọc: "Ở `locked_stage` em có lọc lúc đọc; ở `m4_validate.py` em lọc ngay sau khi đọc. Kết quả giống nhau vì test không đi vào bước nào của chọn cấu hình, và hai lượt chạy giống từng byte."

### B2. Việc khác của Vương liên quan đến gói của Phong

1. Trả lời Phong về hai điều sau: bạn xác nhận Vương sẽ sửa chú thích `m4_validate.py` (B1); Phong gộp Chương 1–3 theo A4.
2. Khi nhận bản chính của Phong: kiểm hash theo `SHA256.txt`, so QMD mới với QMD hiện tại để chắc ba chỗ ở A4 đã gộp và Chương 4 không bị đổi ngoài hai diễn giải ở 4.5–4.6.
3. Đọc lại hai diễn giải Phong hạ mức ở 4.5–4.6 (hệ số ngành không còn "so với nhóm chuẩn"; câu validation/test không loại trừ quá khớp) và xác nhận bạn đồng ý, vì đó là văn của bạn.

### B3. Nhật ký của Vương

1. Dòng 360 (phiên 29/10): đang viết 45 trang là "mục tiêu điều hành nội bộ, không phải trần cứng"; CLAUDE.md ghi giảng viên đã xác nhận tối đa 45 trang từ bìa đến hết Chương 5. Sửa cho thống nhất với quy định đã xác nhận.
2. Dòng 398–399 (phiên 26/10 tối): có ký tự xuống dòng chen vào chữ `\resizebox` (hiện thành "esizebox" ở dòng sau). Sửa lại.
3. Ghi phiên mới: nhận gói Chương 5 và rà soát Chương 4 của Phong, kết quả kiểm hash và đối chiếu số, quyết định về `m4_validate.py`.
4. Kiểm lại liên kết sống sau khi sửa (hiện 63/63 sống), sao lưu bản trước.

## Thứ tự làm đề xuất

1. Vương: sửa chú thích `m4_validate.py`, chạy kiểm tra B1, gửi Phong tệp mới.
2. Phong: A4 trước (gộp Chương 1–3), rồi A1 đến A3.
3. Phong gửi lại gói theo A5.
4. Cả hai: cập nhật nhật ký (A6 và B3).
5. Sau khi nội dung Chương 4 và 5 chốt: cắt Chương 3 và Chương 1–2 cho tổng không quá 45 trang.
