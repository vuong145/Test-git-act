# Chạy và kiểm tra M1

Hai script lấy thư mục bài từ vị trí của chính script, không phụ thuộc thư mục
hiện hành của terminal. `--clean-dir` và `--output-dir`, nếu là đường dẫn tương
đối, luôn được tính từ thư mục bài (thư mục cha của `scripts/`).

Từ thư mục bài, kiểm tra đường dẫn mà không chạy xử lý dữ liệu:

```powershell
python scripts/m1_build_master.py --check-inputs
python scripts/m1_benchmark.py --check-inputs
python tests/test_m1_portability.py
```

Từ một thư mục khác, chỉ cần truyền đúng đường dẫn tới script. Không cần đổi
các hằng số trong mã. Chế độ kiểm tra đầu vào không cần pandas/PyArrow/psutil.

Chạy thực nghiệm khi cần tái tạo sản phẩm:

```powershell
python scripts/m1_build_master.py --chunksize 250000
python scripts/m1_benchmark.py
```

Môi trường chạy đầy đủ cần Python >= 3.11, pandas >= 2.0, NumPy, PyArrow và
psutil. Hồ sơ benchmark ngày 20/10/2026 ghi Python 3.12.10, pandas 3.0.3,
PyArrow 24.0.0 và psutil 7.2.2. Không đổi môi trường rồi coi số đo mới là cùng
lượt thực nghiệm cũ. Không dùng `python -O`, vì chế độ này bỏ các assertion
kiểm toán; CLI từ chối chạy xử lý khi phát hiện chế độ tối ưu đó.

Master được ghép/ghi theo khối, nhưng kiểm tra miền và đối soát toàn bảng vẫn
dùng RAM theo quy mô dữ liệu. Benchmark C chỉ so sánh nạp/ghép lại với đọc
Master sẵn có, không đo toàn bộ pipeline xây dựng và kiểm toán Master.

Xuất bản Master dùng bản sao tạm tại từng đích, kiểm tra hash và `os.replace`.
Một lỗi sao chép hoặc thay thế giữ nguyên tệp cũ tại đích đó. Hai bản Master
và các báo cáo không phải một giao dịch chung: nếu lượt chạy thất bại sau khi
đã thay thế một bản, cần chạy lại thành công và đối chiếu cả hai hash với hồ sơ.
Không diễn giải thao tác đóng writer là bảo đảm an toàn trước mất điện.

Đường dẫn trong hồ sơ mới được lưu tương đối theo thư mục bài, có `path_base`.
Đường dẫn tuyệt đối trong JSON của lượt chạy cũ là dấu vết lịch sử; chúng không
được dùng làm cấu hình đầu vào và không được sửa để giả lập một lượt chạy mới.

## Kiểm toán bổ trợ cho mục 3.3

Chạy `python scripts/m1_quality_summary.py` để tạo `missingness_summary.csv` và
`basket_quality_summary.json` trong `Bao cao lam sach/`. Script không sửa CSV hay
Master; IQR toàn bảng chỉ phục vụ kiểm toán chất lượng, không chọn mô hình.

Cài gói chung bằng `python -m pip install -r requirements.txt` từ thư mục bài.
Quarto CLI, XeLaTeX và font Times New Roman là công cụ ngoài pip cần cho PDF.
Script render không tự đóng ứng dụng đọc PDF; nếu tệp bị khóa, đóng tệp rồi chạy lại.

Bước render sao chép QMD, bibliography và các thư mục tài nguyên báo cáo vào
thư mục tạm riêng trước khi gọi Quarto. Nếu PDF chính bị khóa, bản biên dịch
thành công được giữ ở tệp `.build.pdf`; đóng PDF chính rồi xuất bản bản mới.
