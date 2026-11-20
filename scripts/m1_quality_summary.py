"""Tỷ lệ thiếu theo bảng nguồn và kiểm toán IQR kích thước giỏ trên toàn Master train.

Chạy sau summarize_cleaning.py và m1_build_master.py. Đây là kiểm toán cấu trúc,
không dùng ngưỡng IQR để lọc mẫu hay chọn mô hình (EDA mô hình chỉ dùng reference).

ĐỌC NHANH: hai bảng chất lượng cho mục 3.2-3.3. (1) Tỷ lệ thiếu theo bảng nguồn (trước/sau làm sạch);
  (2) kiểm toán IQR kích thước giỏ trên toàn Master: CHỈ để mô tả, KHÔNG dùng để lọc dòng hay chọn mô hình.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "BAO CAO/Bao cao lam sach"
MASTER = ROOT / "DATA/Data đã làm sạch/master_train.parquet"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    # Khối 1: tỷ lệ thiếu theo bảng nguồn, từ before_after.csv.
    before = REPORTS / "before_after.csv"
    sources = {p.relative_to(ROOT).as_posix(): digest(p) for p in (MASTER, before)}
    missing = pd.read_csv(before)
    total = missing["missing_final"] + missing["nonmissing_final"]
    if total.le(0).any():
        raise ValueError("Empty source table in quality report")
    missing["rows"] = total
    missing["missing_before_pct"] = 100 * missing["missing_tokens_before"] / total
    missing["missing_final_pct"] = 100 * missing["missing_final"] / total
    # Khối 2: IQR của kích thước giỏ trên Master; giỏ vượt hàng rào chỉ bị đánh dấu, vẫn giữ lại.
    master = pd.read_parquet(MASTER, columns=["order_id", "product_id"])
    if master.isna().any().any() or master.duplicated().any():
        raise ValueError("Missing or duplicated basket-product keys")
    sizes = master.groupby("order_id", observed=True).size()
    q1, q3 = sizes.quantile([0.25, 0.75]).tolist()
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    flagged = sizes.lt(lower) | sizes.gt(upper)
    # Báo cáo kèm hash nguồn và hash script để truy vết.
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "scope": "full train Master; structural quality audit only",
        "source_sha256": sources, "script_sha256": digest(Path(__file__)),
        "pandas_version": pd.__version__, "rows": len(master), "baskets": len(sizes),
        "minimum": int(sizes.min()), "maximum": int(sizes.max()),
        "q1": q1, "q3": q3, "iqr": iqr, "lower_fence": lower, "upper_fence": upper,
        "quantile_interpolation": "linear", "flagged_baskets": int(flagged.sum()),
        "flagged_pct": 100 * float(flagged.mean()),
        "decision": "retain; statistical flag alone is not an invalid-record rule",
        "limitations": "No household inference; no model tuning on full Master. "
                       "Model-directed EDA must use reference after splitting."}
    if {name: digest(ROOT / name) for name in sources} != sources:
        raise ValueError("Source changed during quality audit")
    missing.to_csv(REPORTS / "missingness_summary.csv", index=False, encoding="utf-8-sig")
    (REPORTS / "basket_quality_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
