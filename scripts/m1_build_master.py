"""Tạo bảng Master train (M1): 4 phép ghép trái nhiều–một, kiểm tra và xuất bản Parquet.

Mỗi khối train lần lượt ghép orders, products, aisles, departments bằng
merge(how="left", validate="many_to_one", indicator=True). Dừng nếu có dòng
left_only, đổi số dòng, đổi chuỗi cặp khóa (order_id, product_id) hoặc sinh cột _x/_y.
Trước khi thu hẹp kiểu: kiểm tra miền số nguyên và Float64 -> Float32 không mất giá trị.
Ghi master_train.tmp.parquet, đọc lại bằng dtype_backend="numpy_nullable", chạy 13
tiêu chí rồi mới xuất bản. Đầu ra:
  DATA/Data đã làm sạch/master_train.parquet
  DATA/Data đã làm sạch/Bảng master TLCK/{join_audit,master_schema,master_dictionary}.csv
  DATA/Data đã làm sạch/Bảng master TLCK/master_verification.json

ĐỌC NHANH (vấn đáp):
  Mục đích: tạo bảng Master 1.384.617 dòng x 15 cột để làm bài toán hoàn thiện giỏ (chỉ lấy đơn train: mỗi khách đúng một đơn).
  Năm bước: (1) kiểm tra trước khi thu hẹp kiểu; (2) nạp 4 bảng bên phải; (3) ghép từng khối train với 4 bảng;
  (4) ghi Parquet tạm, đọc lại, chạy 13 tiêu chí; (5) xuất bản nguyên tử và ghi các bảng bằng chứng.
  Vì sao left merge + validate='many_to_one'? Giữ mọi dòng train và chặn việc nhân dòng khi bảng kia trùng khóa.
  Vì sao Parquet và thu hẹp kiểu? RAM giảm 88,16%, tệp nhỏ hơn CSV 7,75 lần (số đo trong m1_benchmark.py).
"""
import hashlib
import json
import sys
import time

from m1_common import atomic_publish, parse_args, report_path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Số kỳ vọng của Master, dùng cho tiêu chí kiểm tra cuối.
ROWS, BASKETS = 1384617, 131209
CATEGORIES = ["eval_set", "product_name", "aisle", "department"]
# Hợp đồng 15 cột: tên, kiểu lưu trữ gọn (int8/int16/int32...) và cột nào được phép thiếu (nullable).
SCHEMA = pa.schema([
    pa.field("order_id", pa.int32(), nullable=False),
    pa.field("product_id", pa.int32(), nullable=False),
    pa.field("add_to_cart_order", pa.int16(), nullable=False),
    pa.field("reordered", pa.int8(), nullable=True),
    pa.field("user_id", pa.int32(), nullable=False),
    pa.field("eval_set", pa.dictionary(pa.int8(), pa.string()), nullable=False),
    pa.field("order_number", pa.int16(), nullable=False),
    pa.field("order_dow", pa.int8(), nullable=True),
    pa.field("order_hour_of_day", pa.int8(), nullable=True),
    pa.field("days_since_prior_order", pa.float32(), nullable=True),
    pa.field("product_name", pa.dictionary(pa.int32(), pa.string()), nullable=True),
    pa.field("aisle_id", pa.int16(), nullable=False),
    pa.field("department_id", pa.int8(), nullable=False),
    pa.field("aisle", pa.dictionary(pa.int16(), pa.string()), nullable=True),
    pa.field("department", pa.dictionary(pa.int8(), pa.string()), nullable=False),
])
COLUMNS = SCHEMA.names
# Kiểu đọc CSV theo từng bảng; cột có thể thiếu dùng kiểu cho phép thiếu (Int8, Float32).
DTYPES = {
    "orders": {"order_id": "int32", "user_id": "int32", "eval_set": "string",
               "order_number": "int16", "order_dow": "Int8", "order_hour_of_day": "Int8",
               "days_since_prior_order": "Float32"},
    "products": {"product_id": "int32", "product_name": "string",
                 "aisle_id": "int16", "department_id": "int8"},
    "aisles": {"aisle_id": "int16", "aisle": "string"},
    "departments": {"department_id": "int8", "department": "string"},
    "order_products__train": {"order_id": "int32", "product_id": "int32",
                              "add_to_cart_order": "int16", "reordered": "Int8"},
}
# 4 phép ghép theo thứ tự: orders (order_id), products (product_id), aisles (aisle_id), departments (department_id).
JOINS = [("1_orders", "orders", "order_id"), ("2_products", "products", "product_id"),
         ("3_aisles", "aisles", "aisle_id"), ("4_departments", "departments", "department_id")]
LIMITS = {"int8": (-128, 127), "Int8": (-128, 127), "int16": (-32768, 32767),
          "int32": (-2147483648, 2147483647)}


def read(clean_dir, table, **kwargs):
    return pd.read_csv(clean_dir / f"{table}.csv", keep_default_na=False, na_values=[""], **kwargs)


# SHA-256 của chuỗi cặp (order_id, product_id): bằng chứng phép ghép không đổi số dòng và thứ tự dòng.
def key_hash(order_id, product_id):
    """SHA-256 của chuỗi cặp khóa theo đúng thứ tự dòng."""
    h = hashlib.sha256()
    for o, p in zip(order_id, product_id):
        h.update(f"{o},{p}\n".encode("utf-8"))
    return h.hexdigest()


# BƯỚC 1: kiểm tra trước khi thu hẹp kiểu: giá trị nằm trong miền kiểu mới, không có số lẻ, Float64 -> Float32 không mất giá trị.
def audit_downcasting(clean_dir):
    """Kiểm tra trước khi thu hẹp kiểu: miền, số lẻ, null và Float64 -> Float32."""
    orders = read(clean_dir, "orders", usecols=list(DTYPES["orders"]))
    s64 = pd.to_numeric(orders["days_since_prior_order"], errors="coerce")
    s32 = s64.astype("Float32")
    valid = s64.notna()
    max_diff = float((s64[valid] - s32[valid].astype("float64")).abs().max())
    same_nulls = bool(s64.isna().equals(s32.isna()))
    result = {"days_since_prior_order": {
        "source_dtype": "float64", "target_dtype": "Float32", "total_rows": len(s64),
        "valid_count": int(valid.sum()), "null_count": int(s64.isna().sum()),
        "min_value": float(s64.min()), "max_value": float(s64.max()),
        "max_abs_diff": max_diff, "null_positions_preserved": same_nulls,
        "is_safe_to_downcast": max_diff == 0.0 and same_nulls}}
    assert result["days_since_prior_order"]["is_safe_to_downcast"], "Float32 làm sai lệch giá trị"
    frames = {"orders": orders, "train": read(clean_dir, "order_products__train"),
              "products": read(clean_dir, "products")}
    checks = [(t, frames[t], col, dt, dt.startswith("Int")) for t, name in
              [("orders", "orders"), ("train", "order_products__train"), ("products", "products")]
              for col, dt in DTYPES[name].items() if dt in LIMITS]
    for table, frame, column, target, nullable in checks:
        s = pd.to_numeric(frame[column], errors="coerce")
        values, nulls = s.dropna(), int(s.isna().sum())
        assert nullable or nulls == 0, f"[{table}.{column}] có {nulls} null nhưng {target} không cho phép"
        odd = int(((values % 1) != 0).sum())
        assert odd == 0, f"[{table}.{column}] có {odd} giá trị lẻ thập phân"
        low, high = LIMITS[target]
        c_min, c_max = float(values.min()), float(values.max())
        assert low <= c_min and c_max <= high, f"[{table}.{column}] tràn miền {target}"
        result[f"{table}.{column}"] = {"target_dtype": target, "min_val": c_min,
                                       "max_val": c_max, "null_count": nulls,
                                       "non_integer_count": odd, "fits_domain": True}
    return result


# BƯỚC 2: nạp 4 bảng bên phải (orders chỉ giữ các đơn có trong train); khóa không được thiếu hoặc trùng.
def load_right_tables(clean_dir, train_orders):
    chunks = read(clean_dir, "orders", dtype=DTYPES["orders"], chunksize=250000)
    orders = pd.concat([m for c in chunks if not (m := c[c["order_id"].isin(train_orders)]).empty],
                       ignore_index=True)
    tables = {"orders": orders}
    for name in ["products", "aisles", "departments"]:
        tables[name] = read(clean_dir, name, dtype=DTYPES[name])
    for name, key in [(n, k) for _, n, k in JOINS]:
        assert tables[name][key].notna().all(), f"{name}.{key} có null"
        assert not tables[name][key].duplicated().any(), f"{name}.{key} bị trùng"
    return tables


# BƯỚC 3-5: ghép từng khối, ghi Parquet tạm, đọc lại, chạy 13 tiêu chí, rồi mới xuất bản.
def build(clean_dir, output_dir, chunksize):
    output_dir.mkdir(parents=True, exist_ok=True)
    tmp, final = clean_dir / "master_train.tmp.parquet", clean_dir / "master_train.parquet"
    pre_audit = audit_downcasting(clean_dir)
    inputs = {}
    for name in ["order_products__train", "orders", "products", "aisles", "departments"]:
        path = clean_dir / f"{name}.csv"
        with open(path, "rb") as f:
            inputs[path.name] = {"path": report_path(path), "size_bytes": path.stat().st_size,
                                 "sha256": hashlib.file_digest(f, "sha256").hexdigest()}
    ids = read(clean_dir, "order_products__train", usecols=["order_id", "product_id"])
    expected_rows, input_hash = len(ids), key_hash(ids["order_id"], ids["product_id"])
    right = load_right_tables(clean_dir, set(ids["order_id"].unique()))
    del ids
    tmp.unlink(missing_ok=True)
    audit, written, raw_dtypes = [], [], {}
    # Mỗi khối train: ghép lần lượt 4 bảng; dừng ngay nếu có dòng không khớp, đổi số dòng, lệch thứ tự khóa hoặc sinh cột _x/_y.
    with pq.ParquetWriter(str(tmp), schema=SCHEMA, compression="snappy") as writer:
        for number, frame in enumerate(read(clean_dir, "order_products__train",
                                            dtype=DTYPES["order_products__train"],
                                            chunksize=chunksize), start=1):
            chunk_hash = key_hash(frame["order_id"], frame["product_id"])
            for step, table, key in JOINS:
                merged = frame.merge(right[table], on=key, how="left", validate="many_to_one",
                                     indicator=True, sort=False)
                unmatched = int((merged["_merge"] == "left_only").sum())
                same = key_hash(merged["order_id"], merged["product_id"]) == chunk_hash
                assert unmatched == 0, f"Khối {number}, {step}: {unmatched} dòng không khớp"
                assert len(merged) == len(frame), f"Khối {number}, {step}: đổi số dòng"
                assert same, f"Khối {number}, {step}: lệch chuỗi cặp khóa"
                assert not any(c.endswith(("_x", "_y")) for c in merged.columns), "Cột _x/_y"
                audit.append({"chunk_id": number, "step": step, "right_table": table,
                              "join_key": key, "rows_before": len(frame),
                              "rows_after": len(merged), "unmatched_rows": unmatched,
                              "key_sequence_preserved": same})
                frame = merged.drop(columns=["_merge"])
            assert set(frame.columns) == set(COLUMNS), f"Khối {number}: sai tập cột"
            frame = frame[COLUMNS]
            if number == 1:
                raw_dtypes = {c: str(frame[c].dtype) for c in COLUMNS}
            for column in CATEGORIES:
                frame[column] = frame[column].astype("category")
            written.append(frame.copy())
            writer.write_table(pa.Table.from_pandas(frame, schema=SCHEMA, preserve_index=False))
            print(f" - Khối {number}: {sum(map(len, written)):,}/{expected_rows:,} dòng")

    # Đọc lại tệp tạm bằng kiểu numpy_nullable rồi đối chiếu với bản trước khi ghi.
    before = pd.concat(written, ignore_index=True)
    del written
    after = pd.read_parquet(tmp, dtype_backend="numpy_nullable")
    per_user = after.groupby("user_id")["order_id"].nunique()
    # 13 tiêu chí: đủ số dòng/cột, đủ 131.209 giỏ và khách, mỗi khách một đơn train, không trùng/thiếu khóa, nội dung không đổi.
    checks = {
        "row_count_exact_1384617": len(after) == ROWS,
        "column_count_exact_15": after.shape[1] == 15,
        "columns_match_contract": list(after.columns) == COLUMNS,
        "distinct_orders_131209": int(after["order_id"].nunique()) == BASKETS,
        "distinct_users_131209": int(after["user_id"].nunique()) == BASKETS,
        "one_train_order_per_user": bool((per_user == 1).all()),
        "missing_keys_count_zero": not after[["order_id", "product_id", "user_id"]].isna().any().any(),
        "duplicate_key_pairs_zero": not after.duplicated(subset=["order_id", "product_id"]).any(),
        "eval_set_all_train": set(after["eval_set"].dropna().unique()) == {"train"}
                              and after["eval_set"].isna().sum() == 0,
        "key_pairs_and_sequence_preserved": key_hash(after["order_id"], after["product_id"]) == input_hash,
    }
    # So từng cột: vị trí thiếu và giá trị trước/sau khi ghi phải giống hệt.
    columns = {}
    for col in COLUMNS:
        b, a = before[col], after[col]
        mask_b, mask_a = b.isna(), a.isna()
        same_mask = bool(mask_b.equals(mask_a))
        vb, va = b.loc[~mask_b], a.loc[~mask_a]
        if col in CATEGORIES:
            vb, va = vb.astype(str), va.astype(str)
        same_values = bool(np.array_equal(vb.to_numpy(), va.to_numpy()))
        assert same_mask and same_values, f"Cột {col}: giá trị hoặc vị trí thiếu thay đổi"
        columns[col] = {"column": col, "raw_merged_dtype": raw_dtypes.get(col, "unknown"),
                        "dtype_before_write": str(b.dtype), "dtype_after_read": str(a.dtype),
                        "pyarrow_storage_type": str(SCHEMA.field(col).type),
                        "missing_before": int(mask_b.sum()), "missing_after": int(mask_a.sum()),
                        "missing_mask_preserved": same_mask, "values_preserved": same_values}
    checks["content_preserved_before_after"] = all(c["values_preserved"] for c in columns.values())
    checks["missing_positions_preserved_before_after"] = all(
        c["missing_mask_preserved"] for c in columns.values())
    bad_labels = {"Unknown", "unknown", "nan", "<NA>", "None"}
    checks["category_labels_and_nulls_valid"] = not any(
        bad_labels & set(after[c].cat.categories) for c in CATEGORIES)
    checks = {k: bool(v) for k, v in checks.items()}
    failed = [k for k, v in checks.items() if not v]
    assert not failed, f"Kiểm tra cuối không đạt: {failed}"

    atomic_publish(tmp, final)   # chỉ xuất bản sau khi 13 tiêu chí đều đạt
    tmp.unlink()
    with open(final, "rb") as f:
        final_sha = hashlib.file_digest(f, "sha256").hexdigest()
    # Xuất các bảng bằng chứng: join_audit.csv, master_schema.csv, master_dictionary.csv, master_verification.json.
    audit = pd.DataFrame(audit)
    totals = [{"chunk_id": "TOTAL_SUMMARY", "step": step, "right_table": table, "join_key": key,
               **{c: int(audit.loc[audit.step == step, c].sum())
                  for c in ["rows_before", "rows_after", "unmatched_rows"]},
               "key_sequence_preserved": bool(audit.loc[audit.step == step,
                                                        "key_sequence_preserved"].all())}
              for step, table, key in JOINS]
    pd.concat([audit, pd.DataFrame(totals)], ignore_index=True).to_csv(
        output_dir / "join_audit.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame([{k: v for k, v in c.items()} for c in columns.values()]).to_csv(
        output_dir / "master_schema.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame([{"column_name": c, "pandas_dtype_read": v["dtype_after_read"],
                   "pyarrow_type": v["pyarrow_storage_type"], "missing_count": v["missing_after"],
                   "missing_pct": round(v["missing_after"] / ROWS * 100, 2)}
                  for c, v in columns.items()]).to_csv(
        output_dir / "master_dictionary.csv", index=False, encoding="utf-8-sig")
    size = final.stat().st_size
    report = {
        "status": "PASSED", "path_base": "thesis directory (parent of scripts/)",
        "inputs": inputs, "pre_downcasting_audit": pre_audit,
        "master_size": {"rows": len(after), "columns": len(after.columns),
                        "distinct_orders": BASKETS, "distinct_users": BASKETS,
                        "train_orders_per_user": 1},
        "checks": checks, "column_verifications": columns,
        "file_info": {"primary_file": report_path(final), "size_bytes": size,
                      "size_mb": round(size / (1024 * 1024), 2),
                      "compression": "snappy", "sha256": final_sha},
        "environment": {"python": sys.version.split()[0], "pandas": pd.__version__,
                        "pyarrow": pa.__version__, "numpy": np.__version__},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    with open(output_dir / "master_verification.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"MASTER PASSED: {len(after):,} dòng; {final}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    args = parse_args("Build and verify the PRJ-08 Master table")
    build(args.clean_dir, args.output_dir, args.chunksize)
