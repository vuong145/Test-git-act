# Tài liệu nội bộ: hồ sơ quá trình làm bài

Trong lúc làm bài, nhóm làm việc trong một thư mục chung `Chung/` (không nộp nguyên thư mục này vì có dữ liệu lớn và nhiều bản sao trùng). Thư mục `TAI_LIEU_NOI_BO/` chép lại phần dùng làm minh chứng, giữ cấu trúc đường dẫn như trong `Chung/` (`archive/`, `Gửi và nhận/`, `Hướng dẫn chung/`). Mã và dữ liệu chạy được nằm ở thư mục bài, không phụ thuộc thư mục này.

## `Gửi và nhận/` — trao đổi giữa hai thành viên

- `Gửi/`: các gói Vương gửi Phong. `Nhận/`: các gói Phong gửi Vương (thư mục bắt đầu bằng "Gửi Vương_…" hoặc tệp lẻ).
- Mỗi gói thường có `README_GUI_PHONG.md`, `README_GUI_VUONG.md` hoặc `ĐỌC_TRƯỚC.md` (nội dung gửi, việc cần làm), `DANH_SACH.txt` hoặc `SHA256.txt` (SHA-256 các tệp trong gói), các tệp `.diff` (thay đổi so với bản trước), nhật ký chạy kiểm thử (`*.log`) và các biên bản xác nhận, duyệt (ví dụ đồng ý khóa trước khi chấm test ngày 04/11, xác nhận bản chốt ngày 07/11, kiểm tra bản chốt V2 ngày 11/11).
- Trong `Nhận/` có giữ các tệp `.py` Phong gửi (bản đầu của mã phân tích đa biến, kiểm định, Pipeline phân loại, chấm test, kiểm thử). Đây là bản tại thời điểm gửi; bản cuối nằm trong `scripts/` và `tests/` của thư mục bài.
- **[`DANH_MUC_MINH_CHUNG.tsv`](<Gửi và nhận/DANH_MUC_MINH_CHUNG.tsv>)** liệt kê từng tệp theo thứ tự thời gian: ngày sửa gốc trên máy của Vương, chiều gửi, gói, đường dẫn, dung lượng và SHA-256. Khi tải từ GitHub, ngày của tệp là ngày tải về, nên ngày gốc được ghi trong bảng này và trong tên gói (`…_20261104`).

**Đã lược bỏ** khi chép từ `Chung/Gửi và nhận/` (khoảng 1,5 GB, hơn 1.500 tệp): tệp ZIP (trùng với thư mục cùng tên), dữ liệu và kết quả (CSV, Parquet, mô hình `.joblib`), hình và PDF bản nháp, bản sao nguyên workspace bên trong gói (bản cũ của tệp đã có trong bài), tệp trùng nội dung (chỉ giữ bản sớm nhất), bản tự chấm theo barem, và nhật ký riêng của Phong (Phong tự nộp). Còn lại 155 tệp, khoảng 1,7 MB.

**Hai chỗ rút ngắn đường dẫn** (để đường dẫn đầy đủ khi tải về Windows không vượt 260 ký tự): gói `GUI_PHONG_DOI_CHIEU_TOAN_BO_V2_20261111` trong `Chung/` nằm lồng bên trong thư mục `GUI_PHONG_BAN_CHOT_20261107`, ở đây được đặt cùng cấp trong `Gửi/`; tệp `THONG_NHAT_CHUONG4_LAN1_PHONG_XAC_NHAN_20261104.md` được đặt thẳng trong gói `Gửi Vương_Mã chấm test đã rà và biên bản_20261104` thay vì trong thư mục con `Chung/Hướng dẫn chung/` của gói. Nội dung và ngày sửa không đổi.

## Các thư mục khác

- `Hướng dẫn chung/`: thiết kế và kế hoạch đã thống nhất (Chương 3, Chương 4).
- `archive/code_cu_truoc_rut_gon_20261031/`: các tệp mã cũ trước đợt rút gọn ngày 31/10 mà nhật ký nhắc tới (không phải toàn bộ bản lưu trữ).
- `archive/truoc-*`: bản sao lưu trước mỗi thay đổi lớn (QMD, PDF, tệp băm).
- `README_WORKSPACE.md`: ghi chú cấu trúc workspace tại phiên 30/10 (đã cũ, giữ vì nhật ký liên kết tới).
