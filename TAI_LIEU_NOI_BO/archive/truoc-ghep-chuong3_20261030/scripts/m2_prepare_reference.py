"""Finish G0; do not compute EDA, cooccurrence or hypothesis results."""

import pandas as pd

from m2_common import (build_baskets, config, digest, environment, path, read_json,
                       require, snapshot, verify_hashes, write_frame, write_json)


def main():
    cfg = config()
    reports, data = path(cfg["report_dir"]), path(cfg["data_dir"])
    write_json(reports / "foundation_validation.json", {"status": "building"})
    split = read_json(reports / "split_manifest.json")
    for key in ("sources", "configs", "code", "outputs"):
        verify_hashes(split[key])
    reference = pd.read_parquet(data / "reference.parquet")
    baskets = build_baskets(reference, cfg)
    lookup = pd.read_csv(path(cfg["clean_dir"]) / "departments.csv",
                         keep_default_na=False).sort_values("department_id")
    require(lookup.department_id.tolist() == list(range(1, 22)),
            "Expected exactly department IDs 1..21")
    require(reference.department_id.isin(lookup.department_id).all(),
            "Unknown department")
    names = lookup.set_index("department_id").department.to_dict()
    hypotheses = read_json(path("configs/hypotheses_config.json"))
    for pair in hypotheses["pairs"]:
        require(names[pair["a"]] == pair["a_name"] and
                names[pair["b"]] == pair["b_name"], "Hypothesis ID/name mismatch")
    require(names[21] == "missing", "Literal missing must be preserved")
    write_frame(data / "basket_summary.parquet", baskets)
    write_frame(data / "department_lookup.csv", lookup)
    pd.testing.assert_frame_equal(baskets, pd.read_parquet(data / "basket_summary.parquet"))
    contract = {
        "version": 1, "scope": "G0 only; reference full baskets; no EDA results",
        "paths_relative_to": "project directory containing scripts",
        "basket_columns": {name: {"dtype": str(baskets[name].dtype),
                                   "nullable": name in ["order_dow", "order_hour_of_day",
                                                        "days_since_prior_order", "hour_band"]}
                           for name in baskets.columns},
        "units": {"basket_size": "distinct products/order", "n_departments": "distinct departments/order",
                  "n_aisles": "distinct aisles/order", "order_dow": "unmapped code 0..6",
                  "order_hour_of_day": "hour 0..23", "days_since_prior_order": "days, capped at 30",
                  "hour_band": cfg["hour_labels"]},
        "missing": "Preserve NA; no imputation; literal department 'missing' is a valid label",
        "ratios": {"_rate/_share/_coverage/popularity/support_AB": "0..1",
                   "_pct": "0..100", "_pp": "percentage points", "lift": "ratio, not percent"},
        "csv": {"encoding": "utf-8", "decimal": ".", "null_numeric": "empty field",
                "category_reader": "keep_default_na=False; handle empty labels explicitly"},
        "denominators": {"basket_coverage": "all reference baskets",
                         "row_share": "all reference product-order rows",
                         "observed_reorder_rate": "rows with valid reordered only"},
        "parquet_reader": "pd.read_parquet default; no dtype_backend override",
        "reference_dtypes": {k: str(v) for k, v in reference.dtypes.items()},
        "department_order": list(range(1, 22)),
        "restrictions": ["No Top-N filtering or singleton removal in reference",
                         "No fit/validation/test behavioral EDA", "Do not modify source files"]}
    write_json(reports / "data_contract.json", contract)
    for key in ("sources", "configs", "code", "outputs"):
        verify_hashes(split[key])
    manifest = {**environment(), "stage": "foundation", "sources": split["sources"],
                "configs": split["configs"],
                "code": {**split["code"], **snapshot([path("scripts/m2_prepare_reference.py"),
                    path("scripts/m2_evidence.py")])},
                "outputs": {**split["outputs"], **snapshot([
                    data / "basket_summary.parquet", data / "department_lookup.csv",
                    reports / "data_contract.json", reports / "split_manifest.json"])},
                "counts": {**split["counts"], "reference_baskets": len(baskets),
                           "reference_users": int(baskets.user_id.nunique()), "departments": len(lookup)},
                "canonical_split_sha256": split["canonical_split_sha256"],
                "limitations": ["No human joint sign-off claimed",
                                "No statistical hypothesis test or cooccurrence heatmap run",
                                "Hypotheses locked before this M2 run; no assertion about prior human exposure"]}
    write_json(reports / "foundation_manifest.json", manifest)
    write_json(reports / "foundation_validation.json", {
        **environment(), "status": "prepared",
        "manifest_sha256": digest(reports / "foundation_manifest.json"),
        "checks": {**split["checks"], "one_basket_per_user": True,
                   "order_attributes_consistent_including_na": True,
                   "sum_basket_size_equals_reference_rows": True,
                   "basket_counts_ordered": True, "department_lookup_21": True,
                   "hypothesis_id_names_verified": True, "parquet_roundtrip": True},
        "scope": "Preparation only; independent verification required before EDA"})
    print(manifest["counts"])


if __name__ == "__main__":
    from m2_evidence import writer_lock
    with writer_lock():
        main()
