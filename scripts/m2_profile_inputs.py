"""Dấu vết kiểm tra đầu vào: shape, info(memory_usage="deep"), isna().mean()*100, describe().

Tách tỷ lệ thiếu cấp dòng Master (train) khỏi cấp giỏ reference. Không thay thế EDA 3.4–3.6.
Đầu ra: BAO CAO/Bao cao EDA/common/profile/.

ĐỌC NHANH: ghi dấu vết kiểm tra đầu vào (shape, info, tỷ lệ thiếu, describe) cho mục 3.2; mẫu số ghi rõ là dòng Master hay giỏ reference.
"""
import io

import pandas as pd

from project_io import check_hashes, config, path, write_frame, write_json


# Bảng tỷ lệ thiếu theo cột, ghi rõ mẫu số và đơn vị.
def missing_table(frame, unit):
    return pd.DataFrame({"column": frame.columns, "missing": frame.isna().sum().values,
                         "missing_pct": (frame.isna().mean() * 100).values,
                         "denominator": len(frame), "unit": unit})


# main: kiểm hash -> ghi info/thiếu/describe của Master và của bảng giỏ reference.
def main():
    cfg = config()
    record = check_hashes()
    folder = path("BAO CAO/Bao cao EDA/common/profile")
    master = pd.read_parquet(path(cfg["master"]))
    buffer = io.StringIO()
    master.info(buf=buffer, memory_usage="deep")
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "master_info.txt").write_text(buffer.getvalue(), encoding="utf-8")
    write_frame(folder / "master_missing.csv", missing_table(master, "train product-order row"))
    baskets = pd.read_parquet(path(cfg["data_dir"]) / "basket_summary.parquet")
    write_frame(folder / "reference_missing.csv", missing_table(baskets, "reference basket"))
    write_frame(folder / "reference_describe.csv",
                baskets[cfg["correlation_columns"]].describe().reset_index())
    write_json(folder / "inspection.json", {
        "scope": "Basic inspection trace, not completed section 3.4",
        "master_shape": list(master.shape), "reference_baskets_shape": list(baskets.shape),
        "canonical_split_sha256": record["canonical_split_sha256"]})
    print(master.shape, baskets.shape)


if __name__ == "__main__":
    main()
