"""Read-only structural inspection of the inherited M1 artifact, not a benchmark."""
from pathlib import Path
import hashlib
import io
import json
import platform

import pandas as pd
import pyarrow

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = ROOT / "Data đã làm sạch/master_train.parquet"
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    ordinary = pd.read_parquet(source)
    nullable = pd.read_parquet(source, dtype_backend="numpy_nullable")
    pd.testing.assert_frame_equal(ordinary, nullable, check_dtype=False, check_exact=True,
                                  check_categorical=False)
    assert ordinary.isna().equals(nullable.isna())
    report = ROOT / "Bao cao kiem chung hien tai"
    report.mkdir(exist_ok=True)
    buffer = io.StringIO()
    nullable.info(buf=buffer, memory_usage="deep")
    (report / "master_info.txt").write_text(buffer.getvalue(), encoding="utf-8")
    missing = pd.DataFrame({"missing": nullable.isna().sum(),
                            "missing_pct": nullable.isna().mean() * 100,
                            "default_dtype": ordinary.dtypes.astype(str),
                            "nullable_dtype": nullable.dtypes.astype(str)})
    missing.index.name = "column"
    missing.to_csv(report / "master_read_modes.csv", encoding="utf-8", lineterminator="\n")
    result = {"scope": "structural artifact audit; full Master; not behavioral EDA or benchmark",
              "master_sha256": before, "shape": list(nullable.shape),
              "default_and_nullable_values_equal": True, "missing_masks_equal": True,
              "python": platform.python_version(), "pandas": pd.__version__,
              "pyarrow": pyarrow.__version__,
              "source_unchanged": before == hashlib.sha256(source.read_bytes()).hexdigest()}
    (report / "master_read_modes.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
