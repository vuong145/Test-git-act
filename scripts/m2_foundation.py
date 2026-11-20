"""Nền M2 (G0): chia tập theo người dùng, tạo reference và bảng giỏ; không làm EDA.

1. Kiểm tra Master và 6 CSV sạch khớp hồ sơ M1/làm sạch (master_verification.json,
   verification.json).
2. validate_master; make_split (PCG64 seed 42, test=ceil(N/5), validation=floor(N/5),
   reference=floor(phần còn lại/2), fit=phần còn lại); tái lập khi đảo thứ tự ID.
3. Ghi split_manifest.parquet, reference.parquet, basket_summary.parquet,
   department_lookup.csv vào DATA/Data phai sinh/M2/.
4. Ghi BAO CAO/Bao cao EDA/common/hashes.json: SHA-256 các file trên, số đếm, dtype
   thực đọc của reference. Script phía sau gọi project_io.check_hashes() trước khi đọc.

ĐỌC NHANH (vấn đáp):
  Mục đích: chia 131.209 người dùng thành 4 tập (reference 30%, fit 30%, validation 20%, test 20%) và tạo bảng giỏ cho EDA.
  Vì sao chia theo NGƯỜI, không theo dòng? Một người ở hai tập sẽ làm mô hình học lại chính họ (rò rỉ thông tin).
  Vì sao có hashes.json? Mọi script sau phải kiểm hash trước khi đọc: dữ liệu bị sửa là dừng.
  Tái lập: chia lại với danh sách ID đảo ngược phải ra đúng kết quả cũ.
"""
import hashlib

import numpy as np
import pandas as pd

from project_io import (FOUNDATION_HASHES, config, path, read_json, relative, require,
                        sha256, write_frame, write_hashes)

# Sáu CSV sạch phải khớp hash đã ghi lúc làm sạch.
CLEAN = ("aisles", "departments", "products", "orders",
         "order_products__prior", "order_products__train")


# CHIA TẬP: xáo ID người dùng bằng PCG64 seed 42 rồi cắt thành test, reference, fit, validation.
def make_split(users, seed=42):
    values = np.asarray(sorted(users), dtype=np.int64)
    require(len(values) == len(np.unique(values)), "Duplicate user IDs")
    n = len(values)
    require(n >= 5, "At least five users needed")
    # test = làm tròn lên N/5; validation = làm tròn xuống N/5; phần còn lại chia đôi cho reference và fit.
    n_test, n_validation = (n + 4) // 5, n // 5
    remaining = n - n_test - n_validation
    counts = {"test": n_test, "reference": remaining // 2,
              "fit": remaining - remaining // 2, "validation": n_validation}
    shuffled = np.random.Generator(np.random.PCG64(seed)).permutation(values)
    labels = [label for label, count in counts.items() for _ in range(count)]
    return pd.DataFrame({"user_id": shuffled, "split": labels}).sort_values(
        "user_id").reset_index(drop=True)


# Dấu vân tay của bảng chia tập (sắp theo user_id) để chứng minh chia tập không đổi.
def canonical_split_sha256(split):
    text = split.sort_values("user_id").to_csv(index=False, lineterminator="\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# Kiểm tra Master: không thiếu khóa, không trùng cặp, mỗi người đúng một giỏ, chỉ có train, mỗi quầy thuộc một ngành.
def validate_master(frame):
    keys = ["order_id", "product_id", "user_id", "aisle_id", "department_id"]
    require(not frame[keys].isna().any().any(), "Missing identifiers")
    require(all(pd.api.types.is_integer_dtype(frame[k]) for k in keys),
            "Identifiers must have integer dtype")
    require(not frame.duplicated(["order_id", "product_id"]).any(), "Duplicate order/product key")
    pairs = frame[["user_id", "order_id"]].drop_duplicates()
    require(not pairs.user_id.duplicated().any(), "Multiple baskets per user")
    require(not pairs.order_id.duplicated().any(), "Multiple users per order")
    require(frame.eval_set.eq("train").all(), "Master must contain train only")
    require(frame.groupby("aisle_id", observed=True).department_id.nunique().le(1).all(),
            "Aisle maps to multiple departments")
    return pairs


# Gom dòng sản phẩm thành bảng giỏ: kích thước giỏ, số ngành, số quầy, ngày, giờ và khung giờ (hour_band).
def build_baskets(reference, cfg):
    validate_master(reference)
    attributes = ["user_id", "order_dow", "order_hour_of_day", "days_since_prior_order"]
    grouped = reference.groupby("order_id", observed=True, sort=True)
    require(grouped[attributes].nunique(dropna=False).le(1).all().all(),
            "Conflicting order attributes, including missing values")
    baskets = grouped.agg(basket_size=("product_id", "nunique"),
                          n_departments=("department_id", "nunique"),
                          n_aisles=("aisle_id", "nunique")).reset_index()
    attributes_frame = reference[["order_id"] + attributes].drop_duplicates("order_id")
    baskets = baskets.join(attributes_frame.set_index("order_id"),
                           on="order_id", validate="one_to_one")
    for column, low, high in (("order_dow", 0, 6), ("order_hour_of_day", 0, 23),
                              ("days_since_prior_order", 0, 30)):
        require(baskets[column].dropna().between(low, high).all(), f"Invalid domain: {column}")
    baskets["hour_band"] = pd.cut(
        baskets.order_hour_of_day.astype("float64"), bins=cfg["hour_bins"],
        labels=cfg["hour_labels"], right=False, ordered=True)
    require(baskets.basket_size.sum() == len(reference), "Basket row mismatch")
    require((baskets.n_departments.ge(1) & baskets.n_departments.le(baskets.n_aisles) &
             baskets.n_aisles.le(baskets.basket_size)).all(), "Invalid basket counts")
    return baskets.sort_values("order_id").reset_index(drop=True)


# Cổng đầu vào: Master và 6 CSV sạch phải khớp hash của M1 và của bước làm sạch.
def check_sources(cfg):
    """Master và CSV sạch phải khớp hash đã ghi ở M1 và ở bước làm sạch."""
    m1 = read_json(path(cfg["clean_dir"]) / "Bảng master TLCK" / "master_verification.json")
    require(m1["status"] == "PASSED", "M1 chưa đạt")
    require(sha256(path(cfg["master"])) == m1["file_info"]["sha256"], "Master khác hồ sơ M1")
    clean = read_json(path("BAO CAO/Bao cao lam sach/verification.json"))
    require(clean["status"] == "verified", "Làm sạch chưa được xác minh")
    recorded = {r["table"]: r["new_sha256"] for r in clean["comparison_previous"]}
    for name in CLEAN:
        require(sha256(path(cfg["clean_dir"]) / f"{name}.csv") == recorded[name],
                f"CSV khác hồ sơ làm sạch: {name}")


# main: kiểm nguồn -> chia tập -> lấy reference -> dựng bảng giỏ -> ghi 4 tệp -> ghi hashes.json (cổng cho mọi script sau).
def main():
    cfg = config()
    data = path(cfg["data_dir"])
    check_sources(cfg)
    master = pd.read_parquet(path(cfg["master"]))
    pairs = validate_master(master)
    split = make_split(pairs.user_id, cfg["seed"])
    pd.testing.assert_frame_equal(split, make_split(pairs.user_id.iloc[::-1], cfg["seed"]))
    require(set(split.user_id) == set(pairs.user_id), "Split does not cover population")
    users = split.loc[split.split.eq("reference"), "user_id"]
    reference = master.loc[master.user_id.isin(users)].sort_values(
        ["order_id", "product_id"]).reset_index(drop=True)
    require(reference.user_id.nunique() == len(users), "Missing reference users")
    baskets = build_baskets(reference, cfg)
    lookup = pd.read_csv(path(cfg["clean_dir"]) / "departments.csv",
                         keep_default_na=False).sort_values("department_id")
    require(lookup.department_id.tolist() == list(range(1, 22)), "Expected department IDs 1..21")
    require(reference.department_id.isin(lookup.department_id).all(), "Unknown department")
    names = lookup.set_index("department_id").department.to_dict()
    require(names[21] == "missing", "Literal missing must be preserved")
    for pair in read_json(path(cfg["hypotheses_config"]))["pairs"]:
        require(names[pair["a"]] == pair["a_name"] and names[pair["b"]] == pair["b_name"],
                "Hypothesis ID/name mismatch")
    outputs = {"split_manifest.parquet": split, "reference.parquet": reference,
               "basket_summary.parquet": baskets, "department_lookup.csv": lookup}
    for name, frame in outputs.items():
        write_frame(data / name, frame)
        if name.endswith(".parquet"):   # đọc lại để chắc nội dung và dtype không đổi
            pd.testing.assert_frame_equal(frame, pd.read_parquet(data / name))
    counts = {"master_rows": len(master), "users": len(pairs), "reference_rows": len(reference),
              "split_users": {str(k): int(v) for k, v in split.split.value_counts().items()},
              "reference_baskets": len(baskets),
              "reference_users": int(baskets.user_id.nunique()), "departments": len(lookup)}
    write_hashes(FOUNDATION_HASHES,
                 [path(cfg["master"])] + [data / n for n in outputs] + [path(cfg["hypotheses_config"])],
                 counts=counts, canonical_split_sha256=canonical_split_sha256(split),
                 reference_dtypes={k: str(v) for k, v in reference.dtypes.items()},
                 basket_dtypes={k: str(v) for k, v in baskets.dtypes.items()},
                 parquet_reader="pd.read_parquet mặc định, không đổi dtype_backend")
    print(counts, relative(path(FOUNDATION_HASHES)))


if __name__ == "__main__":
    main()
