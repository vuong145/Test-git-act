# Kết quả xử lý phản biện — cây Vương, 29/10/2026

Đối chiếu phương án của Phong nhưng chỉ sửa cây vận hành trên máy Vương.
Không ghi đè snapshot/ZIP cũ; không gọi thông tin máy Phong là kết quả máy này.

| Vấn đề | Đã xử lý / bằng chứng |
|---|---|
| Render mất hình EDA | stage_resources giữ đường dẫn tương đối; config tài nguyên nhẹ; thiếu/ngoài gốc/quá lớn bị từ chối. Đã render Quarto thật với hình EDA và bảng nhẹ ở Data phai sinh |
| Hash treo khi verify riêng | runs/verification và runs/environment bất biến; latest chỉ trỏ phiên committed. Pipeline lưu đường dẫn acceptance riêng của phiên, không bị đổi bởi verify mới |
| Fail-open | verifying trước khi đọc; lỗi/gián đoạn → failed; consumer yêu cầu state/acceptance/run_id/manifest và toàn chuỗi hash. 10 regression tests đạt, gồm assertion lỗi dù input hash đúng |
| Config nhánh thiếu | outputs, min_group_n=30, hypotheses_config; alpha/Holm/Fisher chỉ có một nguồn trong hypotheses_config.json |
| split_rule không kiểm tra | Xác thực đúng chuỗi và contract_version; không eval chuỗi |
| Dtype | QMD ghi rõ Sau đọc là numpy_nullable; G0 contract nêu đọc mặc định |
| Mẫu số thiếu | Phân biệt orders, dòng Master và giỏ/dòng reference; script kiểm tra xuất số liệu kèm đơn vị/mẫu số |
| Môi trường | M1 lịch sử và G0 ghi riêng; không nhận requirements khoảng phiên bản là lock |
| API | Nêu merge/concat đúng code; join thật ở bảng giỏ; trace shape/info/isna/describe; duplicates không bị giả thành giao dịch đã xóa; không tạo ngày lịch giả |
| Mẫu số/giả định khoa học | Chia tập, reference và bảng giỏ không đổi byte; không thêm phân tích test/kiểm định nghiên cứu |
| Hình thức | Giữ 12 pt, bỏ hình giả và code phụ lục minh họa, thêm viết tắt, bỏ khẳng định PEP 8 chưa có lint |
| Ngân sách | Hủy dự trù Chương 3 sáu trang; có NGAN_SACH_TRANG_VA_API.md, không tự tách phụ lục riêng hoặc ép font |
| Nhật ký | Bổ sung phiên thực ở gốc TLCK, đúng công cụ Codex; không gán thao tác máy Vương cho Phong |
| Review cũ | Giữ nguyên hồ sơ lịch sử; review_index.json trỏ kiểm tra mới gắn hash QMD/PDF |

PDF hiện hành: 37 trang; Chương 1–2 vẫn 7 trang. Bảy bảng 3.1–3.7 giữ
12 pt danh định (PDF đo khoảng 11,96 bp); quét biên không phát hiện ký tự
vượt vùng kiểm tra, đã xem hình render các trang sửa bố cục.

## Cách nghiệm thu mới

Trong thư mục bài, dùng .venv-m2 để chạy m2_run_foundation.py. Khi chỉ nhận gói,
chạy m2_verify_foundation.py và m2_check_environment.py. Đọc README_M2 mới;
không còn dùng foundation_acceptance.json/foundation_run.json cũ ở gốc common.
Consumer phải dùng load_foundation(), không thay bằng load_foundation_inputs().

## Chưa được nhận là hoàn tất

Các mục C/D trong phương án là việc theo giai đoạn: 3.4–3.6, Chương 4–5,
insight thật, tóm tắt cuối, cam đoan tác giả xác nhận, lint toàn dự án,
toàn văn code và trích nhật ký hoàn chỉnh trước nộp. Bản này không bịa kết quả
để lấp chỗ chờ hoặc tự cam kết mức điểm. Phụ lục hiện ghi rõ chưa hoàn tất,
không còn nhúng code minh họa như thể là code thực tế.

Gói bàn giao sửa có hậu tố DA_SUA; bản BAN_GIAO_G0_2026-10-29 cũ chỉ là snapshot
lịch sử. Agent nhận phải đọc hướng dẫn ghép, kiểm tra xung đột QMD và code,
không ghi đè mù bản của Phong.
