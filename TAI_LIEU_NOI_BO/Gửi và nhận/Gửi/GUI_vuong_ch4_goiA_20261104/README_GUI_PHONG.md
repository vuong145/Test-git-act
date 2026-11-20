# Gói A của Vương – Chương 4, ngày 04/11/2026

Gói bàn giao từ lượt validation đầy đủ trên máy Vương. Phong dùng để kiểm môi trường, chạy thử luồng phân loại trên dữ liệu phát triển và tự kiểm chéo Rules. Bản `lock.json` ghi kết quả A–C tại ngày chạy và đang chờ duyệt. Các điều kiện mở test ghi ở mục 8 của biên bản lần 1.

## Nhận và kiểm tệp

1. Giải nén ZIP vào thư mục tạm. Chạy lệnh dưới đây **tại thư mục vừa giải nén** để so SHA-256 của từng tệp trong danh sách.
2. Chép theo đường dẫn tương đối vào một bản làm việc của thư mục bài. Môi trường dùng bộ phiên bản trong `requirements.txt`. Kiểm tra `tai_lieu/PHU_THUOC_CO_SAN.txt` với cây đã có bên Phong. Danh sách này ghi hash các script phụ thuộc và test dùng trên máy Vương. Nếu bản của Phong khác thì đối chiếu trước khi tích hợp.
3. Tại thư mục bài, chạy các lệnh ở khối thứ hai. `lock.json` dẫn tới cả hai Pipeline đã huấn luyện. Gói mang theo cả hai vì cần chúng để kiểm hash và tái sử dụng cho suy luận validation.
4. Trên máy Vương, bộ test hiện tại chạy 55 test. Ghi số thực chạy trên máy Phong và mọi lỗi nếu có.

```powershell
$entries = Import-Csv -LiteralPath 'DANH_SACH.txt' -Delimiter ([char]9)
foreach ($entry in $entries) {
    $actual = (Get-FileHash -LiteralPath $entry.path -Algorithm SHA256).Hash
    if ($actual -ne $entry.sha256) { throw "SHA-256 khác: $($entry.path)" }
}
"Đạt: $($entries.Count) tệp"
```

```powershell
.\.venv-m2\Scripts\python.exe -c "import sys; sys.path.insert(0,'scripts'); from project_io import check_hashes; check_hashes(); check_hashes('DATA/Data phai sinh/M4/hashes.json'); check_hashes('BAO CAO/Bao cao mo hinh/lock.json'); print('OK')"
.\.venv-m2\Scripts\python.exe -m unittest discover -s tests -p 'test_*.py'
```

## Phong kiểm chéo 50 giỏ

Lấy 50 giỏ đầu trong validation có `eligible=True`, sau khi sắp `order_id` tăng dần. Tính độc lập theo bước 1–7 mục 6 của biên bản lần 1. Để giữ phép kiểm độc lập, tự sinh thứ hạng từ giỏ quan sát, danh mục và luật trước khi mở bảng kết quả của Vương. Loại ứng viên đã có trong giỏ. Phá hòa lần lượt bằng độ phổ biến giảm dần và mã sản phẩm tăng dần. Recall@10 của từng giỏ có mẫu số là toàn bộ sản phẩm bị che.

- `tai_lieu/rules_top10_50.csv` là 500 dòng xếp hạng xuất từ phía Vương, score là confidence lớn nhất hoặc 0. Có cột hit để tìm nguyên nhân nếu số trúng lệch.
- `tai_lieu/doi_chieu_50_may_Vuong.csv` đối chiếu bản xuất với bảng chỉ số chính thức của máy Vương. Phong ghi bảng đối chiếu của mình, gồm mã giỏ, số trúng, mẫu số và sai lệch. Ngưỡng cho từng giỏ là 1e-12.
- `tai_lieu/xuat_bang_goi_A.py` tái xuất các bảng bàn giao của Vương. Chạy từ thư mục bài bằng Python của dự án. Script này dùng hàm khớp luật phía Vương, vì thế dành cho tái lập bản xuất của Vương.
- Có thể dùng hai Pipeline trong gói để chạy thử phần suy luận trên các giỏ validation đã chọn. Đối với điểm số báo cáo, dùng các CSV của lượt chạy chính thức trên máy Vương.

## Tài liệu ghép QMD

`tai_lieu/PHAN_VUONG_CHUONG4.qmd` là ba mục để Phong ghép vào các tiêu đề hiện có. Phần Apriori và FP-Growth thuộc mục 4.3.1. Khi ghép, để Quarto tự đánh số bảng. Tổng dung lượng theo trang cần đo ở lần render của bản chính.

| Bảng hoặc luận điểm | Tệp nguồn tương đối trong ZIP |
|---|---|
| Bảng 4.1 và danh sách biến | `tai_lieu/bang_4_1_dac_trung.csv`, `scripts/m4_common.py`, đối chiếu `NUMERIC/CATEGORY` của Phong |
| Tương quan trên fit, phép bỏ nhóm trên validation | `BAO CAO/Bao cao mo hinh/feature_correlation.csv`, `ablation.csv` cùng thư mục |
| Bảng 4.2 | `tai_lieu/bang_4_2_phan_hoach.csv`, từ `dataset_description.csv` và số người dùng trong G0 của hai máy. Số liệu đánh giá test dành cho lượt sau khi duyệt khóa. |
| Lựa chọn lưới A | `BAO CAO/Bao cao mo hinh/validation_grid_A.csv` và trường stage_A của `lock.json` |
| Bảng 4.3 | `tai_lieu/bang_4_3_benchmark.csv`, từ sáu lượt mỗi cấu hình trong `mining_benchmark_N1000_c20_l2.csv`, `mining_benchmark_N2000_c20_l3.csv` và JSON tương đương cùng hậu tố |
| Dữ liệu cho phần Phong | Lưới B, chỉ số phân loại, bảng theo giỏ, bỏ nhóm, importance, hệ số LR, ví dụ và hình trong `BAO CAO/Bao cao mo hinh/` |

Số Recall ở lưới B và thời gian suy luận ở `validation_methods.csv` có thể thuộc các lần chấm khác nhau. Khi viết lý do chọn cấu hình RF, dùng các dòng của chính `validation_grid_B.csv`. Các tệp mô tả và importance trong gói là kết quả fit/validation. Biên bản, thiết kế cập nhật và hướng dẫn phân việc đặt trong `tai_lieu/`.
