"""Read back G1 artifacts; independently reconcile counts and statistics."""

from pathlib import Path

import numpy as np
import pandas as pd

from m2_common import (
    digest, environment, path, read_json, require, snapshot, verify_hashes,
    write_json,
)
from m2_eda_summary import accepted_summary, branch_paths


def main():
    cfg, foundation, summary = accepted_summary()
    folder, tables = branch_paths(cfg)
    target = folder/"validation.json"
    write_json(target, {"status": "checking"})
    try:
        plot = read_json(folder/"plot_manifest.json")
        draft = read_json(folder/"draft_manifest.json")
        require(plot["status"] == "passed", "Plot stage not passed")
        require(draft["status"] == "generated_peer_review_pending",
                "Draft stage missing")
        for record in (plot, draft):
            require(record["foundation_sha256"] == summary["foundation_sha256"],
                    "Mixed G0 versions")
            for key in ("inputs", "code", "outputs"):
                verify_hashes(record[key])
        ref = pd.read_parquet(path(cfg["data_dir"])/"reference.parquet")
        baskets = pd.read_parquet(path(cfg["data_dir"])/"basket_summary.parquet")
        n = len(baskets)
        stats = pd.read_csv(tables/"eda_summary.csv").set_index("variable")
        desc = baskets[cfg["correlation_columns"]].astype("float64").describe()
        for col in cfg["correlation_columns"]:
            for output, source in {
                "n_valid": "count", "mean": "mean", "std": "std",
                "min": "min", "q1": "25%", "median": "50%",
                "q3": "75%", "max": "max",
            }.items():
                np.testing.assert_allclose(stats.loc[col, output],
                                           desc.loc[source, col], equal_nan=True)
            require(stats.loc[col, "n_missing"] == baskets[col].isna().sum(),
                    "Missing count mismatch")
        frequencies = pd.read_csv(tables/"categorical_frequencies.csv",
                                   keep_default_na=False)
        for row in frequencies.itertuples():
            series = baskets[row.variable]
            if row.is_missing:
                count = int(series.isna().sum())
                require(row.valid_pct == "", "Missing valid_pct must be NA")
            else:
                value = row.value if row.variable == "hour_band" else int(row.value)
                count = int(series.eq(value).sum())
                valid = int(series.notna().sum())
                if valid:
                    np.testing.assert_allclose(float(row.valid_pct), count/valid*100)
                else:
                    require(row.valid_pct == "", "Zero valid denominator must be NA")
            require(row.count == count, "Frequency cell mismatch")
            np.testing.assert_allclose(row.all_pct, count/n*100)
        for filename, key in [("department_summary", "department_id"),
                               ("aisle_summary", "aisle_id")]:
            t = pd.read_csv(tables/f"{filename}.csv")
            for r in t.itertuples():
                sub = ref.loc[ref[key].eq(getattr(r, key))]
                require(len(sub) == r.row_count, "Group row count")
                require(sub.order_id.nunique() == r.basket_count, "Group coverage")
                require(sub.reordered.notna().sum() == r.reordered_valid,
                        "Reordered denominator")
                np.testing.assert_allclose(
                    sub.reordered.mean(), r.observed_reorder_rate, equal_nan=True
                )
        popularity = pd.read_csv(tables/"product_popularity.csv")
        expected = ref.groupby("product_id", observed=True).order_id.nunique()
        expected = expected.rename("basket_count").reset_index().sort_values(
            ["basket_count", "product_id"], ascending=[False, True]
        ).reset_index(drop=True)
        pd.testing.assert_frame_equal(
            popularity[["product_id", "basket_count"]], expected,
            check_dtype=False,
        )
        np.testing.assert_allclose(popularity.popularity, expected.basket_count/n)
        np.testing.assert_allclose(popularity.cumulative_row_share,
                                   expected.basket_count.cumsum()/len(ref))
        for r in pd.read_csv(tables/"top_n_coverage.csv").itertuples():
            ids = set(expected.head(r.n_requested).product_id)
            selected = [(o, p) for o, p in zip(ref.order_id, ref.product_id) if p in ids]
            require(len(selected) == r.row_count, "Top-N row count")
            require(len({o for o, _ in selected}) == r.basket_count,
                    "Top-N union coverage")
        out = read_json(tables/"reference_outliers.json")
        q1, q3 = np.quantile(baskets.basket_size, [0.25, 0.75], method="linear")
        flags = (baskets.basket_size < q1-1.5*(q3-q1)) | (
            baskets.basket_size > q3+1.5*(q3-q1))
        require(flags.sum() == out["flagged_baskets"], "IQR mismatch")
        accepted_summary()
        records = snapshot([folder/"summary_manifest.json", folder/"plot_manifest.json",
                            folder/"draft_manifest.json"])
        write_json(target, {
            **environment(), "status": "passed", "scope": "member 1 only",
            "foundation_sha256": summary["foundation_sha256"],
            "counts": foundation["counts"], "stages": records,
            "verifier_sha256": digest(Path(__file__)),
            "checks": ["describe independent reconciliation", "frequency cells",
                       "group counts and valid-only reorder denominators",
                       "product ranking", "Top-N union counts", "reference IQR",
                       "all stage code/input/output hashes", "source hashes unchanged"],
            "pending": ["peer review", "member 2 results", "main QMD integration"],
        })
        write_json(folder/"run_manifest.json", {
            "status": "ban1_verified_peer_review_pending",
            "foundation_sha256": summary["foundation_sha256"],
            "stages": records, "validation": snapshot([target]),
            "pending": ["peer review", "member 2 results", "main QMD integration"],
        })
        print("BAN1 INDEPENDENT VALIDATION PASSED")
    except BaseException as exc:
        write_json(target, {"status": "failed", "error": str(exc)})
        write_json(folder/"run_manifest.json", {"status": "failed", "error": str(exc)})
        raise


if __name__ == "__main__":
    main()
