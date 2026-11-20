"""Create the ID-only split and untouched reference baskets; no behavioral EDA."""

import pandas as pd

from m2_common import (canonical_manifest, config, configuration_files, environment,
                       make_split, path, require, snapshot, sources, validate_master,
                       verify_hashes, verify_recorded_sources, write_frame, write_json)


def main():
    cfg = config()
    reports, data = path(cfg["report_dir"]), path(cfg["data_dir"])
    write_json(reports / "foundation_validation.json", {"status": "building"})
    source_hashes = snapshot(sources(cfg))
    verify_recorded_sources(cfg, source_hashes)
    config_hashes = snapshot(configuration_files())
    master = pd.read_parquet(path(cfg["master"]))
    pairs = validate_master(master)
    split = make_split(pairs.user_id, cfg["seed"])
    repeated = make_split(pairs.user_id.iloc[::-1], cfg["seed"])
    pd.testing.assert_frame_equal(split, repeated)
    require(set(split.user_id) == set(pairs.user_id), "Split does not cover population")
    ref_users = split.loc[split.split.eq("reference"), "user_id"]
    reference = master.loc[master.user_id.isin(ref_users)].sort_values(
        ["order_id", "product_id"]).reset_index(drop=True)
    require(reference.user_id.nunique() == len(ref_users), "Missing reference users")
    write_frame(data / "split_manifest.parquet", split)
    write_frame(data / "reference.parquet", reference)
    pd.testing.assert_frame_equal(reference, pd.read_parquet(data / "reference.parquet"))
    pd.testing.assert_frame_equal(split, pd.read_parquet(data / "split_manifest.parquet"))
    verify_hashes(source_hashes)
    verify_hashes(config_hashes)
    manifest = {**environment(), "stage": "split", "sources": source_hashes,
                "configs": config_hashes,
                "code": snapshot([path("scripts/m2_common.py"),
                                  path("scripts/m2_split_data.py")]),
                "outputs": snapshot([data / "split_manifest.parquet",
                                     data / "reference.parquet"]),
                "canonical_split_sha256": canonical_manifest(split),
                "counts": {"master_rows": len(master), "users": len(pairs),
                           "reference_rows": len(reference),
                           "split_users": {str(k): int(v) for k, v in
                                           split.split.value_counts().items()}},
                "checks": {"complete_disjoint_partition": True,
                           "sources_match_recorded_m1_cleaning_evidence": True,
                           "same_split_after_input_reversal": True,
                           "reference_all_columns_values_dtypes_preserved": True,
                           "sources_unchanged": True}}
    write_json(reports / "split_manifest.json", manifest)
    print(manifest["counts"])


if __name__ == "__main__":
    from m2_evidence import writer_lock
    with writer_lock():
        main()
