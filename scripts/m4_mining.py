"""Chương 4: danh mục C và luật kết hợp trên reference cho lưới giai đoạn A.

catalog.parquet: mọi sản phẩm reference đã xếp hạng (C với Top-N là rank <= N).
rules_grid.parquet: luật FP-Growth cho mỗi (top_n, min_count, max_len), confidence
>= ngưỡng thấp nhất của lưới; ngưỡng cao hơn lọc khi chấm validation.
Apriori chỉ chạy trong m4_benchmark_mining.py để so sánh và kiểm tra tương đương.
Chạy sau m4_prepare.py; cập nhật M4/hashes.json (giữ tham số che, thêm lưới A).

ĐỌC NHANH: học danh mục C và luật kết hợp CHỈ trên reference. Chạy FP-Growth cho 12 tổ hợp (N, min_count, max_len) của giai đoạn A.
  Apriori không chạy ở đây (chỉ dùng trong benchmark để so sánh).
"""
import itertools

import pandas as pd

from m4_common import HASHES, basket_matrix, catalog, check_mask, config, mine, rules
from project_io import check_hashes, path, write_frame, write_hashes

M2 = "DATA/Data phai sinh/M2"


def main():
    cfg = config()
    grid = cfg["grid_A"]
    check_hashes()
    record = check_hashes(HASHES)
    check_mask(record, cfg)
    reference = pd.read_parquet(path(M2) / "reference.parquet",
                                columns=["order_id", "product_id", "department_id"])
    # Xếp hạng toàn bộ sản phẩm reference theo độ phổ biến -> danh mục C.
    ranked = catalog(reference)
    n = reference.order_id.nunique()
    found = []
    # Mỗi tổ hợp: dựng ma trận giỏ x sản phẩm của Top-N, khai phá FP-Growth, sinh luật với confidence >= ngưỡng thấp nhất của lưới.
    for top_n, min_count, max_len in itertools.product(grid["top_n"], grid["min_count"], grid["max_len"]):
        matrix = basket_matrix(reference, ranked.product_id[:top_n])
        r = rules(mine(matrix, "fpgrowth", min_count, max_len), n, min(grid["min_confidence"]))
        found.append(r.assign(top_n=top_n, min_count=min_count, max_len=max_len))
        print(f"N={top_n} min_count={min_count} max_len={max_len}: {len(r)} luật")
    # Ghi danh mục, bảng luật và cập nhật hash (giữ tham số che).
    data = path(cfg["data_dir"])
    write_frame(data / "catalog.parquet", ranked)
    write_frame(data / "rules_grid.parquet", pd.concat(found, ignore_index=True))
    write_hashes(HASHES, [data / f for f in ("masked_baskets.parquet", "catalog.parquet",
                                             "rules_grid.parquet")],
                 mask=record["mask"], g0_split_sha256=record["g0_split_sha256"],
                 grid_A=grid, reference_baskets=n)


if __name__ == "__main__":
    main()
