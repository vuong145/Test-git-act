"""Chương 4, bước chuẩn bị: dựng giỏ fit/validation/test từ Master và che giỏ cố định.

Đầu ra DATA/Data phai sinh/M4/masked_baskets.parquet: order_id, user_id, split,
basket_size, observed, hidden, eligible (k >= 2). Phép che chỉ dùng seed và order_id,
không xem nội dung tập nào để chọn; mọi phương pháp đọc cùng tệp này.
M4/hashes.json ghi kèm tham số che để bước sau từ chối phép che lệch config.

ĐỌC NHANH: bước đầu Chương 4. Dựng giỏ fit/validation/test từ Master và CHE sản phẩm một lần duy nhất.
  Phép che chỉ phụ thuộc seed và order_id, nên mọi phương pháp đọc cùng một tệp che; tham số che được ghi vào hashes.json.
"""
import pandas as pd

from m4_common import HASHES, baskets, config, mask, mask_params
from project_io import check_hashes, path, require, write_frame, write_hashes

M2 = "DATA/Data phai sinh/M2"


def main():
    cfg = config()
    foundation = check_hashes()
    split = pd.read_parquet(path(M2) / "split_manifest.parquet")
    master = pd.read_parquet(path("DATA/Data đã làm sạch/master_train.parquet"),
                             columns=["order_id", "user_id", "product_id"])
    # Bước 1: dựng giỏ của fit/validation/test từ Master theo bảng chia tập.
    out = baskets(master, split, ["fit", "validation", "test"])
    # Bước 2: che sản phẩm; cùng một giỏ luôn bị che giống nhau (seed + order_id).
    masked = [mask(i, o, cfg["seeds"]["mask"], cfg["hidden_share"])
              for i, o in zip(out["items"], out.order_id)]
    out["basket_size"] = out["items"].map(len)
    out["observed"], out["hidden"] = [m[0] for m in masked], [m[1] for m in masked]
    out["eligible"] = out.basket_size >= 2
    out = out.drop(columns="items")
    # Bước 3: kiểm tra đủ giỏ và che đúng, rồi ghi tệp, hash và tham số che.
    require(len(out) == split.split.ne("reference").sum(), "Thiếu giỏ so với phân hoạch")
    require((out.observed.map(len) + out.hidden.map(len) == out.basket_size).all(), "Che sai")
    target = path(cfg["data_dir"]) / "masked_baskets.parquet"
    write_frame(target, out)
    write_hashes(HASHES, [target], mask=mask_params(cfg),
                 g0_split_sha256=foundation["canonical_split_sha256"])
    print(out.groupby("split").agg(baskets=("order_id", "size"), eligible=("eligible", "sum"),
                                   hidden=("hidden", lambda s: s.map(len).sum())))


if __name__ == "__main__":
    main()
