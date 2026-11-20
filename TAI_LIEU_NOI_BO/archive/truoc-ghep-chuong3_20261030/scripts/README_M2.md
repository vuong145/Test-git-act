# M2/G0 — cây vận hành và giao thức bằng chứng hiện hành

Bài vận hành ở thư mục chứa scripts này; QMD chính cùng cấp với scripts.
Nhật ký chuẩn ở gốc TLCK. Bản snapshot/ZIP không phải cây vận hành.

## Cài và chạy

G0 dùng Python 3.12.14; thư viện khóa trong requirements-m2-lock.txt.
Môi trường này khác lượt M1 lịch sử, không gán benchmark M1 cho G0.
Tạo lại venv trên máy nhận, không chép venv giữa máy:

```powershell
uv venv --python 3.12 .venv-m2
uv pip install --python .venv-m2/Scripts/python.exe -r requirements-m2-lock.txt
.\.venv-m2\Scripts\python.exe scripts/m2_run_foundation.py
.\.venv-m2\Scripts\python.exe scripts/m2_profile_inputs.py
```

Khi chỉ kiểm chứng dữ liệu đã có (không cần split lại):

```powershell
.\.venv-m2\Scripts\python.exe scripts/m2_verify_foundation.py
.\.venv-m2\Scripts\python.exe scripts/m2_check_environment.py
```

Mỗi lần verify/check-environment tạo thư mục phiên mới; không sửa acceptance
hay ảnh fixture của phiên trước. PACKAGE_MANIFEST chỉ mô tả snapshot lúc gửi.
Sau khi giải nén và chạy, hồ sơ mới của máy nhận không cần trùng byte với snapshot;
nguồn dữ liệu và config vẫn phải khớp hash của foundation đang nghiệm thu.

## Trạng thái và con trỏ

- `BAO CAO/Bao cao EDA/common/foundation_manifest.json`: hash nguồn/config/code/output G0.
- `foundation_validation.json`: trạng thái building/prepared/verifying/passed/failed.
- `latest.json`: con trỏ phiên **kiểm chứng hiện hành** trong runs/verification/.
- Phiên gồm acceptance.json và run.json liên kết acceptance bằng SHA-256;
  run_id và foundation hash phải khớp trạng thái committed.
- `pipeline_latest.json`: trỏ phiên chạy toàn chuỗi; đó là chứng cứ lịch sử
  của chuỗi này, không bị sửa nếu chạy độc lập verifier lần nữa.
- `environment_latest.json`: trỏ phiên kiểm tra thư viện/font mới nhất.
- `quality_latest.json`: trỏ shape/info/missing/describe; không thay EDA 3.4.
- `history/before_evidence_fix_20261029`: hồ sơ trước sửa, không dùng làm gate.

Consumer EDA gọi `m2_common.load_foundation()`: phải có state passed,
acceptance passed, đúng run_id, foundation hash, hash các con trỏ/record,
verifier/evidence code và nguồn/config/output còn nguyên.
Verifier dùng lớp `load_foundation_inputs()` để tránh tự đòi acceptance mới
trước khi tạo acceptance. Bắt đầu verify đã vô hiệu hóa trạng thái cũ;
lỗi/gián đoạn không được tiếp tục dùng passed cũ. Chuẩn bị dữ liệu chỉ đạt
prepared, chưa cho EDA dùng trước independent verification.

Khóa `.writer.lock` ngăn hai tiến trình ghi G0 đồng thời. Nếu máy dừng đột ngột,
kiểm tra không còn tiến trình M2 chạy rồi mới gỡ lock cũ và chạy lại verify/
pipeline. Không tự bỏ qua lock hay đổi failed thành passed bằng tay.
Tệp riêng thay nguyên tử bằng os.replace; toàn gói không phải giao dịch đa tệp.

## Config chung — một nguồn cho mỗi tham số

- m2_eda.json: version/split_rule kiểm tra chặt, seed/RNG, thống kê, min_group_n=30,
  các đường dẫn outputs ban1/ban2, figures/plot_data/drafts.
- hypotheses_config.json (được m2_eda.json dẫn tới): alpha, Holm, điều kiện kỳ vọng,
  correction, Fisher, effect size và ba cặp cố định. Không nhân đôi alpha.
- m2_plot_style.json: font, màu, DPI và định dạng.
- render_resources.json: hình/bảng nhẹ được staging; không copy toàn Data phai sinh.

min_group_n chỉ là ngưỡng chú thích nhóm nhỏ, không phải điều kiện Chi-square.
G0 đọc Parquet mặc định; kiểu dữ liệu thực đọc được ghi trong data_contract.
M1 đọc kiểm chứng với numpy_nullable. So giá trị/mask thiếu, không đồng nhất tên dtype.

## Gói dữ liệu

Giữ nguyên giỏ reference gồm singleton và mọi sản phẩm. Không Top-N trước khi
đếm giỏ; không EDA holdout. PCG64 seed42 và cùng quy tắc làm tròn đã khóa:
reference/fit/validation/test = 39.363/39.363/26.241/26.242 người.
Reference = 415.053 dòng; bảng giỏ = 39.363 dòng; 21 ngành trong lookup.

M2 cần Master, sáu CSV sạch và hồ sơ M1/cleaning để kiểm tra hash.
Mọi đường dẫn vận hành tính từ script, không từ cwd. Chỉ dùng fixture tổng hợp
để thử lỗi thống kê; style_fixture là ảnh kiểm tra font, không phải kết quả bài.

Hai nhánh chưa triển khai; xem roadmap và phân công. Không tuyên bố toàn bộ M2
hay Trụ cột II hoàn thành chỉ vì G0 passed. Toàn bộ kết quả mới được ghi theo
phiên thật, không ghi đè/sửa hash chứng cứ lịch sử để làm cho có vẻ phù hợp.
