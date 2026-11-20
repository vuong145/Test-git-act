# Cây vận hành TLCK

- Gốc workspace làm việc/nộp theo thiết kế hiện tại: thư mục TLCK này.
- Bài chính: `2521001118_Nhom01_TieuLuan/2521001118_Nhom01_TieuLuan.qmd`;
  PDF cùng tên là đầu ra. Không có QMD bản chính ở gốc TLCK.
- Nhật ký chuẩn: `nhật ký làm việc.md` tại gốc TLCK; không tạo bản nhật ký thứ hai
  dễ lệch trong thư mục bài. Nếu đổi gốc đóng gói nộp, phải kèm nhật ký tại gốc mới.
- Script/config/dữ liệu vận hành nằm trong `2521001118_Nhom01_TieuLuan/`.
- Môi trường `.venv-m2`, phiên bản khóa trong `2521001118_Nhom01_TieuLuan/requirements.txt`;
  không coi đây là môi trường của lượt benchmark M1 lịch sử.
- Tài liệu của Phong trong `Chung/Gửi và nhận/Nhận/` là nguồn phản biện;
  các đường dẫn/số trang trên máy Phong không thay thế trạng thái trên máy này.
- Thư mục `BAN_GIAO_*` và ZIP là snapshot để gửi. Không chạy/sửa bản sao rồi
  coi PACKAGE_MANIFEST là manifest cập nhật của cây vận hành.

Thứ tự chạy đầy đủ và các cổng kiểm tra: `2521001118_Nhom01_TieuLuan/scripts/README.md`.
Từ thư mục bài, xuất PDF:

```powershell
.\.venv-m2\Scripts\python.exe scripts/render_pdf.py --no-open
```

Code trước đợt rút gọn ngày 31/10/2026 lưu ở `Chung/archive/code_cu_truoc_rut_gon_20261031/`.

Đây vẫn là bài đang triển khai: 3.4–3.6, Chương 4–5, tóm tắt cuối cùng và
toàn văn code/phụ lục nhật ký phải hoàn thiện theo thực nghiệm. Không coi
G0 passed hoặc PDF render thành công là bài đã đạt mọi yêu cầu nộp.
