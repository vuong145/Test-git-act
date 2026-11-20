"""Vương, mục 3.4: thống kê mô tả trên reference -> 8 CSV và reference_outliers.json.

Mẫu số ghi ở từng bảng: giỏ, dòng sản phẩm–đơn hoặc dòng có reordered hợp lệ.
Giữ đủ danh mục (cả nhóm 0 dòng và mã chưa có tên); không lọc Top-N trong reference.

ĐỌC NHANH: tạo 8 bảng thống kê mô tả của mục 3.4 trên tập reference (không đụng test).
  Năm phần trong summarize(): (1) mô tả 4 biến; (2) tần số ngày giờ; (3) ngoại lai IQR (chỉ đánh dấu, giữ 100% giỏ);
  (4) ngành, quầy, độ phổ biến sản phẩm; (5) độ phủ Top-N = tỷ lệ giỏ có ít nhất một sản phẩm trong Top-N.
  Mọi con số trong lời văn mục 3.4 được chép từ các CSV này.
"""
import numpy as np
import pandas as pd

from m2_foundation import build_baskets
from project_io import check_hashes, config, path, require, write_frame, write_json


# Sản phẩm/quầy chưa có tên thì hiện 'Chưa có tên (ID=...)' để không mất dòng.
def display_name(value, identifier):
    return f"Chưa có tên (ID={identifier})" if pd.isna(value) or not str(value).strip() else str(value)


# Bảng theo ngành hoặc quầy: số dòng, số giỏ, tỷ lệ mua lại; giữ đủ danh mục kể cả mã 0 dòng.
def group_summary(reference, lookup, key, label, n_baskets):
    """Theo ngành/quầy, giữ đủ danh mục nguồn kể cả mã không xuất hiện."""
    require(not lookup[key].duplicated().any() and reference[key].isin(lookup[key]).all(),
            "Lookup ID trùng hoặc lạ")
    counts = reference.groupby(key, observed=True).agg(
        row_count=("order_id", "size"), basket_count=("order_id", "nunique"),
        reordered_valid=("reordered", "count"), reordered_yes=("reordered", "sum")).reset_index()
    r = lookup[[key, label]].merge(counts, on=key, how="left", validate="one_to_one"
                                   ).sort_values(key).reset_index(drop=True)
    for column in counts.columns.drop(key):
        r[column] = r[column].fillna(0).astype("int64")
    r["display_name"] = [display_name(v, i) for i, v in zip(r[key], r[label])]
    r["reordered_missing"] = r.row_count - r.reordered_valid
    r["row_share"] = r.row_count / len(reference)
    r["basket_coverage"] = r.basket_count / n_baskets
    r["observed_reorder_rate"] = r.reordered_yes / r.reordered_valid.replace(0, np.nan)
    r["reordered_missing_pct"] = 100 * r.reordered_missing / r.row_count.replace(0, np.nan)
    require(r.row_count.sum() == len(reference) and r.basket_count.le(n_baskets).all(),
            f"Mất dòng hoặc độ phủ sai: {label}")
    return r


# Top-10 ngành cộng một dòng 'các ngành còn lại', dùng cho hình 2.
def department_display(reference, departments, n_baskets):
    """Top-10 ngành theo số dòng và một dòng gộp các ngành còn lại (độ phủ tính theo hợp)."""
    top = departments.sort_values(["row_count", "department_id"], ascending=[False, True]).head(10)
    top = top.assign(group_key=top.department_id.astype(str))
    others = reference.loc[~reference.department_id.isin(top.department_id)]
    rest = pd.DataFrame([{"group_key": "remaining", "display_name": "Các ngành còn lại",
                          "row_count": len(others), "row_share": len(others) / len(reference),
                          "basket_count": others.order_id.nunique(),
                          "basket_coverage": others.order_id.nunique() / n_baskets}])
    return pd.concat([top[rest.columns], rest], ignore_index=True)


# Tính toàn bộ 8 bảng của mục 3.4.
def summarize(reference, baskets, departments, aisles, products, cfg):
    require(len(reference) > 0, "Empty reference")
    pd.testing.assert_frame_equal(baskets, build_baskets(reference, cfg), check_exact=True)
    n, rule = len(baskets), cfg["quantile_interpolation"]
    overview = {"users": baskets.user_id.nunique(), "baskets": n, "product_order_rows": len(reference),
                "products_observed": reference.product_id.nunique(),
                "departments_observed": reference.department_id.nunique(),
                "aisles_observed": reference.aisle_id.nunique(),
                "singleton_baskets": int(baskets.basket_size.eq(1).sum())}
    # (1) Mô tả 4 biến định lượng: trung bình, độ lệch chuẩn mẫu, phân vị, độ lệch, độ nhọn vượt chuẩn.
    rows = []
    for column in cfg["correlation_columns"]:   # std mẫu (ddof=1), kurtosis vượt chuẩn
        s = baskets[column].dropna().astype("float64")
        q = s.quantile([0.25, 0.5, 0.75], interpolation=rule)
        varied = s.nunique() > 1
        rows.append({"variable": column, "n_total": n, "n_valid": len(s), "n_missing": n - len(s),
                     "missing_pct": 100 * (n-len(s))/n, "mean": s.mean(), "std": s.std(ddof=1),
                     "min": s.min(), "q1": q.loc[0.25], "median": q.loc[0.5], "q3": q.loc[0.75],
                     "max": s.max(), "skew": s.skew() if len(s) >= 3 and varied else np.nan,
                     "kurtosis_excess": s.kurt() if len(s) >= 4 and varied else np.nan})
    # (2) Tần số theo ngày, giờ, khung giờ: có hàng NA riêng và hai mẫu số (cả mẫu / chỉ giá trị hợp lệ).
    frequencies = []
    for column, domain in {"order_dow": range(7), "order_hour_of_day": range(24),
                           "hour_band": cfg["hour_labels"]}.items():
        s = baskets[column]
        valid = int(s.notna().sum())
        for value in [*domain, None]:   # None = dòng NA
            count = int(s.eq(value).sum()) if value is not None else n - valid
            frequencies.append({"variable": column, "value": "NA" if value is None else str(value),
                                "is_missing": value is None, "count": count, "n_total": n,
                                "n_valid": valid, "all_pct": 100 * count/n,
                                "valid_pct": 100 * count/valid if valid and value is not None else np.nan})
    # (3) Ngoại lai kích thước giỏ theo IQR: chỉ đánh dấu, quyết định giữ lại 100% giỏ.
    sizes = baskets.basket_size
    q1, q3 = sizes.quantile([0.25, 0.75], interpolation=rule)
    iqr = float(q3-q1)
    lower, upper = float(q1-cfg["iqr_multiplier"]*iqr), float(q3+cfg["iqr_multiplier"]*iqr)
    flagged = int((sizes.lt(lower) | sizes.gt(upper)).sum())
    outliers = {"scope": "reference baskets only", "n_baskets": n, "q1": float(q1), "q3": float(q3),
                "iqr": iqr, "lower_fence": lower, "upper_fence": upper, "flagged_baskets": flagged,
                "flagged_rate": flagged/n, "flagged_pct": 100*flagged/n,
                "decision": "retain all baskets", "quantile_interpolation": rule}
    # (4) Ngành, quầy, độ phổ biến sản phẩm (xếp theo số giỏ chứa, hòa thì theo product_id).
    dept = group_summary(reference, departments, "department_id", "department", n)
    pop = reference.groupby("product_id", observed=True).agg(
        basket_count=("order_id", "nunique"), row_count=("order_id", "size")).reset_index()
    require(pop.basket_count.eq(pop.row_count).all(), "Duplicate product/giỏ")
    require(pop.product_id.isin(products.product_id).all(), "Unknown product")
    pop = pop.merge(products[["product_id", "product_name"]], on="product_id", how="left",
                    validate="one_to_one")
    pop["display_name"] = [display_name(v, i) for i, v in zip(pop.product_id, pop.product_name)]
    pop = pop.sort_values(["basket_count", "product_id"], ascending=[False, True]).reset_index(drop=True)
    pop["popularity"] = pop.basket_count/n
    pop["rank"] = np.arange(1, len(pop)+1)
    pop["row_share"] = pop.row_count/len(reference)
    pop["cumulative_row_share"] = pop.row_share.cumsum()
    # (5) Độ phủ Top-N: hợp các giỏ có chứa sản phẩm trong Top-N (không cộng các popularity).
    top_rows = []
    for requested in cfg["top_n_grid"]:   # độ phủ là hợp các giỏ, không cộng popularity
        ids = pop.head(requested).product_id
        subset = reference.loc[reference.product_id.isin(ids)]
        count = subset.order_id.nunique()
        top_rows.append({"n_requested": requested, "n_actual": len(ids), "row_count": len(subset),
                         "row_share": len(subset)/len(reference), "basket_count": count,
                         "basket_coverage": count/n, "n_rows_total": len(reference),
                         "n_baskets_total": n, "outside_row_count": len(reference)-len(subset),
                         "outside_row_share": 1-len(subset)/len(reference)})
    top = pd.DataFrame(top_rows)
    require(top.basket_coverage.is_monotonic_increasing and top.row_share.is_monotonic_increasing,
            "Top-N không tăng dần")
    tables = {"sample_overview": pd.DataFrame({"metric": overview.keys(), "value": overview.values()}),
              "eda_summary": pd.DataFrame(rows), "categorical_frequencies": pd.DataFrame(frequencies),
              "department_summary": dept,
              "aisle_summary": group_summary(reference, aisles, "aisle_id", "aisle", n),
              "product_popularity": pop, "top_n_coverage": top,
              "department_display": department_display(reference, dept, n)}
    require(np.isclose(tables["department_display"].row_share.sum(), 1), "Top-10 + phần còn lại ≠ 100%")
    return tables, outliers


# main: kiểm hash -> nạp reference và bảng tra -> summarize -> ghi 8 CSV và reference_outliers.json.
def main():
    cfg = config()
    check_hashes()
    data, clean = path(cfg["data_dir"]), path(cfg["clean_dir"])
    reference, baskets = (pd.read_parquet(data/f) for f in ("reference.parquet", "basket_summary.parquet"))
    lookups = (pd.read_csv(p, keep_default_na=False) for p in
               (data/"department_lookup.csv", clean/"aisles.csv", clean/"products.csv"))
    tables, outliers = summarize(reference, baskets, *lookups, cfg)
    output = path(cfg["outputs"]["tables"])
    for name, frame in tables.items():
        write_frame(output/f"{name}.csv", frame)
    write_json(output/"reference_outliers.json", outliers)
    print("EDA SUMMARY:", {k: len(v) for k, v in tables.items()})


if __name__ == "__main__":
    main()
