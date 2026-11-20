# Gửi Phong — phần Chương 4 của Vương trước lần ghép thứ nhất

Ngày 01/11/2026. Đây là code và kết quả thử của phần dữ liệu (che giỏ, danh mục, luật, benchmark khai phá). Chưa phải kết quả thực nghiệm chính thức: chưa chấm validation, chưa có gói pilot.

## Có trong gói

- `scripts/m4_common.py`: hàm dùng chung. Chữ ký và docstring nằm trong tệp: `config`, `mask_params`, `check_mask`, `baskets`, `mask`, `catalog`, `basket_matrix`, `mine`, `rules`, `itemset_signature`, `max_support_gap`, `worst_support_gap`.
- `scripts/m4_prepare.py`: dựng giỏ fit/validation/test từ Master và che sản phẩm.
- `scripts/m4_mining.py`: danh mục C và lưới luật (FP-Growth, 12 tổ hợp).
- `scripts/m4_benchmark_mining.py`: benchmark Apriori và FP-Growth.
- `tests/test_m4_data.py`: test phần dữ liệu.
- `configs/m4_model.json`: cấu hình Chương 4 (7 biến chưa có tệp schema riêng; xem dưới).
- `requirements.txt`: bản khóa phiên bản của máy Vương, để đối chiếu, không ghi đè bản của bạn nếu khác.
- `Chung/Hướng dẫn chung/THIET_KE_CHUONG4_20261101.md`: bản thiết kế (đề xuất, chờ chốt ở lần ghép thứ nhất).
- `Chung/RA_SOAT_CLAUDE_20261101_CODEX.md`: báo cáo Codex rà soát; cả 5 lỗi đã sửa (A phép che gắn tham số, B benchmark mỗi cấu hình một tệp, C lượt lỗi/quá giờ vẫn ghi báo cáo, D so support chưa làm tròn dung sai 1e-12, E importance cho cả LR và RF).
- `output/`: kết quả benchmark thử N=500, min_count=50, max_len=2 (Apriori `low_memory` trung vị 1,71 s, FP-Growth 1,12 s, cùng 2.016 itemset, lệch support 0,0). Chỉ để tham khảo.
- `DANH_SACH.txt`: SHA-256 từng tệp. Kiểm trước khi chép.

## Không có trong gói

- Dữ liệu `DATA/Data phai sinh/M4/` (giỏ đã che, danh mục, lưới luật): máy bạn tự tạo bằng `m4_prepare.py` rồi `m4_mining.py` từ G0 và Master, hoặc đợi gói pilot.
- Hàm khớp luật, 7 đặc trưng, lấy mẫu âm, chỉ số xếp hạng, gói pilot, `lock.json`, `feature_schema.json`: chưa làm, thuộc giai đoạn sau lần ghép thứ nhất.

## Trả lời bốn yêu cầu của bạn

1. `m4_common.py`: có trong gói. Hàm chấm xếp hạng và iter_features chưa viết, nên chưa thể nêu kiểu từng lô.
2. `m4_model.json`: có. Đã đặt 20 mẫu âm/giỏ, dung sai 0,002, pilot_baskets=2000, lưới B như bạn nêu. `feature_schema.json` chưa tạo.
3. Gói pilot: chưa có.
4. `lock.json`: chưa triển khai; cách khóa và kiểm hash theo mục 3 và 4 của bản thiết kế, thống nhất ở lần ghép.

## Cần thống nhất khi ghép

- Hàm đặc trưng luật sẽ trả 0 (không để thiếu) khi ứng viên không khớp luật nào, vì Pipeline của bạn điền median cho ô thiếu.
- Bộ nhớ khi chấm toàn bộ validation (hàng chục triệu cặp): chốt cách giữ score và y sau khi đo pilot.
- Ngoại lệ cho phép bạn ghi `m4_classifier.py`, `m4_test.py`, `m4_interpret.py` và test tương ứng trong `scripts/`, `tests/`: ghi vào THONG_NHAT.
- Máy bạn Python 3.12.10, máy Vương 3.12.14: ghi vào nhật ký.

## Chạy kiểm tra sau khi nhận

```powershell
$env:PYTHONUTF8='1'
& .venv-m2/Scripts/python.exe -m unittest discover -s tests -p 'test_m4_data.py' -v
```

Test dùng dữ liệu dựng tay, không cần Master. `m4_prepare.py`, `m4_mining.py` và benchmark cần G0 và Master trên máy bạn.
