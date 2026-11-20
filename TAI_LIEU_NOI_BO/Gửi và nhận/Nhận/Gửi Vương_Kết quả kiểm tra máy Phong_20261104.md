# Kết quả kiểm tra máy Phong — 04/11/2026

Yêu cầu: đồng bộ requirements, check_hashes, chạy 55 test, chạy classifier trên pilot và kiểm chéo Rules Recall@10 trên 50 giỏ validation.

## Đã thực hiện

- Chạy `.venv-m2/Scripts/python.exe -m pip install -r requirements.txt`: tất cả đã được cài; đối chiếu độc lập 23/23 phiên bản chính xác. Danh sách khóa phiên bản hiện tại khớp requirements trong gói Vương ngày 01/11. Python Phong 3.12.10.
- `pip check`: No broken requirements found.
- `check_hashes('BAO CAO/Bao cao EDA/common/hashes.json')`: 6/6 tệp đạt.
- `check_hashes('BAO CAO/Bao cao EDA/ban2/hashes.json')`: 10/10 tệp đạt.
- Manifest gói GUI_phong_chuong4_phan_vuong_20261101: 12/12 tệp khớp SHA-256.
- Toàn bộ tests hiện hành trên máy Phong: 41/41 đạt ở lượt chạy lại, 6,807 giây. Test gói Vương chạy riêng: 8/8 đạt, 0,032 giây. Đây là hai lượt riêng, không phải bộ 55 test tích hợp.
- Lượt đầu có một ImportError: Windows Application Control chặn DLL sklearn `_binning`; log giữ nguyên. Chạy lại cùng môi trường đạt, không thay chính sách bảo mật và không sửa code để né kiểm tra. Chưa xác định nguyên nhân lỗi thoáng qua.

## Chưa thể thực hiện do chưa có đầu vào trong workspace

Đã tìm cả tên tệp ẩn (loại môi trường ảo/.git/cache) trong workspace. Thư mục nhận vẫn chỉ có gói Chương 4 ngày 01/11 nói rõ chưa có pilot; DATA/Data phai sinh hiện chỉ có M2. Không tìm thấy features_fit.parquet hoặc basket_metrics_validation.csv. Không có bộ code/test mới tương ứng yêu cầu 55 test. Không suy ra gói mới bị sai hoặc không tồn tại trên máy Vương.

1. Chạy đủ 55 test: cần gói code/test mới cùng requirements và manifest.
2. Pilot qua classifier: cần gói pilot thực tế, schema/cấu hình và hướng dẫn chạy tương ứng. Không thay bằng demo tự tạo hoặc tự tạo một pilot khác rồi nhận là đã nghiệm thu gói Vương.
3. Recall@10 Rules trên 50 giỏ: cần masked_baskets validation (observed/hidden), catalog/rules đúng cấu hình chọn và basket_metrics_validation.csv; nếu có rankings_validation.parquet thì gửi kèm để phân biệt sai điểm/xếp hạng với sai cách tính chỉ số. Có thể gửi riêng mẫu 50 giỏ và toàn bộ nguồn cần để tái tính cho mẫu đó, kèm manifest.

Kế hoạch kiểm chéo khi nhận đủ: lấy 50 giỏ validation đủ điều kiện theo order_id tăng (không chọn theo kết quả); tự khớp tiền đề luật với observed; xếp Rules theo confidence, popularity và product_id đúng quy ước đã chốt; lấy Top-10, tính |Top10 ∩ hidden| / |hidden|, giữ sản phẩm ẩn ngoài danh mục trong mẫu số. Giỏ không có ứng viên vẫn được tính với tử số 0. Đối chiếu từng giỏ và trung bình, lưu danh sách mã giỏ, số trúng, mẫu số, hai giá trị Recall và sai lệch. Không gọi lại hàm Recall chính thức để giả làm phép kiểm độc lập.

## Hồ sơ trên máy Phong

Trong `output/kiem_tra_phong_20261104/`:
- pip_install.log, pip_check.log.
- verification.json: phiên bản thực tế, hash requirements, số tệp trong các manifest đã kiểm.
- tests_workspace.log: lượt đầu lỗi DLL.
- tests_workspace_retry.log: 41 test đạt.
- tests_vuong_received.log: 8 test gói nhận đạt.

Chưa chạy pilot hoặc kiểm chéo Recall; không sửa nhật ký/QMD, không chạy lại cleaning/Master/mining và không mở test nghiên cứu. File báo cáo nhẹ nên để nguyên, không đóng ZIP.
