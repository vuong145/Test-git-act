# Kết quả tiếp nhận gói A và kiểm chéo trên máy Phong — 04/11/2026

Đã nhận đúng `Gửi và Nhận/Nhận/GUI_vuong_ch4_goiA_20261104`. Báo cáo này thay thế trạng thái “chưa nhận gói A/chưa chạy kiểm chéo” trong các báo cáo trước ngày 04/11; các log cũ giữ để truy vết.

## Nghiệm thu đã thực hiện

| Hạng mục | Kết quả | Bằng chứng |
|---|---|---|
| Manifest gói A | 52/52 file khớp SHA-256 | acceptance.json; DANH_SACH.txt trong gói nhận |
| Môi trường | 23/23 phiên bản đúng; pip check không lỗi | pip_install.log, pip_check.log, source_numbers.json |
| check_hashes | G0 6/6, ban2 10/10, M4 6/6, lock 8/8 | acceptance.json |
| Test workspace sau ghép | **55/55 đạt**, 5,007 giây | tests.log |
| Thử classifier | LR và RF suy luận đủ **2.000 giỏ validation**, **1.990.983 cặp ứng viên**, 1.997 dương | classifier.log, classifier_2000.csv, selected_2000.csv |
| Đối chiếu classifier | P@5, R@5, P@10, R@10, HR@10 từng giỏ khớp nguồn, sai lệch lớn nhất 5,551115123125783e-17 | comparison_2000.csv; lr/rf_validation_2000.csv |
| Kiểm Rules độc lập | **50/50 giỏ đạt**, Recall trung bình hai bên 0,12285714285714285 | output/kiem_cheo_rules_50/recall_comparison.csv và verification.json |
| Kiểm thứ hạng Rules | **500/500 dòng** product_id khớp; điểm khớp trong 1e-12 | output/kiem_cheo_rules_50/rankings_independent.csv; tai_lieu/rules_top10_50.csv; classifier_verification.json |

Bộ 55 test máy Phong gồm 41 test có trước, 13 test dữ liệu mới của Vương và 1 test kiểm Recall độc lập của Phong. Không khẳng định danh sách test giống hệt bộ 55 phía Vương chỉ vì trùng số lượng.

## Cách chạy và giới hạn kết luận

Theo README gói A, dùng hai Pipeline đã huấn luyện để chạy thử suy luận. Chọn 2.000 giỏ validation eligible đầu theo order_id tăng; lô 100 giỏ để hạn chế RAM. Dựng đủ ứng viên/đặc trưng bằng make_batches, predict_proba, xếp hạng, tính chỉ số phân loại ở ngưỡng nhận từ lock; chạy thêm bootstrap RF–LR trên mẫu phát triển. Không fit lại hoặc chạy lưới A/B trên máy Phong, không mở test. Đây là chạy thử luồng suy luận và đánh giá, không phải huấn luyện lại toàn luồng.

Recall@10 mẫu 2.000 giỏ: LR khoảng 0,090588; RF khoảng 0,093011. Chỉ dùng nghiệm thu trên mẫu, không thay số validation đầy đủ. Thời gian đo trên Phong khoảng 1,750 giây LR và 6,084 giây RF là riêng luồng suy luận/xếp hạng mẫu, không phải benchmark chính thức.

Kiểm độc lập 50 giỏ dùng scripts/m4_crosscheck.py, tự khớp tiền đề tập hợp, loại observed, xếp confidence/popularity giảm rồi product_id tăng; giữ sản phẩm ẩn ngoài C trong mẫu số. Không gọi evaluate hoặc hàm đặc trưng Vương để tạo kết quả kiểm độc lập. Sau khi có bảng độc lập mới đối chiếu 500 dòng xếp hạng Vương. Recall 0,122857 của 50 giỏ không phải Recall của toàn validation.

## Số chính thức validation đã đối chiếu CSV nguồn

| Phương pháp | Recall@10 toàn validation |
|---|---|
| Popularity | 0,07524927103868119 |
| Rules | 0,09318108808834646 |
| LR | 0,09231662838828687 |
| RF | 0,09714602107476494 |

Nguồn: BAO CAO/Bao cao mo hinh/validation_methods.csv, đối chiếu trung bình R@10 trong basket_metrics_validation.csv theo method, dung sai 1e-12. Trần khoảng 0,521060455709808. Đã kiểm 24 dòng lưới A, 8 dòng lưới B và quy tắc chọn A/B/C: lựa chọn ghi trong gói khớp dung sai 0,002 và thứ tự ưu tiên. Thời gian RF dùng giải thích chọn lưới phải lấy validation_grid_B (47,873 giây so với 86,305 giây), không lấy 63,552 giây của lượt chấm lại trong validation_methods.

## Khác biệt phụ thuộc cần Vương biết

11/13 hash phụ thuộc có sẵn khớp. Hai file khác là scripts/project_io.py và tests/test_m2_multivariate.py; gói A không chứa bản tương ứng của Vương để diff nội dung. Giữ nguyên bản Phong, kiểm API được các script mới gọi và chạy toàn bộ test thành công. Chi tiết hash nằm trong acceptance.json. Chưa kết luận hai bản khác nhau chỉ vì xuống dòng hoặc đã đồng nhất toàn bộ code hai máy.

Các tệp scripts/tests/configs/DATA/BAO CAO thuộc gói đã chép đúng đường dẫn vào workspace; các file Phong sở hữu không bị ghi đè bởi gói. Script accept.py lưu bản trước nếu đích đã tồn tại. Gói nhận nguyên vẹn. Hash M4 và lock kiểm lại sau chạy vẫn đạt.

## Trạng thái khóa

Kiểm hash lock đạt nghĩa là các tệp được liệt kê khớp; **không đồng nghĩa đã duyệt khóa**. lock.json vẫn là bản nháp nhận từ Vương, dù có trường locked_at. Chưa đánh dấu cả hai đã khóa, chưa mở test, chưa sửa m4_test.py thành chương trình chấm test chính thức. Không sửa QMD hoặc nhật ký trong đợt nghiệm thu này.

Đã hoàn tất các yêu cầu tiếp nhận môi trường/test, chạy thử classifier bằng gói A thay pilot, và kiểm chéo Recall trên 50 giỏ. Hồ sơ gửi Vương để nguyên thư mục vì dung lượng nhỏ.
