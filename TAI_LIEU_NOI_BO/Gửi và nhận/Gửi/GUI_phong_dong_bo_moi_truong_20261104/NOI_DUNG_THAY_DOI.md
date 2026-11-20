# Đồng bộ môi trường — nội dung thay đổi (04/11/2026)

Vương đã thống nhất môi trường cho toàn bài: bảng Master và benchmark M1 (trước đó chạy bằng Python toàn cục 3.12.10, pandas 3.0.3, PyArrow 24.0.0) được chạy lại trong `.venv-m2` (Python 3.12.14, pandas 3.0.1, NumPy 2.3.5, PyArrow 26.0.0). Gói này gồm QMD đã sửa các chỗ liên quan và bốn hình ban2 tạo trên máy Vương. Phong xem lại lời văn, dùng bản QMD này làm bản chính nếu đồng ý; các sửa chỉ gồm số liệu chép từ CSV/JSON và câu mô tả môi trường.

## 1. Kết quả kiểm chứng

| Việc | Kết quả |
|---|---|
| Master mới so với bản 20/10 | Giống từng ô, so chính xác, cả chế độ đọc mặc định và `numpy_nullable`; cùng 1.384.617 dòng, 15 cột, cùng schema; vẫn 16.992.331 byte |
| SHA-256 Master | Đổi: bản mới bắt đầu `2741c970…`, bản 20/10 bắt đầu `669ef3f9…` (khác byte vì PyArrow ghi siêu dữ liệu `created_by` khác phiên bản) |
| 13 tiêu chí kiểm tra Master | Đạt |
| Chạy lại chuỗi M2 sau khi đổi Master | 97 tệp đầu ra; chỉ hai tệp đổi nội dung: `common/hashes.json` (hash Master) và `basket_quality_summary.json` (ghi hash nguồn); 95 tệp còn lại giống từng byte, gồm mọi CSV mục 3.4–3.6 và Chương 4 |
| Unittest | 55/55 đạt |
| PDF | Render được, 50 trang, không còn tham chiếu thiếu; bản mới lưu ở `PDF_ban_moi.pdf` vì tệp PDF cũ đang mở ở chương trình khác |

## 2. Sửa trong QMD (16 chỗ)

**Mục 2.5 (môi trường):** viết lại đoạn "Môi trường được ghi theo từng lượt...": mọi lượt chính thức dùng `.venv-m2` trên một máy; Master tạo lần đầu 20/10 trong môi trường khác và tạo lại 04/11 (giống từng ô); benchmark đo lại 04/11; máy Phong dùng Python 3.12.10 để phát triển và kiểm chứng, không sinh số liệu trong bài.

**Mục 3.2 (hồ sơ Master):** lượt chạy ngày 04/11 trong `.venv-m2`; bỏ cụm "hai bản xuất bản giống nhau" (đã nêu ở danh sách việc của Phong; nay chỉ còn một bản Master) và thay bằng câu so sánh từng ô giữa Master tạo lại và bản 20/10.

**Bảng 3.5 (benchmark, trung vị ba lượt, đơn vị MiB và giây):**

| Thao tác | Cũ (RSS đỉnh / giây) | Mới (RSS đỉnh / giây) |
|---|---|---|
| Thu hẹp kiểu | 491,98 / 1,0952 | 483,35 / 1,1697 |
| Ghi CSV | 292,66 / 8,8145 | 295,54 / 9,7270 |
| Ghi Parquet | 311,99 / 1,0504 | 302,15 / 1,0131 |
| Đọc CSV | 250,99 / 5,9227 | 224,13 / 6,1819 |
| Đọc Parquet | 294,12 / 0,1974 | 299,08 / 0,2089 |
| Nạp 5 CSV và ghép | 404,25 / 7,8016 | 394,59 / 9,3488 |
| Đọc Master Parquet | 299,70 / 0,1911 | 290,02 / 0,2033 |

Cột RAM DF (423,04; 50,10; 51,11) và cột đĩa (118,86; 15,34) không đổi.

**Lời văn phân tích Bảng 3.5:**
- Tối ưu kiểu: thời gian 1,1697 giây (cũ 1,0952), Peak RSS 483,35 MiB (cũ 491,98); mức giảm 88,16% không đổi.
- Parquet so với CSV: nhỏ hơn 7,75 lần (không đổi); ghi nhanh hơn **9,60 lần** (cũ 8,39: 1,0131 giây so với 9,7270 giây); đọc nhanh hơn **29,59 lần** (cũ 30,00: 0,2089 giây so với 6,1819 giây, $6{,}1819 / 0{,}2089 \approx 29{,}59$).
- Tái sử dụng Master: tỷ số **45,99 lần** (cũ 40,82: 9,3488 giây so với 0,2033 giây), chênh lệch Peak RSS 104,57 MiB (cũ 104,55).
- Đoạn "đánh đổi bộ nhớ": đọc 299,08 so với 224,13 MiB; ghi 302,15 so với 295,54 MiB. Phần kết luận (Parquet có Peak RSS cao hơn CSV) vẫn đúng.
- Khoảng dao động ba lượt: ghi CSV 9,6451–10,7859 giây; ghi Parquet 1,0021–1,0232 giây; đọc CSV 6,0317–6,6182 giây; đọc Parquet 0,1876–0,3120 giây.

Nguồn: `DATA/Data đã làm sạch/Bảng master TLCK/data_benchmark.csv` (lượt chạy 04/11/2026 14:12). Môi trường ghi trong `data_benchmark_metadata.json`: Python 3.12.14, pandas 3.0.1, PyArrow 26.0.0, psutil 7.2.2; phần cứng và hệ điều hành không đổi (Windows 11, 8 nhân/16 luồng, RAM 23,31 GiB).

## 3. Bốn hình ban2 (thay trong `assets/chuong3/`)

`fig-ref-time-frequency.pdf`, `fig-ref-time-basket-size.pdf`, `fig-ref-corr-spearman.pdf`, `fig-ref-department-lift.pdf`: thay bằng bản code tạo trên máy Vương (cùng dữ liệu vẽ, phông nhúng kiểu 42). Hai hình ban1 trước đó đã giống từng byte. Từ nay cả sáu hình đều giống bản gốc trong `BAO CAO/Bao cao EDA/figures/`. Chưa vẽ lại hình theo mục 6.6 của THONG_NHAT.

## 4. Việc của Phong

- [ ] Đọc lại các đoạn trong mục 2.5, 3.2 và Bảng 3.5 ở trên; nếu muốn đổi cách viết thì sửa trong bản QMD của Phong, giữ đúng các số.
- [ ] Dùng QMD và bốn hình trong gói làm bản chính, hoặc gửi lại chỗ cần sửa.
- [ ] Đồng bộ máy Phong theo mục 5 (Master mới, `hashes.json` mới, `project_io.py`, `test_m2_multivariate.py`, `requirements.txt`), rồi chạy `check_hashes()` của G0 và toàn bộ unittest.

## 5. Tệp đồng bộ kèm theo (bổ sung)

| Tệp trong gói | Việc cần làm trên máy Phong |
|---|---|
| `DATA/Data đã làm sạch/master_train.parquet` (SHA-256 bắt đầu `2741c970`) | Sao lưu Master hiện có, rồi chép Master mới **trước** |
| `BAO CAO/Bao cao EDA/common/hashes.json` | Chép **sau** khi đã thay Master; nếu chép trước, `check_hashes()` báo lỗi |
| `scripts/project_io.py` (bắt đầu `d55bbb39`) | Thay bản hiện có: chỉ khác bản cũ ở các chú thích khối, cấu trúc code không đổi |
| `tests/test_m2_multivariate.py` (bắt đầu `6e28dd33`) | Thay bản hiện có: bản mới thêm test phân vị lift |
| `requirements.txt` (bắt đầu `79edb2c0`) | Thay bản hiện có: cùng 23 phiên bản, khác thứ tự dòng; để hash hai máy giống nhau |

Thứ tự trên máy Phong: sao lưu, thay Master, chép `hashes.json`, chép ba tệp còn lại, chạy `check_hashes()` cho G0 (6 tệp) và nhánh ban2 (10 tệp), chạy toàn bộ unittest, ghi lại kết quả.
- [ ] Ghi vào nhật ký của Phong (nếu có phiên riêng) việc nhận bản đồng bộ.
