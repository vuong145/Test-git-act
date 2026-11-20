# KIẾN TRÚC DỮ LIỆU & TỔNG HỢP KIỂM TOÁN CHẤT LƯỢNG DỮ LIỆU
Báo cáo toàn diện về từ điển dữ liệu (Data Dictionary), tổng quan kiến trúc, và chi tiết các lỗi chất lượng dữ liệu phát hiện trong bộ dữ liệu đã làm dơ.

________________________________________
## PHẦN I: TỪ ĐIỂN DỮ LIỆU (DATA DICTIONARY)

### 1. Từ Điển Dữ Liệu Chi Tiết - Bộ Dữ Liệu Gốc (Raw Dataset)
Bảng mô tả cấu trúc chuẩn của 6 tệp dữ liệu nguyên bản: tên biến, ý nghĩa thực tế/kinh tế, đơn vị tính, kiểu dữ liệu lý thuyết và cột khóa liên kết giữa các bảng.

| Tên bảng | Tên biến (Column Name) | Ý nghĩa thực tế / Kinh tế | Đơn vị tính | Kiểu dữ liệu (Dữ liệu gốc) | Cột khóa liên kết giữa các bảng |
| --- | --- | --- | --- | --- | --- |
| orders.csv | order_id | Mã định danh duy nhất của từng đơn hàng giao dịch | Mã số ID (Định danh) | int64 | Khóa chính (Primary Key - PK) |
| orders.csv | user_id | Mã định danh duy nhất của người tiêu dùng đặt đơn | Mã số ID (Định danh) | int64 | Khóa logic khách hàng (liên kết User) |
| orders.csv | eval_set | Nhãn phân chia tập dữ liệu máy học (prior, train, test) | Danh mục (3 nhãn chuẩn) | object | Không (Thuộc tính phân vùng dữ liệu) |
| orders.csv | order_number | Số thứ tự lần mua hàng tích lũy của khách hàng (Đơn 1, 2, 3...) | Lần mua (Số thứ tự tích lũy) | int64 | Không (Thuộc tính đo lường tần suất mua) |
| orders.csv | order_dow | Thứ trong tuần phát sinh đơn (0: Chủ Nhật -> 6: Thứ Bảy) | Ngày trong tuần (0 - 6) | int64 | Không (Thuộc tính chu kỳ tuần) |
| orders.csv | order_hour_of_day | Khung giờ trong ngày khách thực hiện giao dịch (0h -> 23h) | Giờ trong ngày (0 - 23h) | int64 | Không (Thuộc tính thời gian trong ngày) |
| orders.csv | days_since_prior_order | Khoảng cách số ngày kể từ lần đặt đơn gần nhất trước đó | Số ngày (0.0 - 30.0 ngày) | float64 | Không (Thuộc tính chu kỳ giữ chân / Retention) |
| order_products__prior.csv | order_id | Mã đơn hàng lịch sử tương ứng trong bảng orders | Mã số ID (Định danh) | int64 | Khóa ngoại (FK) -> orders.order_id; Khóa chính phức hợp |
| order_products__prior.csv | product_id | Mã sản phẩm có trong giỏ hàng lịch sử | Mã số ID (Định danh) | int64 | Khóa ngoại (FK) -> products.product_id; Khóa chính phức hợp |
| order_products__prior.csv | add_to_cart_order | Thứ tự sản phẩm được khách chọn đưa vào giỏ hàng | Số thứ tự (1, 2, 3...) | int64 | Không (Thuộc tính tâm lý / Độ ưu tiên chọn) |
| order_products__prior.csv | reordered | Cờ chỉ báo khách từng mua sản phẩm này chưa (1: Mua lại, 0: Mua đầu) | Cờ nhị phân (0 hoặc 1) | int64 | Không (Thuộc tính đo lường lòng trung thành) |
| order_products__train.csv | order_id | Mã đơn hàng mới nhất của khách phục vụ kiểm thử mô hình | Mã số ID (Định danh) | int64 | Khóa ngoại (FK) -> orders.order_id; Khóa chính phức hợp |
| order_products__train.csv | product_id | Mã sản phẩm có trong giỏ hàng mới nhất | Mã số ID (Định danh) | int64 | Khóa ngoại (FK) -> products.product_id; Khóa chính phức hợp |
| order_products__train.csv | add_to_cart_order | Thứ tự sản phẩm được khách chọn cho vào giỏ hàng mới nhất | Số thứ tự (1, 2, 3...) | int64 | Không (Thuộc tính tâm lý / Độ ưu tiên chọn) |
| order_products__train.csv | reordered | Cờ chỉ báo khách từng mua sản phẩm này chưa (1: Mua lại, 0: Mua đầu) | Cờ nhị phân (0 hoặc 1) | int64 | Không (Thuộc tính đo lường lòng trung thành) |
| products.csv | product_id | Mã định danh duy nhất của từng mặt hàng bán lẻ | Mã số ID (Định danh) | int64 | Khóa chính (Primary Key - PK) |
| products.csv | product_name | Tên thương mại, thương hiệu và quy cách sản phẩm | Chuỗi ký tự (Tên hàng hóa) | object | Không (Thuộc tính mô tả danh mục) |
| products.csv | aisle_id | Mã khu vực kệ hàng / quầy trưng bày sản phẩm | Mã số ID (Định danh) | int64 | Khóa ngoại (FK) -> aisles.aisle_id (PK) |
| products.csv | department_id | Mã ngành hàng / phòng ban quản lý danh mục sản phẩm | Mã số ID (Định danh) | int64 | Khóa ngoại (FK) -> departments.department_id (PK) |
| aisles.csv | aisle_id | Mã định danh duy nhất của quầy kệ trưng bày hàng hóa | Mã số ID (Định danh) | int64 | Khóa chính (Primary Key - PK) |
| aisles.csv | aisle | Tên phân loại quầy kệ hàng (vd: yogurt, fresh fruits, cookies...) | Chuỗi ký tự (Tên kệ hàng) | object | Không (Thuộc tính mô tả phân loại) |
| departments.csv | department_id | Mã định danh duy nhất của ngành hàng kinh doanh | Mã số ID (Định danh) | int64 | Khóa chính (Primary Key - PK) |
| departments.csv | department | Tên ngành hàng kinh doanh (vd: produce, dairy eggs, beverages...) | Chuỗi ký tự (Tên ngành) | object | Không (Thuộc tính phân cấp kinh doanh cao nhất) |

________________________________________
### 2. Từ Điển Dữ Liệu Chi Tiết - Bộ Dữ Liệu Đã Làm Dơ (Dirty Dataset)
Bảng đối chiếu sự biến dạng của các trường thông tin trong bộ dữ liệu dơ: kiểu dữ liệu bị ép lệch, cờ khóa, cùng tình trạng lỗi phát hiện trên từng cột.

| Tên bảng | Tên biến (Column Name) | Ý nghĩa thực tế / Kinh tế | Đơn vị tính | Kiểu dữ liệu (Dữ liệu dơ) | Cột khóa liên kết giữa các bảng | Tình trạng dữ liệu dơ / Lỗi phát hiện |
| --- | --- | --- | --- | --- | --- | --- |
| orders.csv | order_id | Mã định danh duy nhất của từng đơn hàng giao dịch | Mã số ID (Định danh) | int64 | Khóa chính (Primary Key - PK) | Bảo toàn nguyên vẹn, không có null |
| orders.csv | user_id | Mã định danh duy nhất của người tiêu dùng đặt đơn | Mã số ID (Định danh) | int64 | Khóa logic khách hàng (liên kết User) | Bảo toàn nguyên vẹn, không có null |
| orders.csv | eval_set | Nhãn phân chia tập dữ liệu máy học | Danh mục (Bị nhiễu) | object | Không | Bị thiếu 224,458 dòng (6.56%); Vỡ thành 13 nhãn do dính chữ hoa (PRIOR, TRAIN), khoảng trắng (  pri), ký tự rác (chưa rõ, ?, unknown) |
| orders.csv | order_number | Số thứ tự lần mua hàng tích lũy của khách hàng | Lần mua (Bị biến dạng) | float64 (bị ép kiểu) | Không | Bị thiếu 532,674 dòng (15.57%); 141,354 dòng bị số âm (-100 đến -1); Giá trị cực đại vô lý lên đến 100,000 |
| orders.csv | order_dow | Thứ trong tuần phát sinh đơn hàng | Ngày trong tuần (Bị biến dạng) | float64 (bị ép kiểu) | Không | Bị thiếu 308,694 dòng (9.02%); 188,670 dòng vi phạm miền giá trị 0-6 (gồm 86,124 dòng âm tới -6 và giá trị ngoại lai 9,999) |
| orders.csv | order_hour_of_day | Khung giờ trong ngày khách thực hiện giao dịch | Giờ trong ngày | float64 (bị ép kiểu) | Không | Bị thiếu 396,286 dòng (11.58%); Miền giá trị số vẫn nằm trong 0-23 |
| orders.csv | days_since_prior_order | Khoảng cách số ngày kể từ lần đặt đơn gần nhất | Số ngày | float64 | Không | Bị thiếu 586,588 dòng (17.15%), tức bị làm rỗng nhân tạo thêm 380,379 đơn hàng so với 206,209 dòng của dữ liệu gốc |
| order_products__prior.csv | order_id | Mã đơn hàng lịch sử tương ứng trong bảng orders | Mã số ID (Định danh) | int64 | Khóa ngoại (FK) -> orders.order_id; Khóa chính phức hợp | Bảo toàn nguyên vẹn tính toàn vẹn tham chiếu |
| order_products__prior.csv | product_id | Mã sản phẩm có trong giỏ hàng lịch sử | Mã số ID (Định danh) | int64 | Khóa ngoại (FK) -> products.product_id; Khóa chính phức hợp | Bảo toàn nguyên vẹn tính toàn vẹn tham chiếu |
| order_products__prior.csv | add_to_cart_order | Thứ tự sản phẩm được khách chọn cho vào giỏ hàng | Số thứ tự (Bị biến dạng) | float64 (bị ép kiểu) | Không | Bị thiếu 2,148,588 dòng (6.62%); Có 611,915 dòng mang giá trị âm (tới -96); Giá trị cực đại vô lý lên đến 132,000 |
| order_products__prior.csv | reordered | Cờ chỉ báo khách từng mua sản phẩm này chưa | Cờ nhị phân (Bị biến dạng) | float64 (bị ép kiểu) | Không | Bị thiếu 3,624,374 dòng (11.17%); 2,041,483 dòng vi phạm miền nhị phân {0, 1} (gồm 963,652 dòng -1 và 1,077,831 dòng 9999) |
| order_products__train.csv | order_id | Mã đơn hàng mới nhất phục vụ kiểm thử mô hình | Mã số ID (Định danh) | int64 | Khóa ngoại (FK) -> orders.order_id; Khóa chính phức hợp | Bảo toàn nguyên vẹn tính toàn vẹn tham chiếu |
| order_products__train.csv | product_id | Mã sản phẩm có trong giỏ hàng mới nhất | Mã số ID (Định danh) | int64 | Khóa ngoại (FK) -> products.product_id; Khóa chính phức hợp | Bảo toàn nguyên vẹn tính toàn vẹn tham chiếu |
| order_products__train.csv | add_to_cart_order | Thứ tự sản phẩm cho vào giỏ hàng mới nhất | Số thứ tự (Bị biến dạng) | float64 (bị ép kiểu) | Không | Bị thiếu 232,639 dòng (16.80%); Có 61,507 dòng mang giá trị âm (tới -55); Giá trị cực đại vô lý lên đến 61,000 |
| order_products__train.csv | reordered | Cờ chỉ báo khách từng mua sản phẩm này chưa | Cờ nhị phân (Bị biến dạng) | float64 (bị ép kiểu) | Không | Bị thiếu 141,067 dòng (10.19%); 82,478 dòng vi phạm miền nhị phân {0, 1} (gồm 38,344 dòng -1 và 44,134 dòng 9999) |
| products.csv | product_id | Mã định danh duy nhất của từng mặt hàng bán lẻ | Mã số ID (Định danh) | int64 | Khóa chính (Primary Key - PK) | Bảo toàn nguyên vẹn, không có null |
| products.csv | product_name | Tên thương mại và quy cách sản phẩm | Chuỗi ký tự (Bị nhiễu) | object | Không | Bị mất thông tin tên sản phẩm ở 6,923 dòng (13.93%), gồm 4,286 dòng null và 2,637 dòng rác (unknown: 888, ?: 887, chưa rõ: 862) |
| products.csv | aisle_id | Mã khu vực kệ hàng / quầy trưng bày | Mã số ID (Định danh) | int64 | Khóa ngoại (FK) -> aisles.aisle_id (PK) | Bảo toàn nguyên vẹn, không có null |
| products.csv | department_id | Mã ngành hàng / phòng ban quản lý | Mã số ID (Định danh) | int64 | Khóa ngoại (FK) -> departments.department_id (PK) | Bảo toàn nguyên vẹn, không có null |
| aisles.csv | aisle_id | Mã định danh duy nhất của quầy kệ trưng bày | Mã số ID (Định danh) | int64 | Khóa chính (Primary Key - PK) | Bảo toàn nguyên vẹn, không có null |
| aisles.csv | aisle | Tên phân loại quầy kệ hàng | Chuỗi ký tự (Bị nhiễu) | object | Không | Bị thiếu 22 dòng null (16.42%) và có 18 dòng bị thay bằng chuỗi rác (chưa rõ: 8, unknown: 6, ?: 4) |
| departments.csv | department_id | Mã định danh duy nhất của ngành hàng kinh doanh | Mã số ID (Định danh) | int64 | Khóa chính (Primary Key - PK) | Bảo toàn nguyên vẹn, không có null |
| departments.csv | department | Tên ngành hàng kinh doanh | Chuỗi ký tự (Lỗi định dạng) | object | Không | Không thiếu dòng nào nhưng dính lỗi khoảng trắng thừa (frozen   , dairy eggs   ) và lỗi in hoa hoàn toàn (INTERNATIONAL, BABIES) |

________________________________________
## PHẦN II: TỔNG HỢP CÁC LỖI TRONG BỘ DỮ LIỆU ĐÃ LÀM DƠ
1. BẢNG TỔNG QUAN LỖI TRÊN 6 TỆP DỮ LIỆU
Tên Tệp	Tổng Số Dòng	Số Cột	Danh Sách Cột	Các Cột Dính Lỗi	Các Dạng Lỗi Chính Xuất Hiện
orders.csv	3,421,083	7	order_id, user_id, eval_set, order_number, order_dow, order_hour_of_day, days_since_prior_order	order_number, order_dow, days_since_prior_order, eval_set, order_hour_of_day, các cột ID	Thiếu dữ liệu (NaN, ?, -), số âm, cực đại giả mạo, dính % và VND, khoảng trắng thừa
products.csv	49,688	4	product_id, product_name, aisle_id, department_id	product_name, product_id, aisle_id, department_id	Thiếu tên sản phẩm (NaN, ?, unknown, chưa rõ), dính đơn vị tính rác, khoảng trắng đầu số
aisles.csv	134	2	aisle_id, aisle	aisle, aisle_id	Thiếu tên kệ hàng (NaN, chưa rõ, ?, unknown), khoảng trắng thừa
departments.csv	21	2	department_id, department	department	Khoảng trắng đuôi chuỗi, lỗi viết hoa bất nhất
order_products__train.csv	1,384,617	4	order_id, product_id, add_to_cart_order, reordered	add_to_cart_order, reordered, các cột ID	Thiếu giá trị, số âm, cực đại khống, sai miền nhị phân (-1, 9999), dính chữ lạ, khoảng trắng
order_products__prior.csv	32,434,489	4	order_id, product_id, add_to_cart_order, reordered	add_to_cart_order, reordered, các cột ID	Thiếu giá trị diện rộng, số âm, cực đại khống (132,000), sai miền nhị phân (-1, 9999), dính chữ lạ
________________________________________
2. CHI TIẾT LỖI CỤ THỂ THEO TỪNG TỆP
2.1. Tệp orders.csv (3,421,083 dòng, 7 cột)
	Danh sách 7 cột: order_id, user_id, eval_set, order_number, order_dow, order_hour_of_day, days_since_prior_order
	Lỗi khuyết thiếu & rác ngụy trang (NaN, ?, -):
	order_number: Thiếu 798,715 dòng (23.35%).
	days_since_prior_order: Thiếu 753,252 dòng (22.02%).
	order_hour_of_day: Thiếu 555,547 dòng (16.24%).
	order_dow: Thiếu 463,331 dòng (13.54%).
	eval_set: Thiếu 359,330 dòng (10.50%).
	Lỗi ngoại lai & vi phạm logic miền giá trị:
	order_number: Có 141,354 dòng âm (nhỏ nhất -100); ngoại lai cực đại giả mạo chạm mốc 100,000.
	order_dow: Có 86,124 dòng âm (nhỏ nhất -6); có 188,670 dòng vượt quá chu kỳ tuần (>6, cực đại chạm 9,999).
	eval_set: Nhãn bị cắt cụt ký tự và sai chính tả (chứa '  pri', 'pri', 'tra').
	Lỗi ô nhiễm đơn vị tính (chuyển cột số thành chuỗi):
	order_dow: 313,280 dòng bị dính ký tự '%' (ví dụ: '2 %').
	order_number: 139,221 dòng bị dính chữ 'VND' (ví dụ: '2 VND').
	Lỗi khoảng trắng thừa: Hơn 270,000 ô ở các cột order_id, user_id và eval_set bị dính khoảng trắng đầu/cuối.
________________________________________
2.2. Tệp products.csv (49,688 dòng, 4 cột)
	Danh sách 4 cột: product_id, product_name, aisle_id, department_id
	Lỗi khuyết thiếu tên sản phẩm (product_name):
	Tổng cộng mất tên: 6,923 dòng (13.93%).
	Gồm: 4,286 dòng để trống (NaN) và 2,637 dòng bị điền rác ngụy trang ('unknown': 888 dòng, '?': 887 dòng, 'chưa rõ': 862 dòng).
	Lỗi dính đơn vị tính: 1,041 dòng tên sản phẩm bị dính đơn vị đo lường ở cuối tên.
	Lỗi khoảng trắng ở cột khóa: Hơn 3,900 ô ở product_id, aisle_id, department_id bị chèn khoảng trắng đầu (ví dụ: ' 1'), làm hỏng phép kết nối bảng (merge/join).
________________________________________
2.3. Tệp aisles.csv (134 dòng, 2 cột) & departments.csv (21 dòng, 2 cột)
	Tại aisles.csv (2 cột: aisle_id, aisle):
	Khuyết thiếu: 40 kệ hàng bị thiếu tên (chiếm 29.85%), gồm 22 dòng NaN và 18 dòng ký tự rác ('chưa rõ': 8, 'unknown': 6, '?': 4).
	Khoảng trắng: 14 dòng aisle_id và 37 dòng aisle dính khoảng trắng.
	Tại departments.csv (2 cột: department_id, department):
	Khoảng trắng: Dính dấu cách ở đuôi chữ ('frozen   ', 'dairy eggs   ').
	Định dạng: Viết hoa toàn bộ mất tính đồng nhất ('INTERNATIONAL', 'BABIES').
________________________________________
2.4. Tệp order_products__train.csv (1,384,617 dòng, 4 cột)
	Danh sách 4 cột: order_id, product_id, add_to_cart_order, reordered
	Cột add_to_cart_order:
	Khuyết thiếu: 348,739 dòng (25.19%) (gồm 232,639 NaN và 116,100 rác).
	Vi phạm miền giá trị: Có 61,507 dòng mang giá trị âm (nhỏ nhất -55); ngoại lai cực đại lên tới 61,000.
	Dính đơn vị tính: 115,527 dòng dính ký tự lạ.
	Cột reordered:
	Khuyết thiếu: 211,571 dòng (15.28%).
	Vi phạm miền nhị phân {0,1}: Có 82,478 dòng sai miền, gồm 38,344 dòng âm (-1) và 44,134 dòng cực đại (9,999).
	Dính đơn vị tính: 126,722 dòng dính chữ lạ.
	Khoảng trắng: ~110,600 dòng ở order_id và product_id dính khoảng trắng.
________________________________________
2.5. Tệp order_products__prior.csv (32,434,489 dòng, 4 cột)
	Danh sách 4 cột: order_id, product_id, add_to_cart_order, reordered
	Cột add_to_cart_order:
	Khuyết thiếu: 3,223,158 dòng (9.94%).
	Vi phạm miền giá trị: Có 611,915 dòng mang giá trị âm (nhỏ nhất -96); ngoại lai cực đại chạm mốc 132,000.
	Dính đơn vị tính: 2,170,087 dòng dính chữ lạ/đơn vị tính.
	Cột reordered:
	Khuyết thiếu: 5,438,428 dòng (16.77%).
	Vi phạm miền nhị phân {0,1}: Có 2,041,483 dòng sai miền, gồm 963,652 dòng mang giá trị âm (-1) và 1,077,831 dòng mang giá trị cực đại (9,999).
	Dính đơn vị tính: 1,569,397 dòng dính ký tự rác.
	Khoảng trắng: Hàng triệu ô ở các cột ID dính khoảng trắng thừa.
