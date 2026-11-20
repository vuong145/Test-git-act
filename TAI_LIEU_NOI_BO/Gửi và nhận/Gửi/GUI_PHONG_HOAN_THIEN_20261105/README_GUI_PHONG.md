# Gửi Phong — Bản hoàn thiện tiểu luận (05/11/2026 tối)

Vương gửi Phong bản tiểu luận đã hoàn thiện nội dung, kèm tệp toàn bộ mã nguồn, nhật ký làm việc và mọi tệp đã đổi trong phiên 05/11 tối. Nhờ Phong **kiểm tra và xác nhận** theo danh sách ở mục 4, rồi gửi lại theo mục 5.

Thư mục không nén. Kiểm SHA-256 của từng tệp với `DANH_SACH.txt` trước khi dùng.

---

## 1. Trong thư mục này có gì

| Thư mục | Nội dung |
|---|---|
| `01_DE_DOC/` | `2521001118_Nhom01_TieuLuan.pdf` (bản mới, 46 trang), `nhật ký làm việc.md` (Vương, đã thêm phiên 05/11 tối), `toàn bộ mã nguồn.md` (48 tệp code, cấu hình, test; đánh số dòng, có ghi chú từng tệp) |
| `02_TEP_DA_DOI_theo_duong_dan_thu_muc_bai/` | Mọi tệp trong thư mục bài đã đổi so với bản Phong đang giữ, đặt đúng đường dẫn tương đối như trong `2521001118_Nhom01_TieuLuan/` để chép đè |
| `03_SO_SANH_truoc_sau/` | Bản so sánh dạng `diff` của QMD, `apa.csl`, hai script vẽ; bản gốc `m2_plot_multivariate.py` trước khi sửa; PDF cũ 61 trang để đối chiếu |

## 2. Kết quả chính

- PDF **46 trang; từ bìa đến hết Chương 5 = 44 trang** (bản 05/11; bản 06/11 xem mục 4c) (giới hạn 45); mục lục 2 trang; không có `??`.
- Chương 3 từ 29 xuống **14 trang** (trang 16–29); Chương 4 trang 30–39; Chương 5 trang 40–44; tài liệu tham khảo 45–46.
- Không chạy lại bước sinh dữ liệu nào ngoài hai script vẽ hình. Không đụng tệp trong khóa, không chạy lại test.
- Kiểm trên máy Vương sau khi sửa: 57/57 test đạt; `lock.json` 16/16 tệp khớp; `hashes.json` common 6/6, ban2 10/10, M4 6/6.

## 3. Những gì đã đổi

**a) Chương 3 rút gọn (QMD).** Gộp từ điển dữ liệu vào Bảng 3.1; gộp hai bảng thống kê giỏ thành Bảng 3.7; bỏ bảng 10 quầy (thay bằng một câu dẫn `aisle_summary.csv`); giữ đủ bảng ghép, lược đồ, benchmark, quy tắc làm sạch, trước–sau, ngành Top-10, Top-N, kiểm định; giữ mọi số trong bảng. Bảng chuyển sang float `[htbp]`; ngưỡng xếp float chỉ nới trong Chương 3. Lời văn rút ý lặp, giữ số và kết luận. **Phần văn của Phong cũng bị rút** (mô tả Hình 3.4–3.7, I4, I5, mục 3.6) — xem `03_SO_SANH_truoc_sau/2521001118_Nhom01_TieuLuan.qmd.diff`.

**b) Sáu hình Chương 3 vẽ lại** (rộng giữ 6,3 inch = 16 cm, chữ 12 pt, thấp hơn; tổng chiều cao ~38 → ~24 inch):
- `scripts/m2_plot_univariate.py` (Vương): Hình 3.2, 3.3 thấp hơn.
- `scripts/m2_plot_multivariate.py` (**tệp của Phong, Vương sửa theo quyết định của Vương ngày 05/11**): Hình 3.4 và 3.5 đặt hai khung cạnh nhau, bỏ tiêu đề dài (số N nằm ở chú thích hình); Spearman và Pearson hiển thị 3 chữ số; heatmap lift in "ID tên ngành" trên trục tung (bỏ đoạn chú giải 21 ID trong bài). Không đổi `configs/m2_plot_style.json` (tệp khóa).
- Hai script đã chạy lại: `check_hashes` đạt; `plot_data/` giống từng byte bản cũ; 6 PDF trong `assets/chuong3/` giống từng byte bản code sinh.

**c) Sửa diễn giải (QMD).**
- 3.2: thêm câu nêu prior 32.434.489 dòng đọc theo khối 250.000 dòng và kiểm tra quan hệ qua SQLite; bước dựng Master giữ bản trước ghi và bản đọc lại để đối soát từng ô; chưa đo RSS đỉnh riêng.
- I1: đối chiếu với Chương 4 (giỏ một sản phẩm không vào đánh giá; 1.387 giỏ validation, `dataset_description.csv`).
- I2: thêm tỷ lệ mua lại quan sát được trên reference (`department_summary.csv`): produce 66,31%, dairy eggs 67,32%, mức chung 59,67%, pantry 36,13%; ghi giới hạn ~30% dòng thiếu `reordered`.
- 4.5: hệ số LR làm tròn lại 0,192 (lift lớn nhất) và 0,140 (confidence lớn nhất) theo `lr_coefficients.csv`; thêm câu phân biệt Average Precision trên cặp giỏ–ứng viên với Recall@10 theo giỏ; câu "đóng góp trực tiếp của cỡ giỏ trong LR không đổi thứ tự xếp hạng trong giỏ".
- 4.6: câu kết luận RF so với Rules đổi thành "khoảng tin cậy bootstrap 95% không chứa 0 nhưng mức cải thiện nhỏ và chưa được kiểm chứng qua nhiều lần chia tập".
- 5.1 (khung hòa vốn): bỏ khoảng ΔH 0,004–0,008 (không quy đổi được từ khoảng tin cậy Recall@10 vì Recall chia cho số sản phẩm bị che từng giỏ), giữ ΔH ≈ 0,00627 là ước lượng điểm; phần chi phí viết lại thành **một kịch bản giả định**: thuê trọn máy 16 vCPU, 0,05 USD/vCPU-giờ = 0,80 USD/giờ; (63,55 − 6,19)/24.854 ≈ 2,31 ms/giỏ → 0,641 giờ mỗi triệu giỏ → ≈ 0,51 USD; mức lợi ích cần có 0,51/6.270 ≈ 8,2 × 10⁻⁵ USD mỗi sản phẩm trúng thêm ngoại tuyến; ghi rõ các giả định; bỏ câu "chi phí điện toán nhiều khả năng không phải điểm nghẽn".

**d) Lời cam đoan và Lời cảm ơn** (trang ii): đã viết thay cho hai ô chờ.

**e) Tài liệu tham khảo.** `styles/apa.csl` thêm locale `vi`: in "(2nd ed.)", "(3rd ed., Vol. 398)" thay cho "2nd a.b", "Vol 398". Thêm `\interlinepenalty=10000` trước danh mục nên không mục nào bị tách trang. `references.bib` **không đổi**. Chữ "từhttps" khi trích văn bản PDF là lỗi của công cụ trích; ảnh trang vẫn có khoảng trắng nên giữ `urldate`.

**f) `scripts/m4_validate.py`** (SHA-256 `42f00253…`): bản đã sửa bốn dòng chú thích ngày 04/11 ("test bị loại ngay sau khi đọc"); khác byte với bản Phong đang giữ nếu Phong chưa nhận. Không đổi lệnh.

## 4. Nhờ Phong kiểm tra và xác nhận

1. **Kiểm hash** mọi tệp với `DANH_SACH.txt`.
2. **Sao lưu** thư mục bài trên máy Phong, rồi chép `02_TEP_DA_DOI_theo_duong_dan_thu_muc_bai/` đè vào `2521001118_Nhom01_TieuLuan/`. Từ nay coi QMD này là **bản chính** (SHA-256 `78a77ae1…`).
3. **Chạy unittest** trên máy Phong: `python -m unittest discover -s tests -p "test_*.py"` (kỳ vọng 57/57 đạt). Có thể chạy thêm kiểm chéo 50 giỏ như lần trước.
4. **Đọc và xác nhận các phần của Phong:**
   - a. Phần văn của Phong trong Chương 3 sau khi rút (Hình 3.4–3.7, I4, I5, mục 3.6): còn đúng ý không.
   - b. Thay đổi trong `scripts/m2_plot_multivariate.py` (xem `m2_plot_multivariate.py.diff`): đồng ý giữ không; đồng thời chốt THONG_NHAT mục 6.6 (kích thước hình vẽ lại).
   - c. **Câu phân công trong Lời cam đoan** (trang ii): đúng với thực tế không.
   - d. **Hosmer "Vol. 398"** trong `references.bib` (dòng 46, `volume={398}`): chưa xác minh được. Sách thuộc Wiley Series in Probability and Statistics; nếu 398 là số trong bộ sách thì APA 7 không ghi cho sách một tập, nên bỏ `volume`. Phong xem trang bản quyền của sách rồi quyết.
5. **Đối chiếu 10 số ngẫu nhiên** trong phần Phong viết với CSV nguồn.
6. **Ghi những gì còn thiếu hoặc sai** (nội dung, số liệu, định dạng, tệp cần Vương gửi thêm).

Đã biết, chưa làm (không cần Phong báo lại): trang PDF 39 chỉ có đoạn "Giới hạn" cuối Chương 4; PEP 8 cho tệp không khóa; chuẩn bị bản sao chạy demo vấn đáp.

## 4b. Cập nhật 06/11: nhật ký và mã nguồn nằm trong thư mục bài

- `nhật ký làm việc.md` và `toàn bộ mã nguồn.md` nay đặt **trong** `2521001118_Nhom01_TieuLuan/` (không còn ở gốc `TLCK/`); bản trong `02_...` đã kèm hai tệp này.
- 72/72 liên kết trong nhật ký đã sửa và sống: liên kết vào thư mục bài bỏ tiền tố `2521001118_Nhom01_TieuLuan/`; liên kết vào `Chung/` (không nộp) trỏ sang thư mục mới `TAI_LIEU_NOI_BO/` trong thư mục bài, chỉ chứa đúng các tài liệu được nhật ký liên kết (6,3 MB; có `README.md`). Chép `02_.../TAI_LIEU_NOI_BO/` vào thư mục bài trên máy Phong để liên kết mở được.
- Nhãn hiển thị của liên kết vẫn ghi đường dẫn cũ `Chung/...` (đúng với nơi tài liệu nằm lúc ghi nhật ký); đích liên kết đã đổi.

## 4c. Cập nhật 06/11: Chương 4 gọn lại, cả bài 44 trang

- Ngưỡng xếp hình nới ở Chương 3 nay kéo dài hết Chương 4 (trả về mặc định trước Chương 5), nên hai hình Chương 4 không còn để ¼ trang trống.
- Bỏ các câu lặp trong Chương 4 (phần văn của Vương): câu liệt kê các mục ở đầu chương; khoảng dao động ba lượt đo ở nguồn Bảng 4.3; câu thời gian dựng ma trận và sinh luật; đoạn mô tả nội dung hai giỏ ví dụ; câu "Recall tính trên toàn bộ…; Precision chia cho K" (đã có ở nguồn Bảng 4.5); câu ngưỡng F1 (đã có trong Bảng 4.6); ở 4.6: rút Câu hỏi 3, bỏ ý trùng 4.4 ở Câu hỏi 4, bỏ câu importance cuối đoạn Chi phí, rút đoạn Giới hạn (bỏ ý nhãn 0, thời gian–RAM phụ thuộc máy, gộp ý một lượt chia).
- Kết quả: **PDF 44 trang; từ bìa đến hết Chương 5 = 42 trang**; Chương 4 trang 22–29 (8 trang, trang cuối đầy); Chương 5 trang 30–34; tài liệu tham khảo 43–44 (PDF); không có `??`. QMD và PDF trong gói đã thay bằng bản mới; `03_.../2521001118_Nhom01_TieuLuan.qmd.diff` so với bản trước khi hoàn thiện.
- Còn một chỗ nhỏ: dòng "Nguồn" của Bảng 4.6 nằm đầu trang sau bảng.

## 5. Gửi lại cho Vương

Tạo thư mục **không nén** `Chung/Gửi và nhận/Nhận/Gửi Vương_Kiểm tra bản hoàn thiện_20261105/` gồm:
- `KET_QUA_KIEM_TRA.md`: kết quả từng bước ở mục 4 (đạt/không đạt, chỗ cần sửa kèm trang hoặc dòng QMD, câu đề xuất nếu có).
- Các tệp Phong sửa (nếu có), đặt đúng đường dẫn tương đối như thư mục bài; ghi rõ sửa gì.
- Nhật ký nộp riêng của Phong (bản cuối).
- `DANH_SACH.txt` có SHA-256 các tệp gửi.
