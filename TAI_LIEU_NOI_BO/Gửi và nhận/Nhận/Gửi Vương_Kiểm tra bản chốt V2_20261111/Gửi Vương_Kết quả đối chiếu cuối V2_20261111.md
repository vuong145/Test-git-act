# Kết quả đối chiếu cuối gói V2 trên máy Phong — 11/11/2026

**Kết luận:** Có thể chốt phần nội dung QMD/PDF V2 qua các kiểm tra dưới đây. Chưa có cơ sở xác nhận toàn bộ workspace Phong trùng 380/380 tệp bản nộp Vương. Hai kết luận này cần được tách riêng. Không phát hiện lỗi mới buộc làm lại dữ liệu, chạy lại benchmark, huấn luyện hay chấm test.

Đây là báo cáo rà soát, không phải biên bản Phong đã tự tay phê duyệt. Chưa chép V2 đè lên dự án, chưa sửa QMD/bib/mã khóa, chưa ghi nhật ký cá nhân. Không chạy lại cleaning, dựng Master, pipeline nghiên cứu hoặc `m4_test.py test`. Kiểm thử chạy trên bản sao riêng bằng dữ liệu fixture.

## 1. Đúng phiên bản đã kiểm tra

Gói nhận: `Gửi và Nhận/Nhận/GUI_PHONG_DOI_CHIEU_TOAN_BO_V2_20261111/`.

| Tệp trong `01_BAI_TIEU_LUAN/` | SHA-256, 16 ký tự đầu |
|---|---|
| 2521001118_Nhom01_TieuLuan.qmd | 79cf06b0bb10a865 |
| 2521001118_Nhom01_TieuLuan.pdf | 1807db1ab1e9169a |
| references.bib | 8c7864f78491c957 |
| nhật ký làm việc.md | f581f5aa1a471d83 |
| toàn bộ mã nguồn.md | d51bde398363e498 |

Đã đọc README, bản đánh giá, các diff; đối chiếu QMD và bib với bản đang ở gốc máy Phong; đọc mã thay đổi, cấu hình, test, tài liệu tổng hợp mã và nhật ký đi kèm. Không có `CLAUDE.md` ngay tại gốc workspace Phong. Nhật ký trong gói xác định người nộp là **Vương**, không dùng thay nhật ký nộp riêng của Phong.

## 2. Kết quả kiểm tra trực tiếp

| Hạng mục | Kết quả và giới hạn |
|---|---|
| Tính toàn vẹn gói nhận | **72/72** tệp trong `DANH_SACH.txt` khớp SHA-256 và dung lượng. |
| Các tệp bản nộp được gửi thực tế | **64/64** tệp QMD/PDF/bib/nhật ký/mã/cấu hình/test/style/assets khớp manifest 380 tệp. Các tài liệu hướng dẫn, diff và manifest là phần ngoài 64 tệp này. |
| Bảng số trong bài | Các dòng bảng Markdown và các khối bảng LaTeX không đổi so với QMD cũ tại gốc. Đối chiếu thêm nguồn gốc ở mục 5, không chỉ dựa vào diff. |
| Trích dẫn | **22 khóa duy nhất**, cả 22 đều được dùng; không thấy trích dẫn thiếu mục bib hoặc mục bib thừa. Các `@10`, `@5`, `@K` trong tên chỉ số không phải khóa tài liệu. |
| Tham chiếu nội bộ | Các tham chiếu `fig-/tbl-/sec-/eq-` có nhãn đích trong QMD; PDF không có `??`; không thấy ô TODO/TBD/FIXME trong QMD. |
| Tài nguyên hình | Đủ **8/8 PDF hình** được gọi trong QMD; có logo và `styles/apa.csl`. Đường dẫn tương đối đúng khi ghép `01_BAI_TIEU_LUAN` với `02_MA_NGUON` vào cùng thư mục bài như cấu trúc nộp. Không render trực tiếp từ cấu trúc gói nhận bị tách hai tầng. |
| PDF | **44 trang vật lý**; Chương 4 ở trang 30–37, Chương 5 ở 38–42, tài liệu tham khảo 43–44. Bìa đến hết Chương 5 **42 trang**, đạt giới hạn 45. |
| QMD và PDF | Các sửa đổi cuối về biến y, CRISP-DM, mẫu Li, Holm, bootstrap, permutation importance và tài liệu tham khảo đều hiện trong PDF. Hình 3.2 thể hiện 1.000/2.000. Đã trích văn bản toàn PDF và xem các trang thay đổi/cuối bài. Không tự render lại nên không tuyên bố tái tạo được PDF giống từng byte. |
| Tệp gom mã | **48/48 phần** khớp từng dòng với tệp nguồn tương ứng sau khi bỏ cột số dòng; tiền tố hash cũng khớp. |
| Môi trường kiểm thử | **23/23** phiên bản thư viện cài trong `.venv-m2` khớp `requirements.txt`. Python thực tế máy Phong **3.12.10**, không phải 3.12.14 ghi trong hồ sơ máy Vương. |
| Unittest V2 trên máy Phong | **57/57 đạt**, `Ran 57 tests in 5.700s`, `OK`. Dùng đúng 11 tệp test trong gói, không cộng test kiểm chéo riêng của Phong. |
| Khóa thực nghiệm | Tìm được khóa chính thức `e38b04f22b66438a7…` trong gói kết quả 04/11. **16/16** tệp khóa khớp hash khi lấy đúng bằng chứng đã nhận; approvals Phong/Vuong đều true; `results_test.json` trỏ đúng khóa này. |
| Hash nền | Manifest G0/common: **6/6** khớp; manifest M4: **6/6** khớp. Kiểm độc lập bằng SHA-256, không chạy pipeline. |
| Hash ban2 | Bộ ban2 hiện tại tại gốc tự khớp **10/10 theo manifest cũ của chính nó**, nhưng `ban2/hashes.json` khác manifest V2. Vì V2 không gửi CSV/JSON đó, **chưa xác minh 10/10 của V2**. Không dùng kết quả của bộ cũ để xác nhận bộ mới. |

Lần thử unittest đầu gặp ba lỗi quyền truy cập thư mục tạm của môi trường chạy. Đổi TEMP/TMP sang thư mục kiểm tra trong workspace rồi chạy lại nguyên bộ, đạt 57/57; không sửa mã hoặc test. Log thành công được gửi riêng. Kết quả này xác nhận unit test, không phải chạy lại nghiên cứu.

## 3. Các thay đổi cuối có thể chấp nhận về nội dung

Số dòng dưới đây thuộc QMD V2 `79cf06b0`.

| Vị trí | Nhận xét |
|---|---|
| 1.4, dòng 250 | Đổi `purchase_label` thành y là đúng, thống nhất tên nhãn trong phần mô hình. |
| 2.2, dòng 292 | Bổ sung 19.435 người dùng và 13.897 sản phẩm làm rõ tỷ lệ mua lại 0,597 thuộc mẫu đã xử lý của Li và cộng sự, không phải kết quả đồ án. Các số khớp Bảng 1 bản tác giả. |
| 2.3, dòng 296 | Nêu CRISP-DM có sáu giai đoạn gốc, nhóm triển khai thành bảy bước chi tiết: hợp lý, tránh gán bảy bước cho nguồn gốc. |
| 2.4/3.6, dòng 321/774 | Thêm nguồn Holm đúng chỗ cho điều chỉnh đa kiểm định. Cỡ hiệu ứng và giới hạn suy diễn vẫn được giữ. |
| 2.4/4.4, dòng 341/908 | Thêm Efron cho phương pháp bootstrap; vẫn phân biệt RF–Popularity là phép chính với RF–Rules và LR–RF là bổ trợ. |
| 2.5, dòng 347 | Bỏ vị trí nhật ký “tại gốc” không làm mất thông tin phương pháp. |
| 4.5, dòng 938 | Trích dẫn tài liệu scikit-learn về tương quan đặc trưng, giữ cảnh báo importance theo AP chỉ bổ trợ nhiệm vụ Recall theo giỏ. |
| Bib | Bổ sung bốn nguồn có thật và liên quan; Pedregosa đủ 16 tác giả; Kaminskas hiển thị Article 2; ba tiêu đề sách/bài đã được chỉnh sentence case. |
| Hình 3.2–3.3 | Thay định dạng trục hàng nghìn là sửa trình bày. Diff `m2_plot_univariate.py` chỉ thêm bộ định dạng cho hai trục; không có thay đổi thuật toán tạo dữ liệu trong diff này. |

Đối chiếu nguồn bên ngoài: [CRISP-DM 1.0, bản SPSS lưu tại IBM](https://public.dhe.ibm.com/software/analytics/spss/documentation/modeler/14.2/es/CRISP-DM.pdf); [Holm, hồ sơ số tạp chí](https://www.jstor.org/stable/i412579); [Efron, DOI chính thức](https://doi.org/10.1214/aos/1176344552); [scikit-learn về permutation importance](https://scikit-learn.org/stable/modules/permutation_importance.html); [Pedregosa tại JMLR](https://www.jmlr.org/papers/v12/pedregosa11a.html); [Li, bản tác giả và Bảng 1](https://irlab.science.uva.nl/wp-content/papercite-data/pdf/li-2021-next-arxiv.pdf); [Kaminskas, hồ sơ cơ quan tác giả](https://research.ucc.ie/en/publications/diversity-serendipity-novelty-and-coverage-a-survey-and-empirical/).

## 4. Phạm vi đồng bộ workspace: chưa được nói 380/380

So đúng đường dẫn tương đối trong manifest với thư mục gốc máy Phong:

- **157** tệp khớp.
- **34** tệp hiện có nhưng khác hash.
- **189** đường dẫn chưa có ở vị trí đó.

Sau khi tìm trong các gói đã nhận và tính cả nội dung V2, tìm được bằng chứng khớp hash cho **330/380** mục. Điều này không có nghĩa đã đồng bộ 330 tệp vào đúng vị trí gốc. Còn **50 mục chưa tìm được bản khớp hash**: 17 ngoài `TAI_LIEU_NOI_BO`, 33 trong tài liệu/lưu trữ nội bộ. Có thể có bản trong ZIP chưa giải nén; phạm vi tìm là các tệp đã hiện trên filesystem, không khẳng định máy Vương thiếu dữ liệu.

17 mục ngoài tài liệu nội bộ chưa xác minh từng byte:

1. `BAO CAO/Bao cao EDA/ban2/correlation_pearson.csv`
2. `BAO CAO/Bao cao EDA/ban2/hashes.json`
3. `BAO CAO/Bao cao EDA/ban2/lift_baseline.csv`
4. `BAO CAO/Bao cao EDA/figures/ban1/fig-ref-basket-distribution.png`
5. `BAO CAO/Bao cao EDA/figures/ban1/fig-ref-category-concentration.png`
6. `BAO CAO/Bao cao EDA/plot_data/ban2/correlation_pearson.csv`
7. `BAO CAO/Bao cao lam sach/basket_quality_summary.json`
8. `BAO CAO/Bao cao lam sach/phong/20261101_165346_057637/run_report.json`
9. `BAO CAO/Bao cao lam sach/phong/latest.json`
10. `BAO CAO/Bao cao lam sach/verification.json`
11. `BAO CAO/Bao cao lam sach/vuong/20261101_165342_468830/run_report.json`
12. `BAO CAO/Bao cao lam sach/vuong/latest.json`
13. `BAO CAO/Bao cao mo hinh/cai_thu_vien_20261101/chuong3_hash_sau_cai.sha`
14. `BAO CAO/Bao cao mo hinh/cai_thu_vien_20261101/chuong3_hash_truoc_cai.sha`
15. `BAO CAO/Bao cao mo hinh/cai_thu_vien_20261101/freeze_sau.txt`
16. `BAO CAO/Bao cao mo hinh/cai_thu_vien_20261101/freeze_truoc.txt`
17. `DATA/Data đã làm sạch/Bảng master TLCK/master_read_modes.json`

Bảng TSV gửi cùng báo cáo ghi đầy đủ cả 380 mục, hash yêu cầu, trạng thái tại gốc và nơi tìm được bằng chứng. Khác hash JSON/PDF/hình chưa đủ để kết luận khác dữ liệu; chưa có nội dung V2 tương ứng thì chỉ ghi chưa xác minh.

**Đặc biệt:** gốc máy Phong còn `m4_lock.py` cũ và `lock.json` nháp. Khóa chính thức cùng các bảng test khớp V2 đã có tại `Gửi và Nhận/Nhận/GUI_PHONG_TOAN_BO_20261104/KET_QUA_TEST/BAO CAO/Bao cao mo hinh/`. Khi đồng bộ, dùng tệp chính thức đã có; không tạo lại khóa và không chấm test lại.

## 5. Đối chiếu số liệu trực tiếp với CSV/JSON

Quy ước nguồn trong bảng:

- **B** = `DATA/Data đã làm sạch/Bảng master TLCK/data_benchmark.csv` ở gốc Phong.
- **E** = `BAO CAO/Bao cao EDA/` ở gốc Phong.
- **M** = `BAO CAO/Bao cao mo hinh/` ở gốc Phong.
- **T** = `Gửi và Nhận/Nhận/GUI_PHONG_TOAN_BO_20261104/KET_QUA_TEST/BAO CAO/Bao cao mo hinh/`.

Các tệp dùng trong bảng dưới khớp manifest V2, trừ `lift_baseline.csv` cũ được ghi riêng ở mục 6. Đối chiếu dùng bản CSV/JSON thực đọc; không lấy từ README hay bản đánh giá. Dấu phẩy trong QMD là dấu thập phân.

| # | Vị trí/số trong QMD V2 | Số nguồn, bản ghi và trường | Kết quả |
|---|---|---|---|
| 1 | 3.2, dòng 424: 1.384.617 dòng | B: `rows=1384617` ở các lượt đo | Khớp |
| 2 | 3.2, dòng 525–526: 423,04 → 50,10 MiB | B: A_Dtype_Downcasting, `run_id=median`, reconstructed_unoptimized/optimized, `dataframe_mib=423.04/50.1` | Khớp |
| 3 | 3.2, dòng 545: giảm 88,16% | Tính từ hai số B: `(1-50.1/423.04)*100 = 88.1571…` | Khớp làm tròn |
| 4 | 3.2, dòng 531–532: đọc CSV/Parquet 6,1819/0,2089 giây | B: B_Format_and_IO, read_disk, median, `elapsed_seconds=6.1819/0.2089` | Khớp |
| 5 | 3.2, dòng 546: nhanh 29,59 lần | `6.1819/0.2089 = 29.5926…` | Khớp |
| 6 | 3.4, dòng 636: 39.363 giỏ, 415.053 dòng, 28.742 sản phẩm | E/sample_overview.csv: metrics `baskets`, `product_order_rows`, `products_observed` | Khớp |
| 7 | 3.4, dòng 650: trung bình 10,54; trung vị 9; Q1–Q3 5–14 | E/eda_summary.csv: variable=basket_size; `mean=10.544242054721439`, median=9, q1=5, q3=14 | Khớp |
| 8 | 3.5/5.1: produce phủ 73,95% | E/department_summary.csv: department=produce; `basket_count=29108`, `basket_coverage=0.7394761578131748` | Khớp |
| 9 | 3.5/5.1: dairy eggs phủ 66,76% | Cùng tệp, dairy eggs: basket_count=26277, basket_coverage=0.6675558265376115 | Khớp |
| 10 | 3.5, dòng 768: 210 cặp; 182 lift > 1; trung vị 1,225 | E/ban2/department_pair_summary.csv, lọc department_a < department_b: 210 dòng, 182 lift > 1, median=1.224933840455027 | Khớp |
| 11 | 3.5/5.1: phân vị 51; 80; 39 | Cùng bảng cặp: số lift <= chính lift cặp lần lượt 107/210; 168/210; 81/210 → 50.95238%; 80%; 38.57143% | Khớp làm tròn |
| 12 | 3.6, dòng 778: H1 chi² 1.584,256; V=0,201 | E/ban2/hypotheses.csv H1: chi2_pearson=1584.2560130559395; cramers_v=0.20061739506635412 | Khớp |
| 13 | 3.6, dòng 779: H2 chi² 910,419; V=0,152 | Cùng tệp H2: 910.4189424714375; 0.15208155607094512 | Khớp |
| 14 | 3.6, dòng 780: H3 chi² 913,934; V=0,152 | Cùng tệp H3: 913.9337953882543; 0.15237484377674004 | Khớp |
| 15 | 3.6: p Holm <0,001 cả ba | Cùng tệp p_holm: H1=0.0 (underflow số thực), H2=5.331902839655457e-200, H3=1.8358479465459764e-200 | Khớp; không diễn giải p thật bằng 0 |
| 16 | 4.4, dòng 890: 24.877 giỏ test | T/results_test.json: baskets=24877 | Khớp |
| 17 | Bảng 4.5: R@10 Popularity/Rules/LR/RF = 0,0755/0,0924/0,0910/0,0971 | T/ranking_metrics_test.csv, R@10: 0.07553173010925152 / 0.092378445675668 / 0.09103349808619736 / 0.09710870411718583 | Khớp |
| 18 | Bảng 4.5/Chương 5: Recall trần 0,5198 | Cùng tệp: R@10_ceiling=0.51980119387966 | Khớp |
| 19 | 4.4/5.1: HR@10 RF 17,08% | Cùng tệp RF, HR@10=0.1707601398882502 | Khớp |
| 20 | Dòng 908/966: RF−Popularity 0,0216, CI [0,0192;0,0239] | T/paired_bootstrap_test.csv RF/Popularity: difference=0.021576974007934333, ci_low=0.019227514667981765, ci_high=0.023862091606142333; primary=True | Khớp |
| 21 | Dòng 908/970: RF−Rules 0,0047, CI [0,0031;0,0063] | Cùng tệp RF/Rules: 0.004730258441517837; 0.0030868508704964062; 0.006304780559312857; primary=False | Khớp, đúng phép bổ trợ |
| 22 | Dòng 908: 2.000 lần bootstrap, seed 42 | Cùng tệp: repeats=2000, seed=42, n_users=24877 | Khớp |
| 23 | 4.4, dòng 910: 24.758.284 cặp, 25.958 dương | T/classifier_metrics_test.csv, n=24758284, positives=25958 | Khớp |
| 24 | Bảng 4.6: LR threshold=0,73128, AP=0,01401; RF threshold=0,57771, AP=0,01685 | Cùng tệp: threshold=0.7312827512437302/0.5777123663354883; average_precision=0.014009092501192765/0.01684687281014189 | Khớp |
| 25 | Bảng 4.7: LR TP=2.106; RF TP=2.345 | T/confusion_matrix_test.csv tp=2106/2345; cả bốn ô TN/FP/FN/TP cũng khớp bảng QMD | Khớp |
| 26 | 4.5, dòng 934: 5.000 giỏ, 4.976.269 cặp; AP nền 0,01386/0,01649 | M/importance_baseline.json: baskets=5000, candidate_rows=4976269, average_precision.LR=0.013864114513318017, RF=0.016494800167231417 | Khớp |
| 27 | 5.1, dòng 971: 88,38% có luật | M/rule_coverage.json: with_matching_rule=21966, validation_baskets=24854, share=0.8838014001770339 | Khớp |
| 28 | 5.1, dòng 970/993: RF chậm khoảng 10,3 lần | M/validation_methods.csv RF inference_seconds=63.55208400002448; Rules=6.189890400011791; tỷ số≈10.267 | Khớp |
| 29 | 5.1, dòng 999: bỏ luật RF 0,0971 → 0,0788 | M/ablation.csv RF full/no_rules, recall_at_10=0.09714602107476494/0.07875542809255692 | Khớp |
| 30 | 5.1, dòng 987: thêm khoảng 0,00627 món trúng/giỏ | T/ranking_metrics_test.csv: 10×(P@10_RF−P@10_Rules)=10×(0.01874020179282068−0.018113116533344055)=0.00627085259476625 | Khớp; không lấy CI Recall để thay CI số món |

## 6. Việc còn lại, mức ảnh hưởng và cách xử lý

| Vị trí | Phát hiện/bằng chứng | Mức ảnh hưởng | Cách xử lý đề xuất |
|---|---|---|---|
| Workspace gốc Phong | QMD/PDF/bib và một số mã, khóa, kết quả không cùng phiên bản V2; bảng đối chiếu ghi 34 khác và 189 chưa có đúng chỗ. | Quan trọng nếu định nộp/chạy từ gốc Phong; không phải lỗi nội dung V2. | Tạo bản nộp Phong riêng, ghép đúng tệp V2 và dữ liệu có hash khớp; kiểm lại manifest. Giữ riêng bản làm việc cũ. Không chép khóa nháp vào bản nộp. |
| E/ban2/lift_baseline.csv cũ; QMD dòng 768/1001 | CSV cũ ghi 50.47619;79.52381;38.09524. Tính trực tiếp từ bảng cặp khớp V2, dùng <= và bao gồm chính cặp đó, cho 50.95238;80;38.57143. | Có lệch giữa nguồn cũ của Phong và bài, nhưng **số 51/80/39 trong bài đúng**. | Nhận lift_baseline.csv cùng hashes.json ban2 V2 và correlation_pearson.csv/copy plot_data đồng bộ. Không sửa QMD quay về 50/80/38; không chạy lại EDA chỉ để giải quyết bàn giao. |
| 50 mục chưa có bằng chứng byte | Có manifest nhưng chưa có tệp khớp, gồm 17 mục liệt kê ở mục 4 và 33 tài liệu nội bộ. | Giới hạn đối chiếu toàn bộ hồ sơ; không tự suy ra dữ liệu sai. | Nếu muốn xác nhận 380/380, gửi phần bổ sung theo TSV rồi kiểm lại. Nếu chỉ chốt bài PDF, ghi rõ giới hạn này. |
| Python máy Phong | Thực tế 3.12.10; hồ sơ máy Vương ghi 3.12.14; thư viện 23/23 khớp, test 57/57 đạt. | Nhẹ cho rà soát hiện tại; cần chú ý khi tuyên bố môi trường tái lập hoàn toàn. | Ghi đúng phiên bản máy chạy. Khi làm môi trường vấn đáp mới, có thể dùng 3.12.14 theo hồ sơ; không nâng môi trường đang khóa hoặc chạy lại test nghiên cứu để sửa con số. |
| references.bib: efron1979 | Nguồn đúng nhưng đang thiếu DOI có sẵn: 10.1214/aos/1176344552. | Nhẹ, hoàn thiện thông tin thư mục; không thiếu cơ sở khoa học. | Nên bổ sung DOI trước bản xuất cuối nếu còn chỉnh bib. Nếu chỉnh, render và cập nhật hash QMD/PDF/bib/manifest liên quan; không cần sửa mã/mô hình. |
| references.bib: chapman2000 | Đủ tác giả, năm, tựa, cơ quan; chưa có đường dẫn bản báo cáo. | Tùy chọn, giúp người đọc truy cập. | Có thể thêm URL IBM đã kiểm ở mục 3. |
| Bảng 4.6, PDF trang 34–35 | Bảng ở cuối trang 34, dòng Nguồn sang trang 35 sau Hình 4.1. | Hình thức nhỏ, đã được ghi nhận trong gói. | Có thể giữ như phương án đã chốt; nếu chỉnh bố cục, giữ dòng nguồn gần bảng và kiểm lại tổng trang. |
| Ngày truy vấn trong tài liệu tham khảo | “11 Tháng Mười-Một 2026” do locale. | Hình thức, không sai ngày. | Không bắt buộc sửa. |
| Bản đánh giá mục 1–4 và mục 6 | Phần đầu còn hash V1, danh sách “chưa sửa”, câu code không đổi; mục 6 mới ghi V2 đã sửa. | Dễ nhầm trạng thái bàn giao. | Thêm một câu ngay đầu: phần 1–4 là ghi nhận trước 17:00, trạng thái cuối theo mục 6/README V2. Không cần sửa bài. |
| Code dài dòng theo PEP 8 | Là điểm cải thiện phong cách đã nêu trong đánh giá, không phải lỗi làm sai kết quả ở các kiểm tra này. | Ưu tiên thấp. | Giữ nguyên tệp đã khóa. Tài liệu luyện vấn đáp nên diễn giải ngắn; không nén/đổi mã nghiên cứu chỉ để giảm dòng lúc chốt. |

## 7. Điều kiện chốt đề xuất

1. **Nội dung học thuật:** chấp nhận các sửa đổi V2 trong phần văn Phong và bib; không cần đổi các bảng kết quả. Tài liệu tham khảo đã bổ sung các nhóm nguồn còn thiếu, còn điểm nhỏ về DOI/URL như trên.
2. **Bản nộp:** xác định duy nhất QMD/PDF V2 có hash ở mục 1. Không dùng QMD cũ tại gốc hoặc gói V1 để nộp nhầm.
3. **Xác nhận đồng bộ toàn bộ hai máy:** chỉ thực hiện sau khi bổ sung phần chưa xác minh và đặt đúng tệp vào bản nộp riêng. Hiện có thể xác nhận 72/72 gói nhận, 64/64 tệp bản nộp được gửi, 330/380 mục tìm được bằng chứng; không xác nhận 380/380.
4. **Giữ kết quả nghiên cứu:** Master, mô hình khóa và kết quả test có bằng chứng khớp; không mở lại test, không đổi m4_lock.py để tạo khóa mới.

Tệp gửi kèm: `Gửi Vương_Đối chiếu 380 tệp V2_20261111.tsv` và `Gửi Vương_Log 57 test V2_20261111.txt`. Các tệp nhẹ được để nguyên, không đóng ZIP.
