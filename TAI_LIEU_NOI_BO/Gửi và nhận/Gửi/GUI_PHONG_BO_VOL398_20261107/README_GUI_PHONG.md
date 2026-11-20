# Gửi Phong — bỏ số bộ sách của Hosmer (07/11/2026)

- **Thay đổi:** `references.bib` mục `hosmer2013` bỏ dòng `volume={398}`.
- **Lý do:**
  - Thông tin của nhà xuất bản và các thư viện chỉ ghi: tái bản lần 3, Wiley 2013, thuộc bộ Wiley Series in Probability and Statistics. Không nơi nào ghi số 398.
  - Số này chỉ thấy ở một nhà sách ("Del 398").
  - APA 7 không ghi số trong bộ sách cho sách một tập.
- **Danh mục tài liệu tham khảo nay ghi:** Hosmer, D. W., Lemeshow, S., & Sturdivant, R. X. (2013). *Applied logistic regression* (3rd ed.). John Wiley & Sons.
- **PDF:** 44 trang; từ bìa đến hết Chương 5 là 42 trang; không có `??`.
- **Ghi nhận khác:**
  - Câu phân công trong Lời cam đoan đã duyệt.
  - Dòng "Nguồn" của Bảng 4.6 giữ nguyên.
- **Bản nộp:** đã tạo bản nộp đã dọn tại `TLCK/NOP_BAI_20261107/2521001118_Nhom01_TieuLuan/`, gồm 380 tệp, 1,46 GiB. Đã bỏ: `.venv-m2`, `__pycache__`, `.mplcache`, lượt làm sạch cũ ngày 19/10, các tệp kiểm bản nháp trong `review/` và các tệp tạm.
- **Kiểm tra:** 57/57 test đạt; `lock.json` khớp 16/16; liên kết nhật ký 72/72.
- **Phong cần làm:** kiểm hash theo `DANH_SACH.txt`, rồi chép `references.bib` vào thư mục bài.
- Ghi chú: ngoài dòng `volume`, tệp bib chỉ được đồng nhất ký tự xuống dòng về CRLF (nội dung không đổi); diff bỏ qua khác biệt này.
