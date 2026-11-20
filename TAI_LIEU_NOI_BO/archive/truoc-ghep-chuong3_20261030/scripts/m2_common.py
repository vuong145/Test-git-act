"""Shared G0 contracts. Paths are relative to this project, never the cwd."""

import hashlib
import json
import os
import platform
import tempfile
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow

ROOT = Path(__file__).resolve().parents[1]
CLEAN_NAMES = ("aisles", "departments", "products", "orders",
               "order_products__prior", "order_products__train")
CONFIG_NAMES = ("m2_eda.json", "hypotheses_config.json", "m2_plot_style.json")
SPLIT_RULE = ("test=ceil(N/5);validation=floor(N/5);"
              "reference=floor(remaining/2);fit=remainder")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def path(value):
    return (ROOT / value).resolve()


def relative(value):
    return Path(value).resolve().relative_to(ROOT).as_posix()


def digest(value):
    with Path(value).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read_json(value):
    return json.loads(Path(value).read_text(encoding="utf-8"))


def config():
    result = read_json(path("configs/m2_eda.json"))
    require(result["contract_version"] == 1, "Unsupported contract_version")
    require(result["report_dir"] == "BAO CAO/Bao cao EDA/common", "State directory is fixed")
    require(result["split_rule"] == SPLIT_RULE, "Unsupported split_rule")
    require(result["min_group_n"] == 30, "Reporting threshold must be 30")
    require(result["hypotheses_config"] == "configs/hypotheses_config.json",
            "Hypothesis parameters have one canonical source")
    for value in result["outputs"].values():
        require(not Path(value).is_absolute() and path(value).is_relative_to(ROOT),
                "Output paths must remain relative to the project")
    require(result["seed"] == 42 and result["rng"] == "PCG64",
            "G0 split contract requires PCG64 seed 42")
    require(result["expected_one_basket_per_user"], "One basket/user required")
    require(result["slice_order"] == ["test", "reference", "fit", "validation"],
            "Unexpected split order")
    return result


def atomic_write(destination, writer):
    """Atomic replacement per file; manifest hashes gate multi-file validity."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=destination.parent, suffix=".tmp")
    os.close(fd)
    temporary = Path(name)
    try:
        writer(temporary)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def write_json(destination, obj):
    atomic_write(destination, lambda p: p.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8"))


def write_frame(destination, frame):
    if str(destination).endswith(".parquet"):
        atomic_write(destination, lambda p: frame.to_parquet(p, index=False))
    else:
        atomic_write(destination, lambda p: frame.to_csv(
            p, index=False, encoding="utf-8", lineterminator="\n"))


def snapshot(files):
    return {relative(p): digest(p) for p in files}


def verify_hashes(records):
    for name, expected in records.items():
        require(digest(path(name)) == expected, f"Changed artifact: {name}")


def sources(cfg):
    return [path(cfg["master"]), path(cfg["clean_dir"]) / "master_verification.json",
            path("BAO CAO/Bao cao lam sach/verification.json")] + [
        path(cfg["clean_dir"]) / f"{name}.csv" for name in CLEAN_NAMES]


def verify_recorded_sources(cfg, hashes):
    """Compare against saved M1/cleaning evidence, not an original Kaggle copy."""
    m1 = read_json(path(cfg["clean_dir"]) / "master_verification.json")
    require(m1["status"] == "PASSED", "M1 evidence is not passed")
    require(hashes[relative(path(cfg["master"]))] == m1["file_info"]["sha256"],
            "Master differs from M1 evidence")
    clean = read_json(path("BAO CAO/Bao cao lam sach/verification.json"))
    require(clean["status"] == "verified", "Cleaning evidence is not verified")
    expected = {r["table"]: r["new_sha256"] for r in clean["comparison_previous"]}
    require(set(expected) == set(CLEAN_NAMES), "Incomplete cleaning evidence")
    for name in CLEAN_NAMES:
        require(hashes[relative(path(cfg["clean_dir"]) / f"{name}.csv")] == expected[name],
                f"CSV differs from recorded cleaning evidence: {name}")


def configuration_files():
    return ([path("configs") / name for name in CONFIG_NAMES]
            + [path("requirements-m2.txt"), path("requirements-m2-lock.txt")])


def environment():
    return {"created_at_utc": datetime.now(timezone.utc).isoformat(),
            "python": platform.python_version(), "pandas": pd.__version__,
            "numpy": np.__version__, "pyarrow": pyarrow.__version__,
            "packages": {name: version(name) for name in
                         ("numpy", "pandas", "pyarrow", "scipy", "matplotlib", "seaborn")}}


def canonical_manifest(frame):
    text = frame.sort_values("user_id").to_csv(index=False, lineterminator="\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def make_split(users, seed=42):
    values = np.asarray(sorted(users), dtype=np.int64)
    require(len(values) == len(np.unique(values)), "Duplicate user IDs")
    n = len(values)
    require(n >= 5, "At least five users needed")
    n_test, n_validation = (n + 4) // 5, n // 5
    remaining = n - n_test - n_validation
    counts = {"test": n_test, "reference": remaining // 2,
              "fit": remaining - remaining // 2, "validation": n_validation}
    shuffled = np.random.Generator(np.random.PCG64(seed)).permutation(values)
    labels = [label for label, count in counts.items() for _ in range(count)]
    return pd.DataFrame({"user_id": shuffled, "split": labels}).sort_values(
        "user_id").reset_index(drop=True)


def validate_master(frame):
    keys = ["order_id", "product_id", "user_id", "aisle_id", "department_id"]
    require(not frame[keys].isna().any().any(), "Missing identifiers")
    require(all(pd.api.types.is_integer_dtype(frame[k]) for k in keys),
            "Identifiers must have integer dtype")
    require(not frame.duplicated(["order_id", "product_id"]).any(),
            "Duplicate order/product key")
    pairs = frame[["user_id", "order_id"]].drop_duplicates()
    require(not pairs.user_id.duplicated().any(), "Multiple baskets per user")
    require(not pairs.order_id.duplicated().any(), "Multiple users per order")
    require(frame.eval_set.eq("train").all(), "Master must contain train only")
    require(frame.groupby("aisle_id", observed=True).department_id.nunique().le(1).all(),
            "Aisle maps to multiple departments")
    return pairs


def build_baskets(reference, cfg):
    validate_master(reference)
    attributes = ["user_id", "order_dow", "order_hour_of_day", "days_since_prior_order"]
    grouped = reference.groupby("order_id", observed=True, sort=True)
    require(grouped[attributes].nunique(dropna=False).le(1).all().all(),
            "Conflicting order attributes, including missing values")
    baskets = grouped.agg(basket_size=("product_id", "nunique"),
                          n_departments=("department_id", "nunique"),
                          n_aisles=("aisle_id", "nunique")).reset_index()
    attributes_frame = reference[["order_id"] + attributes].drop_duplicates("order_id")
    baskets = baskets.join(attributes_frame.set_index("order_id"),
                            on="order_id", validate="one_to_one")
    for column, low, high in (("order_dow", 0, 6), ("order_hour_of_day", 0, 23),
                              ("days_since_prior_order", 0, 30)):
        valid = baskets[column].dropna()
        require(valid.between(low, high).all(), f"Invalid domain: {column}")
    baskets["hour_band"] = pd.cut(
        baskets.order_hour_of_day.astype("float64"), bins=cfg["hour_bins"],
        labels=cfg["hour_labels"], right=False, ordered=True)
    require(baskets.basket_size.sum() == len(reference), "Basket row mismatch")
    require((baskets.n_departments.ge(1) &
             baskets.n_departments.le(baskets.n_aisles) &
             baskets.n_aisles.le(baskets.basket_size)).all(), "Invalid basket counts")
    return baskets.sort_values("order_id").reset_index(drop=True)


def load_foundation_inputs():
    """Verifier input gate; intentionally does not require its own acceptance."""
    cfg = config()
    reports = path(cfg["report_dir"])
    manifest = read_json(reports / "foundation_manifest.json")
    for name in ("sources", "configs", "code", "outputs"):
        verify_hashes(manifest[name])
    return cfg, manifest


def load_foundation():
    """EDA gate requires committed acceptance, state and an intact hash chain."""
    from m2_evidence import accepted_foundation
    return accepted_foundation()
