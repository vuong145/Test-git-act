# Rà soát công việc Claude — 01/11/2026

Người kiểm tra: Codex, kiểm tra trực tiếp workspace máy Vương theo bản tổng kết người dùng gửi. Không sửa code, cấu hình, QMD, dữ liệu hoặc đầu ra chính thức; chỉ chạy kiểm thử, đọc/đối chiếu dữ liệu và tái hiện lỗi trong thư mục tạm. Không chạy lại cleaning, Master, pipeline M2 hoặc benchmark lớn. Không chấm chất lượng mô hình trên test.

## Kết luận

Phần lớn công việc được nêu có bằng chứng trên máy. Dữ liệu nền Chương 3 và các đầu ra Chương 4 hiện có vượt qua các phép kiểm tra thực hiện trong phiên này. Không có căn cứ yêu cầu làm lại từ đầu.

Tuy nhiên, chưa thể coi phần Vương trong Chương 4 đã hoàn thành. Hiện mới có chuẩn bị giỏ, danh mục, khai phá luật và benchmark thử. Cần sửa cơ chế liên kết phép che với cấu hình trước khi chọn cấu hình trên validation; sửa công cụ benchmark trước lượt đo chính thức; chốt đối tượng phân tích importance trước khi Phong triển khai.

## 1. Những việc đã xác minh

Đường dẫn trong các mục dưới tính từ `2521001118_Nhom01_TieuLuan/`, trừ khi ghi rõ gốc TLCK.

| Nội dung | Bằng chứng kiểm tra trực tiếp | Kết quả |
|---|---|---|
| Gói Chương 3 của Phong | Tính lại SHA-256 từng đường dẫn trong `TLCK/Chung/Gửi và nhận/Nhận/GUI_vuong_chuong3_hoan-thien_20261031/DANH_SACH.txt` | 71/71 tệp khớp |
| Bản sao lưu trước ghép | Tính lại SHA-256 theo `TLCK/Chung/archive/truoc-ghep-chuong3-hoan-thien_20261101/SHA256.txt` | 3/3 tệp khớp |
| Ghép QMD | Diff trực tiếp với QMD trong gói nhận | Đúng hai đoạn thay đổi: requirements và đích Master |
| Bibliography và hình đã chép | So SHA-256 `references.bib` và 6 PDF trong `assets/chuong3/` với gói nhận | Đều khớp |
| PDF hiện tại | `pdfinfo` và đọc trang bằng pypdf | 50 trang; Chương 3 bắt đầu trang vật lý 17, còn nội dung tại trang 45; Chương 4 bắt đầu trang 46. Chưa đánh giá toàn bộ chất lượng dàn trang bằng hình ảnh |
| CSV sạch | Tính SHA-256 thực của 6 CSV và so với `comparison_previous.csv` | 6/6 khớp; bảng đối chiếu ghi True cho cả sáu |
| Cổng dữ liệu | Gọi `project_io.check_hashes()` cho G0, ban2 và M4 | Lần lượt 6, 10, 4 tệp đều khớp |
| Master hai chế độ đọc | Đọc lại mặc định và `numpy_nullable`, so chính xác giá trị và mặt nạ thiếu | Bằng nhau; 1.384.617 × 15; 16.992.331 byte |
| Phân vị lift | Tính lại tỷ lệ `lift <= giá trị đang xét` từ bảng cặp ngành, đọc float theo round-trip | 50,95238095; 80; 38,57142857. Có 210 cặp, 182 cặp lift > 1 |
| Môi trường hiện tại | Đối chiếu phiên bản đã cài với từng dòng khóa trong requirements | 23/23 dòng khớp, gồm scikit-learn 1.9.1, mlxtend 0.25.0, psutil 7.2.2 |
| Kiểm thử | Chạy lại toàn bộ unittest | 35/35 đạt |
| Quy mô code mới | Đếm sáu tệp config, bốn script và test được liệt kê | Tổng đúng 323 dòng, gồm chú thích và dòng trống |
| Giỏ đã che | Đối chiếu tập người dùng, tập sản phẩm gốc, O/H rời nhau, công thức h, điều kiện singleton; tái tính phép che seed 42 | Đạt với toàn bộ 91.846 giỏ; fit có 37.388 giỏ đủ điều kiện, tổng 75.006 sản phẩm che |
| Danh mục | Tính độc lập số giỏ mỗi sản phẩm, thứ hạng và độ phổ biến từ reference | Khớp 28.742 sản phẩm |
| Khả thi Top-N | Tính lại tỷ lệ dòng fit thuộc danh mục từ reference | Top-500: 41,5361%; Top-1.000: 52,2840%; Top-2.000: 64,2284% |
| Luật đã lưu | Dùng tập mã đơn chứa từng sản phẩm để đếm độc lập tiền đề, hậu đề, hợp; tính lại support/confidence/lift/leverage/conviction | 75.148 dòng luật của 12 tổ hợp khớp, đúng ngưỡng và thuộc danh mục tương ứng |
| Benchmark thử đã lưu | Đọc CSV và JSON | N=500, min_count=50, max_len=2; ba lượt mỗi thuật toán đều ok; 2.016 itemset, 2.079 luật; chữ ký số đếm khớp |

Kiểm tra 75.148 dòng luật xác nhận tính đúng của các luật đã lưu, không phải bằng chứng độc lập rằng không bỏ sót bất kỳ luật có thể sinh nào. Chưa chạy lại khai phá toàn lưới hoặc benchmark để thay số đo lịch sử.

Lượt unittest đầu gặp PermissionError ở thư mục tạm sandbox Codex. Chạy lại với TEMP/TMP trong workspace đạt đủ 35 test. Đây là vấn đề quyền ghi của môi trường kiểm tra, không quy thành lỗi code dự án.

## 2. Các vấn đề cần sửa

### A. Hash M4 có thể xác nhận nhầm phép che cũ với cấu hình mới

- Vị trí: `scripts/m4_mining.py:35`, phối hợp với `scripts/m4_prepare.py`.
- Bước chuẩn bị tạo `masked_baskets.parquet` nhưng không lưu bằng chứng cấu hình nào đã tạo phép che. Bước mining lấy hash cấu hình hiện tại và hash tệp mask đang tồn tại rồi ghi chung vào `M4/hashes.json`.
- Đã tái hiện trên dữ liệu dựng tay, trong thư mục tạm: tạo mask bằng seed 42, đổi seed cấu hình thành 43, chạy `m4_mining.main()` mà không chạy lại prepare. Mining hoàn thành, `check_hashes()` cho M4 vẫn đạt dù mask còn nguyên seed 42 và khác phép che seed 43.
- Hậu quả: một thay đổi seed/hidden_share có thể được ghi nhận trong config nhưng chưa áp dụng vào giỏ; cổng hash phía sau không phát hiện. Tệp hash chứng minh các tệp chưa đổi kể từ lúc ghi hash, chưa chứng minh chúng được tạo từ cùng một cấu hình.
- Đề nghị: prepare ghi metadata/hash gắn với các tham số phép che và nguồn Master/split; mining và các bước sau kiểm tra quan hệ này trước khi ghi hoặc dùng đầu ra. Thêm test đổi seed/hidden_share nhưng giữ mask cũ phải bị từ chối.
- Mức xử lý: sửa trước validation chính thức. Đầu ra hiện tại đã được tái tính và khớp seed 42; không kết luận dữ liệu hiện tại bị sai.

### B. Benchmark ghi đè kết quả khi chạy cấu hình tiếp theo

- Vị trí: `scripts/m4_benchmark_mining.py:63–64`.
- Mọi cấu hình ghi cùng `mining_benchmark.csv` và `itemset_equivalence.json`, không gộp hoặc lưu phiên cũ.
- Thiết kế mục 3.3 yêu cầu đo cấu hình đã chọn và thêm cấu hình nặng nhất. Chạy hai lệnh liên tiếp theo giao diện hiện tại sẽ chỉ giữ cấu hình cuối trong các tệp đầu ra này.
- Đề nghị: lưu từng cấu hình vào đường dẫn riêng hoặc cập nhật bảng theo khóa cấu hình/thuật toán/lượt, đồng thời giữ hồ sơ tương đương cho từng cấu hình. Phân biệt benchmark thử với benchmark chính thức.
- Mức xử lý: sửa trước khi chạy benchmark chính thức nhiều cấu hình.

### C. Benchmark không hoàn tất báo cáo khi hết thời gian hoặc tiến trình lỗi

- Vị trí: `scripts/m4_benchmark_mining.py:50–70`.
- Đã mô phỏng cả hai thuật toán timeout: ghi được CSV trạng thái, sau đó lỗi `AttributeError: 'DataFrame' object has no attribute 'signature'` tại bước tạo JSON vì không có lượt thành công.
- Ngoài ra, nhánh xử lý chỉ bắt `TimeoutExpired`; nếu tiến trình con trả mã lỗi, `CalledProcessError` sẽ thoát trước bước xuất bảng tổng hợp. Đây là đường đi có thể xảy ra khi cấu hình vượt tài nguyên.
- Đề nghị: xác định schema kết quả kể cả khi không có lượt thành công; ghi trạng thái thất bại và thông báo lỗi; trả tương đương là chưa xác minh khi thiếu bằng chứng. Không để CSV mới đi cùng JSON cũ của lượt trước.
- Mức xử lý: sửa trước benchmark cấu hình nặng. Không phải lỗi đã xảy ra trong sáu lượt thành công hiện có.

### D. Phép so support chưa đáp ứng dung sai 1e-12 trong thiết kế

- Vị trí: `scripts/m4_common.py:90–93`, dùng bởi benchmark.
- `itemset_signature()` chuyển support về `round(support * N)` rồi chỉ so số nguyên. Hai support khác nhau vẫn có thể cho cùng chữ ký.
- Tái hiện: cùng itemset, N=39.363, support 0,5 và 0,500001 cho chữ ký giống nhau; chênh 1e-6 lớn hơn nhiều dung sai 1e-12 đã đề ra.
- Đề nghị: so tập itemset và support chưa làm tròn bằng dung sai tuyệt đối 1e-12; số đếm làm tròn vẫn giữ để báo cáo. Ghi sai số support lớn nhất vào hồ sơ tương đương.
- Mức xử lý: sửa trước khi dùng JSON tương đương làm bằng chứng cho tiêu chí support. Không có bằng chứng rằng support hai thuật toán thực tế đang lệch.

### E. Thiết kế importance chưa xử lý trường hợp phương pháp chính là Popularity hoặc Rules

- Vị trí: `TLCK/Chung/Hướng dẫn chung/THIET_KE_CHUONG4_20261101.md:158` và mục 4.3 của tài liệu.
- Mục 3.5 yêu cầu permutation importance của “mô hình chính”, nhưng bước chọn chính có thể chọn Popularity hoặc Rules. Hai phương pháp này không phải Pipeline phân loại bảy đặc trưng để áp dụng nguyên quy trình importance/AP dự kiến.
- Đề nghị: quy định trước importance cho LR/RF (cả hai hoặc classifier tốt nhất trên validation), độc lập với phương pháp thắng chung. Nếu Rules/Popularity thắng, diễn giải riêng cơ chế và độ phủ của chúng.
- Mức xử lý: chốt trước khi Phong viết `m4_interpret.py`, không phải chờ kết quả test mới chọn cách xử lý.

## 3. Việc chưa triển khai, không nên gọi là lỗi đã làm sai

- `m4_common.py` chưa có sinh ứng viên, khớp luật với giỏ, bảy đặc trưng, Popularity/Rules và chỉ số xếp hạng.
- `m4_prepare.py` mới tạo giỏ che, chưa có lấy mẫu âm, đặc trưng fit, tương quan và lựa chọn giai đoạn A.
- Chưa có `m4_classifier.py`, `m4_lock.py`, `m4_test.py`, `m4_interpret.py`, `tests/test_m4_model.py`, `features_fit.parquet` hoặc `lock.json`.
- `pilot_baskets=2000` có trong config nhưng chưa được script hiện có đọc. Hiện không có chế độ pilot hoạt động chỉ bằng đổi giá trị này. Khi thêm cần tách đầu ra pilot khỏi kết quả chính thức.
- 35 test đạt gồm 30 test cũ và 5 test Chương 4; chưa chứng minh đặc trưng không rò rỉ, tính đúng Recall, lấy mẫu âm, Pipeline hoặc khóa test vì các phần đó chưa được triển khai.
- Giao diện mục 11.4 yêu cầu danh sách mã `int32`; schema Parquet hiện là `list<int64>` ở observed/hidden/antecedent và consequent là int64. Giá trị không sai, nhưng cần thống nhất dtype trước khi bàn giao để tránh hai máy dùng hợp đồng khác nhau.

12 tổ hợp luật đã lưu và 24 cấu hình giai đoạn A không mâu thuẫn: mỗi tổ hợp (N, min_count, max_len) sinh ở confidence 0,05; ngưỡng 0,10 sẽ lọc khi đánh giá.

## 4. Bằng chứng lịch sử chưa đủ để xác nhận lại

- “61/61 đầu ra giống từng byte sau cài thư viện”: có ghi trong nhật ký/thiết kế; phiên này xác minh phiên bản hiện tại, hash hiện tại và log M2 chạy thành công. Chưa tìm được bảng hash đầy đủ trước/sau đợt cài trong các hồ sơ đã rà soát để tái xác nhận con số 61/61.
- “Apriori mặc định dùng khoảng 14 GB và 27–42 giây”: hiện bảng benchmark chỉ còn lượt low_memory=True. Chưa tìm được đầu ra đo của chế độ mặc định để độc lập xác nhận số này. Không nên đưa số đo đó vào thân bài như kết quả đã kiểm chứng nếu chưa khôi phục hồ sơ đo. Không cần chạy lại chế độ nặng chỉ để rà soát.
- Việc chạy script của Phong trong scratchpad và “chỉ sửa hai đường dẫn” của script: xác minh được script hiện tại, đầu ra và hai chế độ đọc bằng nhau; chưa có bản script gốc để diff độc lập trong phiên này.
- Không kiểm tra lại từng số trong toàn bộ CLAUDE.md/QMD, không khẳng định “không có số nào lệch” cho toàn bài. Các con số trọng tâm đã kiểm tra được liệt kê ở mục 1.

## 5. Tài liệu còn lệch trạng thái

- `CLAUDE.md:55` và checklist dòng 210 vẫn nói I1–I3/chùm insight/diễn giải còn phải viết, trong khi QMD đã có.
- `CLAUDE.md:58` nói chưa phân công code Chương 4; tài liệu mới đã có đề xuất chi tiết nhưng vẫn chờ hai người chốt. Cần phân biệt “đã có đề xuất” với “đã thống nhất”.
- Câu “hai bản xuất bản giống nhau” tại QMD dòng 581 vẫn tồn tại, đúng là việc còn phải sửa; khi sửa cần phân biệt hồ sơ hồi quy lịch sử với cơ chế xuất bản hiện hành.
- Nhật ký hiện đã có phiên 01/11 gộp đủ các phần chính và phiên rút gọn 31/10, nhưng checklist nhật ký trong CLAUDE.md chưa phản ánh hết.

## 6. Thứ tự tiếp tục đề nghị

1. Gửi thiết kế và giao diện cho Phong, kèm báo cáo này; chốt phần importance và dtype.
2. Sửa A trước validation; sửa B–D trước benchmark chính thức, bổ sung các test tái hiện tương ứng.
3. Hoàn thiện phần Vương còn thiếu: ứng viên, khớp luật, đặc trưng, lấy mẫu âm, chỉ số và đánh giá giai đoạn A. Phong có thể phát triển Pipeline và kiểm thử trên dữ liệu dựng tay song song.
4. Chốt danh mục/luật bằng validation, rồi triển khai LR/RF, khóa cấu hình và đánh giá cuối theo thiết kế.

Không cần chờ rút Chương 3 xuống 17 trang mới tiếp tục code Chương 4. Đây là công việc trình bày có thể làm song song; tổng giới hạn trang vẫn cần kiểm tra khi đủ nội dung các chương.
