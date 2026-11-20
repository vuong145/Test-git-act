# THỐNG NHẤT CHƯƠNG 4 — LẦN 1 (04/11/2026)

Căn cứ: `THIET_KE_CHUONG4_20261101.md` (mục 9, 11.2, 11.4, 4), `THONG_NHAT_PHAN_VIEC_20261031.md`, báo cáo "Kết quả kiểm tra máy Phong 04/11".
Mục đích: ghi những điều hai bạn đã chốt ở lần ngồi chung thứ nhất và phân việc cho giai đoạn tiếp theo.
Tệp này chỉ là bản đề nghị chốt do Vương soạn; mỗi mục có ô xác nhận, Phong đánh dấu khi đồng ý. Tệp `THONG_NHAT_PHAN_VIEC_20261031.md` không bị sửa.

---

## 1. Kết quả kiểm tra máy Phong (đã đối chiếu với bài)

| Việc | Kết quả trên máy Phong | Đối chiếu máy Vương |
|---|---|---|
| Cài `requirements.txt`, `pip check` | 23/23 phiên bản đúng, không lỗi phụ thuộc | `requirements.txt` có 23 dòng khóa phiên bản: khớp |
| `check_hashes` G0 (`common/hashes.json`) | 6/6 tệp đạt | 6 tệp: khớp |
| `check_hashes` nhánh đa biến (`ban2/hashes.json`) | 10/10 tệp đạt | 10 tệp: khớp |
| Manifest gói Chương 4 ngày 01/11 | 12/12 tệp khớp SHA-256 | Gói gửi có 12 tệp: khớp |
| Unittest | 41/41 (workspace Phong) và 8/8 (test gói Vương), hai lượt riêng | Bộ 55 test chỉ có trên máy Vương vì Phong chưa nhận code mới |
| Lỗi thoáng qua | Lượt đầu lỗi `ImportError`: Windows Application Control chặn DLL `_binning` của scikit-learn; chạy lại đạt; không đổi chính sách bảo mật, không sửa code | Chưa rõ nguyên nhân, xem mục 7 |
| Pilot qua classifier; kiểm chéo Rules Recall@10 trên 50 giỏ | **Chưa làm** vì Phong chưa nhận gói đầu vào | Lỗi ở phía gửi (Vương chưa đóng ZIP mới), không phải gói sai |

Kết luận: môi trường hai máy tương thích và dữ liệu nền khớp hash. Hai việc còn lại chuyển sang mục 5.

Ghi chú trạng thái: gói pilot trong thiết kế (bước 2) không còn cần. Vương đã chạy trực tiếp trên validation đầy đủ nên gửi **gói A** (mục 5) thay cho gói pilot, và Phong dùng gói A để chạy thử luồng của mình.

## 2. Phân công (xác nhận mục 11.2, 11.3)

- [x] Giữ nguyên bảng 11.2: Vương làm code nền, đặc trưng, chỉ số xếp hạng, giai đoạn A, benchmark, chạy chính thức; viết **4.1, 4.2, 4.3.1** (khoảng 3,5 trang). Phong làm Pipeline, chỉ số phân loại, bootstrap, importance; viết **4.3.2, 4.4, 4.5, 4.6** (khoảng 5,5 trang) và hợp nhất QMD.
- [x] Ngoại lệ chủ sở hữu tệp: Phong ghi `m4_classifier.py`, `m4_test.py`, `m4_interpret.py`, `tests/test_m4_model.py`, `tests/test_m4_interpret.py`, `tests/test_m4_environment.py`; mọi tệp `m4_*` còn lại và `configs/m4_model.json` là của Vương. Người kia chỉ đọc và gửi đề xuất.
- [x] Mọi lượt chính thức (validation đầy đủ, benchmark, test) chạy trên máy Vương. Máy Phong chỉ phát triển và chạy mẫu nhỏ.

## 3. Môi trường (mục 9.2)

- [x] Môi trường chuẩn là `.venv-m2` khóa trong `requirements.txt` (23 dòng). Python 3.12.10 (Phong) và 3.12.14 (Vương) khác bản vá, chấp nhận; cả hai ghi trong hồ sơ.
- [ ] **Đã thống nhất môi trường (04/11):** bảng Master và benchmark M1 (trước đó chạy bằng Python toàn cục 3.12.10, pandas 3.0.3, PyArrow 24) đã được tạo lại trong `.venv-m2`. Master mới giống từng ô bản cũ, vẫn 16.992.331 byte, SHA-256 mới bắt đầu `2741c970`. Bảng 3.5 có số mới; QMD mục 2.5, 3.2 và 4 hình ban2 đã sửa theo (xem `GUI_phong_dong_bo_moi_truong_20261104`). Phong cần nhận Master mới nếu chạy `check_hashes()` của G0 trên máy Phong.
- [x] Số liệu đưa vào bài chỉ lấy từ máy Vương; số chạy trên máy Phong không dùng làm kết quả.
- [ ] Phong thêm một câu vào mục 2.5 của QMD: mọi lượt chính thức của Chương 4 chạy trên một máy (Windows 11, RAM 24 GB, `.venv-m2`). Vương không sửa QMD.
- [x] Không trích con số "Apriori mặc định cần khoảng 14 GB" vào bài vì chưa đo lại có lưu.
- [x] Chương 2 không sửa (không đổi đặc trưng, nhãn, chỉ số chính, cách chia tập).

## 4. Tham số (mục 4 và 9.4): giữ nguyên, đã dùng trong lượt chạy thật 01/11

Các tham số này ghi vào bản thiết kế trước khi chạy. Giữ nguyên để chứng minh không chỉnh theo kết quả. Đổi bất kỳ tham số nào thì phải chạy lại giai đoạn A, B, C và ghi lý do vào nhật ký.

| Tham số | Giá trị chốt |
|---|---|
| Seed che / mẫu âm / importance / bootstrap | 42 / 43 / 44 / 42 |
| K | 5 và 10; chỉ số chính Recall@10 |
| Bootstrap | 2.000 lần, ghép cặp theo người dùng, khoảng tin cậy phân vị 2,5%–97,5% |
| Lưới A | N ∈ {500; 1.000; 2.000}; min_count ∈ {20; 50}; max_len ∈ {2; 3}; min_confidence ∈ {0,05; 0,1} |
| Lưới B | LR: C ∈ {0,01; 0,1; 1; 10}; RF: max_depth ∈ {10; 20} × min_samples_leaf ∈ {20; 100} |
| Dung sai hòa | 0,002 |
| Mẫu âm | 20 mỗi giỏ, chỉ ở tập fit |
| Importance | 5.000 giỏ validation, 10 lần hoán vị, đo bằng AP |
| Quy tắc hòa khi xếp hạng | `product_id` tăng; Precision chia K; Recall chia |H| kể cả ngoài C |

Hai điều phải nêu trong bài (không đổi tham số): (a) cấu hình A chọn nằm ở cạnh lưới (min_count 20, max_len 2, min_confidence 0,05) nhưng cấu hình tốt nhất tuyệt đối (N = 2.000, max_len 3: 0,0944) chỉ hơn 0,0012, trong dung sai; (b) RF chọn độ sâu 10, min_samples_leaf 100 (0,0971) dù độ sâu 20, leaf 20 đạt 0,0990, vì chênh 0,0019 trong dung sai và suy luận nhanh hơn (48 giây so với 86 giây).

## 5. Giao diện dữ liệu (mục 11.4): ba chỗ lệch giữa thiết kế và code đã có

Đối chiếu ngày 04/11: các Parquet `masked_baskets`, `catalog`, `rules_grid`, `features_fit` và `basket_metrics_validation.csv` khớp cột và kiểu đã ghi. Ba chỗ còn lệch, đề nghị chốt như sau (sửa bản thiết kế cho khớp code, không sửa code):

| Thiết kế ghi | Thực tế | Đề nghị chốt |
|---|---|---|
| Hàm `iter_features(split, batch_size)` | Code dùng `make_batches(frame, ctx, idx, size)` trong `m4_common.py` | [x] Đổi tên trong thiết kế thành `make_batches`; Phong gọi hàm này |
| `rankings_<split>.parquet` (Top-10 mỗi giỏ) | Chưa có; code chỉ lưu chỉ số theo giỏ | [x] Không tạo bảng đầy đủ. Vương chỉ xuất bảng xếp hạng Top-10 của Rules cho 50 giỏ kiểm chéo (mục 6) để Phong phân biệt sai xếp hạng với sai chỉ số |
| `feature_schema.json` | Chưa có | [x] Bỏ. Nguồn duy nhất của tên và kiểu đặc trưng là `NUMERIC`, `CATEGORY` trong `m4_classifier.py` và `features_fit.parquet` |

Ghi thêm: `basket_metrics_<split>.csv` có cột `method` đặt cuối bảng (không ảnh hưởng đọc theo tên); `basket_metrics_test.csv` chỉ được tạo khi chấm test.

## 6. Việc kiểm chéo Recall@10 của Rules trên 50 giỏ (Phong)

Đặc tả để hai bên tính cùng một cách, không gọi lại hàm `evaluate` của Vương:

1. Lấy `masked_baskets.parquet`, `split == "validation"` và `eligible == True`; sắp theo `order_id` tăng; lấy 50 giỏ đầu.
2. Từ `rules_grid.parquet` chọn cấu hình đã chọn ở giai đoạn A: `top_n = 1000`, `min_count = 20`, `max_len = 2`, `confidence >= 0,05` (xem `lock.json`, mục `stage_A`).
3. Danh mục C là các sản phẩm `rank <= 1000` trong `catalog.parquet`. Ứng viên của một giỏ là C trừ phần `observed`.
4. Một luật khớp khi mọi sản phẩm của tiền đề nằm trong `observed`. Điểm của ứng viên là confidence lớn nhất trong các luật khớp có hậu đề là ứng viên đó; không khớp luật nào thì điểm 0.
5. Xếp ứng viên theo điểm giảm dần, hòa thì `popularity` giảm dần, hòa tiếp thì `product_id` tăng dần; lấy Top-10.
6. Recall@10 của giỏ = |Top-10 giao `hidden`| / |`hidden`|; mẫu số là mọi sản phẩm bị che, kể cả sản phẩm ngoài C. Giỏ không có ứng viên vẫn tính, tử số 0.
7. So từng giỏ và trung bình với dòng `method == "Rules"` trong `basket_metrics_validation.csv` (cột `R@10`, khớp theo `order_id`). Lưu danh sách mã giỏ, số trúng, mẫu số, hai giá trị Recall và sai lệch.

Đạt khi sai lệch từng giỏ bằng 0 (hoặc ≤ 1e-12) ở cả 50 giỏ. Nếu lệch, gửi danh sách giỏ lệch cho Vương trước khi làm tiếp.

## 7. Giai đoạn tiếp theo: việc của từng người

Thay đổi so với bảng 11.5: giai đoạn A, B, C đã chạy xong trên máy Vương (01/11), nên bước 2 đến 4 coi như hoàn thành phía Vương; `lock.json` hiện là bản nháp chờ Phong duyệt.

### Vương
- [ ] Đóng ZIP **gói A** `GUI_vuong_ch4_goiA_<ngày>.zip` trong `Chung/Gửi và nhận/Gửi/`: `m4_common.py`, `m4_validate.py`, `m4_lock.py`, `m4_report.py`, `m4_prepare.py`, `m4_mining.py`, `m4_benchmark_mining.py`, `configs/m4_model.json`, `tests/test_m4_data.py`, `requirements.txt`; đầu ra `DATA/Data phai sinh/M4/` (masked_baskets, catalog, rules_grid, features_fit, hashes.json; hai tệp `pipeline_*.joblib` chỉ gửi nếu Phong cần chạy lại suy luận); `BAO CAO/Bao cao mo hinh/` (validation_grid_A/B, validation_methods, basket_metrics_validation, classifier_validation, ablation, lock.json, benchmark và importance); kèm `README_GUI_*.md` và `DANH_SACH.txt` có SHA-256.
- [ ] Xuất bảng xếp hạng Top-10 của Rules cho 50 giỏ kiểm chéo, kèm trong gói A.
- [ ] Viết 4.1, 4.2, 4.3.1 và các bảng nguồn (Bảng 4.1, 4.2, kết quả benchmark khai phá); chỉ chép số từ CSV/JSON.
- [ ] Ghi nhật ký phiên làm việc.

### Phong
- [ ] Nhận gói A, kiểm SHA-256, chạy toàn bộ unittest trên máy Phong (kỳ vọng 55 test) và ghi kết quả.
- [ ] Làm kiểm chéo 50 giỏ theo mục 6; gửi lại kết quả.
- [ ] Viết `m4_test.py`: đọc `lock.json`; kiểm SHA-256 từng tệp liệt kê trong đó, sai thì dừng; nạp tập test một lần duy nhất; gọi `evaluate` và `make_batches` của `m4_common.py`; giữ `score` và `y`; tính chỉ số phân loại, bootstrap 2.000 lần ghép cặp; ghi `basket_metrics_test.csv` và kết quả kèm hash; chạy lần thứ hai thì từ chối. Kiểm thử bằng dữ liệu tự tạo trước, chưa chạm test thật.
- [ ] Thêm đường chạy thật cho `m4_interpret.py` (đầu ra vào `BAO CAO/Bao cao mo hinh/`, không còn hậu tố `_SYNTHETIC`) và hình Recall@K theo K = 1…10.
- [ ] Viết khung 4.3.2 đến 4.6 từ kết quả validation; sửa mục 2.5 (câu về Chương 4, mục 3 ở trên); sửa câu "hai bản xuất bản giống nhau" ở mục 3.2.

### Cả hai
- [ ] Phong duyệt `lock.json` sau khi kiểm chéo đạt. Bản nháp: phương pháp chính RF; N = 1.000, min_count 20, max_len 2, min_confidence 0,05; LR C = 0,1; RF độ sâu 10, min_samples_leaf 100. Số validation: Popularity 0,0752; Rules 0,0932; LR 0,0923; RF 0,0971; Recall@10 trần 0,521.
- [ ] Khóa xong (cả hai ghi "đã khóa" vào đây kèm ngày) thì **không sửa code, config hay mô hình**. Chạy `m4_test.py` và `m4_interpret.py` một lần trên máy Vương.
- [ ] Đọc chéo: Vương đọc 4.4–4.6, Phong đọc 4.1–4.3.1.

## 8. Điều kiện mở tập test

Chỉ mở khi đủ ba điều: (1) kiểm chéo 50 giỏ đạt; (2) `m4_test.py` có cổng kiểm tra khóa và đã chạy thử trên dữ liệu tự tạo; (3) cả hai đã duyệt `lock.json`. Test chưa được mở tại thời điểm viết tệp này.

## 9. Điểm lưu ý cho nộp bài và vấn đáp

- Lỗi DLL thoáng qua trên máy Phong chưa rõ nguyên nhân. Nếu xuất hiện lại khi chạy thử hoặc khi vấn đáp, chạy lại và ghi nhận trong nhật ký; không sửa chính sách bảo mật.
- Câu trả lời thống nhất về hai phiên bản Python: khác bản vá trong cùng dòng 3.12, thư viện tính toán khóa phiên bản, số trong bài lấy từ một máy, kết quả kiểm bằng hash; Master dạng Parquet đã được tạo lại trong `.venv-m2` ngày 04/11, giống từng ô bản tạo lần đầu ngày 20/10 (hai bản khác byte vì phiên bản PyArrow).
- Không nói hai máy cho kết quả giống hệt khi chưa có hồ sơ so sánh.

## 10. Theo dõi

| Mục | Vương | Phong | Ngày |
|---|---|---|---|
| Xác nhận phân công, môi trường, tham số (mục 2–4) | | | |
| Chốt giao diện (mục 5) | | | |
| Gói A đã gửi / đã nhận | Đã chuẩn bị gói A tại thư mục Gửi để chuyển cho Phong | Đã nhận; 52/52 tệp khớp SHA-256; 55/55 test đạt trên máy Phong (báo cáo nghiệm thu 04/11) | 04/11/2026 |
| Kiểm chéo 50 giỏ đạt | Khớp 50/50 trên máy Vương (04/11) | Khớp 50/50 giỏ và 500/500 dòng xếp hạng trên máy Phong; Vương tính lại, hai bảng giống hệt | 04/11/2026 |
| `m4_test.py` có cổng khóa | Đã chép nguyên bản cuối của Phong (m4_test, m4_common, test_m4_gate; hash khớp); 57/57 test đạt; chạy lại toàn bộ validation hai lượt, sáu tệp kết quả giống từng byte | Đã rà, thêm `n_jobs=1` cho RF, 58/58 test đạt trên máy Phong | 04/11/2026 |
| `lock.json` được duyệt | Đã tạo khóa nháp bằng `m4_lock.py` mới (16 tệp, hash `fe2db0a7`, approvals false) và gửi Phong rà (`GUI_phong_lock_nhap_20261104`) | Chờ Phong chạy `kiem_lock.py` và báo đồng ý | |
| Đã khóa | | | |

**Bàn giao phía Vương (04/11).** Gói `GUI_vuong_ch4_goiA_20261104.zip` kèm bản 4.1, 4.2, 4.3.1, bảng nguồn và 500 dòng xếp hạng cho 50 giỏ validation. Đối chiếu nội bộ của Vương đạt dung sai ở cả 50 giỏ. Phong thực hiện phép tính độc lập ở mục 6 và ghi kết quả vào phần theo dõi khi hoàn tất.

## Cập nhật xác nhận phía Phong sau rà mã chấm test — 04/11/2026

- [x] Xác nhận phân công, môi trường và giữ nguyên các tham số mục 4 (không thay kết quả chọn A/B/C).
- [x] Chốt phía Phong ba thay đổi giao diện mục 5: make_batches, không lưu rankings đầy đủ, không cần feature_schema.json riêng.
- [x] Đồng ý tính Recall@K với K=1 đến 10 cho Hình 4.1; chỉ số chọn mô hình vẫn Recall@10.
- [x] Đã nhận gói A, 50/50 giỏ kiểm độc lập đạt; 500 dòng Top-10 khớp, luồng suy luận 2.000 giỏ đạt (hồ sơ output/tiep_nhan_goiA_20261104).
- [x] Đã rà và tích hợp m4_test.py/m4_common.py; 57/57 test đạt (55 hiện có + 2 test mới). Mã test kiểm đầy đủ khóa, chặn khóa nháp và chạy lại, kiểm thử bằng dữ liệu tự tạo.
- [ ] Duyệt lock.json chính thức: chờ cập nhật hash mã nguồn, dữ liệu/môi trường cuối cùng và xác nhận của Vương trên mã Phong vừa sửa.
- [ ] Đã khóa / cho chạy test thật: chưa thực hiện.

Hiện G0 cũ trên Phong vẫn khớp hash. Chưa nhận gói đồng bộ chứa Master mới và hashes.json mới; khi nhận phải sao lưu, thay Master trước rồi cập nhật manifest và kiểm lại. Không tự ghi nhật ký. Biên bản này thay trạng thái tiến độ cũ ở mục 1/10 cho phía Phong; giữ thông tin lịch sử để đối chiếu.
