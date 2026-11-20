# Gửi Phong — BẢN CHỐT bài tiểu luận (07/11/2026)

Gói này **thay cho hai gói gửi trước trong ngày 07/11**: `GUI_PHONG_DA_AP_DE_XUAT_20261107` và `GUI_PHONG_BO_VOL398_20261107`. Phong chỉ cần nhận gói này. Gói gồm mọi tệp đã đổi kể từ bản 06/11 Phong đang có (QMD `99dfb455`).

## 1. Thay đổi so với bản 06/11

- **Lời văn:** đã áp đủ 23 câu sửa theo bản Phong duyệt (`Nhận/Gửi Vương_Duyệt đề xuất sửa theo góp ý_20261107.md`):
  - ý 2: $m$ là biên lợi nhuận tăng thêm;
  - ý 3: sửa mục tiêu 2, và mục 3.2 ghi 600,79 giây làm sạch bảng prior;
  - ý 6: thêm Hu (2020) và Li (2023) vào mục 2.2;
  - rút 11 câu rào đón ở Chương 5;
  - thêm số liệu vào kết luận câu hỏi 1;
  - sửa câu "ô dưới 30 giỏ";
  - ghi cách tính tỷ lệ 22,3%;
  - 4 câu bù trang.
- **Phần không dùng bảng prior:** giữ nguyên, không sửa.
- **Tài liệu tham khảo:** thêm `hu2020` và `li2023`; mục `hosmer2013` bỏ `volume={398}` và giờ ghi "(3rd ed.)".
- **Hình:**
  - Dùng dấu phẩy thập phân: `m2_plot_multivariate.py` cho các heatmap trung vị, Spearman, Pearson và lift; `m4_report.py` cho hình importance, vẽ lại từ `importance.csv`.
  - Tiêu đề khung (a) đổi thành "(a) Median".
  - Hình Recall@K giữ nguyên.
  - `plot_data/` giống từng byte bản cũ; `check_hashes` đạt.
- **Quyết định đã chốt:** câu phân công trong Lời cam đoan đã duyệt; dòng "Nguồn" của Bảng 4.6 giữ nguyên.

## 2. Hash bản chốt (16 ký tự đầu)

| Tệp | SHA-256 |
|---|---|
| QMD | `cfbb8f34b1565296` |
| PDF | `cd4dea05ef74c400` |
| `references.bib` | `c5c0e7d0c5435d28` |
| `m2_plot_multivariate.py` | `b909d52186266fcf` |
| `m4_report.py` | `f9ef4f84c176d89e` |
| `nhật ký làm việc.md` | `31014e63cad710a4` |
| `toàn bộ mã nguồn.md` | `97c394f22cb8151d` |

## 3. Kiểm tra đã chạy

- PDF có 44 trang; **từ bìa đến hết Chương 5 = 42 trang** (giới hạn 45). Không còn chỗ tham chiếu lỗi (`??`).
- 57/57 test đạt.
- `lock.json` khớp 16/16; `hashes.json` khớp 6/6, 10/10, 6/6.
- Nhật ký: 72/72 liên kết mở được.

## 4. Hồ sơ nộp

- Bản nộp đã dọn: `TLCK/NOP_BAI_20261107/2521001118_Nhom01_TieuLuan/`, gồm 380 tệp, 1,46 GiB.
- Đã bỏ khỏi bản nộp: `.venv-m2`, `__pycache__`, `.mplcache`, lượt làm sạch ngày 19/10, các tệp nháp trong `review/` và các tệp tạm.
- Đã kiểm trên chính bản nộp: liên kết, tài nguyên của QMD, khóa và unittest.
- Các tệp trong gói này trùng với bản nộp: **có**.

## 5. Gói gồm

- `01_DE_DOC/`: PDF, nhật ký, `toàn bộ mã nguồn.md`.
- `02_TEP_DA_DOI_theo_duong_dan_thu_muc_bai/`: mọi tệp đã đổi, đặt đúng đường dẫn trong thư mục bài.
- `03_SO_SANH_voi_ban_06-11/`: diff của QMD, bib và hai script so với bản 06/11; kèm PDF bản 06/11.
- `DANH_SACH.txt`: SHA-256 của từng tệp.

## 6. Phong làm

1. Kiểm hash theo `DANH_SACH.txt`.
2. Sao lưu bản trên máy Phong.
3. Chép `02_...` vào thư mục bài.
4. Chạy unittest.
5. Xem PDF.
6. Xác nhận phần văn Chương 3 của Phong đã được rút gọn từ ngày 05/11.
7. Chuẩn bị nhật ký nộp riêng của Phong.

Live code vấn đáp làm sau.
