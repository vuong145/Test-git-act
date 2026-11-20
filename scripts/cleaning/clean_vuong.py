"""Vương: làm sạch aisles, departments và order_products__prior.

Chạy: python scripts/cleaning/clean_vuong.py   (cấu hình: config_vuong.json)
Khóa ngoại của prior được đối chiếu với order_id/product_id đọc trực tiếp từ
orders.csv/products.csv nhiễu; script này không làm sạch hai bảng đó.

ĐỌC NHANH: file này chỉ khai báo THỨ TỰ làm sạch phần của Vương; toàn bộ logic nằm trong common.py.
  Aisles và departments (bảng nhỏ) làm trước; prior (32,4 triệu dòng) làm sau vì cần đối chiếu khóa ngoại với orders/products nhiễu.
"""
from common import clean_detail, clean_dimension, cli

TABLES = ['aisles', 'departments', 'order_products__prior']


# Thứ tự: 2 bảng danh mục trước, rồi bảng prior (đọc theo khối, tái dựng add_to_cart_order).
def steps(c):
    clean_dimension('aisles', c)
    clean_dimension('departments', c)
    clean_detail('order_products__prior', c, c.references['orders'], c.references['products'])


if __name__ == '__main__':
    cli('vuong', TABLES, steps)
