# CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI VÀ MỤC TIÊU NGHIÊN CỨU

## 1.1. Bối cảnh nghiên cứu và lý do chọn đề tài

Trong bán lẻ truyền thống và thương mại điện tử, xác định các sản phẩm thường được mua cùng nhau có ý nghĩa quan trọng đối với trải nghiệm khách hàng và tối ưu doanh thu. Thách thức lớn của doanh nghiệp là **khai thác dữ liệu giao dịch để nhận diện nhu cầu mua kèm và tối ưu chiến lược bán chéo**, thay vì chỉ dựa vào mức độ phổ biến đơn lẻ của từng sản phẩm làm hạn chế cơ hội gia tăng giá trị đơn hàng.

Phân tích giỏ hàng (Market Basket Analysis – MBA) là phương pháp khai phá dữ liệu nhằm phát hiện các sản phẩm thường xuất hiện cùng nhau trong một giao dịch. Thuật toán Apriori (Agrawal & Srikant, 1994) và FP-Growth (Han và cộng sự, 2000) cho phép khai phá tập mặt hàng phổ biến và luật kết hợp, làm nền tảng phát triển các cơ chế gợi ý giỏ hàng và bán chéo sản phẩm (Rendle và cộng sự, 2010).

Đề tài sử dụng bộ dữ liệu đa bảng *Instacart Market Basket Analysis* (Instacart, 2017) với hơn 200.000 người dùng. Phiên bản dữ liệu được bổ sung nhiễu tạo điều kiện kiểm chứng quy trình tiền xử lý, tích hợp và khai phá hành vi đồng mua sát với các vấn đề dữ liệu thực tế.

Nghiên cứu tập trung vào **mối quan hệ đồng xuất hiện và khả năng gợi ý sản phẩm mua kèm**, không xem luật kết hợp là quan hệ nhân quả. Do không có dữ liệu về giá bán, chi phí và lợi nhuận, đề tài đánh giá chất lượng gợi ý thay vì khẳng định mức tăng doanh thu thực tế.

## 1.2. Xác định vấn đề và câu hỏi nghiên cứu

Vấn đề trung tâm của đề tài là xây dựng và đánh giá quy trình khai thác dữ liệu giao dịch đa bảng để nhận diện các sản phẩm thường được mua cùng nhau, từ đó xếp hạng sản phẩm gợi ý có căn cứ định lượng.

Nghiên cứu tập trung trả lời năm câu hỏi:

1. Quy trình làm sạch và tích hợp sáu bảng dữ liệu bảo đảm tính toàn vẹn quan hệ, quy mô phân tích và hiệu quả sử dụng bộ nhớ đến mức nào?
2. Cấu trúc giỏ hàng và các mối quan hệ đồng xuất hiện giữa sản phẩm, ngành hàng có đặc điểm gì nổi bật?
3. Apriori và FP-Growth khác nhau ra sao về thời gian thực thi, mức sử dụng RAM và kết quả khai phá trong cùng điều kiện?
4. Phương pháp xếp hạng dựa trên luật kết hợp, Logistic Regression và Random Forest có cải thiện chất lượng gợi ý ngoài mẫu so với phương pháp dựa trên độ phổ biến hay không?
5. Kết quả thực nghiệm hỗ trợ những khuyến nghị nào về gợi ý bán chéo và triển khai thử nghiệm trong doanh nghiệp?

## 1.3. Mục tiêu nghiên cứu theo nguyên tắc SMART

**Mục tiêu tổng quát:** Xây dựng, tối ưu và đánh giá một quy trình phân tích giỏ hàng trên dữ liệu Instacart đa bảng, nhằm phát hiện quy luật đồng mua và nâng cao chất lượng xếp hạng sản phẩm gợi ý so với phương pháp cơ sở.

**Mục tiêu cụ thể:**

1. **Chất lượng dữ liệu:** Làm sạch và tích hợp sáu tệp CSV, tạo tập phân tích có tối thiểu **100.000 bản ghi sản phẩm–đơn hàng hợp lệ**; thống kê số bản ghi trước và sau xử lý, kiểm tra khóa chính, khóa ngoại, dữ liệu trùng và tính nhất quán lịch sử giao dịch.
2. **Tối ưu tài nguyên:** Áp dụng đọc dữ liệu theo khối (`chunksize`), tối ưu kiểu dữ liệu (`dtype`) và lưu trữ Parquet; đo RAM cực đại, thời gian xử lý và dung lượng lưu trữ trước và sau tối ưu, đồng thời kiểm tra tính tương đương của kết quả xử lý.
3. **Khai phá luật kết hợp:** Áp dụng Apriori và FP-Growth trên cùng dữ liệu giao dịch; tính toán support, confidence, lift và so sánh hiệu năng thực thi. Các ngưỡng khai phá được lựa chọn theo tiêu chí xác định trước trên tập xác thực.
4. **Xây dựng mô hình:** Huấn luyện Logistic Regression (LR) (Hosmer và cộng sự, 2013) và Random Forest (RF) (Breiman, 2001) để dự đoán khả năng sản phẩm ứng viên xuất hiện trong giỏ hàng mục tiêu, kết hợp các đặc trưng sản phẩm, lịch sử giao dịch và quan hệ đồng mua.
5. **Đánh giá định lượng:** So sánh bốn phương pháp gồm Popularity Baseline, Association Rules, LR và RF trên cùng tập kiểm thử và không gian ứng viên. Chỉ số chính là **macro Recall@10**, dựa trên các nguyên lý xếp hạng và đánh giá truy xuất thông tin (Manning và cộng sự, 2008), kết hợp các chỉ số bổ trợ để đánh giá hiệu quả và khả năng ứng dụng.

**Tính khả thi và thời hạn:** Thuật toán và dữ liệu phù hợp với môi trường Python cá nhân nhờ kỹ thuật tối ưu bộ nhớ. Tiến độ gồm 4 tuần: tuần 1 hoàn thành khảo sát, làm sạch và tích hợp; tuần 2 tối ưu tài nguyên, EDA và khai phá luật; tuần 3 huấn luyện, đánh giá mô hình; tuần 4 tổng hợp kết quả, khuyến nghị và hoàn thiện báo cáo theo thời hạn học phần.

## 1.4. Đối tượng, biến nghiên cứu và phạm vi dữ liệu

**Đối tượng nghiên cứu** là hành vi đồng mua sản phẩm trong các giỏ hàng Instacart và khả năng dự đoán sản phẩm phù hợp để gợi ý.

**Phạm vi dữ liệu:** Bộ dữ liệu gồm sáu bảng (`orders`, `order_products__prior`, `order_products__train`, `products`, `aisles`, `departments`) liên kết qua các khóa `order_id`, `product_id`, `aisle_id`, `department_id`. Bảng `train` (1.384.617 dòng) dùng làm nguồn nhãn đánh giá chính; bảng `prior` (32.434.489 dòng) cung cấp lịch sử giao dịch quy mô lớn. Bản dữ liệu nhiễu là đầu vào xử lý chính, bản gốc dùng để đối chứng; tập kiểm thử chiếm 20% số người dùng được tách biệt độc lập.

**Bản chất bài toán:** Kết hợp khai phá luật kết hợp không giám sát với **phân loại nhị phân (Binary Classification)** bằng LR và RF để xếp hạng sản phẩm gợi ý, không hồi quy giá trị liên tục hay phân cụm khách hàng.

- **Biến mục tiêu (Y):** `purchase_label`, nhận giá trị 1 nếu sản phẩm ứng viên thực sự xuất hiện trong giỏ hàng mục tiêu được giữ lại để đánh giá, và 0 nếu không xuất hiện. Nhãn được xác định từ dữ liệu giao dịch thực tế, không đồng nhất với cột `reordered`.
- **Các biến giải thích (X):** Gồm đặc trưng lịch sử người dùng–sản phẩm (tần suất mua, tỷ lệ mua lại), đặc trưng sản phẩm (độ phổ biến, ngành hàng), đặc trưng hành vi mua sắm (quy mô giỏ hàng, khoảng cách đơn) và đặc trưng quan hệ đồng mua (support, confidence, lift), thu thập trước giao dịch mục tiêu nhằm tránh rò rỉ dữ liệu.

Đơn vị quan sát của mô hình phân loại là cặp **giỏ hàng mục tiêu–sản phẩm ứng viên**; đối với khai phá luật kết hợp, mỗi `order_id` tương ứng với một giao dịch chứa tập các `product_id`.

## 1.5. Ý nghĩa lý luận và thực tiễn

**Về lý luận:** Đề tài xây dựng quy trình thực nghiệm kết hợp kiểm soát chất lượng dữ liệu quan hệ, khai phá tập phổ biến và phân loại nhị phân. Việc tách dữ liệu theo người dùng thành các tập `reference`, `classifier_fit`, `validation` và `test` hướng đến giảm rò rỉ dữ liệu và bảo đảm đánh giá ngoài mẫu, đồng thời so sánh hiệu năng thực thi giữa Apriori và FP-Growth.

**Về thực tiễn:** Giúp doanh nghiệp định lượng hóa việc gợi ý mua kèm và bố trí danh mục hàng hóa thay vì dựa vào cảm tính. Các mô hình hiệu quả sẽ được đề xuất thử nghiệm A/B với các KPI như tỷ lệ nhấp gợi ý, tỷ lệ thêm vào giỏ và giá trị đơn hàng trước khi triển khai vận hành thực tế.

**Tài liệu tham khảo**

Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules. In *Proceedings of the 20th International Conference on Very Large Data Bases* (pp. 487–499). Morgan Kaufmann.

Breiman, L. (2001). Random forests. *Machine Learning*, *45*(1), 5–32. https://doi.org/10.1023/A:1010933404324

Han, J., Pei, J., & Yin, Y. (2000). Mining frequent patterns without candidate generation. *ACM SIGMOD Record*, *29*(2), 1–12. https://doi.org/10.1145/335191.335372

Hosmer, D. W., Lemeshow, S., & Sturdivant, R. X. (2013). *Applied logistic regression* (3rd ed.). John Wiley & Sons.

Instacart. (2017). *Instacart Market Basket Analysis* [Data set]. Kaggle. https://www.kaggle.com/competitions/instacart-market-basket-analysis

Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to information retrieval*. Cambridge University Press.

Rendle, S., Freudenthaler, C., & Schmidt-Thieme, L. (2010). Factorizing personalized Markov chains for next-basket recommendation. In *Proceedings of the 19th International Conference on World Wide Web* (pp. 811–820). Association for Computing Machinery. https://doi.org/10.1145/1772690.1772773