# Đề xuất sửa theo góp ý chấm thử (07/11/2026) — gửi Phong duyệt

## 1. Tình trạng

- **Chưa sửa bản chính.** Mọi thay đổi dưới đây mới áp lên một **bản sao** để render thử. QMD chính (SHA-256 `99dfb4557efde955`) và `references.bib` (`5486763bf1b3b8b7`) giữ nguyên.
- Bản thử: `BAN_THU_DA_SUA_44_trang.pdf`. Bản này có **44 trang; từ bìa đến hết Chương 5 là 42 trang**, bằng bản chính. Mỗi chương bắt đầu ở cùng trang PDF như bản chính: Chương 1 trang 9, Chương 2 trang 12, Chương 3 trang 16, Chương 4 trang 30, Chương 5 trang 38, tài liệu tham khảo trang 43. Không có `??`.
- So sánh từng dòng: `2521001118_Nhom01_TieuLuan.qmd.diff` và `references.bib.diff`.

## 2. Tóm tắt quyết định theo từng ý góp ý

| Ý | Góp ý | Quyết định |
|---|---|---|
| 1 | Không dùng bảng prior làm đặc trưng | **Không sửa bài.** Bài toán nhóm chọn là hoàn thiện giỏ hiện tại, không cần bảng prior. Chỉ chuẩn bị câu trả lời vấn đáp (mục 4) |
| 2 | Hoàn thiện giỏ chưa phải bán chéo | Sửa 2 câu ở 5.1 (khung hòa vốn) |
| 3 | Chunksize và "quy mô lớn" chưa được đo | Sửa mục tiêu 2 và một đoạn ở 3.2 |
| 4 | Chi-square với N lớn | Không sửa; chuẩn bị câu trả lời vấn đáp |
| 5 | Importance đo bằng AP | Không sửa; chuẩn bị câu trả lời vấn đáp |
| 6 | Tổng quan tài liệu mỏng | Thêm 2 công trình làm trên Instacart vào 2.2 và `references.bib` |
| 7a | Chương 5 nhiều lời rào đón | Gom các lưu ý về một câu ở đầu 5.1 và mục 5.3, bỏ 11 câu hoặc vế lặp. Mật độ rào đón giảm từ 38 xuống 29 trên 100 câu; phần còn lại phần lớn nằm ở 5.3 hoặc là điều kiện bắt buộc của khung hòa vốn |
| 7b | Lỗi hình thức | Sửa 3 câu; hai việc về hình là đề xuất sửa code, chưa làm (mục 3) |

Các sửa ở Chương 2 và 3 làm hai chương này dài thêm vài dòng và tràn sang trang mới. Vì vậy có 4 câu **bù trang**: chỉ rút phần lặp, không bỏ ý.

## 3. Các câu sửa đề xuất

Phong cần duyệt mọi câu ghi "Văn của: Phong" và hai mục mới trong `references.bib`. Câu ghi "Văn của: Vương" gửi để Phong biết và góp ý.

### Ý 2 — Hoàn thiện giỏ chưa phải bán chéo

- **Vị trí:** 5.1 Định nghĩa m · **Văn của:** Vương · **Loại:** sửa
  - Cũ: - $m$ là biên lợi nhuận gộp bình quân trên một sản phẩm.
  - Mới: - $m$ là biên lợi nhuận gộp tăng thêm trên một sản phẩm được gợi ý trúng. Sản phẩm bị che là món khách vốn định mua, nên một lần trúng có thể chỉ nhắc lại món đó thay vì tạo doanh thu mới; $\Delta H$ đo khả năng gợi ý trúng, không đo doanh thu tăng thêm. Phần tăng thêm chỉ đo được bằng thử nghiệm A/B có nhóm đối chứng.
- **Vị trí:** 5.1 Điều kiện đầy đủ · **Văn của:** Vương · **Loại:** sửa
  - Cũ: thử nghiệm A/B phải đo $p$ và $\Delta H$ thực,
  - Mới: thử nghiệm A/B phải đo $p$, $m$ tăng thêm và $\Delta H$ thực,

### Ý 3 — Chunksize và "quy mô lớn"

- **Vị trí:** 1.3 Mục tiêu cụ thể 2 · **Văn của:** Phong · **Loại:** sửa
  - Cũ: **Tài nguyên, tuần 2:** Áp dụng chunksize, tối ưu dtype và Parquet; lập bảng RAM đỉnh
  - Mới: **Tài nguyên, tuần 2:** Đọc theo khối (chunksize) để xử lý bảng prior 32,4 triệu dòng; tối ưu dtype và Parquet cho bảng Master; lập bảng RAM đỉnh
- **Vị trí:** 3.2 Ghép nối và tối ưu bộ nhớ · **Văn của:** Vương · **Loại:** sửa
  - Cũ: Phần ghép và ghi đi qua sáu khối, tối đa 250.000 dòng/khối; tuy vậy bước kiểm tra miền và đối soát vẫn đọc toàn bảng vào RAM. Bước có quy mô lớn nhất (prior 32.434.489 dòng) được đọc theo khối 250.000 dòng và kiểm tra quan hệ qua SQLite trên đĩa. Bước dựng Master giữ toàn bộ bản trước ghi và bản đọc lại để đối soát từng ô; nhóm chưa đo RSS đỉnh riêng của bước này.
  - Mới: Bảng lớn nhất (prior 32.434.489 dòng, CSV 585,66 MiB) được đọc theo khối 250.000 dòng và kiểm tra quan hệ qua SQLite trên đĩa để chạy được trên máy 24 GB; lượt làm sạch ngày 01/11 xử lý prior cùng hai bảng nhỏ trong 600,79 giây (`run_report.json`). Bước dựng Master ghép và ghi qua sáu khối nhưng giữ toàn bộ bản trước ghi và bản đọc lại để đối soát từng ô. Nhóm chưa đo RSS đỉnh của hai bước này và chưa benchmark đọc theo khối so với đọc toàn bộ.

### Ý 6 — Tổng quan tài liệu

- **Vị trí:** 2.2 Tổng quan nghiên cứu (thay đoạn kết) · **Văn của:** Phong · **Loại:** sửa
  - Cũ: Từ các hướng trên, nhu cầu kiểm chứng của đề tài là liệu luật đồng mua và classifier cải thiện gợi ý so với độ phổ biến trong điều kiện dữ liệu nhiễu và tài nguyên giới hạn. Nghiên cứu kết nối xử lý đa bảng, benchmark khai phá và đánh giá xếp hạng; không suy rộng kết quả công trình trước thành kết quả đồ án.
  - Mới: Trên Instacart, @hu2020 cho thấy phương pháp dựa trên tần suất mua của từng người dùng (TIFU-KNN) nhiều lần vượt các mô hình học sâu dùng RNN; @li2023 ghi nhận tỷ lệ món mua lại 0,597 và phần lớn mức cải thiện của các phương pháp gần đây đến từ món mua lại. Hai công trình dự đoán giỏ kế tiếp; đồ án xét bài toán hoàn thiện giỏ hiện tại, kiểm chứng liệu luật đồng mua và classifier có cải thiện gợi ý so với độ phổ biến trong điều kiện dữ liệu nhiễu và tài nguyên giới hạn; không suy rộng kết quả công trình trước thành kết quả đồ án.

### Ý 7a — Rút lời rào đón Chương 5

- **Vị trí:** 5.1 Đoạn mở (gom lưu ý) · **Văn của:** Phong · **Loại:** rút gọn
  - Cũ: Tuy nhiên, HR@10 của RF chỉ đạt 17,08%; phần lớn giỏ chưa có sản phẩm che được tìm thấy trong Top-10. Vì vậy, cải thiện ngoại tuyến là căn cứ thử nghiệm, chưa đủ để cam kết hiệu quả thương mại.
  - Mới: HR@10 của RF là 17,08%, tức phần lớn giỏ chưa có sản phẩm bị che trong Top-10. Mọi bằng chứng trong chương là kết quả ngoại tuyến trên một lần chia dữ liệu, dùng làm căn cứ thử nghiệm chứ chưa phải bằng chứng hiệu quả thương mại; các giới hạn được gom ở mục 5.3.
- **Vị trí:** Bảng 5.1 dòng kiểm định · **Văn của:** Phong · **Loại:** rút gọn
  - Cũ: Hai cặp còn lại chỉ thử khi có lý do kinh doanh riêng; không suy ra nhân quả |
  - Mới: Hai cặp còn lại chỉ thử khi có lý do kinh doanh riêng |
- **Vị trí:** 5.1 ΔH · **Văn của:** Vương · **Loại:** rút gọn
  - Cũ: Đây là ước lượng điểm của một so sánh bổ trợ, đo ngoại tuyến trên tập test.
  - Mới: Đây là ước lượng điểm trên tập test.
- **Vị trí:** 5.1 Kịch bản chi phí · **Văn của:** Vương · **Loại:** rút gọn
  - Cũ: theo mô hình giả định; đây không phải lợi nhuận trên một sản phẩm bán thêm thực tế.
  - Mới: theo mô hình giả định.
- **Vị trí:** 5.1 Phép bỏ nhóm · **Văn của:** Phong · **Loại:** rút gọn
  - Cũ: Điều này ủng hộ giữ thông tin đồng mua trong hệ thống, chưa chứng minh kiến trúc nào tối ưu cho mọi doanh nghiệp.
  - Mới: Điều này ủng hộ giữ thông tin đồng mua trong hệ thống.
- **Vị trí:** 5.2 Bước 1 · **Văn của:** Phong · **Loại:** rút gọn
  - Cũ: Đây là đầu vào kỹ thuật, chưa phải một hệ thống đã triển khai tại doanh nghiệp.
  - Mới: 
- **Vị trí:** Bảng 5.2 dòng nguồn · **Văn của:** Phong · **Loại:** rút gọn
  - Cũ: Đây là kế hoạch đo trong tương lai; nghiên cứu hiện tại chưa đo doanh thu, tỷ lệ nhấp hay độ phủ danh mục được gợi ý.
  - Mới: Đây là kế hoạch đo trong tương lai.
- **Vị trí:** 5.4 Hướng phát triển · **Văn của:** Phong · **Loại:** rút gọn
  - Cũ: Đây là các hướng chưa triển khai trong phạm vi đồ án.
  - Mới: 
- **Vị trí:** 5.4 Kết luận câu hỏi 2 · **Văn của:** Phong · **Loại:** rút gọn
  - Cũ: Các kết quả mô tả hỗ trợ đặt giả thuyết kinh doanh, không thay thế thử nghiệm.
  - Mới: 
- **Vị trí:** 5.3 Giới hạn mô hình · **Văn của:** Phong · **Loại:** rút gọn
  - Cũ: N = 1.000 nằm giữa {500; 1.000; 2.000}. Nghiên cứu không chứng minh tối ưu ngoài phạm vi đã khảo sát.
  - Mới: N = 1.000 nằm giữa {500; 1.000; 2.000}.
- **Vị trí:** 5.4 Kết luận câu hỏi 4 · **Văn của:** Phong · **Loại:** rút gọn
  - Cũ: chênh lệch với Rules là 0,0047 trong so sánh bổ trợ chưa hiệu chỉnh đa so sánh.
  - Mới: hơn Rules 0,0047 trong so sánh bổ trợ (mục 5.1).

### Ý 7b — Lỗi hình thức trong lời văn

- **Vị trí:** 5.4 Kết luận câu hỏi 1 (thêm số) · **Văn của:** Phong · **Loại:** sửa
  - Cũ: Đối với câu hỏi 1, nghiên cứu xây dựng quy trình làm sạch và ghép sáu bảng thành Master, kèm đối soát quan hệ và hồ sơ tối ưu kiểu dữ liệu ở Chương 3.
  - Mới: Đối với câu hỏi 1, sáu bảng được làm sạch và ghép thành Master 1.384.617 dòng × 15 cột, cả bốn phép ghép khớp 100%; tối ưu kiểu giảm 88,16% bộ nhớ DataFrame và Parquet đọc nhanh hơn CSV khoảng 29,59 lần trên máy đã đo.
- **Vị trí:** 3.5 Hình kích thước giỏ theo thời gian · **Văn của:** Phong · **Loại:** sửa
  - Cũ: Ô dưới 30 giỏ (đánh dấu *) chỉ để tham khảo.
  - Mới: Không ô nào dưới 30 giỏ nên không có ô đánh dấu *.
- **Vị trí:** 4.6 Câu hỏi 4 (22,3%) · **Văn của:** Vương · **Loại:** sửa
  - Cũ: Rules cao hơn khoảng 22,3% và LR khoảng 20,5% nhưng thấp hơn Rules và RF.
  - Mới: Rules cao hơn khoảng 22,3% và LR khoảng 20,5% (tỷ lệ tính từ giá trị chưa làm tròn), nhưng LR thấp hơn Rules và RF.

### Câu bù trang (không đổi ý, chỉ bỏ phần lặp)

- **Vị trí:** 2.5 Môi trường · **Văn của:** Phong · **Loại:** bù trang
  - Cũ: Mã nguồn và nhật ký làm việc được nộp riêng, không đưa toàn văn vào phụ lục của bản tiểu luận.
  - Mới: Mã nguồn và nhật ký được nộp riêng.
- **Vị trí:** 3.2 Mở đầu · **Văn của:** Vương · **Loại:** bù trang
  - Cũ: Làm sạch và chuẩn hóa khóa (mục 3.3) được chạy trước khi ghép, vì khoảng trắng và sai định dạng khóa phải được xử lý trước khi kiểm tra quan hệ; thứ tự trình bày 3.2 rồi 3.3 theo đề cương, không phải thứ tự chạy.
  - Mới: Làm sạch khóa (mục 3.3) chạy trước khi ghép, vì khoảng trắng và sai định dạng khóa phải được xử lý trước khi kiểm tra quan hệ.
- **Vị trí:** 3.2 Máy đo benchmark · **Văn của:** Vương · **Loại:** bù trang
  - Cũ: Máy đo chạy Windows 11, CPU AMD 8 nhân/16 luồng, RAM 24 GB;
  - Mới: Máy đo (mục 2.5) có CPU AMD 8 nhân/16 luồng;
- **Vị trí:** 3.2 Benchmark · **Văn của:** Vương · **Loại:** bù trang
  - Cũ: Đây là lượt đo ngày 04/11/2026, phụ thuộc dữ liệu, thư viện và bộ nhớ đệm của máy thực nghiệm. Kết quả ủng hộ
  - Mới: Kết quả phụ thuộc thư viện và bộ nhớ đệm của máy đo; nó ủng hộ

### Hai việc về hình (đề xuất sửa code, chưa làm, chưa có trong bản thử)

1. **Chú thích "\* N<30" ở hình kích thước giỏ theo mã ngày và khung giờ.** Trong `time_pivot_small_group.csv` mọi ô đều là `False`, tức không ô nào dưới 30 giỏ. Đề xuất sửa `scripts/m2_plot_multivariate.py` dòng 58 (tệp của Phong): đổi `title='(a) Median; * N<30'` thành `title='(a) Median'`. Logic gắn dấu \* ở dòng 55 giữ nguyên. Sau đó chạy lại script, kiểm `check_hashes` và `plot_data` giống từng byte, rồi chép PDF vào `assets/chuong3/`. Câu ở 3.5 trong bản thử đã nói "không ô nào dưới 30 giỏ", nên vẫn khớp cả khi chưa sửa hình.
2. **Hình dùng dấu chấm thập phân** (ví dụ 8.5, 0.863, 0.02), còn văn bản dùng dấu phẩy.
   - **Sáu hình Chương 3:** sửa được bằng một bộ định dạng số đặt trong các script vẽ. Hai script cần sửa là `m2_plot_univariate.py` (của Vương) và `m2_plot_multivariate.py` (của Phong). Không đổi `configs/m2_plot_style.json` vì tệp này đang bị khóa.
   - **Hình importance:** vẽ lại được từ CSV.
   - **Hình Recall@K:** do `m4_test.py` (tệp khóa) sinh ra, và mã băm của hình đã ghi trong `results_test.json`. Đề xuất giữ nguyên hình này.
   - Nếu Phong đồng ý, Vương sẽ làm thành một đợt riêng và gửi lại để kiểm.

### Hai mục thêm vào `references.bib` (tệp của Phong)

```bibtex
@inproceedings{hu2020,
  author = {Hu, Haoji and He, Xiangnan and Gao, Jinyang and Zhang, Zhi-Li},
  title = {Modeling personalized item frequency information for next-basket recommendation},
  booktitle = {Proceedings of the 43rd International ACM SIGIR Conference on Research and Development in Information Retrieval},
  year = {2020}, pages = {1071--1080},
  publisher = {Association for Computing Machinery},
  doi = {10.1145/3397271.3401066}
}
@article{li2023,
  author = {Li, Ming and Jullien, Sami and Ariannezhad, Mozhdeh and {de Rijke}, Maarten},
  title = {A next basket recommendation reality check},
  journal = {ACM Transactions on Information Systems},
  volume = {41}, number = {4}, pages = {Article 116}, year = {2023},
  doi = {10.1145/3587153}
}
```

**Đã kiểm thông tin ngày 07/11** từ bản arXiv và trang của nhóm tác giả:

- **Hu và cộng sự (2020).** DOI 10.1145/3397271.3401066; SIGIR 2020, trang 1071–1080. Bài dùng 4 bộ dữ liệu: ValuedShopper, Instacart, Dunnhumby và TaFeng. Câu gốc: phương pháp "frequently outperforms the state-of-the-art NBR methods – including deep learning based methods using RNNs".
- **Li và cộng sự (2023).** ACM TOIS 41(4), Article 116; DOI 10.1145/3587153. Bài dùng 3 bộ dữ liệu: TaFeng, Dunnhumby và Instacart. Bảng 1 ghi Instacart có tỷ lệ mua lại 0,597 và tỷ lệ món mới 0,403. Một kết luận của bài là thiên lệch về món mua lại "accounts for most of the performance gains of recently published methods".
- Nguồn: <https://arxiv.org/abs/2006.00556>, <https://arxiv.org/abs/2109.14233>, <https://irlab.science.uva.nl/wp-content/papercite-data/pdf/li-2023-next.pdf>.
- Trong danh mục tài liệu tham khảo của bản thử, hai mục hiển thị đúng APA: "Li, M., Jullien, S., Ariannezhad, M., & de Rijke, M. (2023)… *41*(4), Article 116".

## 4. Câu trả lời vấn đáp chuẩn bị sẵn

- **Ý 1. Vì sao không dùng bảng prior?** "Bài toán nhóm chọn là hoàn thiện giỏ hiện tại: dựa vào phần giỏ khách đang có để gợi ý món thường được mua kèm. Đầu vào chỉ gồm phần giỏ quan sát và thống kê đồng mua học từ tập reference, nên mô hình không cần lịch sử của từng khách và dùng được cả cho khách mới. Dự đoán từ lịch sử mua là một bài toán khác, dự đoán giỏ kế tiếp hoặc mua lại; mục 2.2 đã nêu hai công trình theo hướng đó trên Instacart. Bảng prior vẫn được làm sạch và kiểm tra quan hệ theo khối như phần dữ liệu lớn nhất."
  - Nếu bị hỏi tiếp "lịch sử có làm Recall tăng không": nói thật là có thể tăng, vì 59,67% dòng hợp lệ ở reference là mua lại (Li và cộng sự ghi 0,597 trên Instacart). Đó là hướng mở rộng. Nhóm không thêm vào sau khi đã mở test, vì như vậy test không còn là đánh giá độc lập.
  - **Không trả lời "vì sợ rò rỉ":** đơn prior xảy ra trước đơn train nên không gây rò rỉ.
- **Vì sao chỉ lấy 1.000 sản phẩm?** Số này chọn theo lưới trên validation (`validation_grid_A.csv`, cùng tham số luật đã chọn):

  | Danh mục | Trần Recall@10 | Recall@10 của Rules |
  |---:|---:|---:|
  | 500 | 0,4104 | 0,0915 |
  | 1.000 | 0,5211 | 0,0932 |
  | 2.000 | 0,6363 | 0,0940 |

  Từ 1.000 lên 2.000, Recall@10 chỉ tăng 0,0008, dưới dung sai 0,002, trong khi số cặp ứng viên và thời gian chấm gần gấp đôi. Món ngoài Top-1.000 hiếm và gần như không có luật nên khó lọt vào Top-10.
- **Ý 2. Gợi ý trúng có phải bán chéo không?** "Chưa. Món bị che là món khách vốn định mua. Gợi ý trúng cho thấy mô hình nhận ra món hợp với giỏ, không chứng minh đã bán thêm. Vì vậy m trong khung hòa vốn là biên lợi nhuận tăng thêm, chỉ đo được bằng A/B có nhóm đối chứng."
- **Ý 4. Chi-square với N lớn.** "Với 39.363 giỏ, Chi-square gần như chắc chắn có ý nghĩa, nên nhóm đọc Cramér's V (0,152–0,201, mức nhỏ). Kích thước giỏ là yếu tố gây nhiễu chưa kiểm soát: giỏ lớn chứa nhiều ngành hơn, và 182 trong 210 cặp ngành có lift lớn hơn 1. Bước tiếp theo là kiểm định phân tầng theo nhóm cỡ giỏ."
- **Ý 5. Importance đo bằng AP.** "AP gộp mọi cặp của nhiều giỏ nên chịu ảnh hưởng của biến cấp giỏ như cỡ giỏ: hoán vị cỡ giỏ làm AP của LR giảm dù biến này không đổi thứ tự trong giỏ. Vì vậy nhóm dùng phép bỏ nhóm đặc trưng, đo bằng Recall@10, để kết luận: bỏ ba biến luật làm Recall@10 của RF giảm từ 0,0971 xuống 0,0788."

## 5. Phong trả lời

1. Ghi **đồng ý** hoặc **sửa** cho từng câu "Văn của: Phong", cho hai mục bib và cho hai việc về hình ở mục 3.
2. Gửi lại vào `Chung/Gửi và nhận/Nhận/`.

Sau khi Phong đồng ý, Vương sẽ làm theo thứ tự:
1. Sao lưu bản chính.
2. Áp đúng những câu đã được duyệt.
3. Nếu Phong đồng ý phần hình thì làm một đợt riêng: sửa script, vẽ lại hình và kiểm `plot_data`.
4. Render, rồi kiểm số trang và `??`.
5. Chạy unittest.
6. Gửi lại QMD và PDF.
