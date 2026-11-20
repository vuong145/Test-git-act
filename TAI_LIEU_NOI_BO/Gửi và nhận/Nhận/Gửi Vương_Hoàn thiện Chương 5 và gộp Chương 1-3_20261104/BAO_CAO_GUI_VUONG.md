# Phong gửi Vương — hoàn thiện Chương 5 và gộp Chương 1–3

Thực hiện ngày 04/11/2026 theo `HUONG_DAN_HOAN_THIEN_CHUONG5_VA_M4_VALIDATE_20261104.md`, phần A. Phần B do Vương phụ trách; Phong không sửa `m4_validate.py`, scripts, tests, configs, mô hình hoặc lock, không chạy lại validation/test/cleaning/Master.

## A1–A2: đã sửa đủ

| Góp ý | Thay đổi trong QMD và bản tách `chuong5.qmd` |
|---|---|
| Cạnh dưới của lưới | Chỉ rõ min_count=20, max_len=2, min_confidence=0,05 ở mức thấp nhất; N=1.000 nằm giữa {500; 1.000; 2.000}. Sửa cùng ý ở câu giới hạn 4.6 để không mâu thuẫn |
| Ba cặp ngành | Ưu tiên dry goods pasta–pantry; bakery–dairy eggs gần trung vị, produce–meat seafood dưới trung vị; hai cặp này chỉ thử khi có lý do kinh doanh riêng |
| RF–Rules | Bảng, đoạn diễn giải, kết luận và tóm tắt đều phân biệt đây là so sánh bổ trợ chưa hiệu chỉnh đa so sánh. Căn cứ xác nhận chính là RF–Popularity |
| Trích dẫn | Thêm Kohavi, Tang & Xu (2020) cho thiết kế thử nghiệm trực tuyến; Kaminskas & Bridge (2016) cho đa dạng/độ phủ bên cạnh accuracy. Đã mở nguồn thật, không lấy metadata từ câu trả lời AI |
| Bảo mật | Nêu phân quyền tài khoản, tách khóa giả danh nếu doanh nghiệp tạo bảng ánh xạ, nhật ký truy cập, dữ liệu thử nghiệm đã loại định danh trực tiếp, giới hạn lưu, từ chối gợi ý và tiếp nhận yêu cầu xóa. Ghi rõ là đề xuất triển khai, chưa phải chức năng đồ án đã xây dựng |
| Chi phí RF | Thêm 63,55/6,19 giây và khoảng 10,3 lần vào bảng khuyến nghị; đoạn văn ghi công thức tỷ số và giới hạn đo theo lô |

11 nhóm số A3 được giữ nguyên; kiểm lại trực tiếp từ CSV/JSON và lưu `doi_chieu_11_nhom.csv`. Có bảng 10 số chọn ngẫu nhiên với seed 20261104 để Vương kiểm chéo tiếp. Tóm tắt sau sửa vẫn trong 250–350 từ; số từ và số trang chính xác ở `verification.json`.

**Phân vị:** dùng `output/hoan_thanh_chuong3/lift_baseline.csv`, định nghĩa `100 × count(lift <= target)/210`, cho 50,9524; 80; 38,5714, làm tròn 51–80–39. `BAO CAO/Bao cao EDA/ban2/lift_baseline.csv` là bảng lịch sử theo `<` (50,4762; 79,5238; 38,0952), không lấy nhầm bảng đó để giải thích lời văn. Không sửa hoặc chạy lại đầu ra EDA trong phiên này.

## A4: đã gộp có đối chiếu nguồn

- Mục 2.5: thống nhất môi trường chính thức `.venv-m2` của Vương; tách lịch sử Master 20/10 và việc Phong phát triển/kiểm chứng.
- Mục 3.2: một đích xuất bản Master; hồ sơ 04/11 `PASSED`, 16.992.331 byte và 13/13 kiểm tra đạt. Câu so sánh từng ô với bản 20/10 được quy nguồn cho biên bản đồng bộ của Vương; phiên này không chạy lại so sánh hai Master.
- Bảng 3.5: đọc CSV mới trong gói `GUI_phong_dong_bo_moi_truong_20261104`, kiểm timestamp metadata `2026-11-04T14:12:44+0700`, dựng 32 ô theo đúng dòng `run_id=median`. Không lấy số từ diff. CSV ở thư mục chính của Phong trước đó vẫn là bản cũ; đã sao lưu rồi đồng bộ `data_benchmark.csv`, `data_benchmark_metadata.json`, `master_verification.json` tại `DATA/Data đã làm sạch/Bảng master TLCK/`. Không thay Master hoặc hashes.
- Tỷ số tính từ CSV: 9,60 lần ghi; 29,59 lần đọc; 45,99 lần tái sử dụng; 88,16% giảm bộ nhớ DataFrame; 7,75 lần dung lượng; chênh RSS 104,57 MiB. Lời văn có công thức và khoảng dao động ba lượt.
- Không chép đè toàn bộ QMD Vương: các sửa tám điểm, Chương 4–5 và câu nộp mã/nhật ký riêng của Phong được giữ.

## A6: nhật ký

1. Phiên 04/11 16:35–21:37 đã có sẵn trong file thực tế. Giữ phiên này, bỏ lời “đối soát 100% mọi số”, ghi đúng 100 phép kiểm; cập nhật liên hệ với phiên kết thúc 16:09. Sửa “8.449 giỏ rỗng ứng viên” thành “không có sản phẩm che thuộc danh mục”. Không tự gán giờ mới.
2. Tách sự kiện nhận 3.4 lúc 20:54:26 khỏi phiên 14:37–18:15 ngày 30/10; không kéo dài khống giờ làm.
3. Đính chính theo phản hồi Vương: 3.3 đã được Vương tích hợp 26/10; năm điểm Phong ghi là rà soát lại, không coi là năm đóng góp mới. Bản 3.1 Mermaid là lịch sử, không còn trong QMD hiện hành. Sửa “chờ tích hợp 3.3”.
4. Thêm mục hồi cứu phản biện `render_pdf.py`, ghi rõ chỉ có xác nhận từ Vương trong A6.4; **chưa xác minh ngày giờ, prompt gốc và thay đổi cụ thể**. Không bịa phiên hoặc nhận công chưa có bằng chứng.
5. Sửa 15 lượt liên kết cũ về nơi hiện có. Mã trước rút gọn trỏ `Chung/archive/`; link `phong/verification.json` vốn không tồn tại được sửa sang hồ sơ verification chung. Nhật ký gốc giữ liên kết tương đối từ gốc workspace; bản `nhat_ky_Phong_nop_rieng.md` trong gói đổi liên kết cục bộ thành tên/đường dẫn văn bản, nên không phụ thuộc máy Phong. Danh mục đường dẫn và trạng thái đính kèm.

## Tài liệu đã kiểm chứng

- Kohavi, R., Tang, D., & Xu, Y. (2020). *Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing*. Cambridge University Press. DOI 10.1017/9781108653985. [Trang nhà xuất bản](https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/D97B26382EB0EB2DC2019A7A7B518F59) xác nhận tác giả/năm/DOI, nội dung về chỉ tiêu đánh giá và kiểm chứng thí nghiệm. Trích dẫn dùng cho khung A/B; ngưỡng triển khai cụ thể vẫn là đề xuất của nhóm.
- Kaminskas, M., & Bridge, D. (2016). *Diversity, Serendipity, Novelty, and Coverage: A Survey and Empirical Analysis of Beyond-Accuracy Objectives in Recommender Systems*. ACM Transactions on Interactive Intelligent Systems, 7(1), Article 2. DOI 10.1145/2926720. [Hồ sơ công bố của University College Cork](https://research.ucc.ie/en/publications/diversity-serendipity-novelty-and-coverage-a-survey-and-empirical/) xác nhận metadata và abstract. DOI/ACM trả 403 trong lần đọc; metadata và nội dung được kiểm trên hồ sơ cơ sở nghiên cứu của tác giả. Nguồn này hỗ trợ đa dạng/độ phủ, không được dùng như bằng chứng hệ thống đã công bằng.

## Còn lại

- Vương sửa chú thích `m4_validate.py` theo phần B và gửi bản mới; Phong chưa nhận thay đổi đó trong phiên này.
- Xác minh phiên phản biện lịch sử khi có trao đổi gốc.
- Rút trang sau khi chốt nội dung. Đây chưa phải bản nộp cuối nếu còn vượt 45 trang từ bìa đến hết Chương 5. Không thu chữ hoặc lề để ép trang.

Sao lưu trước sửa ở `output/hoan_thien_chuong5_20261104/truoc_sua/`; log render, bảng đối chiếu, hash trước/sau và diff nằm cùng hồ sơ. Xem README để biết số trang của bản dựng cuối và cách ghép gói.
