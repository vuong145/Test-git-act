# THỐNG NHẤT PHÂN VIỆC GIỮA HAI THÀNH VIÊN — PRJ-08

Ngày 31/10/2026. Tài liệu này là bản chốt cuối cùng về vai trò và việc cần làm. Khi khác với `KE_HOACH_HOAN_THANH_CHUONG3_VA_RUT_GON.md` hoặc `HUONG_DAN_RUT_GON_CODE.md` về **vai trò, phân công hoặc quyết định**, theo tài liệu này. Phần kỹ thuật (cách rút gọn từng file, công cụ so sánh đầu ra, quy tắc code tối thiểu, quy tắc gói ZIP) vẫn dùng hai tài liệu kia.

Đường dẫn tính từ thư mục bài `2521001118_Nhom01_TieuLuan/`, trừ khi ghi rõ gốc `TLCK/`.

---

## 1. Quy định của giảng viên (đã xác nhận)

- **Tối đa 45 trang, tính từ bìa đến hết Chương 5.**
- **Mã nguồn và nhật ký làm việc nộp thành tệp riêng**, không đưa vào PDF.
- Bố cục theo khung trong `projects.pdf` (bìa → cam đoan → mục lục → các danh mục → tóm tắt → Chương 1–5 → tài liệu tham khảo).
- Chữ thân bài và bảng 12 pt; không thu nhỏ chữ hay lề để ép trang. Muốn hình nhỏ hơn thì vẽ lại trong code, không co ảnh.

## 2. Vai trò

| Người | Vai trò | Sở hữu (chỉ người này ghi vào) |
|---|---|---|
| **Phong** | **Người hợp nhất**: ghép nội dung, viết lời văn, render, giữ bản QMD chính | `2521001118_Nhom01_TieuLuan.qmd`, `references.bib`, `drafts/`, phần cấu hình trong đầu QMD |
| **Vương** | **Rút gọn toàn bộ code đến hết Chương 3**; góp ý và duyệt nội dung | `scripts/`, `tests/`, `configs/`, `requirements*.txt`, các đầu ra trong `DATA/Data phai sinh/` và `BAO CAO/` do code tạo ra |

- Bản chính của **QMD/PDF** nằm trên máy Phong. Bản chính của **code** nằm trên máy Vương.
- Ngoại lệ Chương 4 (01/11): Phong ghi `scripts/m4_classifier.py`, `scripts/m4_test.py`, `scripts/m4_interpret.py` và các test của chúng; mọi tệp khác trong `scripts/`, `tests/`, `configs/` vẫn do Vương ghi.
- Không ai sửa file thuộc phần người kia. Cần sửa thì gửi đề xuất, người sở hữu sửa.
- Trao đổi bằng gói ZIP nhỏ theo mục 1.2 của `KE_HOACH_HOAN_THANH_CHUONG3_VA_RUT_GON.md`: chỉ chứa file mới hoặc đã đổi, kèm `DANH_SACH.txt` ghi SHA-256; không gửi lại toàn bộ thư mục bài.

## 3. Trạng thái hiện tại (31/10)

- Chương 3 đã ghép đủ 3.4–3.6 vào QMD chính. PDF render ngày 30/10, **55 trang** (Chương 3 chiếm 34 trang).
- Lời văn phần Phong (mô tả hình 3–5, I4, I5, mục 3.6) đang **giữ nguyên bản thảo của Phong**, chỉ chuẩn hóa hình thức (số kiểu Việt, ghi p là "< 0,001", nhãn bảng/hình).
- I1–I3 hiện chỉ là bằng chứng số liệu từ `drafts/m2/ban1_evidence_i1_i3.md`, chưa viết thành văn.
- Bản QMD có lời văn viết lại đầy đủ hơn (thêm mức nền lift 210 cặp, diễn giải V, mô tả hình chi tiết) được lưu tại `TLCK/Chung/archive/truoc-ghep-chuong3_20261030/QMD_ban_ghep_viet_lai_22h41.qmd`, dùng để tham khảo khi viết bản cuối.
- Code của Phong đã đưa vào `scripts/` (đường dẫn `DATA/…`, `BAO CAO/…`, kiểm tra dữ liệu bằng hash qua `scripts/m2_data_hashes.py`). Đầu ra khớp gói Phong gửi; riêng `correlation_pearson.csv` lệch ở chữ số thứ 16 do làm tròn máy.
- `BAO CAO/Bao cao EDA/common/hashes.json` đã được **tạo lại** ngày 30/10 sau khi bị ghi đè nhầm: cùng hash dữ liệu nền, chỉ khác nội dung chữ của file JSON. Cần ghi điều này vào nhật ký.

## 4. Việc của Phong (người hợp nhất)

**4.1. Hoàn thiện lời văn Chương 3**

- Viết bản cuối 5 insight theo khung: số đo + mẫu số → cơ chế kinh tế → hành động có thể thử → giới hạn. Tham khảo bảng gợi ý ở bước A4 của kế hoạch và bản QMD lưu trữ ở mục 3.
- Viết lại đoạn "Diễn giải và giới hạn" của 3.6: cỡ hiệu ứng V (0,15–0,20 là liên hệ nhỏ), kích thước giỏ là yếu tố gây nhiễu, so với mức nền lift của 210 cặp (nếu hai bạn chốt ở mục 6).
- Mọi con số chép từ CSV, không chép từ bản tóm tắt hay từ lời công cụ AI.

**4.2. Viết Chương 4 và Chương 5** (sau khi Vương xong đợt rút gọn code, xem mục 5.3)

- Chương 4 tối đa **9 trang**, Chương 5 tối đa **4 trang**, viết đúng ngân sách ngay từ đầu.
- Áp dụng ngay khi viết: dòng nguồn ngắn; không nêu tên file `.csv`/`.json`/`.py` trong lời văn; mỗi số liệu chỉ nói chi tiết một lần; các câu "không chứng minh nhân quả" gom về 5.3.

**4.3. Rút ngắn toàn bài xuống 45 trang** (làm sau cùng, khi đã đủ 5 chương)

| Phần | Hiện tại | Ngân sách |
|---|---|---|
| Phần đầu (bìa, cam đoan, mục lục, 3 danh mục, tóm tắt) | 9 | **7** (mục lục chỉ hiện chương và mục cấp 2) |
| Chương 1–2 | 7 | **6** |
| Chương 3 | 34 | **17** |
| Chương 4 | — | **9** |
| Chương 5 | — | **4** |
| Tài liệu tham khảo | 1 | **1** |
| **Tổng** | | **44** (dư 1 trang) |

Cách rút Chương 3 (đã đo thử bằng render: chỉ chỉnh trình bày còn khoảng 27 trang; cắt mạnh chữ còn khoảng 20; gộp thêm bảng xuống khoảng 17):

- Bỏ lệnh `\clearpage` trong Chương 3; đổi `fig-pos=H` để hình không bị ép gây khoảng trắng.
- Bảng 134 quầy chỉ giữ Top-10.
- 3.2 và 3.3 cắt khoảng một nửa lời văn, giữ đủ các bảng mà rubric chấm (6 tệp, ghép bảng, kiểu dữ liệu trước–sau, benchmark, quy tắc làm sạch, đối soát trước–sau).
- Gộp bảng: 3.8 với 3.9; Top-10 ngành với Top-N; hai bảng ở 3.6.
- Bỏ hai phụ lục (mã nguồn, nhật ký) khỏi QMD; thêm một câu ở 2.5 nói mã nguồn và nhật ký nộp kèm dạng tệp riêng.

**4.4. Render và kiểm tra** mỗi khi nhận gói code mới của Vương: số trang, cỡ chữ, tham chiếu bảng/hình, không còn ô chờ.

## 5. Việc của Vương (rút gọn code đến hết Chương 3)

**5.1. Phạm vi.** Theo `HUONG_DAN_RUT_GON_CODE.md` mục 3, gồm:

- Làm sạch: `common.py` + `clean_vuong.py` + `clean_phong.py`; bỏ hai bản code giống nhau từng byte và code chết.
- Master: `m1_build_master.py` viết gọn (vòng lặp 4 phép ghép, bỏ ghi trùng). **`m1_benchmark.py` giữ nguyên** (đã chốt).
- Nền G0: gộp thành một script, kiểm tra bằng hash đơn giản; bỏ chuỗi manifest–acceptance–`latest.json`–`runs/`.
- EDA và kiểm định (cả phần của Phong): gọn code, bỏ code sinh lời văn QMD; phần kiểm tra độc lập chuyển vào `tests/`. **Holm giữ bản tự viết** (đã chốt).
- Một file tiện ích chung, một file `requirements.txt`, xóa/lưu trữ theo mục 5 của hướng dẫn rút gọn.
- Vẽ lại các hình với kích thước nhỏ hơn trong code (giảm `figsize`), giữ chữ 12 pt, theo quyết định ở mục 6.

**5.2. Điều kiện coi là xong**

- `TLCK/Chung/tools/so_sanh_dau_ra.py` báo khớp: CSV giống từng byte, Parquet giống nội dung. Riêng hình vẽ lại sẽ khác, đó là thay đổi có chủ đích.
- Test đạt hết.
- **Tên và đường dẫn đầu ra mà QMD dùng không đổi** (danh sách ở mục 7). Muốn đổi phải báo Phong trước.
- Phong đã đọc lại phần code của Phong sau khi rút gọn và giải thích được (vấn đáp có thể hỏi bất kỳ dòng nào).
- **Phong tự chạy `clean_phong.py` trên máy Phong**; `orders.csv`, `products.csv`, `order_products__train.csv` khớp hash cũ.
- Có phiên nhật ký: số dòng trước/sau, kết quả so sánh.

**5.3. Thứ tự.** Rút gọn xong và gửi gói code cho Phong **trước khi bắt đầu code Chương 4**, để Chương 4 dùng ngay hạ tầng đã gọn.

**5.4. Góp ý và duyệt.** Đọc chéo lời văn Chương 3–5 của Phong; kiểm tra ngẫu nhiên khoảng 10 con số mỗi chương với CSV.

## 6. Những điểm hai bạn phải chốt trước khi làm

| # | Cần chốt | Đề xuất |
|---|---|---|
| 1 | **Ai viết code Chương 4** (Apriori/FP-Growth, đặc trưng, LR/RF, đánh giá, bootstrap) | Chưa phân công. Phải chốt trước khi Vương xong rút gọn |
| 2 | I5 và 3.6 có đưa so sánh với mức nền lift 210 cặp ngành không | Có (đã chọn trước đó): lift trung vị 1,225; 182/210 cặp có lift > 1; dữ liệu trong `BAO CAO/Bao cao EDA/ban2/lift_baseline.csv` |
| 3 | Hình Pearson (hình bổ trợ) | Bỏ khỏi thân bài, giữ một câu nêu hệ số Pearson cùng chiều với Spearman |
| 4 | Bảng 21 ngành | Bỏ bảng, in tên ngành lên trục heatmap khi vẽ lại hình |
| 5 | Bảng 134 quầy | Giữ Top-10 trong thân bài; bảng đầy đủ để trong CSV |
| 6 | Kích thước hình vẽ lại | Rộng 16 cm như cũ, giảm chiều cao (ví dụ còn khoảng 2/3), chữ vẫn 12 pt |
| 7 | Nhật ký làm việc | Chỉ một file `TLCK/nhật ký làm việc.md`; Phong gửi tóm tắt từng phiên để ghi vào file chung |
| 8 | Tài liệu tham khảo có tính trong 45 trang không | Hỏi lại thầy; ngân sách đang tính cả trang này cho chắc |
| 9 | Cập nhật tài liệu nội bộ | Sửa `roadmap.md`, `NGAN_SACH_TRANG_VA_API.md`, `HUONG_DAN_VIET_TIEU_LUAN_QMD.md`: 45 trang là **yêu cầu của giảng viên**, tính từ bìa đến hết Chương 5; mã nguồn và nhật ký nộp riêng. Phong sửa vì đây là tài liệu trình bày |

## 7. Đầu ra mà QMD đang dùng (không đổi tên khi rút gọn code)

**Hình**

- `BAO CAO/Bao cao EDA/figures/ban1/fig-ref-basket-distribution.pdf`
- `BAO CAO/Bao cao EDA/figures/ban1/fig-ref-category-concentration.pdf`
- `BAO CAO/Bao cao EDA/figures/ban2/fig-ref-time-frequency.pdf`
- `BAO CAO/Bao cao EDA/figures/ban2/fig-ref-time-basket-size.pdf`
- `BAO CAO/Bao cao EDA/figures/ban2/fig-ref-corr-spearman.pdf`
- `BAO CAO/Bao cao EDA/figures/ban2/fig-ref-corr-pearson.pdf` (nếu chốt bỏ ở mục 6.3 thì Phong xóa tham chiếu trước)
- `BAO CAO/Bao cao EDA/figures/ban2/fig-ref-department-lift.pdf`

**Bảng số và dữ liệu** mà lời văn trích: các CSV trong `BAO CAO/Bao cao EDA/` (8 bảng 3.4, `reference_outliers.json`), `BAO CAO/Bao cao EDA/ban2/` (đa biến, `hypotheses.csv`, `lift_baseline.csv`), các báo cáo làm sạch và Master đang được 3.2–3.3 trích.

Trước khi xóa hoặc đổi tên bất kỳ file nào, tìm tên file đó trong QMD.
