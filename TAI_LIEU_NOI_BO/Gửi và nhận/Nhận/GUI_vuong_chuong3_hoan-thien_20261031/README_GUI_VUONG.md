# Phong gửi Vương: Chương 3 đã hoàn thiện nội dung

Ngày 31/10/2026.

- QMD chính và PDF toàn bài nằm ở gốc gói; PDF toàn bài 51 trang, các chương ngoài Chương 3 vẫn còn phần chờ.
- Bản Chương 3 riêng nằm trong output/hoan_thanh_chuong3: 30 trang, giữ số trang và tham chiếu của toàn bài.
- Đã ghép 3.4–3.6, đủ năm insight và hình, bổ sung mức nền 210 cặp và diễn giải kiểm định. KET_QUA.md ghi phạm vi, kiểm tra và phần còn lại.
- assets/chuong3 là hình vector được QMD tham chiếu; phải chép cùng QMD. references.bib bổ sung Cohen (1988). styles và logo kèm để render.
- Các CSV/JSON và hình gốc kèm theo để kiểm tra số liệu; doi_chieu_vuong là bảng đã nhận từ Vương, không phải dữ liệu tính mới của Phong.
- scripts/render_pdf.py và configs/render_resources.json là bản hiện dùng để render, KHÔNG phải bản code rút gọn mới. Đọc diff trước khi thay thế trên máy Vương.
- lift_baseline.csv nằm trong hồ sơ đối chiếu; chưa thay đổi pipeline khoa học của Vương.
- Chưa rút Chương 3 xuống ngân sách 17 trang; chưa nghiệm thu lại toàn luồng bằng code mới của Vương.
- Không kèm dữ liệu gốc/Parquet lớn, môi trường Python, ảnh xem thử, bản sao lưu hay nhật ký.

Giải nén vào thư mục riêng, kiểm tra DANH_SACH.txt rồi đối chiếu trước khi chép vào dự án. Giữ cấu trúc assets và các tài nguyên theo QMD; không ghi đè toàn bộ dự án. Có thể chạy python scripts/render_pdf.py --no-open khi máy có Quarto và XeLaTeX.
