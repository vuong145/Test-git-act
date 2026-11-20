"""
Build Master Table and Detailed 4-Step Join Audit for PRJ-08 (Milestone M1).
Executes 4 sequential left joins with validate='many_to_one', indicator=True, sort=False.
Verifies:
  - Pre-downcasting domain validation (integer boundaries, non-integer check, Float64 vs Float32 zero-loss)
  - No left_only rows (_merge must be 100% 'both')
  - Row counts preserved
  - Key sequence (order_id, product_id) exactly preserved
  - No unexpected duplicate columns (_x, _y)
  - Actual element-wise content and null mask verification between pre-write and post-read
Outputs:
  - Data đã làm sạch/Bảng master TLCK/master_train.parquet
  - Data đã làm sạch/Bảng master TLCK/join_audit.csv
  - Data đã làm sạch/Bảng master TLCK/master_schema.csv
  - Data đã làm sạch/Bảng master TLCK/master_dictionary.csv
  - Data đã làm sạch/master_verification.json
"""
import sys
import gc
import json
import time
import hashlib
from pathlib import Path
from m1_common import atomic_publish, parse_args, report_path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if __name__ == "__main__":
    cli_args = parse_args("Build and verify the PRJ-08 Master table")

import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

MASTER_COLUMNS = [
    "order_id",
    "product_id",
    "add_to_cart_order",
    "reordered",
    "user_id",
    "eval_set",
    "order_number",
    "order_dow",
    "order_hour_of_day",
    "days_since_prior_order",
    "product_name",
    "aisle_id",
    "department_id",
    "aisle",
    "department",
]

PYARROW_SCHEMA = pa.schema([
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


def audit_and_validate_downcasting(clean_dir: Path):
    """
    Kiểm tra thực tế các tiền điều kiện thu hẹp kiểu dữ liệu:
    1. Kiểm tra days_since_prior_order: Float64 vs Float32 (chênh lệch max, mất mát độ chính xác).
    2. Kiểm tra miền giá trị min/max số nguyên so với giới hạn kiểu đích.
    3. Kiểm tra số lẻ thập phân (non-integer check) trên các cột số nguyên.
    4. Kiểm tra sự tồn tại của giá trị thiếu (nullability).
    """
    print("\n--- KIỂM TRA TIỀN ĐIỀU KIỆN THU HẸP KIỂU (PRE-DOWNCASTING AUDIT) ---")
    audit_results = {}

    # 1. Kiểm tra days_since_prior_order trong orders.csv
    df_orders_raw = pd.read_csv(
        clean_dir / "orders.csv",
        usecols=["order_id", "user_id", "order_number", "order_dow", "order_hour_of_day", "days_since_prior_order"],
        keep_default_na=False,
        na_values=[""]
    )
    s_f64 = pd.to_numeric(df_orders_raw["days_since_prior_order"], errors="coerce")
    s_f32 = s_f64.astype("Float32")
    
    valid_mask = s_f64.notna()
    diff = (s_f64[valid_mask] - s_f32[valid_mask].astype("float64")).abs()
    max_abs_diff = float(diff.max())
    null_mask_match = bool(s_f64.isna().equals(s_f32.isna()))
    
    audit_results["days_since_prior_order"] = {
        "source_dtype": "float64",
        "target_dtype": "Float32",
        "total_rows": len(s_f64),
        "valid_count": int(valid_mask.sum()),
        "null_count": int(s_f64.isna().sum()),
        "min_value": float(s_f64.min()),
        "max_value": float(s_f64.max()),
        "max_abs_diff": max_abs_diff,
        "null_positions_preserved": null_mask_match,
        "is_safe_to_downcast": (max_abs_diff == 0.0 and null_mask_match)
    }
    assert audit_results["days_since_prior_order"]["is_safe_to_downcast"], (
        f"Lỗi: Chuyển Float32 cho days_since_prior_order làm sai lệch giá trị! max_diff={max_abs_diff}"
    )
    print(f" [OK] days_since_prior_order: Min={audit_results['days_since_prior_order']['min_value']}, "
          f"Max={audit_results['days_since_prior_order']['max_value']}, Max Abs Diff={max_abs_diff} "
          f"-> Chuyển Float32 an toàn 100% không mất độ chính xác.")

    # 2. Kiểm tra miền giá trị các cột số nguyên trong orders
    int_checks = [
        ("orders", df_orders_raw["order_id"], "int32", -2147483648, 2147483647, False),
        ("orders", df_orders_raw["user_id"], "int32", -2147483648, 2147483647, False),
        ("orders", df_orders_raw["order_number"], "int16", -32768, 32767, False),
        ("orders", pd.to_numeric(df_orders_raw["order_dow"], errors="coerce"), "Int8", -128, 127, True),
        ("orders", pd.to_numeric(df_orders_raw["order_hour_of_day"], errors="coerce"), "Int8", -128, 127, True),
    ]

    # Kiểm tra train
    df_train_raw = pd.read_csv(
        clean_dir / "order_products__train.csv",
        keep_default_na=False,
        na_values=[""]
    )
    int_checks.extend([
        ("train", pd.to_numeric(df_train_raw["order_id"], errors="coerce"), "int32", -2147483648, 2147483647, False),
        ("train", pd.to_numeric(df_train_raw["product_id"], errors="coerce"), "int32", -2147483648, 2147483647, False),
        ("train", pd.to_numeric(df_train_raw["add_to_cart_order"], errors="coerce"), "int16", -32768, 32767, False),
        ("train", pd.to_numeric(df_train_raw["reordered"], errors="coerce"), "Int8", -128, 127, True),
    ])

    # Kiểm tra products
    df_prod_raw = pd.read_csv(clean_dir / "products.csv", keep_default_na=False, na_values=[""])
    int_checks.extend([
        ("products", pd.to_numeric(df_prod_raw["product_id"], errors="coerce"), "int32", -2147483648, 2147483647, False),
        ("products", pd.to_numeric(df_prod_raw["aisle_id"], errors="coerce"), "int16", -32768, 32767, False),
        ("products", pd.to_numeric(df_prod_raw["department_id"], errors="coerce"), "int8", -128, 127, False),
    ])

    for tbl, s, target_type, min_limit, max_limit, allows_null in int_checks:
        col_name = s.name
        val_mask = s.notna()
        null_count = int((~val_mask).sum())
        if not allows_null:
            assert null_count == 0, f"[{tbl}.{col_name}] chứa {null_count} null nhưng target_type {target_type} không cho phép null!"
        
        valid_vals = s[val_mask]
        # Kiểm tra không có số lẻ
        non_integers = int(((valid_vals % 1) != 0).sum())
        assert non_integers == 0, f"[{tbl}.{col_name}] chứa {non_integers} giá trị có phần thập phân lẻ!"
        
        c_min = float(valid_vals.min())
        c_max = float(valid_vals.max())
        assert c_min >= min_limit and c_max <= max_limit, (
            f"[{tbl}.{col_name}] Miền giá trị [{c_min}, {c_max}] tràn ngoài giới hạn [{min_limit}, {max_limit}] của {target_type}!"
        )
        audit_results[f"{tbl}.{col_name}"] = {
            "target_dtype": target_type,
            "min_val": c_min,
            "max_val": c_max,
            "null_count": null_count,
            "non_integer_count": non_integers,
            "fits_domain": True
        }
        print(f" [OK] {tbl}.{col_name}: Min={c_min}, Max={c_max}, Nulls={null_count}, Số lẻ={non_integers} -> Ép sang {target_type} an toàn.")

    del df_orders_raw, df_train_raw, df_prod_raw
    gc.collect()
    return audit_results


def load_lookup_tables(clean_dir: Path, train_order_ids: set):
    print("\n1. Nạp và kiểm tra tính hợp lệ của các bảng bên phải (Right tables)...")
    
    # 1. Bảng orders (lọc các đơn thuộc train để tối ưu RAM)
    orders_chunks = []
    for chunk in pd.read_csv(
        clean_dir / "orders.csv",
        dtype={
            "order_id": "int32",
            "user_id": "int32",
            "eval_set": "string",
            "order_number": "int16",
            "order_dow": "Int8",
            "order_hour_of_day": "Int8",
            "days_since_prior_order": "Float32"
        },
        chunksize=250000,
        keep_default_na=False,
        na_values=[""]
    ):
        matched = chunk[chunk["order_id"].isin(train_order_ids)]
        if not matched.empty:
            orders_chunks.append(matched)
            
    df_orders = pd.concat(orders_chunks, ignore_index=True)
    assert df_orders["order_id"].notna().all(), "orders.order_id có giá trị null!"
    assert not df_orders["order_id"].duplicated().any(), "orders.order_id bị trùng lặp!"
    print(f" - [orders] chuẩn bị xong: {len(df_orders):,} đơn hàng (khóa duy nhất, 0 null)")
    
    # 2. Bảng products
    df_products = pd.read_csv(
        clean_dir / "products.csv",
        dtype={
            "product_id": "int32",
            "product_name": "string",
            "aisle_id": "int16",
            "department_id": "int8"
        },
        keep_default_na=False,
        na_values=[""]
    )
    assert df_products["product_id"].notna().all(), "products.product_id có giá trị null!"
    assert not df_products["product_id"].duplicated().any(), "products.product_id bị trùng lặp!"
    print(f" - [products] chuẩn bị xong: {len(df_products):,} sản phẩm (khóa duy nhất, 0 null)")
    
    # 3. Bảng aisles
    df_aisles = pd.read_csv(
        clean_dir / "aisles.csv",
        dtype={"aisle_id": "int16", "aisle": "string"},
        keep_default_na=False,
        na_values=[""]
    )
    assert df_aisles["aisle_id"].notna().all(), "aisles.aisle_id có giá trị null!"
    assert not df_aisles["aisle_id"].duplicated().any(), "aisles.aisle_id bị trùng lặp!"
    print(f" - [aisles] chuẩn bị xong: {len(df_aisles):,} quầy kệ (khóa duy nhất, 0 null)")
    
    # 4. Bảng departments
    df_departments = pd.read_csv(
        clean_dir / "departments.csv",
        dtype={"department_id": "int8", "department": "string"},
        keep_default_na=False,
        na_values=[""]
    )
    assert df_departments["department_id"].notna().all(), "departments.department_id có giá trị null!"
    assert not df_departments["department_id"].duplicated().any(), "departments.department_id bị trùng lặp!"
    print(f" - [departments] chuẩn bị xong: {len(df_departments):,} ngành hàng (khóa duy nhất, 0 null)")
    
    return df_orders, df_products, df_aisles, df_departments


def hash_key_pairs(series_order_id, series_product_id):
    """Tính mã băm SHA-256 trên chuỗi cặp khóa để kiểm chứng thứ tự tuyệt đối."""
    h = hashlib.sha256()
    for o, p in zip(series_order_id, series_product_id):
        h.update(f"{o},{p}\n".encode("utf-8"))
    return h.hexdigest()


def execute_master_pipeline(clean_dir: Path, output_dir: Path, chunksize: int = 250000):
    output_dir.mkdir(parents=True, exist_ok=True)
    start_time = time.perf_counter()
    train_csv = clean_dir / "order_products__train.csv"
    tmp_parquet = clean_dir / "master_train.tmp.parquet"
    final_parquet_clean = clean_dir / "master_train.parquet"
    final_parquet_tlck = output_dir / "master_train.parquet"
    audit_csv = output_dir / "join_audit.csv"
    dict_csv = output_dir / "master_dictionary.csv"
    schema_csv = output_dir / "master_schema.csv"
    verif_json_clean = clean_dir / "master_verification.json"
    verif_json_tlck = output_dir / "master_verification.json"
    
    # 0. Thực hiện kiểm tra tiền điều kiện thu hẹp kiểu
    pre_audit_info = audit_and_validate_downcasting(clean_dir)
    
    # Tính chữ ký và thu thập siêu dữ liệu của 5 CSV đầu vào
    print("\n0. Tính mã băm SHA-256 của 5 tệp CSV sạch đầu vào...")
    input_files_info = {}
    for fname in ["order_products__train.csv", "orders.csv", "products.csv", "aisles.csv", "departments.csv"]:
        fpath = clean_dir / fname
        with open(fpath, "rb") as f:
            fhash = hashlib.file_digest(f, "sha256").hexdigest()
        input_files_info[fname] = {
            "path": report_path(fpath),
            "sha256": fhash,
            "size_bytes": fpath.stat().st_size
        }
        print(f" - [{fname}] SHA-256: {fhash[:16]}... ({fpath.stat().st_size:,} bytes)")
    
    # Quét trước tập order_id của train và tính chuỗi mã băm đầu vào
    print("\n1. Quét trước tập order_id của train và tính chữ ký cặp khóa ban đầu...")
    df_train_ids = pd.read_csv(train_csv, usecols=["order_id", "product_id"], keep_default_na=False, na_values=[""])
    train_order_ids = set(df_train_ids["order_id"].unique())
    total_expected_rows = len(df_train_ids)
    initial_full_input_hash = hash_key_pairs(df_train_ids["order_id"], df_train_ids["product_id"])
    del df_train_ids
    gc.collect()
    print(f" - Xác nhận: {total_expected_rows:,} dòng, {len(train_order_ids):,} đơn hàng. Hash ban đầu: {initial_full_input_hash}")
    
    # Nạp và kiểm tra 4 bảng bên phải
    df_orders, df_products, df_aisles, df_departments = load_lookup_tables(clean_dir, train_order_ids)
    
    print("\n2. Thực hiện tuần tự 4 phép ghép và ghi vào tệp tạm (master_train.tmp.parquet)...")
    if tmp_parquet.exists():
        tmp_parquet.unlink()
        
    processed_rows = 0
    all_chunks_audit = []
    chunks_before = []  # Lưu giữ DataFrame trước khi ghi để đối chiếu thực tế từng ô
    
    chunk_idx = 0
    raw_merged_dtypes = {}
    
    with pq.ParquetWriter(
        str(tmp_parquet), schema=PYARROW_SCHEMA, compression="snappy"
    ) as writer:
        for chunk in pd.read_csv(
            train_csv,
            dtype={
                "order_id": "int32",
                "product_id": "int32",
                "add_to_cart_order": "int16",
                "reordered": "Int8"
            },
            chunksize=chunksize,
            keep_default_na=False,
            na_values=[""]
        ):
            chunk_idx += 1
            current_df = chunk.copy()
            initial_chunk_hash = hash_key_pairs(current_df["order_id"], current_df["product_id"])
        
            # LƯỢT 1: Ghép orders (on='order_id')
            rows_before = len(current_df)
            merged_1 = current_df.merge(df_orders, on="order_id", how="left", validate="many_to_one", indicator=True, sort=False)
            unmatched_1 = int((merged_1["_merge"] == "left_only").sum())
            assert unmatched_1 == 0, f"Chunk {chunk_idx} - Lượt 1: Có {unmatched_1} dòng không khớp orders!"
            assert len(merged_1) == rows_before, f"Chunk {chunk_idx} - Lượt 1: Biến đổi số dòng!"
            hash_1 = hash_key_pairs(merged_1["order_id"], merged_1["product_id"])
            assert hash_1 == initial_chunk_hash, f"Chunk {chunk_idx} - Lượt 1: Lệch chuỗi cặp khóa!"
            assert not any(c.endswith("_x") or c.endswith("_y") for c in merged_1.columns), "Xuất hiện cột _x, _y!"
            all_chunks_audit.append({
                "chunk_id": chunk_idx, "step": "1_orders", "right_table": "orders", "join_key": "order_id",
                "rows_before": rows_before, "rows_after": len(merged_1), "unmatched_rows": unmatched_1,
                "key_sequence_preserved": (hash_1 == initial_chunk_hash)
            })
            current_df = merged_1.drop(columns=["_merge"])
        
            # LƯỢT 2: Ghép products (on='product_id')
            rows_before = len(current_df)
            merged_2 = current_df.merge(df_products, on="product_id", how="left", validate="many_to_one", indicator=True, sort=False)
            unmatched_2 = int((merged_2["_merge"] == "left_only").sum())
            assert unmatched_2 == 0, f"Chunk {chunk_idx} - Lượt 2: Có {unmatched_2} dòng không khớp products!"
            assert len(merged_2) == rows_before, f"Chunk {chunk_idx} - Lượt 2: Biến đổi số dòng!"
            hash_2 = hash_key_pairs(merged_2["order_id"], merged_2["product_id"])
            assert hash_2 == initial_chunk_hash, f"Chunk {chunk_idx} - Lượt 2: Lệch chuỗi cặp khóa!"
            assert not any(c.endswith("_x") or c.endswith("_y") for c in merged_2.columns), "Xuất hiện cột _x, _y!"
            all_chunks_audit.append({
                "chunk_id": chunk_idx, "step": "2_products", "right_table": "products", "join_key": "product_id",
                "rows_before": rows_before, "rows_after": len(merged_2), "unmatched_rows": unmatched_2,
                "key_sequence_preserved": (hash_2 == initial_chunk_hash)
            })
            current_df = merged_2.drop(columns=["_merge"])
        
            # LƯỢT 3: Ghép aisles (on='aisle_id')
            rows_before = len(current_df)
            merged_3 = current_df.merge(df_aisles, on="aisle_id", how="left", validate="many_to_one", indicator=True, sort=False)
            unmatched_3 = int((merged_3["_merge"] == "left_only").sum())
            assert unmatched_3 == 0, f"Chunk {chunk_idx} - Lượt 3: Có {unmatched_3} dòng không khớp aisles!"
            assert len(merged_3) == rows_before, f"Chunk {chunk_idx} - Lượt 3: Biến đổi số dòng!"
            hash_3 = hash_key_pairs(merged_3["order_id"], merged_3["product_id"])
            assert hash_3 == initial_chunk_hash, f"Chunk {chunk_idx} - Lượt 3: Lệch chuỗi cặp khóa!"
            assert not any(c.endswith("_x") or c.endswith("_y") for c in merged_3.columns), "Xuất hiện cột _x, _y!"
            all_chunks_audit.append({
                "chunk_id": chunk_idx, "step": "3_aisles", "right_table": "aisles", "join_key": "aisle_id",
                "rows_before": rows_before, "rows_after": len(merged_3), "unmatched_rows": unmatched_3,
                "key_sequence_preserved": (hash_3 == initial_chunk_hash)
            })
            current_df = merged_3.drop(columns=["_merge"])
        
            # LƯỢT 4: Ghép departments (on='department_id')
            rows_before = len(current_df)
            merged_4 = current_df.merge(df_departments, on="department_id", how="left", validate="many_to_one", indicator=True, sort=False)
            unmatched_4 = int((merged_4["_merge"] == "left_only").sum())
            assert unmatched_4 == 0, f"Chunk {chunk_idx} - Lượt 4: Có {unmatched_4} dòng không khớp departments!"
            assert len(merged_4) == rows_before, f"Chunk {chunk_idx} - Lượt 4: Biến đổi số dòng!"
            hash_4 = hash_key_pairs(merged_4["order_id"], merged_4["product_id"])
            assert hash_4 == initial_chunk_hash, f"Chunk {chunk_idx} - Lượt 4: Lệch chuỗi cặp khóa!"
            assert not any(c.endswith("_x") or c.endswith("_y") for c in merged_4.columns), "Xuất hiện cột _x, _y!"
            all_chunks_audit.append({
                "chunk_id": chunk_idx, "step": "4_departments", "right_table": "departments", "join_key": "department_id",
                "rows_before": rows_before, "rows_after": len(merged_4), "unmatched_rows": unmatched_4,
                "key_sequence_preserved": (hash_4 == initial_chunk_hash)
            })
            current_df = merged_4.drop(columns=["_merge"])
        
            # Sắp xếp đúng 15 cột chuẩn hợp đồng
            assert set(current_df.columns) == set(MASTER_COLUMNS), f"Chunk {chunk_idx}: Sai tập cột Master!"
            current_df = current_df[MASTER_COLUMNS]
        
            if chunk_idx == 1:
                for c in MASTER_COLUMNS:
                    raw_merged_dtypes[c] = str(current_df[c].dtype)
        
            # Ép kiểu an toàn sang category cho các biến phân loại
            current_df["eval_set"] = current_df["eval_set"].astype("category")
            current_df["product_name"] = current_df["product_name"].astype("category")
            current_df["aisle"] = current_df["aisle"].astype("category")
            current_df["department"] = current_df["department"].astype("category")
        
            # Lưu bản trước ghi vào bộ nhớ để đối chiếu thực tế sau khi đọc lại
            chunks_before.append(current_df.copy())
        
            # Ghi trực tiếp ra Parquet Writer (tệp tạm)
            table = pa.Table.from_pandas(current_df, schema=PYARROW_SCHEMA, preserve_index=False)
            writer.write_table(table)
        
            processed_rows += len(current_df)
            print(f" - Chunk {chunk_idx} đã ghi vào tệp tạm: {len(current_df):,} dòng (Tích lũy: {processed_rows:,} / {total_expected_rows:,})")
        
    # Đóng hoàn toàn bộ ghi Parquet
    elapsed_write = time.perf_counter() - start_time
    print(f"\n3. Đã đóng hoàn toàn bộ ghi tệp tạm trong {elapsed_write:.2f} giây.")
    
    # Hợp nhất toàn bộ các chunk trước ghi thành DataFrame đối chiếu hoàn chỉnh
    print(" - Hợp nhất bản ghi trước Parquet (df_before) để phục vụ đối chiếu chi tiết...")
    df_before = pd.concat(chunks_before, ignore_index=True)
    del chunks_before
    gc.collect()
    
    # 4. Đọc lại tệp tạm và tiến hành bộ kiểm tra cuối bắt buộc
    print("\n4. Đọc lại tệp tạm và thực thi 13 hạng mục kiểm tra cuối bắt buộc...")
    df_read = pd.read_parquet(tmp_parquet, dtype_backend="numpy_nullable")
    
    check_results = {}
    
    # 1. Số dòng == 1.384.617
    check_results["row_count_exact_1384617"] = bool(len(df_read) == 1384617)
    assert check_results["row_count_exact_1384617"], f"Số dòng {len(df_read)} != 1.384.617"
    
    # 2. Số cột == 15
    check_results["column_count_exact_15"] = bool(df_read.shape[1] == 15)
    assert check_results["column_count_exact_15"], f"Số cột {df_read.shape[1]} != 15"
    
    # 3. Tên/thứ tự cột khớp hợp đồng
    check_results["columns_match_contract"] = bool(list(df_read.columns) == MASTER_COLUMNS)
    assert check_results["columns_match_contract"], "Tên/thứ tự cột không khớp hợp đồng!"
    
    # 4. Số đơn khác nhau == 131.209
    distinct_orders = int(df_read["order_id"].nunique())
    check_results["distinct_orders_131209"] = bool(distinct_orders == 131209)
    assert check_results["distinct_orders_131209"], f"Số đơn {distinct_orders} != 131.209"
    
    # 5. Số user khác nhau == 131.209
    distinct_users = int(df_read["user_id"].nunique())
    check_results["distinct_users_131209"] = bool(distinct_users == 131209)
    assert check_results["distinct_users_131209"], f"Số user {distinct_users} != 131.209"
    
    # 6. Đơn train mỗi user == Đúng 1
    orders_per_user = df_read.groupby("user_id")["order_id"].nunique()
    check_results["one_train_order_per_user"] = bool((orders_per_user == 1).all())
    assert check_results["one_train_order_per_user"], "Có user không có đúng 1 đơn train!"
    
    # 7. Khóa bị thiếu == 0
    missing_order_id = int(df_read["order_id"].isna().sum())
    missing_product_id = int(df_read["product_id"].isna().sum())
    missing_user_id = int(df_read["user_id"].isna().sum())
    check_results["missing_keys_count_zero"] = bool(missing_order_id == 0 and missing_product_id == 0 and missing_user_id == 0)
    assert check_results["missing_keys_count_zero"], "Tồn tại giá trị null trong các cột khóa!"
    
    # 8. Cặp (order_id, product_id) trùng == 0
    dup_pairs = int(df_read.duplicated(subset=["order_id", "product_id"]).sum())
    check_results["duplicate_key_pairs_zero"] = bool(dup_pairs == 0)
    assert check_results["duplicate_key_pairs_zero"], f"Có {dup_pairs} cặp khóa bị trùng lặp!"
    
    # 9. Nhãn eval_set: tất cả là 'train'
    eval_set_vals = set(df_read["eval_set"].dropna().unique())
    check_results["eval_set_all_train"] = bool(eval_set_vals == {"train"} and df_read["eval_set"].isna().sum() == 0)
    assert check_results["eval_set_all_train"], f"Nhãn eval_set chứa giá trị ngoài 'train': {eval_set_vals}"
    
    # 10. Cặp khóa và thứ tự dòng giống đầu vào train
    re_read_key_hash = hash_key_pairs(df_read["order_id"], df_read["product_id"])
    check_results["key_pairs_and_sequence_preserved"] = bool(re_read_key_hash == initial_full_input_hash)
    assert check_results["key_pairs_and_sequence_preserved"], "Chuỗi cặp khóa và thứ tự dòng sau đọc khác ban đầu!"
    
    # 11 & 12. THỰC HIỆN ĐỐI CHIẾU THỰC TẾ GIÁ TRỊ VÀ VỊ TRÍ THIẾU TỪNG CỘT
    print(" - Tiến hành đối chiếu thực tế từng cột giữa trước ghi và sau đọc...")
    column_verifications = {}
    for col in MASTER_COLUMNS:
        s_before = df_before[col]
        s_after = df_read[col]
        
        mask_before = s_before.isna()
        mask_after = s_after.isna()
        missing_mask_match = bool(mask_before.equals(mask_after))
        assert missing_mask_match, f"Cột {col}: Vị trí thiếu không khớp giữa df_before và df_read!"
        
        n_missing_before = int(mask_before.sum())
        n_missing_after = int(mask_after.sum())
        assert n_missing_before == n_missing_after, f"Cột {col}: Số lượng thiếu bị lệch ({n_missing_before} vs {n_missing_after})!"
        
        # So sánh giá trị trên các dòng không null
        if col in ["eval_set", "product_name", "aisle", "department"]:
            v_before = s_before.loc[~mask_before].astype(str).to_numpy()
            v_after = s_after.loc[~mask_after].astype(str).to_numpy()
            val_match = bool(np.array_equal(v_before, v_after))
        elif col == "days_since_prior_order":
            v_before = s_before.loc[~mask_before].to_numpy()
            v_after = s_after.loc[~mask_after].to_numpy()
            val_match = bool(np.array_equal(v_before, v_after))
        else:
            v_before = s_before.loc[~mask_before].to_numpy()
            v_after = s_after.loc[~mask_after].to_numpy()
            val_match = bool(np.array_equal(v_before, v_after))
            
        assert val_match, f"Cột {col}: Giá trị không khớp giữa df_before và df_read!"
        
        column_verifications[col] = {
            "column": col,
            "raw_merged_dtype": raw_merged_dtypes.get(col, "unknown"),
            "dtype_before_write": str(s_before.dtype),
            "dtype_after_read": str(s_after.dtype),
            "pyarrow_storage_type": str(PYARROW_SCHEMA.field(col).type),
            "missing_before": n_missing_before,
            "missing_after": n_missing_after,
            "missing_mask_preserved": missing_mask_match,
            "values_preserved": val_match
        }
        print(f"   * [{col}] Đối chiếu đạt: {n_missing_before:,} nulls, Giá trị & Mặt nạ thiếu bảo toàn 100%.")

    content_preserved = all(c["values_preserved"] for c in column_verifications.values())
    missing_positions_preserved = all(c["missing_mask_preserved"] for c in column_verifications.values())
    
    check_results["content_preserved_before_after"] = content_preserved
    check_results["missing_positions_preserved_before_after"] = missing_positions_preserved
    
    # 13. Category kiểm tra nhãn không có Unknown, giữ null thật
    cat_checks_ok = True
    for cat_col in ["eval_set", "product_name", "aisle", "department"]:
        s = df_read[cat_col]
        cats = list(s.cat.categories)
        if any(bad in cats for bad in ["Unknown", "unknown", "nan", "<NA>", "None"]):
            cat_checks_ok = False
            
    check_results["category_labels_and_nulls_valid"] = cat_checks_ok
    assert cat_checks_ok, "Category chứa nhãn rác hoặc mất null thật!"
    
    print("\n - Tất cả 13 hạng mục kiểm tra cuối đều ĐẠT BẰNG ĐỐI CHIẾU THỰC TẾ (100% PASSED)!")
    
    # 5. Chỉ khi đạt mới công nhận và lưu trữ chính thức master_train.parquet
    print("\n5. Công nhận và xuất bản tệp Parquet chính thức...")
    atomic_publish(tmp_parquet, final_parquet_clean)
    atomic_publish(tmp_parquet, final_parquet_tlck)
    tmp_parquet.unlink()
    print(f" - Đã xuất bản file đích chính: {final_parquet_clean}")
    print(f" - Đã đồng bộ file đích thư mục M1: {final_parquet_tlck}")
    
    final_size_bytes = final_parquet_clean.stat().st_size
    with open(final_parquet_clean, "rb") as f:
        final_sha256 = hashlib.file_digest(f, "sha256").hexdigest()
        
    # 6. Xuất các báo cáo join_audit.csv, master_schema.csv, master_dictionary.csv
    df_chunk_audit = pd.DataFrame(all_chunks_audit)
    summary_rows = []
    for step_name in ["1_orders", "2_products", "3_aisles", "4_departments"]:
        sub = df_chunk_audit[df_chunk_audit["step"] == step_name]
        summary_rows.append({
            "chunk_id": "TOTAL_SUMMARY",
            "step": step_name,
            "right_table": sub["right_table"].iloc[0],
            "join_key": sub["join_key"].iloc[0],
            "rows_before": int(sub["rows_before"].sum()),
            "rows_after": int(sub["rows_after"].sum()),
            "unmatched_rows": int(sub["unmatched_rows"].sum()),
            "key_sequence_preserved": bool(sub["key_sequence_preserved"].all())
        })
    df_summary = pd.DataFrame(summary_rows)
    pd.concat([df_chunk_audit, df_summary], ignore_index=True).to_csv(audit_csv, index=False, encoding="utf-8-sig")
    
    # Schema csv: Xuất từ số đo thực tế đo lường ở từng giai đoạn
    schema_records = []
    for col in MASTER_COLUMNS:
        info = column_verifications[col]
        schema_records.append({
            "column": col,
            "raw_merged_dtype": info["raw_merged_dtype"],
            "dtype_before_write": info["dtype_before_write"],
            "dtype_after_read": info["dtype_after_read"],
            "pyarrow_storage_type": info["pyarrow_storage_type"],
            "missing_before": info["missing_before"],
            "missing_after": info["missing_after"],
            "missing_mask_preserved": info["missing_mask_preserved"],
            "values_preserved": info["values_preserved"]
        })
    pd.DataFrame(schema_records).to_csv(schema_csv, index=False, encoding="utf-8-sig")
    print(f" - Đã xuất báo cáo lược đồ thực đo: {schema_csv}")
    
    dict_records = []
    for col in MASTER_COLUMNS:
        info = column_verifications[col]
        dict_records.append({
            "column_name": col,
            "pandas_dtype_read": info["dtype_after_read"],
            "pyarrow_type": info["pyarrow_storage_type"],
            "missing_count": info["missing_after"],
            "missing_pct": round(info["missing_after"] / 1384617 * 100, 2)
        })
    pd.DataFrame(dict_records).to_csv(dict_csv, index=False, encoding="utf-8-sig")
    print(f" - Đã xuất từ điển dữ liệu: {dict_csv}")
    
    # 7. Xuất master_verification.json
    all_passed = all(check_results.values())
    verif_report = {
        "status": "PASSED" if all_passed else "FAILED",
        "path_base": "thesis directory (parent of scripts/)",
        "inputs": input_files_info,
        "pre_downcasting_audit": pre_audit_info,
        "master_size": {
            "rows": len(df_read),
            "columns": len(df_read.columns),
            "distinct_orders": distinct_orders,
            "distinct_users": distinct_users,
            "train_orders_per_user": 1
        },
        "checks": check_results,
        "column_verifications": column_verifications,
        "file_info": {
            "primary_file": report_path(final_parquet_clean),
            "mirror_file": report_path(final_parquet_tlck),
            "size_bytes": final_size_bytes,
            "size_mb": round(final_size_bytes / (1024 * 1024), 2),
            "compression": "snappy",
            "sha256": final_sha256
        },
        "environment": {
            "python": sys.version.split()[0],
            "pandas": pd.__version__,
            "pyarrow": pa.__version__,
            "numpy": np.__version__
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")
    }
    
    with open(verif_json_clean, "w", encoding="utf-8") as f:
        json.dump(verif_report, f, indent=2, ensure_ascii=False)
    with open(verif_json_tlck, "w", encoding="utf-8") as f:
        json.dump(verif_report, f, indent=2, ensure_ascii=False)
        
    print(f" - Đã xuất báo cáo chứng thực JSON: {verif_json_clean}")
    print(f" - Đã xuất báo cáo chứng thực JSON: {verif_json_tlck}")
    print("\n=== HOÀN TẤT THÀNH CÔNG BẢNG MASTER VÀ BỘ CHỨNG THỰC CHO MỤC 3.2 ===")


if __name__ == "__main__":
    execute_master_pipeline(
        cli_args.clean_dir, cli_args.output_dir, chunksize=cli_args.chunksize)
