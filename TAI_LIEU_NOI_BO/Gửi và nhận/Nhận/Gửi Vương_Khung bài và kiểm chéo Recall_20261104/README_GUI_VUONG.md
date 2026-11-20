# Gửi Vương - Khung bài và kiểm chéo Recall, 04/11/2026

Đã có khung viết 4.3.2–4.5 và script kiểm Recall độc lập; không gọi evaluate/hàm khớp luật của Vương. Test tính tay mới đạt 1/1 (0,046 giây). Đây là test bổ sung, không phải bằng chứng 50 giỏ thật đã khớp hoặc bộ 55 test đã chạy.

Chép các file tương ứng vào dự án có scripts/project_io.py và môi trường đã khóa phiên bản. Chỉ chạy trên nguồn gói A đã kiểm manifest và cấu hình đã đối chiếu; các tham số mặc định dưới đây là cấu hình Vương đề nghị, chưa tự xác nhận lock.

```powershell
& .venv-m2/Scripts/python.exe -m unittest discover -s tests -p test_m4_crosscheck.py -v
& .venv-m2/Scripts/python.exe scripts/m4_crosscheck.py --data-dir 'DATA/Data phai sinh/M4' --metrics 'BAO CAO/Bao cao mo hinh/basket_metrics_validation.csv' --top-n 1000 --min-count 20 --max-len 2 --confidence 0.05
```

Script lọc validation khi đọc Parquet, chọn đúng 50 giỏ eligible theo order_id tăng, tính lại Top-10 và Recall. Xuất recall_comparison.csv, rankings_independent.csv, verification.json (hash nguồn, cấu hình và trạng thái) vào output/kiem_cheo_rules_50. Lệch >1e-12 thì dừng. Không ghi đầu ra thành công khi chưa có nguồn.

Hiện thư mục Nhận máy Phong có văn bản THONG_NHAT_CHUONG4_LAN1_20261104.md nhưng chưa có gói A, features_fit hoặc basket_metrics_validation. Do đó chưa chạy classifier trên gói A và chưa kiểm 50 giỏ thật. Theo tài liệu mới dùng gói A thay pilot; khi thử trên Phong vẫn dùng mẫu nhỏ theo quy tắc được ghi lại. Cần gửi gói A kèm code hiện hành, schema thể hiện trong Parquet, cấu hình, đầu ra validation, bảng Rules Top-10 của 50 giỏ và manifest.

Phần importance/hệ số/hình tự tạo đã hoàn thành ở gói trước, không làm lại. Khung bài chưa ghi kết quả test hoặc đưa số validation chưa đối chiếu vào QMD. Không ghi nhật ký. Gói nhẹ để nguyên thư mục, không nén.
