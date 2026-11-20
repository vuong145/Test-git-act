# Gửi Vương — Bản cuối mã chấm test và đồng bộ Phong, 04/11/2026

## Đã đồng bộ

Kiểm đủ 19 tệp theo manifest gói môi trường. Sao lưu tại output/dong_bo_cuoi_20261104/before, chép Master trước common/hashes.json, rồi project_io.py, test_m2_multivariate.py, requirements.txt. Năm tệp đích khớp hash gói nhận; Master mới có SHA-256 2741c97001e6588a565c8e81771c9fb3e1e3c5edc9018dfeed879eb600473935.

check_hashes: G0 **6/6**, ban2 **10/10**, M4 **6/6** đạt. 23 phiên bản thư viện khớp, pip check đạt. Hồ sơ environment_hashes.json và synced_files.json đi kèm. Không chép QMD/PDF/hình hoặc chạy lại benchmark từ gói; đã đọc hướng dẫn thay đổi lời văn, phần bài xử lý riêng.

## Mã cuối

- m4_test.py đặt `models['RF'].named_steps['model'].set_params(n_jobs=1)` ngay sau nạp Pipeline, trước mọi predict_proba. Không ghi lại joblib nên hash mô hình không đổi; không đổi tham số huấn luyện.
- Giữ thời điểm tạo test_started.json trong cổng kiểm tra, trước khi đọc giỏ. Đây là lựa chọn thận trọng, không dời dấu trong đợt này. Dấu tạo bằng chế độ `x`; có dấu thì từ chối chạy lại.
- Nếu máy hỏng: giữ dấu và mọi log/đầu ra. Hai bên kiểm tình trạng, chỉ cùng đồng ý đổi tên dấu thành test_started_failed_<ngày giờ>.json khi chưa có bất kỳ kết quả test nào; không xóa dấu. Phải giữ nguyên khóa/mô hình/code. Nếu đã có kết quả hoặc chưa rõ đã xuất kết quả chưa thì dừng để cùng rà, không tự chạy lại. Không có cơ chế tự khôi phục mở lại test.
- Kèm m4_common.py đã sửa lọc split ngay tại pd.read_parquet (so với bản đề xuất Vương); không đọc toàn bộ giỏ rồi mới lọc. Các công thức không đổi.
- Test cổng khóa kiểm cả trường hợp RF bị ép n_jobs=1 và predict_proba lặp giống hệt trên dữ liệu tự tạo; giữ các kiểm thiếu duyệt/sai hash/thiếu hash code/đổi thư mục ra/chạy lại, bootstrap tự so và Recall 1–10.

## Thiếu một phụ thuộc trong gói môi trường, đã bổ sung rõ ràng

Lượt test đầu lỗi ImportError vì test_m2_multivariate.py mới nhập lift_percentile nhưng m2_eda_multivariate.py bên Phong chưa có hàm này; gói môi trường không kèm script mới. Đã thêm hàm ngắn tính tỷ lệ lift <= giá trị mục tiêu, đồng thời dùng hàm đó tại phần tính percentile_among_pairs. Kèm script để Vương đối chiếu/nhận bản đúng API; không bỏ hoặc hạ yêu cầu test. Đây là thay đổi code cho quy ước phân vị bao gồm cặp mục tiêu, không phải thay đổi lựa chọn mô hình Chương 4.

Không chạy lại M2 và không ghi đè lift_baseline.csv: đầu ra hiện có vẫn giữ nguyên hash. Khi cập nhật Chương 3 sau này cần đối chiếu bảng nền đang lưu với quy ước <=; test code đạt không chứng minh mọi bảng lịch sử đã được tái xuất theo code mới.

## Kiểm chứng cuối

Toàn bộ **58/58 test đạt**, 10,984 giây: 57 ở lượt trước + test lift_percentile của bản test đa biến mới. tests.log là log cuối, tests_before_dependency_fix.log giữ lỗi trước sửa. Không đổi số test thành 56/57 để khớp kỳ vọng cũ.

Chạy thử suy luận hai Pipeline trên 2.000 giỏ validation đầu theo order_id tăng, đầy đủ ứng viên, hai lượt liên tiếp với RF một luồng; kết quả máy đọc trong classifier_verification.json. Đây là kiểm trên mẫu phát triển, không chạy lại toàn bộ validation 24,7 triệu cặp. Mã nghiệm thu verify_reproducibility.py và các bảng kiểm đi kèm. Các chỉ số nguồn Vương và số máy Phong có thể khác chữ số rất nhỏ của AUC/AP khi nguồn cũ dùng song song; tiêu chí tái lập là hai lượt mới cùng RF một luồng khớp chính xác. Không hứa tái lập mọi bit giữa các bản Python/phần cứng khác nhau.

## Nhận và kiểm

Giữ cấu trúc thư mục; kiểm DANH_SACH.txt, chép nguyên scripts/m4_test.py, scripts/m4_common.py, tests/test_m4_gate.py; đối chiếu thêm scripts/m2_eda_multivariate.py vì phụ thuộc vừa bổ sung. Các file môi trường của Vương đã được nhận đúng, không cần gửi lại Master/dữ liệu lớn.

```powershell
$env:PYTHONUTF8='1'
& .venv-m2/Scripts/python.exe -m unittest discover -s tests -v
```

Không chạy lệnh test thật trong phiên này; không sửa m4_lock.py/lock.json. Vương cần dùng m4_lock bản mới để tạo khóa nháp với hash mã cuối, gửi Phong duyệt, rồi mới ghi approvals khi cả hai đồng ý. Hash của bản cuối nằm trong DANH_SACH.txt, thay thế các hash mã Phong gửi trước đó.

Biên bản: Phong giữ các xác nhận phân công/môi trường/tham số và ba giao diện đã tick; đồng ý Recall@K 1–10. Ô duyệt lock/đã khóa vẫn để trống. Không gửi thêm bản biên bản song song, không ghi nhật ký. Gói nhẹ để nguyên thư mục, không ZIP.
