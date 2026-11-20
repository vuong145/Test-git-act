# Gửi Phong — đối chiếu toàn bộ bài và workspace (11/11/2026)

Gói này dùng để Phong đối chiếu toàn bộ bài và workspace với máy của Phong, đồng thời duyệt phần bổ sung nguồn ngày 11/11.

## 1. Bản hiện tại

| Tệp | SHA-256 (16 ký tự đầu) |
|---|---|
| QMD | `79cf06b0bb10a865` |
| PDF | `1807db1ab1e9169a` |
| `references.bib` | `8c7864f78491c957` |
| `nhật ký làm việc.md` | `f581f5aa1a471d83` |
| `toàn bộ mã nguồn.md` | `d51bde398363e498` |

- PDF có 44 trang; từ bìa đến hết Chương 5 là 42 trang; không có `??`.
- Kiểm tra: 57/57 test đạt; `lock.json` khớp 16/16; `hashes.json` khớp 6/6, 10/10, 6/6. Đã kiểm ngay trên bản nộp mới.
- **Thay đổi so với bản chốt ngày 07/11** (Vương làm, Phong chưa duyệt):
  - Thêm 4 nguồn vào bib: `holm1979`, `efron1979`, `chapman2000`, `sklearn_permutation`.
  - Sửa `pedregosa2011` cho đủ 16 tác giả.
  - Sửa `kaminskas2016` để PDF hiện "Article 2".
  - Thêm trích dẫn ở các mục 2.2, 2.3, 2.4, 3.6, 4.4 và 4.5.
  - Rút hai câu ở 4.4 và 4.5 để giữ nguyên số trang.
  - Sửa năm lỗi nhỏ theo bản đánh giá (đợt 17:00):
    - 1.4: `purchase_label` đổi thành $y$.
    - 2.5: câu thành "Nhật ký ghi đúng công cụ…", bỏ cụm "tại gốc".
    - Bib: tên ba tài liệu (Cohen, Kohavi, Kaminskas) đổi sang kiểu viết hoa của APA 7.
    - `scripts/README.md`: sửa tiêu đề và đường dẫn.
    - `m2_plot_univariate.py`: thêm dấu chấm phân cách hàng nghìn cho Hình 3.2–3.3. Đã vẽ lại; `plot_data` giống từng byte.
  - Diff chi tiết nằm trong `04_.../`. **Phong cần duyệt các chỗ sửa trong bib và trong phần văn của Phong (1.4, 2.2–2.4, 2.5, 3.6).**
- Code, cấu hình, test và style so với bản chốt 07/11: chỉ khác `scripts/m2_plot_univariate.py` và `scripts/README.md` (đợt 17:00). Kiểm tự động trùng từng byte: **không, đúng như dự kiến**.
- **Không gửi tệp CSV** để gói nhẹ. Mọi CSV vẫn được liệt kê kèm SHA-256 và dung lượng trong `03_CAU_TRUC_THU_MUC/`.

## 2. Gói gồm

- `00_DANH_GIA/DANH_GIA_THEO_RUBRIC_20261111.md`: chấm ước lượng theo 5 trụ cột; danh sách tám lỗi nhỏ; mục 6 ghi trạng thái đã sửa.
- `01_BAI_TIEU_LUAN/`: PDF, QMD, bib, nhật ký và `toàn bộ mã nguồn.md`.
- `02_MA_NGUON/`: `scripts/`, `tests/`, `configs/`, `styles/`, `assets/` (hình trong bài) và `requirements.txt`, đúng như trong bản nộp; không kèm CSV.
- `03_CAU_TRUC_THU_MUC/`:
  - `CAY_THU_MUC_BAN_NOP.txt`: cây thư mục của bản nộp, kèm số tệp và dung lượng.
  - `SHA256_MOI_TEP_BAN_NOP.tsv`: SHA-256 của toàn bộ 380 tệp trong bản nộp, kể cả dữ liệu. Phong dùng bảng này để so với workspace trên máy mình mà không cần chép dữ liệu nặng.
- `04_SO_SANH_voi_ban_chot_07-11/`: diff của QMD, bib, `m2_plot_univariate.py` và `scripts/README.md`.
- Gói này thay cho gói `GUI_PHONG_DOI_CHIEU_TOAN_BO_20261111` tạo lúc 16:30; gói cũ đã chuyển vào `Chung/archive/`.
- `DANH_SACH.txt`: SHA-256 của từng tệp trong gói.

## 3. Hồ sơ nộp

- Bản nộp mới: `TLCK/NOP_BAI_20261111/2521001118_Nhom01_TieuLuan/` (380 tệp, 1.46 GiB).
- Đã bỏ khỏi bản nộp: `.venv-m2`, `__pycache__`, `.mplcache`, `render_pdf.log`, lượt làm sạch ngày 19/10, các tệp nháp trong `review/`, `BAO_CAO_GUI_CHATGPT.zip`, `master_benchmark.*`.
- Bản `NOP_BAI_20261107/` đã cũ, không dùng để nộp.

## 4. Phong làm

1. Kiểm hash theo `DANH_SACH.txt`.
2. So workspace của Phong với `SHA256_MOI_TEP_BAN_NOP.tsv`.
3. Duyệt diff ở `04_.../`.
4. Trả lời các việc ở mục 3 của tệp đánh giá.
5. Gửi kết quả vào `Chung/Gửi và nhận/Nhận/`.
