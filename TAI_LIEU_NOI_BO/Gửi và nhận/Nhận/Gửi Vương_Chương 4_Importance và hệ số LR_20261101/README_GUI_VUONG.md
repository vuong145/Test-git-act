# Gửi Vương - Importance, hệ số LR và hình mẫu

Ngày 01/11/2026. Hoàn thành bước độc lập của Phong trên dữ liệu tự tạo. Không dùng dữ liệu nghiên cứu, không viết nhật ký, không thay QMD/PDF bài chính.

## Nội dung và chạy lại

- scripts/m4_interpret.py: importance cho LR/RF bằng AP, 10 lần hoán vị seed 44; xuất hệ số LR theo đúng thứ tự biến sau tiền xử lý; vẽ 2 hình mẫu.
- tests/test_m4_interpret.py: 4 test mới. Toàn workspace đạt 41/41 test (37 trước đó +4), lần chạy 01/11/2026 mất 4,896 giây.
- Gói kèm các module phụ thuộc của Phong, project_io.py, requirements.txt và cấu hình hình để đối chiếu. Nếu đã có bản cùng hash thì không cần chép lại; không ghi đè file phía Vương có thay đổi riêng.
- Các CSV, JSON và hình dưới output/ch4_phong_importance_20261101 là kết quả tự tạo. Không dùng các số này làm kết quả Chương 4 chính thức.

Tại gốc dự án có G0 và môi trường đã đồng bộ:

```powershell
$env:PYTHONUTF8='1'
& .venv-m2/Scripts/python.exe -m unittest discover -s tests -p 'test_m4_interpret.py' -v
& .venv-m2/Scripts/python.exe scripts/m4_interpret.py --demo
```

Đường dẫn tương đối theo gốc dự án, không gắn máy Phong. Demo kiểm hash G0 rồi chỉ sinh dữ liệu giả; không đọc Master hoặc tập test. Chạy lại ghi đè riêng các kết quả demo này.

## Đầu ra và cách giải thích khi vấn đáp

1. importance_SYNTHETIC.csv: 14 dòng (7 biến × LR/RF), mức giảm AP trung bình và SD. Hoán vị ngành ở cột đầu vào trước OneHot, nên các cột mã hóa ngành được thay đổi cùng nhau như một biến. Giá trị âm được giữ nguyên, không cắt về 0. SD tính ddof=0, mô tả độ biến động 10 lần hoán vị, không phải CI hoặc kiểm định ý nghĩa thống kê.
2. importance_repeats_SYNTHETIC.csv: đủ 140 giá trị từng lần để đối chiếu mean/SD.
3. lr_coefficients_SYNTHETIC.csv: hệ số của 6 biến số, các mức ngành và intercept. Với số đã chuẩn hóa, tăng một SD làm log-odds đổi theo hệ số khi giữ các biến khác. Không đọc hệ số ngành thành so sánh với một ngành chuẩn vì encoder không drop cột; so hai ngành phải xét hiệu hai hệ số. RF không có hệ số hồi quy.
4. demo_metadata.json: 800 dòng fit seed 42, 400 dòng validation tự tạo seed 43, AP nền mỗi mô hình, seed/lượt importance. Đây không phải mẫu 5.000 giỏ thật. Hàm sample_baskets hỗ trợ chọn tối đa 5.000 giỏ seed 44, giữ tất cả ứng viên; kiểm thử xác nhận không lấy mẫu theo từng dòng.
5. figures/Hinh_mau_1_Importance_LR_RF: hai ô LR/RF, thanh sai số ±1 SD. Hai ô có thang x riêng nên so sánh bằng trị số trên trục, không chỉ chiều dài thanh.
6. figures/Hinh_mau_2_He_so_LR: sáu hệ số số đã chuẩn hóa. Bảng CSV vẫn giữ đầy đủ hệ số ngành/intercept. Đây là hình hỗ trợ vấn đáp, không tự thêm vào ngân sách hình của bài.

Hai hình đều có PNG 300 DPI và PDF vector, rộng 16 cm, chữ Times New Roman 12 pt, ghi rõ DỮ LIỆU TỰ TẠO. Đã render PDF để kiểm tra trực quan.

Trong bộ sinh dữ liệu giả, nhãn phụ thuộc chủ yếu số luật khớp và confidence; vì thế importance số luật lớn là kết quả của cách dựng ví dụ, không phải phát hiện về mua sắm. Hệ số/importance có thể chịu ảnh hưởng tương quan; không diễn giải nhân quả.

## Kiểm chứng bước độc lập

- Tên hệ số khớp tên sau ColumnTransformer; dùng toàn bộ hệ số và intercept tái dựng đúng decision_function của LR.
- Importance cùng seed cho cùng kết quả; xác suất trước/sau không thay đổi; cột hằng có mức giảm AP bằng 0.
- Bảng mean/SD khớp dữ liệu từng lần; một cột ngành duy nhất trong bảng importance.
- Từ chối importance khi chỉ có một lớp; chọn mẫu giữ trọn ứng viên của mỗi giỏ và không phụ thuộc thứ tự dòng.

Đã hoàn thành phạm vi hình mẫu/diễn giải trên dữ liệu tự tạo. Đây là gói bổ sung bước độc lập, không yêu cầu thực hiện ghép chung trong đợt này. Kiểm DANH_SACH.txt (SHA-256) trước khi chép.
