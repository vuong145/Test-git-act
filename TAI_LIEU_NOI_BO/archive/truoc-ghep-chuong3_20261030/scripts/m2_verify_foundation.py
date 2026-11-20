"""Independent G0 acceptance checks; safe to run from any working directory."""

import pandas as pd

from m2_common import (build_baskets, canonical_manifest, digest, environment,
                       load_foundation_inputs, make_split, path, require, snapshot,
                       validate_master, write_json)


def independent_checks(cfg, manifest, checks):
    data, reports = path(cfg["data_dir"]), path(cfg["report_dir"])
    master = pd.read_parquet(path(cfg["master"]))
    population = validate_master(master)
    split = pd.read_parquet(data / "split_manifest.parquet")
    reference = pd.read_parquet(data / "reference.parquet")
    baskets = pd.read_parquet(data / "basket_summary.parquet")
    expected_split = make_split(population.user_id, cfg["seed"])
    pd.testing.assert_frame_equal(split, expected_split)
    require(canonical_manifest(split) == manifest["canonical_split_sha256"],
            "Canonical split hash mismatch")
    memberships = population.merge(split, on="user_id", how="left", validate="one_to_one")
    require(memberships.split.notna().all(), "Unassigned orders/users")
    ref_users = split.loc[split.split.eq("reference"), "user_id"]
    expected = master.loc[master.user_id.isin(ref_users)].sort_values(
        ["order_id", "product_id"]).reset_index(drop=True)
    pd.testing.assert_frame_equal(reference, expected, check_exact=True)
    pd.testing.assert_frame_equal(baskets, build_baskets(expected, cfg), check_exact=True)
    sizes = reference.groupby("order_id", observed=True).size()
    require(sizes.eq(1).sum() == baskets.basket_size.eq(1).sum(), "Singleton lost")
    lookup = pd.read_csv(data / "department_lookup.csv", keep_default_na=False)
    original = pd.read_csv(path(cfg["clean_dir"]) / "departments.csv",
                           keep_default_na=False).sort_values("department_id")
    pd.testing.assert_frame_equal(lookup, original.reset_index(drop=True))
    load_foundation_inputs()  # Recheck hashes after reading sources.
    checks.update({"partition_exact_recomputed": True,
                   "reference_exact_all_rows_columns_dtypes": True,
                   "basket_table_exact_recomputed": True,
                   "singletons_preserved": True,
                   "lookup_matches_clean_source": True})


def main():
    from m2_evidence import verify_and_commit
    verify_and_commit(independent_checks)
    print("G0 ACCEPTANCE PASSED; immutable record linked by common/latest.json")


if __name__ == "__main__":
    main()
