"""Report missingness and basket-size quality checks without changing data.

Full-Master IQR is a structural audit, not a model-selection threshold.
Run from any working directory; outputs are relative to the project folder.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import pandas as pd


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    root = Path(__file__).resolve().parents[1]
    reports = root / "BAO CAO/Bao cao lam sach"
    master_path = root / "DATA/Data đã làm sạch/master_train.parquet"
    before_path = reports / "before_after.csv"
    source_hashes = {str(p.relative_to(root)): digest(p)
                     for p in (master_path, before_path)}
    missing = pd.read_csv(before_path)
    total = missing["missing_final"] + missing["nonmissing_final"]
    if total.le(0).any():
        raise ValueError("Empty source table in quality report")
    missing["rows"] = total
    missing["missing_before_pct"] = 100 * missing["missing_tokens_before"] / total
    missing["missing_final_pct"] = 100 * missing["missing_final"] / total
    master = pd.read_parquet(master_path, columns=["order_id", "product_id"])
    if master.isna().any().any() or master.duplicated().any():
        raise ValueError("Missing or duplicated basket-product keys")
    sizes = master.groupby("order_id", observed=True).size()
    q1, q3 = sizes.quantile([0.25, 0.75]).tolist()
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    flagged = sizes.lt(lower) | sizes.gt(upper)
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "scope": "full train Master; structural quality audit only",
        "source_sha256": source_hashes,
        "script_sha256": digest(Path(__file__)),
        "pandas_version": pd.__version__,
        "rows": len(master), "baskets": len(sizes),
        "minimum": int(sizes.min()), "maximum": int(sizes.max()),
        "q1": q1, "q3": q3, "iqr": iqr,
        "lower_fence": lower, "upper_fence": upper,
        "quantile_interpolation": "linear",
        "flagged_baskets": int(flagged.sum()),
        "flagged_pct": 100 * float(flagged.mean()),
        "decision": "retain; statistical flag alone is not an invalid-record rule",
        "limitations": "No household inference; no model tuning on full Master. "
                        "Model-directed EDA must use reference after splitting.",
    }
    for relative, expected in source_hashes.items():
        if digest(root / relative) != expected:
            raise ValueError("Source changed during quality audit")
    missing.to_csv(reports / "missingness_summary.csv", index=False,
                   encoding="utf-8-sig")
    (reports / "basket_quality_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
