# Phần Bạn 1 — thống kê 3.4 và hai hình đầu 3.5

Chỉ chạy trên G0 đã nghiệm thu. Không sửa Master, sáu CSV sạch, split,
config khoa học hoặc code nền trong quá trình làm nhánh này.

## Chạy lại

Từ thư mục bài, bằng môi trường M2 đã khóa:

```powershell
.\.venv-m2\Scripts\python.exe -B scripts/m2_run_ban1.py --render-preview
```

Hoặc chạy lần lượt `test_m2_summary.py`, `m2_eda_summary.py`,
`m2_plot_univariate.py`, `m2_write_ban1_drafts.py`, `m2_verify_ban1.py`.
Các script phân giải đường dẫn từ gốc bài thông qua config, không từ cwd.
Để thử cwd khác, gọi Python và script bằng đường dẫn tới bản cài trên máy mình.
Quarto/XeLaTeX cần có nếu chọn `--render-preview`.

Chỉ một tiến trình Bạn 1 được chạy tại một thời điểm. Không chạy hai lượt
summary/plot đồng thời vào cùng đầu ra. Chạy lại summary làm trạng thái nhánh
trở về `summary_passed_plots_pending`; phải tạo lại hình/bản thảo và verify.
Không dùng hình cũ nếu input/code/hash đã thay đổi.

## Đầu ra

Các vị trí đọc từ `configs/m2_eda.json`:

- `outputs.tables`: 8 CSV (bao gồm bảng Top-10 + phần còn lại),
  `reference_outliers.json`.
- `outputs.figures_ban1`: 2 hình, mỗi hình có PNG 300 DPI và PDF vector.
- `outputs.plot_data_ban1`: 5 CSV lưu đúng dữ liệu dùng vẽ.
- `outputs.ban1`: manifest summary, plot, draft, validation và manifest nhánh.
- `outputs.drafts`: `ban1_3_4.qmd`, `ban1_3_5_hinh_1_2.qmd`,
  `ban1_evidence_i1_i3.md`, bản xem thử `ban1_preview.qmd/.pdf`.

`sample_overview.csv` chứa số đếm; `eda_summary.csv` có N/thiếu, mean/std,
năm con số, skew và excess kurtosis. Thống kê không xác định giữ NA.
`categorical_frequencies.csv` dùng tên `all_pct`, `valid_pct` (tương ứng
pct_all/pct_valid trong roadmap) để tuân thủ hậu tố `_pct`: thang 0–100.
Mã `NA` có `is_missing=True`; valid_pct của nhóm thiếu là ô rỗng.

Các tỷ lệ `_share`, `_coverage`, `_rate`, popularity nằm [0,1]. CSV không
làm tròn, dấu thập phân `.`, numeric NA là ô rỗng. Khi đọc tên danh mục,
dùng `keep_default_na=False`; tên rỗng vẫn được giữ và có display_name riêng.
Tỷ lệ mua lại chỉ dùng reordered hợp lệ. Nhóm không có dòng có số đếm 0,
nhưng tỷ lệ trên mẫu số 0 là NA. Bảng ngành/quầy giữ đủ danh mục nguồn.
Popularity chỉ xếp các sản phẩm quan sát được trong reference.

Hình xuất rộng 6,3 inch, font 12 pt. Chèn PDF ở rộng 16 cm; không thu nhỏ
hình hay bảng để ép trang. Các bản thảo QMD dùng đường dẫn từ gốc bài;
chỉ bản preview đổi đường dẫn để tự render từ thư mục drafts.

## Kiểm chứng và trạng thái

- 8 fixture tính tay: độ phủ hợp giỏ, mẫu số thiếu/hợp lệ, tên thiếu,
  danh mục không xuất hiện, std/phân vị, phá hòa, dữ liệu mâu thuẫn/trùng,
  toàn thiếu, độ phủ nhóm ngành còn lại.
- `m2_verify_ban1.py`: đọc CSV lại; đối chiếu `describe`, tần số từng ô,
  nhóm ngành/quầy, popularity, Top-N theo tập order và IQR bằng NumPy;
  kiểm tra hash input/code/output của các giai đoạn.
- `run_manifest.json` chỉ xác nhận **Bạn 1**, không nghiệm thu toàn M2.
- QMD/PDF chính không được sửa trong nhánh này. Bản thảo có kết quả thật
  nhưng vẫn chờ review và tích hợp. Không tự điền phần 3.6.

## G1 gửi Bạn 2 và thay đổi cấu trúc thư mục

Gói G0 ZIP đã gửi dùng `Data phai sinh/M2` và `Bao cao EDA/common`.
Cây hiện tại dùng `DATA/Data phai sinh/M2` và `BAO CAO/Bao cao EDA/common`.
`g0_package_compatibility.json` đối chiếu bốn tệp nền: byte giống nhau,
tham số EDA ngoài đường dẫn giống nhau. **Foundation/config/code hash của
hai cấu trúc khác nhau; chưa có xác nhận G0 đồng nhất từ Bạn 2.**

Không chép đè config/common/manifest G0 của Phong. Trước tích hợp, hai người
chốt một cấu trúc chung rồi nghiệm thu lại nền nếu có đổi config/code.
Trong lúc chờ, có thể đối chiếu G1 theo hash reference, basket, split và
lookup, ghi rõ việc chấp nhận ánh xạ đường dẫn. Script Bạn 1 đọc đường dẫn
từ config nên có thể chạy trên mỗi cây đã nghiệm thu riêng; manifest đầu
ra sẽ liên kết với G0 của chính cây đó. Không sửa tay hash để giả đồng nhất.

Danh sách gửi G1 được ghi trong `outputs.ban1/handoff_manifest.json`:
code Bạn 1, test, README này, 8 CSV/JSON thống kê, dữ liệu hình, 2 hình,
bản thảo/bằng chứng I1–I3 và hồ sơ nghiệm thu nhánh. Không cần gửi lại dữ liệu
lớn hoặc môi trường ảo. Manifest bàn giao là snapshot; tạo lại nếu đổi file.

## Những việc phải để lại

- Bạn 2: đọc/kiểm tra G0 và G1, chốt I1–I3; thực hiện đa biến, hình 3–5,
  I4–I5 và toàn bộ 3.6.
- Hai người: xác nhận cấu trúc/hash chung, mẫu số và kết quả review.
- Bạn 1 sau khi đủ hai nhánh: bộ gọi hình chung `m2_eda_visualize.py`,
  kiểm thử tích hợp `test_m2_eda.py`, manifest toàn M2, ghép QMD/PDF chính,
  đối chiếu nguồn trích dẫn và nghiệm thu cuối. Chưa tạo các file giả hoàn tất.
- Nhật ký làm việc được cập nhật theo yêu cầu riêng; lượt triển khai này
  không tự ghi nhật ký hoặc ghi thay đóng góp của Bạn 2.
