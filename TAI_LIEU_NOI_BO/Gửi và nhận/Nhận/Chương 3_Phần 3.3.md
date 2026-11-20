## Quy trình làm sạch và xử lý dữ liệu khuyết thiếu / giá trị bất thường

Mục này trình bày các quy tắc làm sạch ở cấp từng bảng và từng thuộc tính, tập trung vào chất lượng nội dung dữ liệu (*Data Quality & Domain Level*). Khác với Mục 3.2 — nơi trình bày kiến trúc tích hợp, bảng Master và đánh giá hiệu năng lưu trữ — phần này giải thích cách nhận diện, xử lý hoặc giữ lại các giá trị thiếu, sai định dạng, sai miền và bất thường nghiệp vụ trong sáu tệp nguồn.

Về **trình tự thực thi**, việc chuẩn hóa khóa và làm sạch các trường cần thiết được thực hiện trước khi ghép nối để hạn chế mất khóa hoặc ghép sai. Về **cách trình bày báo cáo**, Mục 3.2 tập trung vào kết quả tích hợp và tối ưu hệ thống, còn mục này giải trình chi tiết các quy tắc làm sạch đã áp dụng. Hai mục có liên hệ với nhau nhưng không lặp lại bảng ERD hay benchmark RAM/I/O.

### Nguyên tắc làm sạch và kiểm soát thay đổi

Quy trình làm sạch được xây dựng theo các nguyên tắc sau.

1. **Bảo toàn bản ghi giao dịch.** Không tự động loại bỏ một dòng trong bảng chi tiết chỉ vì một thuộc tính phụ như tên sản phẩm, vị trí thêm vào giỏ hoặc cờ mua lại bị thiếu hay không hợp lệ. Nếu cặp khóa `(order_id, product_id)` còn xác định được, dòng đó vẫn có thể chứa thông tin hữu ích cho phân tích giỏ hàng. Mọi trường hợp không thể xác định khóa phải được báo cáo riêng, không tự tạo mã thay thế.
2. **Phân biệt thiếu có cấu trúc với thiếu do nhiễu.** Một giá trị có thể thiếu hợp lệ theo ngữ nghĩa nghiệp vụ, chẳng hạn khoảng cách đến đơn trước ở đơn hàng đầu tiên. Ngược lại, chuỗi như `?`, `null`, `None` hoặc `chưa rõ` có thể là dấu hiệu thông tin đã bị thay thế. Không được gộp hai trường hợp thành một rồi điền trung bình, trung vị, mode hoặc số 0 một cách máy móc.
3. **Làm sạch theo từng cột.** Quy tắc chuẩn hóa phụ thuộc vào miền hợp lệ và ý nghĩa của cột. Không áp dụng biểu thức chính quy trích số lên mọi chuỗi, vì việc bỏ hậu tố không bảo đảm giá trị số còn lại là giá trị gốc.
4. **Không dùng bản tham chiếu để điền dữ liệu.** Bản gốc được dùng để đối chiếu loại sai lệch và hỗ trợ kiểm chứng quy tắc; không sao chép giá trị từ bản gốc sang tệp nhiễu để điền khuyết hoặc ghi đè.
5. **Không tự động xóa ngoại lai thống kê.** Một giỏ lớn hoặc một vị trí bất thường cần được kiểm tra theo ngữ nghĩa dữ liệu. Không dùng IQR hay một ngưỡng thống kê đơn lẻ làm lý do duy nhất để xóa giao dịch.
6. **Giữ nguyên lược đồ của sáu CSV sạch.** Các kết quả kiểm toán và cờ cảnh báo được lưu trong báo cáo riêng; không tự ý thêm cột như `is_outlier_cart_pos` vào sáu tệp sạch. Nếu một phân tích sau này cần cờ dẫn xuất, cờ đó phải thuộc bảng phân tích phát sinh và được mô tả riêng.

### Phân loại các vấn đề chất lượng dữ liệu

Từ báo cáo kiểm kê, kiểm tra khóa, cấu trúc giỏ hàng và đối chiếu bản nhiễu với bản tham chiếu, các vấn đề được chia thành bốn nhóm: (i) lỗi bề mặt như khoảng trắng thừa và khác biệt chữ hoa/chữ thường; (ii) giá trị thiếu hoặc token giả thiếu; (iii) giá trị không thỏa miền hợp lệ; và (iv) mâu thuẫn về trình tự hoặc phân vùng nghiệp vụ. Các con số dưới đây là **số liệu kiểm toán trên đầu vào đã bị làm nhiễu**, không phải số lỗi còn lại sau làm sạch. Chúng được dùng để mô tả mức độ vấn đề, không được cộng gộp thành số ô lỗi duy nhất nếu các nhóm hoặc cách đếm khác nhau.

### Làm sạch bảng `orders`

Bảng `orders` có một dòng cho mỗi đơn hàng, với các thuộc tính mô tả người dùng, thứ tự đơn và thông tin thời gian. Đây là bảng có nhiều trường bị nhiễu, vì vậy quy trình xử lý được thực hiện theo từng loại thuộc tính.

**Chuẩn hóa khóa định danh.** Khoảng trắng đầu/cuối được loại bỏ khỏi `order_id` và `user_id` trước khi kiểm tra quan hệ với các bảng khác. Đây là bước chuẩn hóa biểu diễn, không làm thay đổi ý nghĩa mã định danh. Sau chuẩn hóa, khóa phải được kiểm tra lại tính hợp lệ và tính duy nhất.

**Khôi phục `eval_set`.** Trong dữ liệu nguồn, `eval_set` có thể nhận các nhãn `prior`, `train` hoặc `test`. Báo cáo đối chiếu ghi nhận 359.330 ô bị thay bằng dạng thiếu và 453.999 nhãn bị phân loại là không hợp lệ; tổng cộng 813.329 ô cần được xem xét khôi phục theo quy tắc phân vùng. Nhóm xác định nhãn thông qua tư cách thành viên của `order_id` trong các bảng chi tiết: mã đơn xuất hiện trong `order_products__prior` được gán phân vùng `prior`; mã đơn xuất hiện trong `order_products__train` được gán phân vùng `train`. Chỉ những mã đơn không thuộc hai bảng chi tiết mới được xem xét là `test`, sau khi kiểm tra tính đầy đủ và không mâu thuẫn của phép phân vùng. Không gán nhãn `test` chỉ vì `eval_set` đang thiếu.

Cần phân biệt **813.329 ô nhãn ở bảng `orders`** với **12.019.100 dòng chi tiết `prior`** và **513.961 dòng chi tiết `train`** được báo cáo là không khớp khi đối chiếu nhãn. Hai nhóm sau là số dòng ở bảng chi tiết, nơi một `order_id` có thể lặp lại theo số sản phẩm trong giỏ; chúng không đại diện cho số đơn hàng duy nhất.

**Xử lý `order_number`.** Trường này phải là số nguyên dương (`>= 1`) biểu thị thứ tự đơn của người dùng. Đầu vào có 798.715 giá trị thiếu theo kiểm kê, 439.996 giá trị không hợp lệ theo kiểm tra miền cục bộ và một số giá trị có vẻ hợp lý nhưng khác với bản tham chiếu. Quy trình tái dựng `order_number` dựa trên thứ tự bản ghi của mỗi người dùng theo giả định rằng thứ tự liên quan trong tệp đầu vào vẫn được bảo toàn. Đây là một **giả định kỹ thuật**, không phải bằng chứng độc lập rằng thứ tự lịch sử thật đã được khôi phục hoàn hảo. Những trường hợp không thể tái dựng một cách nhất quán phải giữ thiếu hoặc được đánh dấu trong báo cáo chất lượng; không sao chép giá trị từ bản tham chiếu.

**Kiểm tra `order_dow` và `order_hour_of_day`.** Miền hợp lệ của `order_dow` là `[0, 6]`, còn `order_hour_of_day` là `[0, 23]`. Các giá trị được chuẩn hóa kiểu và kiểm tra miền sau phân tích cú pháp. Chuỗi như `2 %` không được tự động chuyển thành `2` chỉ bằng cách trích số ở mọi trường hợp; chỉ áp dụng quy tắc khôi phục khi mẫu lỗi được xác định rõ, phép chuyển đổi không mơ hồ và kết quả vượt qua kiểm tra miền. Nếu không đủ căn cứ, giá trị được chuyển thành thiếu (`NA`). `order_dow` được giữ dưới dạng mã số; nghiên cứu không tự tạo ngày lịch hoặc gán tên thứ khi chưa có căn cứ xác nhận quy ước mã.

**Xử lý `days_since_prior_order`.** Kiểm kê đầu vào nhiễu ghi nhận 753.252 giá trị thiếu tại cột này; báo cáo đối chiếu phân loại 547.043 ô là thông tin bị thay bằng giá trị thiếu. Vì `order_number` cũng bị nhiễu, không thể kết luận mọi giá trị thiếu trong cột đều thuộc đơn hàng đầu tiên. Về nghiệp vụ, khoảng cách ngày không áp dụng cho đơn đầu tiên của người dùng nên cần giữ `NA`, không thay bằng `0` hay giá trị trung bình. Đối với những giá trị bị mất mà không thể xác định chắc chắn từ thông tin còn lại, nhóm tiếp tục giữ thiếu và ghi nhận giới hạn này thay vì tự nội suy. Số lượng thiếu có cấu trúc chỉ được báo cáo sau khi các đơn đầu tiên được xác định bằng quy tắc lịch sử đã kiểm chứng.

### Làm sạch bảng `products`

Bảng `products` gồm mã sản phẩm, tên sản phẩm và mã phân loại. Kiểm kê đầu vào ghi nhận 6.923 giá trị thiếu hoặc bị thay thế trong `product_name`; báo cáo đối chiếu cũng cho thấy tên sản phẩm bị đổi thành các token như `null`. Các token chỉ được chuyển thành giá trị thiếu chuẩn (`pd.NA`) khi được xác định là biểu diễn thiếu theo quy tắc của cột. Tên sản phẩm không đủ căn cứ khôi phục được giữ thiếu, không thay bằng một tên phỏng đoán.

`product_id` là khóa chính; `aisle_id` và `department_id` là khóa ngoại tới hai bảng danh mục. Khoảng trắng ở các cột mã được chuẩn hóa trước khi kiểm tra khóa. Báo cáo audit ghi nhận các mã phân loại trong `products` khớp với các bảng danh mục trong phạm vi dữ liệu được cung cấp. Tên sản phẩm bị thiếu không làm mất mã định danh của sản phẩm; do đó, không loại sản phẩm chỉ vì `product_name` không có giá trị. Nếu cần nhãn dễ đọc trong biểu đồ, nhãn hiển thị có thể được tạo ở lớp trình bày mà không ghi ngược vào CSV sạch.

### Làm sạch bảng `aisles` và `departments`

Hai bảng danh mục được kiểm tra về khoảng trắng, giá trị thiếu và tính duy nhất của khóa. Với `aisles`, kiểm kê ghi nhận 40 token thiếu trong cột tên `aisle`; `departments` không có token thiếu được ghi nhận theo kiểm kê, nhưng vẫn có một số giá trị chứa khoảng trắng thừa. Các token được xác định là giá trị thiếu sẽ được chuẩn hóa theo quy tắc đã công bố.

Không được chuyển mọi chuỗi có nội dung `missing` thành `NA` một cách toàn cục. Báo cáo kiểm toán quy định tên danh mục literal `missing` không tự động được coi là null chỉ vì giống một từ biểu thị thiếu. Nếu nhóm muốn hiển thị nhãn này thành “Không xác định” trong bảng hoặc biểu đồ, việc ánh xạ cần được thực hiện rõ ràng ở lớp hiển thị hoặc bảng dẫn xuất, không âm thầm thay đổi ngữ nghĩa trường nguồn. `aisle_id` và `department_id` được chuẩn hóa khoảng trắng và kiểm tra khóa chính sau xử lý.

### Làm sạch hai bảng chi tiết `order_products__prior` và `order_products__train`

Hai bảng chi tiết là nguồn ghi nhận cặp đơn hàng–sản phẩm. Khóa ghép là (`order_id`, `product_id`). Báo cáo khóa chính không phát hiện khóa ghép trùng bổ sung sau chuẩn hóa biểu diễn mã. Kết quả này khác với việc một giỏ có nhiều dòng dùng cùng một giá trị `add_to_cart_order`: audit cấu trúc giỏ hàng ghi nhận 59.266 vị trí trùng bổ sung ở `prior` và 14.406 ở `train`. Đây là vấn đề về vị trí giỏ, không đồng nghĩa với việc cặp khóa (`order_id`, `product_id`) bị trùng.

**Xử lý `add_to_cart_order`.** Theo ngữ nghĩa, đây là số nguyên dương biểu thị vị trí sản phẩm được thêm vào giỏ. Đầu vào `prior` có 3.223.158 giá trị thiếu và 3.007.028 giá trị không hợp lệ theo kiểm kê; đầu vào `train` có lần lượt 348.739 và 186.888 trường hợp. Giá trị dị biệt như `9999` được xem là lỗi vị trí cần xử lý, không phải kích thước giỏ hàng. Quy trình tái dựng vị trí dựa trên giả định thứ tự dòng sản phẩm trong mỗi đơn vẫn được bảo toàn; giả định này phải được công bố và kiểm tra qua các điều kiện nhất quán. Nếu không thể khôi phục vị trí một cách đáng tin cậy, giữ thiếu thay vì tạo một thứ tự giả. Không xóa dòng giao dịch chỉ do vị trí bị lỗi và không thêm cột cờ vào sáu CSV sạch.

Báo cáo cấu trúc giỏ hàng ghi nhận kích thước giỏ tối đa quan sát được là 145 dòng ở `prior` và 80 dòng ở `train`. Đây là kích thước giỏ quan sát trong dữ liệu hiện có, không phải căn cứ để loại bỏ tự động các giỏ lớn. Tính liên tục của vị trí là một phép kiểm tra chất lượng hữu ích nhưng không đủ để chứng minh giỏ hàng hoàn chỉnh, đặc biệt khi dữ liệu có thể bị thiếu hoặc cắt cụt.

**Xử lý `reordered`.** Trường này được định nghĩa là biến nhị phân, chỉ chấp nhận `0` hoặc `1`. Kiểm kê đầu vào `prior` ghi nhận 5.438.428 token thiếu và 3.770.917 giá trị không hợp lệ; đầu vào `train` ghi nhận 211.571 token thiếu và 217.212 giá trị không hợp lệ. Giá trị hợp lệ chính xác là `0` hoặc `1` được giữ; giá trị âm, chuỗi có hậu tố không xác định hoặc giá trị ngoài miền được chuyển thành thiếu nếu không có quy tắc khôi phục được kiểm chứng. Không tự động trích chữ số từ các chuỗi như `1 kg` hoặc `0 USD`, vì phần số còn lại chưa chắc phản ánh đúng giá trị ban đầu.

`reordered` không phải nhãn mục tiêu của mô hình hoàn thiện giỏ hàng trong nghiên cứu. Vì thế, thiếu hoặc sai ở cột này không phải lý do để tự động loại bỏ một dòng vẫn có cặp khóa đơn hàng–sản phẩm hợp lệ. Trường hợp cần sử dụng `reordered` trong một phân tích riêng phải giới hạn mẫu ở những giá trị được xác nhận hợp lệ và báo rõ mẫu số tương ứng.

### Kiểm tra tính nhất quán của lịch sử đơn hàng

Báo cáo kiểm tra lịch sử ghi nhận 189.577 người dùng có chuỗi `order_number` bị đứt gãy hoặc thiếu điểm bắt đầu theo quy tắc kiểm tra; đồng thời có các trường hợp thứ tự đơn trùng lặp hoặc đơn cuối không phù hợp với chuỗi quan sát. Các kết quả này cho thấy cần thận trọng khi diễn giải lịch sử theo người dùng. Tuy nhiên, bản thân các dấu hiệu trên không chứng minh chắc chắn nguyên nhân là dữ liệu bị cắt cụt; chúng có thể liên quan đến nhiễu thuộc tính, thiếu đơn hoặc phạm vi mẫu được cung cấp.

Do không có căn cứ chắc chắn để tái tạo những đơn hàng không tồn tại trong tệp, nhóm không nội suy hoặc tạo thêm giao dịch giả. Các trường hợp không thể khắc phục được giữ trong báo cáo chất lượng và được xem là giới hạn dữ liệu. Những quy tắc tái dựng `order_number` và `add_to_cart_order` phải được hiểu là kết quả theo giả định của pipeline, không phải xác nhận rằng toàn bộ lịch sử mua sắm đã được phục hồi hoàn hảo.

### Tổng hợp quy tắc làm sạch và đối soát trước–sau

Bảng @tbl-dq-before-after tổng hợp các dạng vấn đề chính theo từng tệp, cách xử lý và điều kiện kiểm chứng ở đầu ra. Các số lượng trong cột “phát hiện trên đầu vào” được trích từ báo cáo kiểm kê/đối chiếu; chúng không phải số liệu còn lại sau làm sạch. Báo cáo `before_after.csv`, `relational_summary.csv` và `verification.json` của lượt chạy cuối là nguồn chuẩn để điền số lượng ô thiếu sau xử lý, số trường được khôi phục và mã băm đầu vào/đầu ra. Không suy ra tỷ lệ khắc phục bằng cách cộng các nhóm kiểm toán có định nghĩa khác nhau.

| Bảng | Vấn đề được ghi nhận trên đầu vào | Quy tắc xử lý | Điều kiện kiểm chứng sau xử lý |
|:---|:---|:---|:---|
| `aisles` | 134 dòng; 40 token thiếu ở cột `aisle`; khoảng trắng thừa ở mã/tên | Chuẩn hóa khoảng trắng; chuyển token thiếu đã xác nhận thành `NA`; giữ literal `missing` nếu đó là nhãn danh mục hợp lệ | Giữ số dòng và lược đồ; khóa `aisle_id` duy nhất; trạng thái thiếu được phản ánh trong báo cáo |
| `departments` | 21 dòng; không ghi nhận token thiếu theo kiểm kê; có khoảng trắng thừa | Chuẩn hóa khoảng trắng; không đổi nhãn chỉ vì giống token thiếu | Giữ số dòng và lược đồ; khóa `department_id` duy nhất |
| `products` | 49.688 dòng; 6.923 giá trị thiếu hoặc bị thay thế ở `product_name`; khoảng trắng ở mã và tên | Chuẩn hóa mã; chuyển token thiếu tên đã xác nhận thành `NA`; không điền tên phỏng đoán | Giữ mã `product_id`; kiểm tra khóa ngoại `aisle_id`, `department_id`; báo cáo số thiếu cuối từ kết quả chạy |
| `orders` | 3.421.083 dòng; nhiều giá trị thiếu/sai miền ở `order_number`, `order_dow`, `order_hour_of_day`, `days_since_prior_order`, `eval_set`; khoảng trắng ở ID | Chuẩn hóa ID; kiểm tra miền; tái dựng `order_number` theo giả định chuỗi còn giữ thứ tự; khôi phục `eval_set` bằng membership và kiểm tra phân vùng; giữ `NA` khi không đủ căn cứ | Khóa `order_id` duy nhất; kiểm tra phân vùng không mâu thuẫn; đối chiếu số ô khôi phục và số thiếu cuối với báo cáo chạy |
| `order_products__prior` | 32.434.489 dòng; thiếu/sai miền ở `reordered` và `add_to_cart_order`; khoảng trắng ở ID | Chuẩn hóa ID; kiểm tra khóa ghép; tái dựng vị trí theo giả định thứ tự dòng; giữ thiếu với cờ không thể khôi phục | Giữ khóa ghép duy nhất; kiểm tra liên kết tới `orders`/`products`; báo riêng vị trí trùng và vị trí không hợp lệ |
| `order_products__train` | 1.384.617 dòng; thiếu/sai miền ở `reordered` và `add_to_cart_order`; khoảng trắng ở ID | Áp dụng cùng quy tắc với `prior`; không xóa dòng chỉ vì thuộc tính phụ thiếu hoặc sai | Giữ khóa ghép duy nhất; phép ghép kiểm tra phải bảo toàn 1.384.617 dòng và 131.209 giỏ hàng |

: Quy tắc xử lý và điều kiện đối soát chất lượng trên sáu bảng {#tbl-dq-before-after}

*Nguồn: Nhóm tác giả tổng hợp từ các báo cáo `01_inventory`, `02_primary_keys`, `03_foreign_keys`, `04_order_history`, `05_basket_structure`, `06_compare_original` và các báo cáo đầu ra của pipeline làm sạch.*

Trong báo cáo chính, chỉ công bố tỷ lệ khắc phục và số ô thiếu sau xử lý khi các giá trị này đã được đối chiếu trực tiếp với kết quả chạy mới nhất. Các bản ghi đầu vào và đầu ra phải được kiểm tra về số dòng, tên cột, kiểu dữ liệu, khóa chính/khóa ghép, khóa ngoại và mã băm SHA-256. Chuỗi mã băm đầy đủ có thể lưu trong `verification.json` hoặc manifest kiểm chứng; phần nội dung chỉ cần dẫn nguồn báo cáo để đảm bảo khả năng truy vết.

### Đóng gói dữ liệu sạch và kiểm soát khả năng tái lập

Quy trình làm sạch được thực hiện theo từng khối (`chunksize = 250.000`) để xử lý dữ liệu lớn mà không cần nạp toàn bộ tệp vào bộ nhớ cùng lúc. Sau xử lý, sáu CSV được xuất độc lập trong thư mục `Data đã làm sạch/`, giữ nguyên lược đồ nguồn và không bổ sung cột kiểm toán vào các tệp này. Những thuộc tính không thể khôi phục chắc chắn được giữ thiếu; quy tắc sửa đổi, số lượng thay đổi và thông tin kiểm chứng được lưu trong báo cáo riêng.

Trước khi sử dụng dữ liệu cho các phân tích tiếp theo, nhóm đọc lại các tệp đầu ra và xác minh số dòng, lược đồ, khóa, quan hệ tham chiếu và mã băm theo báo cáo của lượt chạy cuối. Phép ghép kiểm tra đối với `order_products__train` đã được ghi nhận là bảo toàn 1.384.617 dòng và 131.209 giỏ hàng. Kết quả này là bằng chứng cho phép ghép kiểm tra cụ thể; nó không thay thế benchmark `master.parquet`, thời gian I/O và RAM đỉnh được trình bày ở Mục 3.2.

Tóm lại, quy trình làm sạch ưu tiên sửa các lỗi có quy tắc xác định, giữ thiếu đối với thông tin không đủ căn cứ khôi phục và bảo toàn những dòng giao dịch còn định danh hợp lệ. Cách tiếp cận này giúp hạn chế việc tạo dữ liệu giả hoặc làm sai phân phối kích thước giỏ hàng, đồng thời cho phép truy vết các quyết định làm sạch khi diễn giải kết quả khai phá luật kết hợp và mô hình gợi ý.
