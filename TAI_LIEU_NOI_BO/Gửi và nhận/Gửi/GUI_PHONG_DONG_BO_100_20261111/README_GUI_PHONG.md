# Gửi Phong — đồng bộ 100% workspace với máy Vương (11/11/2026)

Mục tiêu: thư mục bài trên máy Phong trùng **từng vị trí và từng byte** với bản nộp trên máy Vương (`NOP_BAI_20261111`, 380 tệp). Khi đó, lúc vấn đáp dùng máy nào cũng chạy ra cùng kết quả.

## Trong gói

| Tệp/thư mục | Nội dung |
|---|---|
| `SO_DO_THU_MUC_DONG_BO.txt` | Cây thư mục chuẩn; mỗi tệp có ký hiệu [=] giữ, [~] thay, [+] thêm, kèm hash |
| `DANH_SACH_380_TEP.tsv` | Đường dẫn, SHA-256, kích thước và việc cần làm cho cả 380 tệp |
| `TEP_CAN_CHEP/2521001118_Nhom01_TieuLuan/` | Đúng 223 tệp cần thay hoặc thêm (22.0 MiB), đặt sẵn theo đường dẫn thư mục bài |
| `kiem_dong_bo.py` | Script tự kiểm: so thư mục bài của Phong với bảng 380 tệp |
| `DANH_SACH.txt` | SHA-256 từng tệp trong gói |

Số tệp: giữ nguyên 157, thay 34, thêm 189. Các tệp dữ liệu nặng (CSV gốc, CSV sạch, Master, khoảng 1,4 GB) máy Phong đã khớp nên không gửi lại.

## Các bước

1. Kiểm hash gói theo `DANH_SACH.txt`.
2. **Sao lưu** thư mục bài hiện tại của Phong (chép sang chỗ khác).
3. Chép **nội dung** của `TEP_CAN_CHEP/2521001118_Nhom01_TieuLuan/` đè vào thư mục bài của Phong, cho phép ghi đè.
   - Bước này thay `lock.json` nháp và `m4_lock.py` cũ bằng bản chính thức.
   - Không tạo lại khóa, không chạy `m4_test.py test`.
4. Chạy script kiểm (bằng Python nào cũng được, chỉ dùng thư viện chuẩn):
   ```
   python kiem_dong_bo.py "<đường dẫn tới thư mục bài 2521001118_Nhom01_TieuLuan trên máy Phong>"
   ```
   - Kết quả đạt: `KHỚP 380/380`, không có tệp thiếu hoặc khác.
   - Script cũng liệt kê các **tệp thừa** (có trên máy Phong nhưng không có trong bản nộp), ví dụ `tests/test_m4_crosscheck.py`. Nên chuyển các tệp thừa ra ngoài thư mục bài, để unittest ra đúng 57 test giống máy Vương. Không cần xóa hẳn.
5. Chạy `.\.venv-m2\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"` → phải ra 57/57.
6. Gửi lại kết quả của bước 4 và bước 5 vào `Chung/Gửi và nhận/Nhận/`.

## Lưu ý

- Thư mục `.venv-m2` mỗi máy tự có; không đồng bộ qua gói. Máy Phong dùng Python 3.12.10, thư viện khớp 23/23 với `requirements.txt`.
- Từ lúc này hai máy coi bản nộp 11/11 là chuẩn; không sửa thêm tệp trong thư mục bài.
- Muốn thử đổi tham số khi luyện vấn đáp thì làm trên một bản sao riêng của thư mục bài, giống `VAN_DAP_LIVE_CODE` trên máy Vương.
