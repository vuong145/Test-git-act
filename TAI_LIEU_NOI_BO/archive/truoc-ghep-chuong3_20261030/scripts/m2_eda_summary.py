"""Reference-only descriptive statistics owned by member 1 (G1)."""

from pathlib import Path

import numpy as np
import pandas as pd

from m2_common import (
    build_baskets, digest, environment, load_foundation, path, read_json,
    relative, require, snapshot, verify_hashes, write_frame, write_json,
)


def display_name(value, identifier):
    if pd.isna(value) or str(value).strip() == "":
        return f"Chưa có tên (ID={identifier})"
    return str(value)


def group_summary(reference, lookup, key, label, n_baskets):
    """Keep the full source dictionary, even zero-count and unnamed IDs."""
    require(not lookup[key].duplicated().any(), "Duplicate lookup ID")
    require(reference[key].isin(lookup[key]).all(), "Unknown lookup ID")
    grouped = reference.groupby(key, observed=True)
    counts = grouped.agg(
        row_count=("order_id", "size"),
        basket_count=("order_id", "nunique"),
        reordered_valid=("reordered", "count"),
        reordered_yes=("reordered", "sum"),
    ).reset_index()
    result = lookup[[key, label]].merge(
        counts, on=key, how="left", validate="one_to_one"
    ).sort_values(key).reset_index(drop=True)
    for column in counts.columns.drop(key):
        result[column] = result[column].fillna(0).astype("int64")
    result["display_name"] = [
        display_name(v, i) for i, v in zip(result[key], result[label])
    ]
    result["reordered_missing"] = (
        result.row_count - result.reordered_valid
    )
    result["row_share"] = result.row_count / len(reference)
    result["basket_coverage"] = result.basket_count / n_baskets
    result["observed_reorder_rate"] = (
        result.reordered_yes / result.reordered_valid.replace(0, np.nan)
    )
    result["reordered_missing_pct"] = (
        100 * result.reordered_missing / result.row_count.replace(0, np.nan)
    )
    return result


def department_display(reference, departments, n_baskets):
    ranked = departments.sort_values(
        ["row_count", "department_id"], ascending=[False, True]
    )
    top = ranked.head(10).copy()
    top["group_key"] = top.department_id.astype(str)
    others = reference.loc[~reference.department_id.isin(top.department_id)]
    rest = pd.DataFrame([{
        "group_key": "remaining", "display_name": "Các ngành còn lại",
        "row_count": len(others),
        "row_share": len(others) / len(reference),
        "basket_count": others.order_id.nunique(),
        "basket_coverage": others.order_id.nunique() / n_baskets,
    }])
    columns = ["group_key", "display_name", "row_count", "row_share",
               "basket_count", "basket_coverage"]
    return pd.concat([top[columns], rest[columns]], ignore_index=True)


def summarize(reference, baskets, departments, aisles, products, cfg):
    require(len(reference) > 0 and len(baskets) > 0, "Empty reference")
    pd.testing.assert_frame_equal(
        baskets, build_baskets(reference, cfg), check_exact=True
    )
    require(cfg["std_ddof"] == 1, "Expected sample std")
    require(cfg["kurtosis"] == "excess", "Expected excess kurtosis")
    n = len(baskets)
    overview = {
        "users": baskets.user_id.nunique(), "baskets": n,
        "product_order_rows": len(reference),
        "products_observed": reference.product_id.nunique(),
        "departments_observed": reference.department_id.nunique(),
        "aisles_observed": reference.aisle_id.nunique(),
        "singleton_baskets": int(baskets.basket_size.eq(1).sum()),
    }
    rows = []
    for column in cfg["correlation_columns"]:
        s = baskets[column].dropna().astype("float64")
        q = s.quantile([0.25, 0.5, 0.75],
                       interpolation=cfg["quantile_interpolation"])
        rows.append({
            "variable": column, "n_total": n, "n_valid": len(s),
            "n_missing": n - len(s), "missing_pct": 100 * (n-len(s))/n,
            "mean": s.mean(), "std": s.std(ddof=cfg["std_ddof"]),
            "min": s.min(), "q1": q.loc[0.25], "median": q.loc[0.5],
            "q3": q.loc[0.75], "max": s.max(),
            "skew": s.skew() if len(s) >= 3 and s.nunique() > 1 else np.nan,
            "kurtosis_excess": (
                s.kurt() if len(s) >= 4 and s.nunique() > 1 else np.nan
            ),
        })
    frequencies = []
    domains = {"order_dow": range(7), "order_hour_of_day": range(24),
               "hour_band": cfg["hour_labels"]}
    for column, domain in domains.items():
        s = baskets[column]
        valid = int(s.notna().sum())
        for value in domain:
            count = int(s.eq(value).sum())
            frequencies.append({
                "variable": column, "value": str(value),
                "is_missing": False, "count": count, "n_total": n,
                "n_valid": valid, "all_pct": 100 * count/n,
                "valid_pct": 100 * count/valid if valid else np.nan,
            })
        count = n - valid
        frequencies.append({
            "variable": column, "value": "NA", "is_missing": True,
            "count": count, "n_total": n, "n_valid": valid,
            "all_pct": 100 * count/n, "valid_pct": np.nan,
        })
    sizes = baskets.basket_size
    q1, q3 = sizes.quantile(
        [0.25, 0.75], interpolation=cfg["quantile_interpolation"]
    )
    iqr = float(q3-q1)
    lower = float(q1-cfg["iqr_multiplier"]*iqr)
    upper = float(q3+cfg["iqr_multiplier"]*iqr)
    flagged = int((sizes.lt(lower) | sizes.gt(upper)).sum())
    outliers = {
        "scope": "reference baskets only", "n_baskets": n,
        "q1": float(q1), "q3": float(q3), "iqr": iqr,
        "lower_fence": lower, "upper_fence": upper,
        "flagged_baskets": flagged, "flagged_rate": flagged/n,
        "flagged_pct": 100*flagged/n, "decision": "retain all baskets",
        "quantile_interpolation": cfg["quantile_interpolation"],
    }
    dept = group_summary(reference, departments, "department_id",
                         "department", n)
    aisle = group_summary(reference, aisles, "aisle_id", "aisle", n)
    pop = reference.groupby("product_id", observed=True).agg(
        basket_count=("order_id", "nunique"),
        row_count=("order_id", "size"),
    ).reset_index()
    require(pop.basket_count.eq(pop.row_count).all(), "Duplicate product/giỏ")
    require(pop.product_id.isin(products.product_id).all(), "Unknown product")
    pop = pop.merge(products[["product_id", "product_name"]],
                    on="product_id", how="left", validate="one_to_one")
    pop["display_name"] = [
        display_name(v, i) for i, v in zip(pop.product_id, pop.product_name)
    ]
    pop = pop.sort_values(["basket_count", "product_id"],
                          ascending=[False, True]).reset_index(drop=True)
    pop["popularity"] = pop.basket_count/n
    pop["rank"] = np.arange(1, len(pop)+1)
    pop["row_share"] = pop.row_count/len(reference)
    pop["cumulative_row_share"] = pop.row_share.cumsum()
    top_rows = []
    for requested in cfg["top_n_grid"]:
        ids = pop.head(requested).product_id
        subset = reference.loc[reference.product_id.isin(ids)]
        count = subset.order_id.nunique()
        top_rows.append({
            "n_requested": requested, "n_actual": len(ids),
            "row_count": len(subset), "row_share": len(subset)/len(reference),
            "basket_count": count, "basket_coverage": count/n,
            "n_rows_total": len(reference), "n_baskets_total": n,
            "outside_row_count": len(reference)-len(subset),
            "outside_row_share": 1-len(subset)/len(reference),
        })
    tables = {
        "sample_overview": pd.DataFrame(
            [{"metric": k, "value": v} for k, v in overview.items()]
        ),
        "eda_summary": pd.DataFrame(rows),
        "categorical_frequencies": pd.DataFrame(frequencies),
        "department_summary": dept, "aisle_summary": aisle,
        "product_popularity": pop,
        "top_n_coverage": pd.DataFrame(top_rows),
        "department_display": department_display(reference, dept, n),
    }
    validate_tables(tables, len(reference), n)
    return tables, outliers


def validate_tables(tables, n_rows, n_baskets):
    for name in ("department_summary", "aisle_summary"):
        t = tables[name]
        require(t.row_count.sum() == n_rows, f"Lost rows: {name}")
        require((t.reordered_valid+t.reordered_missing).eq(t.row_count).all(),
                "Invalid missing denominator")
        require(t.basket_count.le(n_baskets).all(), "Invalid coverage")
    f = tables["categorical_frequencies"]
    require(f.groupby("variable")["count"].sum().eq(n_baskets).all(),
            "Frequency totals omit missing")
    top = tables["top_n_coverage"].sort_values("n_requested")
    require(top.basket_coverage.is_monotonic_increasing, "Top-N coverage")
    require(top.row_share.is_monotonic_increasing, "Top-N row share")
    for table in tables.values():
        for column in table:
            if column.endswith(("_rate", "_share", "_coverage")) or column == "popularity":
                require(table[column].dropna().between(-1e-12, 1+1e-12).all(),
                        f"Invalid ratio {column}")
    require(np.isclose(tables["department_display"].row_share.sum(), 1),
            "Top-10 plus remainder does not cover rows")


def branch_paths(cfg):
    return path(cfg["outputs"]["ban1"]), path(cfg["outputs"]["tables"])


def accepted_summary():
    cfg, foundation = load_foundation()
    folder, _ = branch_paths(cfg)
    record = read_json(folder/"summary_manifest.json")
    require(record["status"] == "passed", "Summary has not passed")
    require(record["foundation_sha256"] == digest(
        path(cfg["report_dir"])/"foundation_manifest.json"), "Changed G0")
    for key in ("inputs", "code", "outputs"):
        verify_hashes(record[key])
    return cfg, foundation, record


def main():
    cfg, foundation = load_foundation()
    folder, output = branch_paths(cfg)
    state = folder/"run_manifest.json"
    report = folder/"summary_manifest.json"
    write_json(state, {"status": "building_summary"})
    write_json(report, {"status": "building"})
    try:
        data = path(cfg["data_dir"])
        inputs = [data/"reference.parquet", data/"basket_summary.parquet",
                  data/"department_lookup.csv", path(cfg["clean_dir"])/"aisles.csv",
                  path(cfg["clean_dir"])/"products.csv"]
        hashes = snapshot(inputs)
        reference, baskets = [pd.read_parquet(p) for p in inputs[:2]]
        departments, aisles, products = [
            pd.read_csv(p, keep_default_na=False) for p in inputs[2:]
        ]
        tables, outliers = summarize(
            reference, baskets, departments, aisles, products, cfg
        )
        outputs = []
        for name, frame in tables.items():
            target = output/f"{name}.csv"
            write_frame(target, frame)
            outputs.append(target)
        target = output/"reference_outliers.json"
        write_json(target, outliers)
        outputs.append(target)
        verify_hashes(hashes)
        load_foundation()
        record = {
            **environment(), "status": "passed", "stage": "ban1_summary",
            "foundation_sha256": digest(
                path(cfg["report_dir"])/"foundation_manifest.json"),
            "canonical_split_sha256": foundation["canonical_split_sha256"],
            "inputs": hashes, "code": snapshot([Path(__file__)]),
            "outputs": snapshot(outputs), "counts": foundation["counts"],
            "csv": {"encoding": "utf-8", "decimal": ".",
                    "numeric_na": "empty", "rounding": "none",
                    "name_reader": "keep_default_na=False",
                    "frequency_percent_columns": "all_pct, valid_pct"},
            "checks": {"basket_recomputed_exact": True,
                       "source_hashes_unchanged": True,
                       "denominators_ranges_monotonicity": True},
            "pending": ["peer review", "I1-I3 final interpretation by member 2"],
        }
        write_json(report, record)
        write_json(state, {"status": "summary_passed_plots_pending",
                           "summary": relative(report),
                           "summary_sha256": digest(report)})
        print("G1 SUMMARY PASSED", foundation["counts"])
    except BaseException as exc:
        failed = {"status": "failed", "error": str(exc)}
        write_json(report, failed)
        write_json(state, failed)
        raise


if __name__ == "__main__":
    main()
