CHƯƠNG 1
TỔNG QUAN ĐỀ TÀI VÀ MỤC TIÊU NGHIÊN CỨU
1.1 Bối cảnh nghiên cứu và Lý do chọn đề tài
Trong bán lẻ trực tuyến, bộ phận kinh doanh và vận hành gợi ý phải lựa chọn sản phẩm mua
kèm phù hợp khi khách đang tạo giỏ. Tình huống nghiên cứu đặt ra là danh sách chỉ dựa trên
độ phổ biến có thể chưa phản ánh nhu cầu của giỏ hiện tại, trong khi dữ liệu phân tán và nhiễu
làm giảm độ tin cậy của phân tích. Đây là bài toán quản trị giả định cần kiểm chứng, không phải
khẳng định về hệ thống đang vận hành của Instacart.
Dữ liệu Instacart được công bố năm 2017, đăng lại bởi psparks trên Kaggle (psparks, 2017) và
từng dùng trong cuộc thi Market Basket Analysis (Instacart, 2017). Đề tài dùng bản bổ sung
nhiễu để kiểm chứng xử lý đa bảng; khai thác quan hệ đồng mua bằng Apriori và FP-Growth để
hoàn thiện giỏ hàng. Câu hỏi quản trị là liệu gợi ý theo phần giỏ quan sát có tốt hơn gợi ý phổ
biến, với chi phí tính toán phù hợp. Do thiếu giá bán, lợi nhuận và lịch sử hiển thị gợi ý, nghiên
cứu chưa đo tác động doanh thu hoặc hiệu quả nhân quả.
1.2 Xác định vấn đề và Câu hỏi nghiên cứu
Nghiên cứu xây dựng quy trình xếp hạng sản phẩm mua kèm từ dữ liệu đa bảng, tập trung trả
lời năm câu hỏi:
1. Quy trình làm sạch và tích hợp sáu bảng dữ liệu bảo đảm tính toàn vẹn quan hệ, quy mô
phân tích và hiệu quả sử dụng bộ nhớ đến mức nào?
2. Cấu trúc giỏ hàng và các mối quan hệ đồng xuất hiện giữa sản phẩm, ngành hàng có đặc
điểm gì nổi bật?
3. Apriori và FP-Growth khác nhau ra sao về thời gian thực thi, mức sử dụng RAM và kết
quả khai phá trong cùng điều kiện?
4. Phương pháp xếp hạng dựa trên luật kết hợp, Logistic Regression và Random Forest có
cải thiện chất lượng gợi ý ngoài mẫu so với phương pháp dựa trên độ phổ biến hay không?
5. Kết quả thực nghiệm hỗ trợ những khuyến nghị nào về gợi ý bán chéo và triển khai thử
nghiệm trong doanh nghiệp?
1.3 Mục tiêu nghiên cứu (Tổng quát và Cụ thể)
Mục tiêu tổng quát: Xây dựng quy trình phân tích giỏ hàng đa bảng có thể tái lập, phát hiện
quan hệ đồng mua và đánh giá chất lượng gợi ý ngoài mẫu để làm căn cứ đề xuất thử nghiệm
bán chéo.
11. Dữ liệu, tuần 1: Làm sạch sáu CSV; tạo bảng phân tích chính trên 1 triệu dòng sản
phẩm–đơn hàng, đối chiếu 1.384.617 dòng train. Đầu ra gồm bảng trước–sau và kiểm
tra không trùng khóa, không khóa ngoại mồ côi, không mất/nhân dòng do ghép; thuộc
tính còn thiếu và giả định khôi phục được công bố.
2. Tài nguyên, tuần 2: Áp dụng chunksize, tối ưu dtype và Parquet; lập bảng RAM đỉnh,
thời gian, dung lượng trước–sau trên cùng dữ liệu và máy, kiểm tra kết quả tương đương.
Báo cáo mức thay đổi thực đo, không mặc định mọi kỹ thuật đều cải thiện.
3. EDA và khai phá, tuần 2: Đúc kết 4–5 insight định lượng kèm biểu đồ và ý nghĩa kinh
doanh; kiểm định liên hệ ngành hàng. Chạy Apriori và FP-Growth trên cùng giao dịch,
danh mục và ngưỡng; đối chiếu itemset, support, confidence, lift và benchmark lặp.
4. Mô hình, tuần 3: Huấn luyện Logistic Regression (LR) (Hosmer và c.s., 2013) và
Random Forest (RF) (Breiman, 2001) từ đặc trưng sản phẩm, giỏ quan sát và thống kê
reference; so sánh với Popularity Baseline và Association Rules trên cùng ứng viên. Đầu
ra gồm cấu hình, metrics và diễn giải đặc trưng.
5. Đánh giá và ứng dụng, tuần 4: Báo cáo macro Recall@10, chênh lệch với baseline và
khoảng tin cậy 95%. Phương pháp chính được chọn trên validation; chỉ kết luận cải thiện
có bằng chứng khi cận dưới khoảng tin cậy chênh lệch trên test lớn hơn 0. Kết quả không
cải thiện vẫn được phân tích. Hoàn thành khuyến nghị, KPI và lộ trình thử nghiệm A/B.
Tính khả thi và thời hạn: Bốn tuần tính từ mốc khởi động 15/10/2026, dự kiến kết thúc
11/11/2026; đây là lịch nghiên cứu, không thay thế hạn nộp học phần. Pilot trên máy 24 GB
RAM dùng để chốt Top-N, ngưỡng khai phá, độ dài tập và quy mô lấy mẫu âm trước thực
nghiệm chính. Mức tối ưu và khả thi chỉ được xác nhận bằng kết quả đo.
1.4 Đối tượng và Phạm vi nghiên cứu
Đối tượng nghiên cứu là hành vi đồng mua sản phẩm trong các giỏ hàng Instacart và khả năng
dự đoán sản phẩm phù hợp để gợi ý.
Phạm vi dữ liệu: Sáu bảng gồm orders, order_products__prior, order_products__train,
products, aisles, departments, liên kết qua các khóa đơn hàng, sản phẩm, quầy và ngành hàng.
Bảng train có 1.384.617 dòng thuộc 131.209 giỏ, là nguồn chia bốn tập nghiên cứu; prior có
32.434.489 dòng, phục vụ kiểm tra dữ liệu lớn và tổng hợp theo khối, không tạo đặc trưng
classifier. Bản gốc chỉ đối chứng, không dùng điền dữ liệu nhiễu.
2Bài toán và biến nghiên cứu: Kết hợp luật kết hợp với phân loại nhị phân bằng LR/RF để xếp
hạng ứng viên cho phần giỏ bị che.
• Biến mục tiêu (Y): purchase_label=1 khi ứng viên thuộc phần bị che; bằng 0 khi không
thuộc giỏ đầy đủ. Sản phẩm đã quan sát được loại khỏi ứng viên. Nhãn này khác reordered.
• Các biến giải thích (X): Độ phổ biến reference, số luật khớp, confidence/lift lớn nhất,
kích thước giỏ quan sát, số sản phẩm cùng ngành và ngành của ứng viên. Chỉ dùng thống
kê reference và phần giỏ quan sát; phần bị che chỉ tạo nhãn và chấm điểm.
Đơn vị phân tích bảng chính là cặp đơn hàng–sản phẩm; đơn vị khai phá là giỏ; đơn vị phân loại
là cặp giỏ–ứng viên. Tập test nghiên cứu chiếm 20% người dùng có giỏ train, được giữ độc lập
với các bước lựa chọn và huấn luyện.
1.5 Ý nghĩa lý luận và Thực tiễn của đề tài
Về lý luận: Đánh giá sự kết hợp giữa thống kê đồng mua và classifier trong bài toán hoàn thiện
giỏ trên người dùng ngoài mẫu; tách vai trò học thống kê, huấn luyện, lựa chọn cấu hình và kiểm
thử. Đóng góp là quy trình ứng dụng có kiểm chứng, không đề xuất thuật toán mới.
Về thực tiễn: Hỗ trợ lựa chọn cơ chế gợi ý và vị trí mua kèm trên ứng dụng. Chương 5 chuyển
bằng chứng về chất lượng, độ phủ và chi phí thành kế hoạch A/B với tỷ lệ nhấp, thêm vào giỏ
và giá trị đơn hàng khi có dữ liệu; cân nhắc thiên lệch sản phẩm phổ biến, bảo mật và giới hạn
suy rộng.
3CHƯƠNG 2
CƠ SỞ LÝ THUYẾT VÀ PHƯƠNG PHÁP NGHIÊN CỨU
2.1 Cơ sở lý thuyết chuyên ngành liên quan
Phân tích giỏ hàng khai thác đồng xuất hiện để hỗ trợ bán chéo. Giỏ được biểu diễn bằng tập mã
sản phẩm, không chứa số lượng hay trình tự lựa chọn. Với 𝑁 giỏ, đặt 𝑠(𝑆) = 𝑛(𝑆)/𝑁, trong
đó 𝑛(𝑆) là số giỏ chứa toàn bộ tập 𝑆. Luật kết hợp 𝐴 → 𝐵 có hai tập sản phẩm khác rỗng và
rời nhau. Các chỉ số được xác định như sau (Mlxtend contributors, không ngày):
Support = 𝑠(𝐴 ∪ 𝐵), Confidence = 𝑠(𝐴 ∪ 𝐵)
𝑠(𝐴) ,
Lift = 𝑠(𝐴 ∪ 𝐵)
𝑠(𝐴)𝑠(𝐵), Leverage = 𝑠(𝐴 ∪ 𝐵) − 𝑠(𝐴)𝑠(𝐵),
Conviction = 1 − 𝑠(𝐵)
1 − Confidence
.
Support đo mức phổ biến; Confidence đo tỷ lệ có 𝐵 trong các giỏ chứa 𝐴; Lift so với kỳ vọng
độc lập. Leverage đo chênh lệch tuyệt đối, Conviction bổ sung hướng liên hệ. Lift không chứng
minh nhân quả hay sự thay thế. Mẫu số phải hợp lệ; Conviction vô hạn/không xác định được
ghi riêng.
Bài toán đánh giá là hoàn thiện giỏ hàng: dùng phần quan sát để xếp hạng sản phẩm bị che,
không dự báo đơn kế tiếp. Đơn vị khai phá là giỏ; đơn vị phân loại là cặp giỏ–ứng viên. Nhãn
𝑦 = 1 khi ứng viên thuộc phần bị che, 𝑦 = 0 khi không thuộc giỏ đầy đủ; nhãn này không phải
reordered và không biểu thị sự yêu thích sản phẩm.
2.2 Tổng quan các nghiên cứu thực nghiệm trước đây
Agrawal & Srikant (1994) đề xuất Apriori/AprioriTid và đánh giá khả năng mở rộng trên cơ sở
dữ liệu giao dịch; kết quả cho thấy lợi thế so với các thuật toán đối chứng được khảo sát. Nhóm
kế thừa nguyên lý cắt tỉa tập ứng viên, nhưng hiệu quả khai phá chưa đồng nghĩa với chất lượng
gợi ý ngoài mẫu.
Han và c.s. (2000) dùng cây FP và phát triển mẫu để tránh sinh tập ứng viên, báo cáo hiệu năng
tốt hơn Apriori trong thực nghiệm của tác giả. Nhóm kế thừa FP-Growth và thiết kế benchmark
cùng điều kiện; mức lợi thế trên dữ liệu Instacart và máy của nhóm phải được đo lại.
Rendle và c.s. (2010) kết hợp sở thích cá nhân và chuyển tiếp tuần tự trong FPMC, cho kết quả
tốt hơn các đối chứng phân rã ma trận và Markov trong thực nghiệm của tác giả. Công trình xét
4giỏ kế tiếp; đồ án xét giỏ hiện tại bị che, không triển khai FPMC do phạm vi và hạn chế dữ liệu
thứ tự.
Từ các hướng trên, nhu cầu kiểm chứng của đề tài là liệu luật đồng mua và classifier cải thiện
gợi ý so với độ phổ biến trong điều kiện dữ liệu nhiễu và tài nguyên giới hạn. Nghiên cứu kết
nối xử lý đa bảng, benchmark khai phá và đánh giá xếp hạng; không suy rộng kết quả công trình
trước thành kết quả đồ án.
2.3 Quy trình nghiên cứu dữ liệu (Data Science Workflow)
Quy trình bảy giai đoạn vận dụng CRISP-DM: xác định vấn đề; thu thập–ghép nối; làm sạch;
EDA; tạo đặc trưng; mô hình hóa; đánh giá–khuyến nghị. Câu hỏi 1 được trả lời tại mục 3.1–3.3
bằng kiểm tra dữ liệu và tài nguyên; câu 2 tại 3.4–3.6 bằng insight và kiểm định; câu 3–4 tại
chương 4 bằng benchmark và đánh giá mô hình; câu 5 tại chương 5 bằng hành động, KPI và lộ
trình ứng dụng.
Bảng chính lấy chi tiết train nối nhiều–một với orders, products, aisles, departments;
prior phục vụ kiểm tra và tổng hợp theo khối, không tạo đặc trưng classifier trong thiết kế này.
Quy trình kiểm chứng số dòng, khóa và thành phần giỏ trước–sau xử lý; không xóa giao dịch
chỉ vì thiếu thuộc tính phụ, không dùng bản gốc để điền. Thuộc tính không khôi phục đáng tin
được giữ thiếu; báo cáo chất lượng lưu riêng. Thứ tự tái dựng theo vị trí dòng là giả định, không
phải giá trị gốc đã được xác minh. Thống kê chất lượng toàn bộ dữ liệu phục vụ kiểm tra cấu
trúc; EDA định hướng mô hình chỉ dùng reference. Ngoại lai về kích thước giỏ được khảo sát
bằng IQR và đối chiếu nghiệp vụ, không tự động xóa giỏ lớn hợp lệ.
Người dùng có giỏ trong order_products__train được chia với seed 42 thành 80% phát triển
và 20% kiểm thử. Phần phát triển gồm reference, classifier fit và validation; tỷ lệ trên toàn quần
thể là:
• Reference — 30%: học độ phổ biến, danh mục ứng viên và luật; thực hiện EDA định
hướng mô hình (phân phối, nhóm hàng và đồng mua).
• Classifier fit — 30%: học tham số tiền xử lý và classifier từ thống kê reference.
• Validation — 20%: chọn cấu hình, ngưỡng và phương pháp.
• Test — 20%: đánh giá sau khi khóa thiết kế, không tham gia lựa chọn hoặc huấn luyện.
Bốn tập không giao người dùng. Test 20% này khác 75.000 đơn eval_set=test của nguồn vốn
không có chi tiết sản phẩm công khai. Tách theo người dùng bảo toàn tính độc lập thay cho
stratify từng dòng ứng viên; tỷ lệ lớp được báo cáo riêng. Reference giúp tránh học luật từ đáp
án của giỏ huấn luyện; tham số điền thiếu, mã hóa và chuẩn hóa classifier chỉ fit trên classifier
fit (Scikit-learn developers, không ngày-b).
Giữ nguyên giỏ reference để học thống kê. Với giỏ fit/validation/test có 𝑘 ≥ 2, che ngẫu nhiên
ℎ = min(𝑘 − 1, max(1, ⌊0,2𝑘⌋)) sản phẩm. Gọi 𝑂𝑗, 𝐻𝑗 là phần quan sát và phần che; ứng viên
là 𝐶
𝑗 = 𝐶 ∖𝑂𝑗, với 𝐶 gồm Top-N sản phẩm từ reference. Không bổ sung đáp án vào 𝐶. Lưu cố
5định phép che theo seed và mã giỏ cho mọi phương pháp; giỏ một sản phẩm chỉ loại khỏi đánh
giá che giỏ. Giỏ không có đáp án trong 𝐶 vẫn được chấm với Recall bằng 0, không bị loại để
làm đẹp kết quả. Che ngẫu nhiên mô phỏng thiếu một phần giỏ, không tái hiện chính xác trình
tự khách thêm hàng trong thực tế.
2.4 Các phương pháp thống kê và Thuật toán Học máy ứng dụng
Khai phá và benchmark. Hai thuật toán dùng ma trận Boolean thưa, cùng giỏ, danh mục,
ngưỡng support và độ dài tập tối đa. Giỏ rỗng sau lọc danh mục vẫn thuộc mẫu số support. Chạy
riêng từng thuật toán ba lần, báo trung vị thời gian, RAM đỉnh và tính nhất quán itemset/support;
tách chi phí tạo ma trận khỏi khai phá. Cấu hình vượt ngân sách pilot được ghi nhận và loại trước
khi khóa thiết kế, không giảm dữ liệu riêng cho một thuật toán.
Gợi ý và classifier. Popularity Baseline xếp theo tỷ lệ giỏ reference chứa sản phẩm. Luật gợi ý
có hậu đề một sản phẩm 𝑏, tiền đề 𝐴 ⊆ 𝑂𝑗; ưu tiên ứng viên có luật, xếp theo confidence lớn
nhất, rồi độ phổ biến. LR học log-odds tuyến tính; RF tổng hợp cây để biểu diễn quan hệ phi
tuyến. Đặc trưng X gồm độ phổ biến, số luật khớp, confidence/lift lớn nhất, kích thước 𝑂𝑗, số
sản phẩm quan sát cùng ngành ứng viên và ngành ứng viên. Không có luật thì ba đặc trưng luật
bằng 0. Ứng viên không có luật xếp sau theo độ phổ biến. Các phương pháp phá hòa cuối cùng
bằng mã sản phẩm tăng dần; không dùng 𝐻𝑗 để tính X.
Pipeline/ColumnTransformer đóng gói điền thiếu, OneHotEncoder (bỏ qua danh mục mới)
và StandardScaler cho biến số của LR; RF không cần chuẩn hóa. Giữ mọi nhãn dương trong
𝐶𝑗
; lấy mẫu âm không hoàn lại từ 𝐶𝑗 ∖ 𝐻𝑗 khi fit, kể cả giỏ không có dương; công bố số âm/giỏ
và seed. Validation/test chấm toàn bộ ứng viên theo lô. Điểm classifier chưa được coi là xác suất
mua đã hiệu chỉnh.
Top-N và ngưỡng luật chọn bằng Recall@10 của phương pháp luật trên validation, sau đó cố
định khi tuning classifier. Vì vậy, kết luận so sánh có điều kiện trên danh mục chung, không phải
tối ưu riêng từng phương pháp. Lưới tìm kiếm và cấu hình cuối ghi ở chương 4; test chỉ mở sau
khi khóa lựa chọn. Các cặp nhãn 0 là chưa mua trong giỏ, không có nghĩa khách không thích
sản phẩm.
Kiểm định và đánh giá. Chi-square kiểm tra sự độc lập giữa hai ngành hàng trên reference, với
giả thuyết không là hai chỉ báo xuất hiện ngành hàng độc lập; kèm Cramér’s V. Chốt các cặp
trước kiểm định, kiểm tra tần số kỳ vọng, dùng một giỏ/người, mức ý nghĩa 0,05 và điều chỉnh
Holm khi kiểm định nhiều cặp. Với bảng 2× 2 không đáp ứng điều kiện xấp xỉ, cân nhắc Fisher
exact; biến hằng không được kiểm định như biến có biến thiên.
Với 𝑀 giỏ đánh giá và danh sách gợi ý 𝑅𝑗𝐾, các chỉ số trung bình theo giỏ là:
6𝑃@𝐾 = 1
𝑀
𝑀 ∑
𝑗=1
|𝑅𝑗𝐾 ∩ 𝐻𝑗|
𝐾 , 𝑅@𝐾 = 𝑀1 ∑𝑀
𝑗=1
|𝑅𝑗𝐾 ∩ 𝐻𝑗|
|𝐻𝑗| ,
𝐻𝑅@𝐾 = 1
𝑀
𝑀 ∑
𝑗=1
1{𝑅𝑗𝐾 ∩ 𝐻𝑗 ≠ ∅}.
Chỉ số chính là Recall@10 (Manning và c.s., 2008); bổ sung các chỉ số trên tại 𝐾 = 5, 10.
Recall tính cả đáp án ngoài 𝐶; Precision vẫn chia 𝐾 khi danh sách ngắn. Báo riêng tỷ lệ đáp án
thuộc danh mục, tỷ lệ giỏ có luật trước dự phòng và tỷ lệ danh mục được gợi ý. Classifier có thêm
Accuracy, Precision, Recall, F1, ROC-AUC, Average Precision và ma trận nhầm lẫn; Average
Precision không đồng nhất với diện tích PR tính bằng hình thang (Scikit-learn developers, không
ngày-a). Ngưỡng phân loại tối đa hóa F1 trên validation; metric không xác định được báo riêng,
không tự gán 0. Bootstrap ghép cặp theo người dùng, 2.000 lần và seed cố định, cho khoảng tin
cậy percentile 95% của chênh lệch Recall@10. Phép so sánh xác nhận dành cho phương pháp
chọn trên validation với baseline; các so sánh còn lại mang tính bổ trợ. Không dùng test để chọn
lại mô hình. Permutation importance trên validation với thước đo Average Precision hỗ trợ diễn
giải classifier, có lưu ý đặc trưng tương quan. Hiệu quả ngoại tuyến là căn cứ đề xuất A/B test,
chưa chứng minh tăng doanh thu.
2.5 Môi trường thực nghiệm và Công cụ lập trình Python
Thực nghiệm được thiết kế cho máy Windows, RAM 24 GB. pandas xử lý bảng và chunking;
NumPy tính toán; SciPy/pandas sparse biểu diễn thưa; PyArrow lưu Parquet; mlxtend khai phá
luật; scikit-learn xây pipeline; SciPy kiểm định; Matplotlib/Seaborn tạo biểu đồ 300 DPI. Phiên
bản Python, thư viện, CPU, seed và cấu hình được ghi theo lần chạy. Ép kiểu, kích thước khối
và danh mục được chọn qua pilot, đánh giá bằng RAM/thời gian thực đo. Mã nguồn tổ chức
theo mô-đun, tuân thủ PEP 8; nhật ký tại thư mục gốc ghi theo P-D-M-V, nêu đúng công cụ hỗ
trợ và các bước tự kiểm chứng trong từng phiên. Quarto quản lý báo cáo, tham chiếu chéo và
trích dẫn APA 7.