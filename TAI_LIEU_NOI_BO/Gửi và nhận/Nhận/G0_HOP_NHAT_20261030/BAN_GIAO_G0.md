# Bàn giao G0 hợp nhất — 30/10/2026

Đã nghiệm thu kỹ thuật trên máy Phong: 95 file gói nhận đúng hash; 21 tests nền/gate đạt trong rebuild_retry.log; verifier độc lập đạt; consumer và profile đầu vào đạt. Ba Parquet chia tập/reference/bảng giỏ giữ nguyên byte so với gói Vương. Xem NGHIEM_THU.json và log. Hai lượt lỗi quyền ghi trước đó được giữ làm bằng chứng, phiên hiện hành đã passed.

## Quyết định hợp nhất

- Giữ toàn bộ gate/session/config version 2 của Phong: kiểm tra lock, acceptance, môi trường và hash. Tích hợp nguyên phép join tạo bảng giỏ của Vương; tích hợp profile shape/info/missing/describe, dùng consumer version 2 và thư mục phiên riêng.
- Giữ renderer và QMD/PDF Phong. Đã lưu qmd_comparison.diff để đối chiếu với Vương; không chép PDF 37 trang đè PDF Phong 38 trang. G0 không yêu cầu sửa nội dung nghiên cứu hoặc chạy lại render. Những phần EDA và phụ lục chưa hoàn thiện vẫn còn chờ.
- Hướng dẫn chung đã chỉnh đường dẫn/trạng thái cho cây Phong; cấu hình outputs lấy trực tiếp từ m2_eda.json, không dùng schema outputs phẳng version 1 của Vương.
- Gói nhận nguyên vẹn; bản trước sửa mã nằm trong backup. Không sửa manifest cũ để khớp mã mới.

## Máy Vương nhận gói cập nhật

ZIP là bản cập nhật G0, không phải workspace nộp đầy đủ. Giải nén vào thư mục tạm. Sao lưu scripts/configs/tests và Bao cao EDA/common đang có. Chép cây project vào thư mục bài chứa QMD, đồng bộ TOÀN BỘ scripts m2 và configs trong gói cùng một lượt. Giữ nguyên Master/sáu CSV sạch và Data phai sinh/M2; hash đầu vào phải khớp foundation_manifest.json. Không dùng m2_evidence.py, latest.json hoặc test_m2_evidence.py phiên bản 1 để điều khiển phiên bản 2; lưu chúng vào hồ sơ lịch sử ngoài cây script/test vận hành.

Tạo venv riêng Python 3.12; cài requirements-m2-lock.txt. Phong chạy Python 3.12.10, Vương trước đây 3.12.14; mỗi máy ghi bản thực tế. Chạy `python scripts/m2_verify_foundation.py` để nghiệm thu lại trên máy nhận, rồi `python scripts/m2_profile_inputs.py`. Cần Times New Roman. Nếu thư mục TEMP mặc định bị từ chối quyền, đặt TEMP/TMP tới thư mục riêng có quyền ghi trước chạy. Không chép venv giữa máy.

Trạng thái có thẩm quyền: Bao cao EDA/common/foundation_validation.json trỏ phiên trong runs/<run_id>. Consumer gọi load_foundation(). Các JSON ở common chỉ là bản tiện tra cứu, acceptance của máy Phong không chứng nhận môi trường máy Vương.

RELEASE_MANIFEST.json trong ZIP chứa hash từng file cập nhật. Chỉ dùng để đối chiếu lúc nhận; sau verifier, hồ sơ phiên mới có thể khác. Toàn bộ code/config trong gói phải đồng bộ trước chạy. Chưa xác nhận Vương đã nhận hoặc chạy bản này; chưa bắt đầu EDA 3.4–3.6.
