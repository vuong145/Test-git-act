# Gửi Phong — đã áp đề xuất sửa theo góp ý (07/11/2026)

## 1. Đã làm theo tệp duyệt của Phong

- **Lời văn và tài liệu tham khảo:** áp đủ 23 câu sửa và hai mục `hu2020`, `li2023`. QMD và `references.bib` sau khi áp **trùng từng byte** với bản thử trong gói `DE_XUAT_SUA_THEO_GOP_Y_20261107`.
- **Hình (một đợt riêng):**
  - `scripts/m2_plot_multivariate.py`: dùng dấu phẩy thập phân cho nhãn heatmap trung vị (8,5), cho heatmap Spearman và Pearson (0,863), và cho thanh màu của hai heatmap tương quan và heatmap lift. Tiêu đề khung (a) đổi thành "(a) Median"; cách đánh dấu \* cho ô dưới 30 giỏ giữ nguyên.
  - `scripts/m4_report.py`: trục hình importance dùng dấu phẩy. Hình được vẽ lại bằng hàm `figure()` từ `importance.csv`, không chạy lại phần tính toán.
  - Hình Recall@K giữ nguyên.
  - Hai hình của `m2_plot_univariate.py` không có số thập phân nên không vẽ lại. Hình tần số theo thời gian chạy lại cho ra tệp giống từng byte bản cũ.
- **Kiểm tra:**
  - `check_hashes` đạt ở đầu và cuối script.
  - `plot_data/` giống từng byte bản trước.
  - Hình trong `assets/` giống từng byte bản do code sinh.

## 2. Kết quả kiểm

- **PDF:** 44 trang; **từ bìa đến hết Chương 5 = 42 trang** (giới hạn 45). Các chương bắt đầu ở trang PDF 9, 12, 16, 30, 38; tài liệu tham khảo ở trang 43–44. Không có `??`; hai tài liệu mới có trong danh mục và được trích ở 2.2.
- **Kiểm thử và khóa:** unittest đạt 57/57; `lock.json` khớp 16/16 tệp; `hashes.json` common 6/6, ban2 10/10, M4 6/6.
- **Hash mới (16 ký tự đầu):**

  | Tệp | Hash |
  |---|---|
  | QMD | `cfbb8f34b1565296` |
  | PDF | `a05a14913ec4ae69` |
  | `references.bib` | `10144d7bd0df42a9` |
  | `m2_plot_multivariate.py` | `b909d52186266fcf` |
  | `m4_report.py` | `f9ef4f84c176d89e` |

- `toàn bộ mã nguồn.md` đã sinh lại: 48 tệp, 5.314 dòng.

## 3. Trong gói

- `01_DE_DOC/`: PDF mới và nhật ký.
- `02_TEP_DA_DOI_theo_duong_dan_thu_muc_bai/`: mọi tệp đã đổi, đặt theo đường dẫn trong thư mục bài. Gồm QMD, bib, hai script, các hình trong `assets/` và `BAO CAO/.../figures/`, nhật ký, `toàn bộ mã nguồn.md`.
- `03_SO_SANH_truoc_sau/`: diff của QMD, bib và hai script; kèm PDF bản trước khi áp.
- `DANH_SACH.txt`: SHA-256 từng tệp.

## 4. Phong kiểm và nhận làm bản chính

1. Kiểm hash theo `DANH_SACH.txt`.
2. Sao lưu bản trên máy Phong.
3. Chép thư mục `02_...` vào thư mục bài.
4. Chạy unittest.
5. Xem PDF.

## 5. Còn mở

- **"Vol. 398" của Hosmer** (`references.bib` dòng 46): chưa xác minh. APA 7 không ghi số trong bộ sách cho sách một tập, nên đề xuất bỏ trường `volume`. Phong quyết.
- **Câu phân công trong Lời cam đoan:** chờ hai người duyệt.
- **Bảng 4.6:** dòng "Nguồn" nằm đầu trang sau bảng. Đây là lỗi nhỏ về hình thức.
