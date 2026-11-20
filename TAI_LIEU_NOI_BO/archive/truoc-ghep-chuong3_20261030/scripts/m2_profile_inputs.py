"""Trace basic inspection APIs; does not replace branch EDA or use test behavior."""
import io

import pandas as pd

from m2_common import (environment, load_foundation, path, relative, snapshot,
                       write_frame, write_json, digest)
from m2_evidence import common_dir, new_run, writer_lock


def main():
    cfg, manifest = load_foundation()
    run_id, directory = new_run("quality")
    master = pd.read_parquet(path(cfg["master"]))
    buffer = io.StringIO()
    master.info(buf=buffer, memory_usage="deep")
    (directory / "master_info.txt").write_text(buffer.getvalue(), encoding="utf-8")
    write_frame(directory / "master_missing.csv", pd.DataFrame({
        "column": master.columns, "missing": master.isna().sum().values,
        "missing_pct": (master.isna().mean() * 100).values,
        "denominator": len(master), "unit": "train product-order row"}))
    baskets = pd.read_parquet(path(cfg["data_dir"]) / "basket_summary.parquet")
    write_frame(directory / "reference_missing.csv", pd.DataFrame({
        "column": baskets.columns, "missing": baskets.isna().sum().values,
        "missing_pct": (baskets.isna().mean() * 100).values,
        "denominator": len(baskets), "unit": "reference basket"}))
    columns = ["basket_size", "n_departments", "n_aisles", "days_since_prior_order"]
    write_frame(directory / "reference_describe.csv", baskets[columns].describe().reset_index())
    load_foundation()
    write_json(directory / "inspection.json", {
        **environment(), "run_id": run_id, "status": "passed",
        "scope": "Basic inspection trace, not completed section 3.4",
        "master_shape": list(master.shape), "reference_baskets_shape": list(baskets.shape),
        "canonical_split_sha256": manifest["canonical_split_sha256"],
        "foundation_manifest_sha256": digest(common_dir() / "foundation_manifest.json"),
        "artifacts": snapshot(list(directory.iterdir()) + [path("scripts/m2_profile_inputs.py")])})
    write_json(common_dir() / "quality_latest.json", {
        "record": relative(directory / "inspection.json"),
        "sha256": digest(directory / "inspection.json")})


if __name__ == "__main__":
    with writer_lock():
        main()
