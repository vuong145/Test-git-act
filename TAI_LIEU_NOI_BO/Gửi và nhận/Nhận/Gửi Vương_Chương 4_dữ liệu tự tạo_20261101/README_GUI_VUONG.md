# Gửi Vương — hai phần Chương 4 của Phong trên dữ liệu tự tạo

Ngày 01/11/2026. Phân công mục 11, 20 mẫu âm/giỏ và dung sai 0,002 đã được Phong xác nhận. Gói này hoàn thành hai việc độc lập: Pipeline LR/RF và chỉ số phân loại/bootstrap trên dữ liệu tự tạo. Không phải gói kết quả thực nghiệm chính thức.

## Những gì đã làm

- `scripts/m4_classifier.py`: ColumnTransformer chọn đúng 7 biến; số điền median, LR thêm StandardScaler; ngành điền most_frequent + OneHotEncoder(ignore, không drop). LR lbfgs/max_iter=1000, L2 mặc định; RF 300 cây, sqrt, seed 42, n_jobs=-1. Chỉ fit tiền xử lý trên fit. Có lựa chọn bỏ nhóm luật/ngành phục vụ bước ablation sau này.
- `fit_grid`: lưới LR 4 cấu hình và RF 4 cấu hình theo thiết kế; nhận callback chấm validation của Vương, chọn Recall@10 trong dung sai 0,002 rồi thời gian suy luận thấp nhất. Nếu cả hai bằng nhau giữ thứ tự lưới. Hàm này chưa chạy lưới trên dữ liệu nghiên cứu. Khi nhiều mô hình cùng trong dung sai, có thể giữ tối đa 4 Pipeline trong RAM; cần đo RAM trên pilot.
- `scripts/m4_test.py`: chọn ngưỡng tối đa F1 trên validation (hòa chọn ngưỡng cao nhất); Accuracy, Precision, Recall, F1, ROC-AUC, AP, TN/FP/FN/TP. Dự đoán dương khi score >= threshold. Không có lớp dương: AP=null; chỉ một lớp: ROC-AUC=null; chỉ số tại ngưỡng dùng zero_division=0. Không diễn giải trường hợp không xác định thành kết quả tốt.
- Bootstrap ghép cặp theo user_id/order_id, một người một giỏ, mặc định 2.000 lần seed 42; CI percentile 2,5–97,5% (nội suy linear), chiều chênh lệch method - baseline. Lấy cùng mẫu người dùng cho hai phương pháp; không âm thầm bỏ giỏ thiếu, không cho khóa trùng. Hai phương pháp giống nhau cho CI [0,0]. Chỉ kết luận cải thiện khi cận dưới >0. Chưa bổ sung p-value hoặc phép so sánh ngoài thiết kế.
- `tests/test_m4_model.py`: 7 test mới về tiền xử lý không học validation, biến ngoài schema không ảnh hưởng, bỏ nhóm, metrics tính tay, tối ưu ngưỡng, bootstrap tính độc lập/ghép đúng khóa và chọn lưới theo dung sai. Toàn workspace đạt **37/37 test** (30 cũ +7 mới), ngày 01/11/2026; kết quả chạy 3,230 giây. Demo kiểm lưu/nạp hai Pipeline cho xác suất giống hệt.

## Chạy kiểm tra sau khi nhận

Tại thư mục gốc bài, kiểm SHA-256 theo DANH_SACH.txt trước khi chép. Các tệp project_io.py và requirements.txt trong gói là bản đối chiếu phụ thuộc; so với bản của Vương, không ghi đè khi khác. Chép hai script m4 và hai test m4 vào đúng thư mục; đầu ra demo chỉ để đối chiếu, không ghép vào bảng thực nghiệm.

```powershell
$env:PYTHONUTF8='1'
uv pip install --python .venv-m2/Scripts/python.exe -r requirements.txt
& .venv-m2/Scripts/python.exe -m unittest discover -s tests -p 'test_m4*.py' -v
& .venv-m2/Scripts/python.exe scripts/m4_classifier.py --demo
```

Demo kiểm hash G0 trước khi chạy; cần G0 sẵn trên máy nhận, không đóng lại G0 trong ZIP. Không yêu cầu uv nếu môi trường đã cài đúng. Demo xuất vào output/ch4_phong_synthetic_20261101; chạy lại ghi đè riêng đầu ra demo. joblib chỉ nạp file do chính mình tạo/nguồn tin cậy.

Demo dùng 400 dòng fit và 120 dòng validation tự tạo độc lập. Thời gian trong lr_demo.json/rf_demo.json là demo, không phải thời gian inference dùng phá hòa hoặc benchmark chính thức. Chỉ số phân loại trong demo dùng chính validation để chọn ngưỡng, chỉ kiểm chức năng, không ước lượng chất lượng khái quát hóa. Bootstrap dùng Recall dựng tay example_A/example_B, **không phải Recall của LR/RF**.

## Giao diện Phong cung cấp để Vương ghép

```python
from m4_classifier import build_pipeline, fit_grid
from m4_test import best_f1_threshold, classification_metrics, paired_bootstrap

# x_fit: DataFrame có 7 tên cột mục 3.1; y_fit: nhãn 0/1 có cả hai lớp.
# candidate_department_id: mã ngành dạng số, thiếu dùng np.nan.
model = build_pipeline('LR', {'C': 1}).fit(x_fit, y_fit)
scores = model.predict_proba(x_validation)[:, 1]
threshold = best_f1_threshold(y_validation, scores)
result = classification_metrics(y_validation, scores, threshold)

# Callback do Vương ghép: chấm toàn bộ validation theo lô bằng m4_common,
# trả {'recall_at_10': float, 'inference_seconds': float}.
winner, grid = fit_grid(x_fit, y_fit, 'LR', evaluate_validation)

# DataFrame dài: user_id, order_id, method, R@10; đủ cùng các giỏ cho hai method.
ci = paired_bootstrap(basket_metrics, 'LR', 'Popularity')
```

Hai module thuần không tự tìm/đọc dữ liệu nghiên cứu; chương trình gọi phải kiểm hash G0/M4, giữ đúng phân hoạch và nguồn đặc trưng. classification_metrics nhận toàn bộ nhãn/xác suất; **không lấy trung bình AUC/AP từng lô**. Chưa có bộ điều phối gom/chấm hàng chục triệu cặp; cần chốt với Vương cách giữ score/y hoặc dùng bộ nhớ ánh xạ tệp sau khi đo pilot. Chưa cam kết thời gian 2–3 phút cho pilot.

## Vương cần gửi lại

1. `m4_common.py` có chữ ký hàm, docstring và cách gọi bộ xếp hạng/metrics; đặc biệt kiểu từng lô từ iter_features, ánh xạ order_id/product_id/y, danh sách giỏ đủ kể cả không có ứng viên. Xếp score giảm dần rồi product_id tăng; Recall tính cả đáp án ngoài C.
2. `configs/m4_model.json` và feature_schema.json: xác nhận 7 biến, kiểu ngành, lưới B nêu trên, 20 âm/giỏ, dung sai 0,002, pilot_baskets=2000. Phong chưa tạo hoặc sửa file thuộc Vương.
3. Gói pilot fit/validation 2.000 giỏ, catalog/rules/features_fit, masked_baskets chỉ chứa phần phát triển, metrics mẫu, code phụ thuộc và hashes. Không gửi test mở cho demo. Ma trận khai phá dùng Pandas Boolean Sparse DataFrame, giữ đủ mẫu số reference gồm hàng rỗng.
4. Cách khóa và kiểm hash của lock.json. Hiện chạy trực tiếp m4_test.py luôn dừng: chưa triển khai chấm test thật, chưa có cổng lock được nghiệm thu. Cần thống nhất cách chuẩn bị/che test chỉ sau khóa vì tài liệu cũ có hai cách diễn đạt khác nhau.

## Phạm vi chưa hoàn thành của Chương 4

Chưa tích hợp pilot, chưa chạy lưới B/ablation thật, chưa chạy validation/test chính thức, chưa làm importance/hệ số/hình hoặc viết kết quả Chương 4. Các việc đó là giai đoạn tiếp theo; không phải yêu cầu hoàn thành hai ô dữ liệu tự tạo hiện tại. Không sửa QMD/PDF, Master, cleaning hoặc nhật ký trong đợt này.

Phần cần gửi nằm nguyên trong gói Gửi Vương_Chương 4_dữ liệu tự tạo_20261101.zip; không cần gửi môi trường ảo, Master, dữ liệu nghiên cứu hoặc các Pipeline demo .joblib (máy nhận tự chạy tạo lại).
