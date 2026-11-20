# Phong duyệt đề xuất sửa theo góp ý ngày 07/11/2026

Vương ơi, mình đồng ý toàn bộ 23 chỉnh sửa lời văn trong gói `DE_XUAT_SUA_THEO_GOP_Y_20261107`, hai mục tài liệu tham khảo và cả hai đề xuất về hình. Bạn có thể áp các câu đã duyệt vào bản chính theo bản diff gửi kèm gói.

| Phần mình viết | Quyết định |
|---|---|
| 1.3, mục tiêu 2 — làm rõ việc đọc bảng prior theo khối | Đồng ý |
| 2.2, đoạn tổng quan nghiên cứu trên Instacart | Đồng ý |
| 2.5, rút câu về nộp riêng mã nguồn và nhật ký | Đồng ý |
| 3.5, ghi rõ mọi ô ngày × khung giờ đều có ít nhất 30 giỏ | Đồng ý |
| 5.1, gom lưu ý về kết quả ngoại tuyến ở đoạn mở | Đồng ý |
| Bảng 5.1, rút lời diễn giải ở dòng kiểm định | Đồng ý |
| 5.1, rút câu kết về phép bỏ nhóm đặc trưng | Đồng ý |
| 5.2, bỏ câu lặp ở bước 1 | Đồng ý |
| Bảng 5.2, rút dòng nguồn về kế hoạch đo | Đồng ý |
| 5.3, rút câu giới hạn sau phần giải thích N = 1.000 | Đồng ý |
| 5.4, bỏ câu lặp ở hướng phát triển | Đồng ý |
| 5.4, thêm số liệu vào kết luận câu hỏi 1 | Đồng ý |
| 5.4, bỏ câu lặp ở kết luận câu hỏi 2 | Đồng ý |
| 5.4, rút câu so sánh bổ trợ RF với Rules ở câu hỏi 4 | Đồng ý |

| Tài liệu và hình | Quyết định |
|---|---|
| Thêm Hu và cộng sự (2020), khóa `hu2020` | Đồng ý |
| Thêm Li và cộng sự (2023), khóa `li2023` | Đồng ý |
| Bỏ “* N<30” khỏi tiêu đề hình kích thước giỏ, giữ logic đánh dấu ô có ít hơn 30 giỏ | Đồng ý |
| Dùng dấu phẩy thập phân cho sáu hình Chương 3 và hình importance, giữ nguyên hình Recall@K đã ghi hash | Đồng ý |

Bạn làm phần hình thành đợt riêng như đề xuất, đối chiếu `plot_data` từng byte và chạy `check_hashes`. Sau khi ghép, bạn xuất PDF, kiểm giới hạn 45 trang từ bìa đến hết Chương 5, rà tham chiếu lỗi, chạy unittest rồi gửi lại QMD và PDF cho mình.

Hoàng Thanh Phong · 07/11/2026
