# Gói tổng hợp gửi Phong — 04/11/2026 (không nén)

Gói này gom mọi thứ Phong cần cho giai đoạn tiếp theo: kiểm chứng mã Chương 4, đối chiếu kết quả test chính thức, nhận Chương 4 đã viết vào QMD, và viết Chương 5, Tóm tắt. Các gói rời trước đó (mã, kết quả test, QMD, thiết kế) đã nằm trong gói này, nên chỉ cần dùng gói này.

## Có gì trong gói

| Thư mục hoặc tệp | Nội dung | Phong làm gì |
|---|---|---|
| `01_THIET_KE_VIET_CHUONG4_5_VA_PHAN_CONG.md` | Phân công mới (Vương viết Chương 4; Phong viết Chương 5 và Tóm tắt), thiết kế chi tiết Chương 4 và 5, bản đồ bằng chứng, tám điểm lệch ở Chương 1 và 2 | **Đọc đầu tiên**, rồi xác nhận phân công (mục 1) |
| `02_THONG_NHAT_CHUONG4_LAN1.md` | Biên bản lần 1 đã gộp, có các dấu `[x]` của Phong, ghi khóa và lượt chấm test | Đọc, tick các ô còn lại nếu đồng ý |
| `CODE_CHUONG4/` | Toàn bộ mã Chương 4 (scripts, tests, configs, `requirements.txt`) kèm `README_CODE_CHUONG4.md` và `DANH_SACH.txt` | Kiểm chứng: hash, unittest, đọc mã. Không chạy lại lượt chính thức |
| `KET_QUA_TEST/` | Kết quả chấm tập test chính thức (`ranking_metrics_test.csv`, `paired_bootstrap_test.csv`, `results_test.json`, `recall_at_k_test.csv`, `classifier_metrics_test.csv`, `confusion_matrix_test.csv`, `basket_metrics_test.csv`), hình Recall@K, `lock.json` chính thức, `test_started.json`; `README_KET_QUA_TEST.md` có bảng số để đối chiếu | Đối chiếu ngẫu nhiên 10 số trước khi đưa vào Chương 5 |
| `TIEU_LUAN/` | `2521001118_Nhom01_TieuLuan.qmd` đã có **Chương 4 (4.1 đến 4.6)**, hai hình ở `assets/chuong4/`, PDF dựng từ bản này (58 trang) | Dùng làm bản chính của QMD; viết Chương 5 và Tóm tắt vào đây |
| `DANH_SACH.txt` | SHA-256 mọi tệp trong gói | Kiểm hash |

## Điều cần biết

- **Toàn bộ mã Chương 4 chạy trên máy Vương** (`.venv-m2`, Windows 11, RAM 24 GB). Phong kiểm chứng, không chạy lại các lượt chính thức và **không chạy `m4_test.py test`** (cổng khóa từ chối vì test đã được chấm một lần).
- **Khóa chính thức** lúc 16:10:47 ngày 04/11, hash `lock.json` bắt đầu `e38b04f2`; **tập test chấm một lần** lúc 16:11:02 đến 16:17:37. Mọi số Chương 4 và 5 lấy từ lượt này và từ các tệp validation đã đối chiếu.
- **QMD:** Chương 4 do Vương viết trực tiếp vào bản này (thay các ô chờ). Dùng bản này làm bản chính để hai bản không lệch nhau; nếu Phong đang giữ bản QMD khác thì ghép Chương 4 từ bản này.
- Hình Recall@K giữ đúng bản do chương trình test sinh (khớp hash trong `results_test.json`); hình importance đã vẽ lại thấp hơn từ CSV để vừa ngân sách trang.

## Việc của Phong, theo thứ tự

1. Kiểm hash từng thư mục theo `DANH_SACH.txt` (gói này và `CODE_CHUONG4/DANH_SACH.txt`).
2. Đọc `01_THIET_KE...` và xác nhận phân công.
3. Đối chiếu 10 số trong `KET_QUA_TEST` với bảng trong `README_KET_QUA_TEST.md` và với các bảng ở Chương 4 trong `TIEU_LUAN`.
4. Kiểm chứng mã: chép `CODE_CHUONG4` vào máy Phong đúng cấu trúc thư mục, chạy `.\.venv-m2\Scripts\python.exe -m unittest discover -s tests -v`, đọc mã theo mục "ĐỌC NHANH" ở đầu mỗi tệp; báo phát hiện cho Vương, không sửa tệp trong `CODE_CHUONG4`.
5. Đọc Chương 4 trong QMD, báo chỗ sai hoặc khó hiểu.
6. Viết **Chương 5** (5.1 đến 5.4) và **Tóm tắt** theo mục 5 và 7 của tệp thiết kế; sửa các điểm lệch ở Chương 1 và 2 (mục 3 của tệp thiết kế).
7. Phần chữ trong QMD tính sau theo kế hoạch hai bạn; cắt Chương 3 và rà số trang (hiện 58 trang, ngân sách 45) làm sau khi có Chương 5.

## Lưu ý về số trang

Chương 4 chiếm 9 trang (trang 46 đến 54 của PDF kèm theo). Tổng 58 trang còn vượt ngân sách 45: Chương 3 còn 29 trang (cần khoảng 17) và Chương 1 đến 2 khoảng 16 trang (ngân sách 13); Chương 5 sẽ thêm khoảng 3 trang.
