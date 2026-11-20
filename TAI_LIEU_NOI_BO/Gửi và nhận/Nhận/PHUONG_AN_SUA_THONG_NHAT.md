# Phương án sửa thống nhất toàn bộ tiểu luận

Ngày đối chiếu: 29/10/2026. Phạm vi: thống nhất phương án trước triển khai 3.4, không tự coi nhận xét trên máy Vương là lỗi đã xảy ra trên máy Phong. Tài liệu này là kế hoạch sửa và tiêu chí nghiệm thu, không phải chứng nhận các sửa đổi dưới đây đã được thực hiện.

## 1. Kết quả đối chiếu thực tế và bản làm việc

- Bài đang chỉnh trên máy Phong: `2521001118_Nhom01_TieuLuan.qmd` ở gốc workspace; không có file tên chính xác `Tieuluan.qmd`. Mục 3.3 vừa được tích hợp đủ 10 tiểu mục, sửa cách diễn đạt số nhãn được khôi phục và xuất PDF 40 trang. Con số 36/37 trang trong nhận xét thuộc phiên bản khác.
- `Dong_bo_TLCK/2521001118_Nhom01_TieuLuan/` là snapshot 128 file, giữ nguyên để đối chiếu. Không áp sửa vào snapshot hoặc gói ZIP.
- Gói `BAN_GIAO_G0_2026-10-29/BAN_GIAO_G0_2026-10-29/` có **47/47 file đúng PACKAGE_MANIFEST.json**. `foundation_run.json` và acceptance hiện cùng hash `31adaedc…`. Chưa có lỗi lệch hash được nêu trên bản gói này. Kết quả này chỉ xác minh byte, chưa phải chạy nghiệm thu G0 bằng môi trường M2 của Phong.
- Mã G0 thực sự chưa yêu cầu acceptance trong consumer gate; verifier độc lập chỉ ghi acceptance khi thành công, không vô hiệu hóa trạng thái cũ khi lỗi. `split_rule` thực sự chưa được kiểm tra trong config().
- M1 đọc đối soát bằng `dtype_backend="numpy_nullable"` tại `scripts/m1_build_master.py`; kiểu đọc mặc định của M2 là một chế độ khác, không tự chứng minh dữ liệu sai.
- Các lời nhận xét về skill Kilo, nhật ký G0 và môi trường máy Vương không được suy ra là trạng thái máy Phong. Không tạo nhật ký thực hiện G0 tại Phong trước khi thực sự chạy.

Chọn duy nhất QMD ở gốc làm bản biên tập hiện tại. Khi tiếp nhận G0 vào cây vận hành, phải đối chiếu từng file giao nhau với code/hồ sơ đã đồng bộ; không ghép toàn bộ bằng cách ghi đè mù. Sau đó khai báo rõ cây vận hành, QMD chính, lệnh render và vị trí môi trường trong README. Mọi bản snapshot vẫn để riêng.

## 2. Thứ tự ưu tiên đã thống nhất

| Mức | Khi nào cần sửa | Nội dung |
|---|---|---|
| A | Trước khi tạo kết quả 3.4–3.6 | Gate G0, quản lý phiên kiểm chứng/hash, split_rule, cấu hình hai nhánh, đường dẫn tài nguyên render, môi trường M2 |
| B | Cùng đợt chuẩn hóa văn bản trước 3.4 | Kiểu đọc Parquet, đơn vị/mẫu số thiếu, dấu vết API, phạm vi imputation, phiên bản môi trường, thuật ngữ và danh mục viết tắt |
| C | Trong triển khai 3.4–3.6 | Thống kê reference, groupby/pivot_table/crosstab/corr, join hợp lý, bảng quyết định, hình thật, kiểm định/effect size, insight và provenance |
| D | Trước nghiệm thu/nộp | Cam đoan/cảm ơn, tóm tắt, toàn văn code, trích nhật ký, bỏ hình giả, lint, nguồn tham khảo và kiểm tra PDF toàn bài |

Các mục D là bắt buộc để nộp, nhưng không phải lý do trì hoãn mọi code 3.4. Không thể đánh giá Trụ cột II là hoàn chỉnh khi 3.4–3.6 chưa có kết quả; không tự hứa mức điểm Khá/Xuất sắc.

## 3. Sửa nền G0 và cấu hình

### 3.1. Verifier và cổng sử dụng dữ liệu

Không bỏ `acceptance_sha256` để che sự không nhất quán. Thiết kế trạng thái `building/verifying → passed` hoặc `failed`; trường hợp thiếu file, sai hash, lỗi assertion/đọc dữ liệu đều phải bị từ chối.

Tách hai lớp kiểm tra:

1. Kiểm tra đầu vào nền: source/config/code/output theo foundation manifest. Verifier gọi lớp này, không đòi acceptance mới trước khi chính nó tạo acceptance.
2. Cổng cho các script EDA: yêu cầu validation **và acceptance** đã đạt, cùng run_id, cùng hash foundation manifest; kiểm tra các hash cần thiết trước khi đọc dữ liệu.

Verifier phải ghi trạng thái đang kiểm tra trước khi bắt đầu; khi lỗi ghi `failed`, kiểm tra đã chạy và lỗi, thoát khác 0. Nếu chính việc ghi trạng thái lỗi cũng thất bại, consumer vẫn phải từ chối vì trạng thái mới nhất chưa passed. Khi thành công mới xuất acceptance và con trỏ phiên hoàn chỉnh. Không tạo quan hệ hash vòng giữa các manifest.

Kiểm thử bắt buộc: không có acceptance; acceptance cũ; lỗi assertion khi hash nguồn vẫn đúng; đổi config; đổi output; chạy độc lập verifier; quá trình bị ngắt; lệnh thành công từ cwd khác.

### 3.2. Hồ sơ bàn giao và lần chạy mới

PACKAGE_MANIFEST mô tả gói nhận, không phải danh sách hash bất biến của một cây đang chạy thử. Giữ nguyên gói nhận; lưu lượt xác minh mới vào thư mục run có thời điểm và môi trường riêng. Dùng con trỏ latest được cập nhật sau khi cả phiên hoàn tất; bản ghi run phải liên kết đúng acceptance thuộc phiên đó. Không chạy hai tiến trình ghi cùng trạng thái.

Chạy lại toàn chuỗi có thể sửa con trỏ hiện tại nhưng không chữa thiết kế verifier độc lập. Sau khi sửa code/config, chạy kiểm thử và tạo lại hồ sơ liên quan trong bản vận hành; không sửa manifest cũ chỉ để khớp mã mới. Xác nhận canonical split và dữ liệu reference không đổi khi quy tắc khoa học không đổi.

### 3.3. Một nguồn cấu hình cho mỗi tham số

- `m2_eda.json`: seed, RNG, quy tắc chia/làm tròn, quantile, ddof, top-N, nhóm giờ, min_group_n=30 và đường dẫn outputs cho ban1/ban2, figures, plot_data, drafts.
- `hypotheses_config.json`: alpha=0,05, Holm, các cặp đã khóa, điều kiện tần số kỳ vọng, correction, Fisher alternative và effect size. Giữ các tham số này tại đây, không nhân đôi alpha ở hai file. `m2_eda.json`/README dẫn rõ nguồn cấu hình kiểm định.
- `m2_plot_style.json`: kích thước hình, font, màu, DPI và định dạng.
- `min_group_n=30` là quy ước báo cáo nhóm nhỏ, không thay điều kiện tần số kỳ vọng của Chi-square/Fisher và không tự cho phép xóa quan sát.
- Với split hiện đã khóa: xác thực đúng chuỗi `split_rule` và contract_version; không diễn giải chuỗi bằng eval. Nếu muốn thay quy tắc, chuyển thành tham số có cấu trúc, tăng phiên bản hợp đồng và tái nghiệm thu.

### 3.4. Render có đủ tài nguyên

Renderer dùng staging an toàn cần chép các hình/bảng nhẹ mà QMD thực sự tham chiếu, gồm `Bao cao EDA/figures/...` và phần bảng xuất được chỉ định. Chép cả cấu trúc thư mục tương đối; kiểm tra tài nguyên thiếu trước chạy Quarto. Chỉ thêm phần cần đọc của `Data phai sinh`, không mang toàn bộ Parquet/CSV lớn sang staging. Render không kích hoạt cleaning, split hay huấn luyện. Giữ PDF cũ nếu thất bại. Kiểm thử bằng một fixture hình và bảng có đường dẫn giống cấu trúc EDA.

## 4. Quy ước nội dung dùng cho toàn bài

### 4.1. Đơn vị quan sát và mẫu số

Mỗi bảng/biểu đồ/chỉ số phải ghi: nguồn, đơn vị, phạm vi tập, N và cách tính thiếu.

| Phạm vi | Đơn vị | Cách diễn giải |
|---|---|---|
| Bảng orders nguồn | Một đơn hàng; 3.421.083 đơn | Thiếu thuộc tính trên toàn orders, dùng ở 3.3 |
| Master train | Một sản phẩm trong đơn; 1.384.617 dòng | Thuộc tính đơn lặp theo số sản phẩm, dùng ở kiểm tra Master/3.2 |
| Reference cấp giỏ | Một giỏ/người; số lượng theo manifest đã nghiệm thu | Thuộc tính đơn lấy một lần mỗi giỏ, dùng ở 3.4 |
| Reference cấp dòng | Một sản phẩm–đơn | Tỷ trọng dòng, sản phẩm, reordered; không gọi là tỷ trọng giỏ |

Câu nối thống nhất: “Số thiếu ở mục 3.2 được đếm trên các dòng sản phẩm–đơn của Master train; mục 3.3 đếm trên từng bảng nguồn; mục 3.4 báo theo tập reference và đơn vị quan sát ghi tại mỗi bảng. Vì vậy các số đếm và tỷ lệ này có mẫu số khác nhau.”

Không đưa số reference 11.074/6.541/6.576 từ nhận xét vào bài như kết quả Phong vừa tính. Đối chiếu lại bằng script nhánh và manifest trước khi dùng.

### 4.2. Dtype và môi trường

Chú thích Bảng 3.4: cột “Sau đọc” là kết quả `pd.read_parquet(..., dtype_backend="numpy_nullable")`. Data contract M2 mô tả chế độ đọc mặc định nếu đó là code đang chạy. Phân biệt kiểu Arrow lưu trữ, dtype pandas khi đọc và kiểu ghép khối; đối chiếu giá trị và mask thiếu, không chỉ tên kiểu.

Mục 2.5 dùng bảng môi trường theo từng giai đoạn/lượt: M1 lịch sử, G0 máy gửi, kiểm chứng/EDA Phong. Ghi đúng phiên bản Python/pandas/NumPy/PyArrow/SciPy và lock tương ứng. Không thay số benchmark M1 bằng môi trường mới; requirements có ngưỡng tối thiểu không được gọi là môi trường đã khóa.

### 4.3. API: chứng minh sử dụng, không chèn tên cho đủ

- Merge/concat: mô tả đúng lệnh đang có và phép bảo toàn. `pd.concat` nối danh sách chunk; không viết “6 khối” nếu chưa đo đúng số chunk. `DataFrame.merge` và `pd.merge` là hai cách gọi API liên quan, không coi khác cách viết là sai khoa học.
- `DataFrame.join` có thể làm quan hệ many-to-one qua index; nhận xét “many-to-one nên join không phù hợp” không đúng. Chọn một phép join thật trên reference (ví dụ gắn thống kê sản phẩm theo product_id), kiểm chứng khóa, số dòng và kết quả tương đương. Nếu đề đòi dùng cả ba API, chỉ giải thích lý do không dùng chưa chắc đáp ứng yêu cầu.
- `drop_duplicates` trên cặp user/order để tạo bảng cấp giỏ không phải chứng cứ đã xóa giao dịch trùng. Cleaning hiện từ chối khóa trùng; dữ liệu nghiệm thu không có trùng nên số giao dịch bị xóa là 0. Nếu minh chứng loại trùng, chỉ dùng bản sao/fixture có trùng chính xác, quy tắc rõ; không xóa âm thầm dòng khóa trùng nhưng thuộc tính mâu thuẫn.
- `pd.to_datetime`: không có ngày lịch để chuyển; nêu không áp dụng cho mã ngày 0–6 hoặc giờ 0–23. Không tạo ngày giả cho đủ API.
- `shape`, `info(memory_usage='deep')`, tỷ lệ isna, `describe`, groupby/pivot_table/crosstab/corr: lập bảng “yêu cầu → nơi triển khai → artifact → mục bài”. Bổ sung thao tác còn thiếu vào script báo cáo thực sự, rồi chạy và lưu kết quả; không ghi đã làm nếu chỉ định viết tên hàm.

### 4.4. Missing và ngoại lai

Giữ bộ sáu CSV sạch, không điền mean/mode chỉ để thỏa danh sách ví dụ. Dùng bảng quyết định gọn: nhóm cột, quy tắc, lý do, phạm vi sử dụng tiếp. Nhãn `missing` có sẵn trong danh mục là nhãn nguồn. Nhãn hiển thị “Chưa có tên (ID=...)” chỉ thuộc lớp báo cáo, không sửa mã/tên nguồn. Nếu mô hình cần imputation, fit chỉ trên classifier_fit theo pipeline đã chốt; không học giá trị điền từ test.

Giữ phân biệt token thiếu với tổng ô không dùng được sau parse; số sửa giá trị quan sát với số điền thiếu; quy mô phân vùng với số nhãn khôi phục. IQR toàn Master ở 3.3 chỉ là kiểm toán cấu trúc, không dùng làm ngưỡng chọn mô hình. Phân tích reference báo rõ ngưỡng riêng và quyết định giữ/xử lý có bằng chứng.

## 5. Hình thức, ngân sách trang và hồ sơ nộp

- Giữ tên/thứ tự các mục bắt buộc. Định dạng chung TNR 12 pt, lề chuẩn, giãn dòng 1,3; không giảm chữ/lề để ép trang.
- Chuẩn hóa thuật ngữ và viết tắt: EDA, ERD, IQR, LR, RF, ROC-AUC, CI, CRISP-DM…; giải thích lần đầu, dùng nhất quán sau đó.
- Chọn bảng/hình có bằng chứng và nguồn. Có thể ghép panel nếu chữ còn đọc được ở kích thước in; 300 DPI không tự bảo đảm chất lượng và Plotly không phải điều kiện duy nhất thay cho insight.
- Thay hình 3.5 giả bằng hình thật khi nhánh EDA nghiệm thu. Không đưa style_fixture vào kết quả nghiên cứu.
- Bản gốc Phong hiện có bảng dài ở 3.1–3.2 xuống trang và vài chuỗi mã chen vào cột kế bên. Cần thống nhất độ rộng cột, cách xuống dòng tên kỹ thuật, lặp header cho bảng dài và vị trí caption/nguồn. Đợt vừa rồi chỉ sửa bố cục hai bảng mới của 3.3, chưa sửa toàn bộ bảng cũ.
- 45 trang là ngân sách nhóm, không tự gán là hạn đề. Bản biên tập hiện 40 trang sau tích hợp 3.3, còn chỗ chờ. Phân bổ lại ngân sách trước EDA: thân bài giữ kết quả cốt lõi và lập luận; chi tiết kiểm toán/dictionary/bảng dài chuyển phụ lục với dẫn chiếu. Chuyển sang phụ lục trong cùng PDF không làm giảm tổng trang; cần rút gọn thực sự hoặc xác nhận cách nộp phụ lục riêng nếu yêu cầu toàn văn code khiến vượt ngân sách. Không tự thay toàn văn code bằng link.
- Phụ lục A: toàn văn code thực tế theo yêu cầu, bỏ code minh họa. Chỉ khẳng định PEP 8 sau lint theo cấu hình công bố. Black mặc định 88 ký tự không tự chứng minh giới hạn 79; kiểm tra docstring, imports và phần còn lại, không chỉ line-length.
- Phụ lục B: trích phiên nhật ký thực tế có nội dung P-D-M-V, công cụ và vai trò từng người. Đặt nhật ký đầy đủ tại gốc project nộp; nhật ký Phong không nhận phiên G0 Vương thành của mình.
- Cam đoan/cảm ơn: viết đúng sự thật; phần khẳng định đóng góp và sử dụng công cụ cần người viết xác nhận. Tóm tắt 250–350 từ viết khi có kết quả cuối; không lấp bằng kết quả tưởng tượng.
- Mỗi lần render nghiệm thu mới lưu hash QMD/PDF, số trang, kiểm tra bảng/hình/citation và ngày chạy mới. Các review ngày 19/10 hoặc phiên 3.3 trước đó là hồ sơ lịch sử, không phải chứng nhận bản hiện tại.
- Đường dẫn skill Kilo chỉ là cấu hình công cụ trên máy dùng Kilo, không phải yêu cầu học thuật hay điều kiện chặn EDA; không tự chuyển thư mục skill trên máy Phong dựa vào nhận xét máy khác.

## 6. Điều kiện cho phép bắt đầu 3.4 và điều kiện nộp

Trước 3.4: cây vận hành duy nhất được chỉ rõ; G0 được nghiệm thu tại máy nhận; consumer từ chối acceptance lỗi/cũ; config hai nhánh thống nhất; split không đổi; nguồn môi trường và tài nguyên render rõ; có quy ước mẫu số/dtype và kế hoạch trang.

Sau 3.4–3.6: mỗi số liệu trong QMD truy được về bảng/manifest; EDA chỉ reference; kiểm định theo cấu hình đã khóa với p hiệu chỉnh và effect size; hình có dữ liệu vẽ và 4–5 insight có số đo, giới hạn, hành động dự kiến.

Trước nộp: hoàn thiện các phần đầu/cuối và phụ lục bắt buộc, không còn ô chờ/hình giả; lint/test phù hợp đạt; render kiểm tra toàn bộ; mô tả đúng những gì thực sự đã chạy. Không kết luận “hoàn hảo” hoặc cam kết điểm chỉ từ checklist.

## 7. Trình tự triển khai đề nghị

1. Chuẩn hóa cây vận hành, sửa gate/config/render và kiểm thử G0.
2. Chuẩn hóa văn bản 2.5, 3.2, 3.3, danh mục viết tắt, bảng API và mẫu số; sửa bảng cũ bị tràn.
3. Khóa lại cấu hình và bàn giao hai nhánh EDA; mới tạo các số liệu/hình 3.4–3.6.
4. Tích hợp kết quả, rút gọn và cân đối trang; tiếp tục Chương 4–5 theo thiết kế.
5. Hoàn thiện hồ sơ nộp và nghiệm thu PDF hiện hành.

Bằng chứng đối chiếu gói nhận trong phiên này: `doi_chieu_goi_g0.json`. Văn bản đề được trích từ bản Phong đang giữ trong `Tài liệu/Hướng dẫn/projects.pdf`; tham chiếu nhận xét máy bạn được đối chiếu lại, không mặc nhiên chấp nhận mọi kết luận.
