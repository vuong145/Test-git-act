"""
Benchmark Resource Optimization for PRJ-08 (Milestone M1) with Strict 3-Run Subprocess Isolation.

Implements:
- Subprocess isolation for every single measurement run to eliminate heap memory contamination.
- Continuous RSS monitoring during execution via dedicated background polling thread (every 5ms).
- Explicit timing scope measurement (wall time in seconds via time.perf_counter()).
- Uniform null handling (keep_default_na=False, na_values=[""]) across all CSV read branches.
- Uniform output dtypes between CSV and Parquet readers to ensure apples-to-apples comparison.
- Consistent benchmark artifacts: Write Parquet and Read Parquet operate on the EXACT SAME file (master_benchmark.parquet).
- Reconstructed unoptimized baseline clearly labeled and described in metadata.
- Explicit cache condition disclosure (Windows OS page cache / warm-cache transparency).
- Standardized units: MiB (1024^2 bytes) and seconds.
- Missing/inapplicable metrics left empty (not 0).
- Records Run 1, Run 2, Run 3 and computes Median.

Outputs:
- data_benchmark.csv (with columns: experiment, state, operation, run_id, rows, columns, dataframe_mib, peak_rss_mib, disk_mib, elapsed_seconds)
- data_benchmark_metadata.json (system info, timing scopes, cache condition, artifact specs)
"""
import os
import gc
import sys
import time
import json
import platform
import threading
import subprocess
from pathlib import Path
from m1_common import parse_args, report_path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if __name__ == "__main__":
    cli_args = parse_args("Milestone M1 Benchmark Runner", benchmark=True)

import psutil
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

MASTER_COLUMNS = [
    "order_id",
    "product_id",
    "add_to_cart_order",
    "reordered",
    "user_id",
    "eval_set",
    "order_number",
    "order_dow",
    "order_hour_of_day",
    "days_since_prior_order",
    "product_name",
    "aisle_id",
    "department_id",
    "aisle",
    "department",
]

OPTIMIZED_DTYPES = {
    "order_id": "int32",
    "product_id": "int32",
    "add_to_cart_order": "int16",
    "reordered": "Int8",
    "user_id": "int32",
    "eval_set": "category",
    "order_number": "int16",
    "order_dow": "Int8",
    "order_hour_of_day": "Int8",
    "days_since_prior_order": "Float32",
    "product_name": "category",
    "aisle_id": "int16",
    "department_id": "int8",
    "aisle": "category",
    "department": "category",
}


def normalize_parquet_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Đưa các cột nguyên không null từ Int32/Int16/Int8 nullable về int32/int16/int8 thuần chuẩn để đồng nhất tuyệt đối với CSV."""
    df["order_id"] = df["order_id"].astype("int32")
    df["product_id"] = df["product_id"].astype("int32")
    df["add_to_cart_order"] = df["add_to_cart_order"].astype("int16")
    df["user_id"] = df["user_id"].astype("int32")
    df["order_number"] = df["order_number"].astype("int16")
    df["aisle_id"] = df["aisle_id"].astype("int16")
    df["department_id"] = df["department_id"].astype("int8")
    return df


class SubprocessPeakTracker:
    def __init__(self, interval=0.005):
        self.interval = interval
        self.process = psutil.Process(os.getpid())
        self.peak_rss = self.process.memory_info().rss
        self._stop_event = threading.Event()
        self._thread = None

    def _monitor(self):
        while not self._stop_event.is_set():
            try:
                rss = self.process.memory_info().rss
                if rss > self.peak_rss:
                    self.peak_rss = rss
            except Exception:
                pass
            time.sleep(self.interval)

    def __enter__(self):
        gc.collect()
        self.peak_rss = self.process.memory_info().rss
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._monitor, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=0.5)
        rss = self.process.memory_info().rss
        if rss > self.peak_rss:
            self.peak_rss = rss

    def get_peak_mib(self):
        return self.peak_rss / (1024 * 1024)


# ==============================================================================
# WORKER ROUTINES (Executed in an isolated fresh subprocess for each single run)
# ==============================================================================
def worker_downcasting(master_parquet_path: str):
    df_raw = pd.read_parquet(master_parquet_path, dtype_backend="numpy_nullable")
    df_unopt = pd.DataFrame()
    for col in MASTER_COLUMNS:
        s = df_raw[col]
        if col in ["order_id", "product_id", "add_to_cart_order", "user_id", "order_number", "aisle_id", "department_id"]:
            df_unopt[col] = s.astype("int64")
        elif col in ["reordered", "order_dow", "order_hour_of_day", "days_since_prior_order"]:
            df_unopt[col] = s.astype("float64")
        else:
            df_unopt[col] = s.astype("object")
            
    mem_unopt_mib = df_unopt.memory_usage(deep=True).sum() / (1024 * 1024)
    del df_raw
    gc.collect()
    
    with SubprocessPeakTracker() as tracker:
        t0 = time.perf_counter()
        df_opt = pd.DataFrame()
        for col in MASTER_COLUMNS:
            df_opt[col] = df_unopt[col].astype(OPTIMIZED_DTYPES[col])
        elapsed = time.perf_counter() - t0
        
    mem_opt_mib = df_opt.memory_usage(deep=True).sum() / (1024 * 1024)
    peak_mib = tracker.get_peak_mib()
    
    res = {
        "mem_unopt_mib": mem_unopt_mib,
        "mem_opt_mib": mem_opt_mib,
        "elapsed_seconds": elapsed,
        "peak_rss_mib": peak_mib,
        "rows": len(df_opt),
        "columns": len(df_opt.columns),
    }
    print("__BENCHMARK_RESULT__" + json.dumps(res))


def worker_write_csv(master_parquet_path: str, target_csv_path: str):
    df = pd.read_parquet(master_parquet_path, dtype_backend="numpy_nullable")
    p_csv = Path(target_csv_path)
    if p_csv.exists():
        p_csv.unlink()
        
    with SubprocessPeakTracker() as tracker:
        t0 = time.perf_counter()
        df.to_csv(p_csv, index=False, encoding="utf-8")
        elapsed = time.perf_counter() - t0
        
    peak_mib = tracker.get_peak_mib()
    disk_mib = p_csv.stat().st_size / (1024 * 1024)
    res = {
        "disk_mib": disk_mib,
        "elapsed_seconds": elapsed,
        "peak_rss_mib": peak_mib,
        "rows": len(df),
        "columns": len(df.columns),
    }
    print("__BENCHMARK_RESULT__" + json.dumps(res))


def worker_write_parquet(master_parquet_path: str, target_parquet_path: str):
    df = pd.read_parquet(master_parquet_path, dtype_backend="numpy_nullable")
    p_parq = Path(target_parquet_path)
    if p_parq.exists():
        p_parq.unlink()
        
    with SubprocessPeakTracker() as tracker:
        t0 = time.perf_counter()
        df.to_parquet(p_parq, compression="snappy", index=False)
        elapsed = time.perf_counter() - t0
        
    peak_mib = tracker.get_peak_mib()
    disk_mib = p_parq.stat().st_size / (1024 * 1024)
    # Giữ nguyên tệp để worker_read_parquet đọc chính tệp đối chứng này!
    res = {
        "disk_mib": disk_mib,
        "elapsed_seconds": elapsed,
        "peak_rss_mib": peak_mib,
        "rows": len(df),
        "columns": len(df.columns),
    }
    print("__BENCHMARK_RESULT__" + json.dumps(res))


def worker_read_csv(target_csv_path: str):
    p_csv = Path(target_csv_path)
    disk_mib = p_csv.stat().st_size / (1024 * 1024)
    
    with SubprocessPeakTracker() as tracker:
        t0 = time.perf_counter()
        df = pd.read_csv(p_csv, dtype=OPTIMIZED_DTYPES, keep_default_na=False, na_values=[""])
        elapsed = time.perf_counter() - t0
        
    peak_mib = tracker.get_peak_mib()
    df_mib = df.memory_usage(deep=True).sum() / (1024 * 1024)
    res = {
        "dataframe_mib": df_mib,
        "disk_mib": disk_mib,
        "elapsed_seconds": elapsed,
        "peak_rss_mib": peak_mib,
        "rows": len(df),
        "columns": len(df.columns),
    }
    print("__BENCHMARK_RESULT__" + json.dumps(res))


def worker_read_parquet(target_parquet_path: str):
    p_parq = Path(target_parquet_path)
    disk_mib = p_parq.stat().st_size / (1024 * 1024)
    
    with SubprocessPeakTracker() as tracker:
        t0 = time.perf_counter()
        df = pd.read_parquet(p_parq, dtype_backend="numpy_nullable")
        # Chuẩn hóa về đúng contract schema để đồng nhất kiểu dữ liệu và bộ nhớ với nhánh CSV
        df = normalize_parquet_dtypes(df)
        elapsed = time.perf_counter() - t0
        
    peak_mib = tracker.get_peak_mib()
    df_mib = df.memory_usage(deep=True).sum() / (1024 * 1024)
    res = {
        "dataframe_mib": df_mib,
        "disk_mib": disk_mib,
        "elapsed_seconds": elapsed,
        "peak_rss_mib": peak_mib,
        "rows": len(df),
        "columns": len(df.columns),
    }
    print("__BENCHMARK_RESULT__" + json.dumps(res))


def worker_merge_workflow(clean_dir_path: str):
    clean_dir = Path(clean_dir_path)
    with SubprocessPeakTracker() as tracker:
        t0 = time.perf_counter()
        df_train = pd.read_csv(
            clean_dir / "order_products__train.csv",
            dtype={"order_id": "int32", "product_id": "int32", "add_to_cart_order": "int16", "reordered": "Int8"},
            keep_default_na=False,
            na_values=[""]
        )
        df_orders = pd.read_csv(
            clean_dir / "orders.csv",
            dtype={"order_id": "int32", "user_id": "int32", "eval_set": "string", "order_number": "int16", "order_dow": "Int8", "order_hour_of_day": "Int8", "days_since_prior_order": "Float32"},
            keep_default_na=False,
            na_values=[""]
        )
        df_products = pd.read_csv(
            clean_dir / "products.csv",
            dtype={"product_id": "int32", "product_name": "string", "aisle_id": "int16", "department_id": "int8"},
            keep_default_na=False,
            na_values=[""]
        )
        df_aisles = pd.read_csv(
            clean_dir / "aisles.csv",
            dtype={"aisle_id": "int16", "aisle": "string"},
            keep_default_na=False,
            na_values=[""]
        )
        df_departments = pd.read_csv(
            clean_dir / "departments.csv",
            dtype={"department_id": "int8", "department": "string"},
            keep_default_na=False,
            na_values=[""]
        )
        
        m1 = df_train.merge(df_orders[df_orders["order_id"].isin(df_train["order_id"])], on="order_id", how="left")
        m2 = m1.merge(df_products, on="product_id", how="left")
        m3 = m2.merge(df_aisles, on="aisle_id", how="left")
        m4 = m3.merge(df_departments, on="department_id", how="left")
        
        for c in ["eval_set", "product_name", "aisle", "department"]:
            m4[c] = m4[c].astype("category")
        elapsed = time.perf_counter() - t0
        
    peak_mib = tracker.get_peak_mib()
    df_mib = m4.memory_usage(deep=True).sum() / (1024 * 1024)
    res = {
        "dataframe_mib": df_mib,
        "elapsed_seconds": elapsed,
        "peak_rss_mib": peak_mib,
        "rows": len(m4),
        "columns": len(m4.columns),
    }
    print("__BENCHMARK_RESULT__" + json.dumps(res))


def worker_parquet_workflow(master_parquet_path: str):
    p_parq = Path(master_parquet_path)
    with SubprocessPeakTracker() as tracker:
        t0 = time.perf_counter()
        df = pd.read_parquet(p_parq, dtype_backend="numpy_nullable")
        df = normalize_parquet_dtypes(df)
        elapsed = time.perf_counter() - t0
        
    peak_mib = tracker.get_peak_mib()
    df_mib = df.memory_usage(deep=True).sum() / (1024 * 1024)
    res = {
        "dataframe_mib": df_mib,
        "elapsed_seconds": elapsed,
        "peak_rss_mib": peak_mib,
        "rows": len(df),
        "columns": len(df.columns),
    }
    print("__BENCHMARK_RESULT__" + json.dumps(res))


# ==============================================================================
# SUBPROCESS EXECUTION RUNNER
# ==============================================================================
def run_worker_in_subprocess(worker_cmd_args: list):
    """Executes a worker in a fresh, isolated Python subprocess and captures JSON output."""
    full_cmd = [sys.executable, str(Path(__file__).resolve()), "--worker"] + worker_cmd_args
    proc = subprocess.run(
        full_cmd, capture_output=True, text=True, encoding="utf-8", check=True)
    out_lines = proc.stdout.splitlines()
    for line in out_lines:
        if line.startswith("__BENCHMARK_RESULT__"):
            json_str = line.replace("__BENCHMARK_RESULT__", "")
            return json.loads(json_str)
    raise RuntimeError(f"Worker did not output benchmark result! Raw output: {proc.stdout}\nStderr: {proc.stderr}")


def verify_readers_equivalence(csv_path: Path, parquet_path: Path):
    """Kiểm chứng độc lập ngoài khoảng thời gian đo: hai cách đọc trả về cùng một dữ liệu chính xác."""
    print("\n--- KIỂM CHỨNG ĐỘC LẬP TÍNH TƯƠNG ĐƯƠNG CỦA HAI PHÉP ĐỌC BENCHMARK ---")
    df_c = pd.read_csv(csv_path, dtype=OPTIMIZED_DTYPES, keep_default_na=False, na_values=[""])
    df_p = pd.read_parquet(parquet_path, dtype_backend="numpy_nullable")
    df_p = normalize_parquet_dtypes(df_p)
    
    assert len(df_c) == len(df_p), f"Lệch số dòng: CSV={len(df_c)}, Parquet={len(df_p)}"
    assert list(df_c.columns) == list(df_p.columns), "Lệch danh sách cột!"
    
    for col in MASTER_COLUMNS:
        dt_c = str(df_c[col].dtype)
        dt_p = str(df_p[col].dtype)
        assert dt_c == dt_p, f"Cột {col}: Lệch dtype giữa CSV ({dt_c}) và Parquet ({dt_p})!"
        
        mask_c = df_c[col].isna()
        mask_p = df_p[col].isna()
        assert mask_c.equals(mask_p), f"Cột {col}: Lệch vị trí null giữa CSV và Parquet!"
        
        if col in ["eval_set", "product_name", "aisle", "department"]:
            vc = df_c.loc[~mask_c, col].astype(str).to_numpy()
            vp = df_p.loc[~mask_p, col].astype(str).to_numpy()
            assert np.array_equal(vc, vp), f"Cột {col}: Lệch giá trị category giữa CSV và Parquet!"
        elif col == "days_since_prior_order":
            vc = df_c.loc[~mask_c, col].to_numpy()
            vp = df_p.loc[~mask_p, col].to_numpy()
            assert np.array_equal(vc, vp), f"Cột {col}: Lệch giá trị float!"
        else:
            vc = df_c.loc[~mask_c, col].to_numpy()
            vp = df_p.loc[~mask_p, col].to_numpy()
            assert np.array_equal(vc, vp), f"Cột {col}: Lệch giá trị int!"
            
    mem_c = df_c.memory_usage(deep=True).sum() / (1024 * 1024)
    mem_p = df_p.memory_usage(deep=True).sum() / (1024 * 1024)
    print(f" [OK] Xác thực hoàn tất: Cả hai phép đọc trả về đúng 100% từng giá trị, cùng vị trí thiếu, cùng 15 dtypes chuẩn.")
    print(f"      Bộ nhớ DataFrame CSV: {mem_c:.2f} MiB | Bộ nhớ DataFrame Parquet: {mem_p:.2f} MiB.")
    del df_c, df_p
    gc.collect()


# ==============================================================================
# MAIN BENCHMARK CONTROLLER (3 Runs with Subprocess Isolation)
# ==============================================================================
def run_benchmark_suite(clean_dir: Path, output_dir: Path, master_parquet: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    bench_csv = output_dir / "master_benchmark.csv"
    bench_parquet = output_dir / "master_benchmark.parquet"
    
    # 0. Đảm bảo file CSV đối chứng được tạo trước nếu chưa có
    if not bench_csv.exists():
        print(f"Khởi tạo tệp Master CSV đối chứng: {bench_csv.name}...")
        df_init = pd.read_parquet(master_parquet, dtype_backend="numpy_nullable")
        df_init.to_csv(bench_csv, index=False, encoding="utf-8")
        del df_init
        gc.collect()
        
    benchmark_rows = []
    
    # --------------------------------------------------------------------------
    # THỰC NGHIỆM A: Bộ nhớ trước–sau tối ưu Dtype
    # --------------------------------------------------------------------------
    print("\n--- [A] THỰC NGHIỆM TỐI ƯU KIỂU DỮ LIỆU (3 lượt tiến trình con độc lập) ---")
    downcast_runs = []
    for r in range(1, 4):
        print(f" * Lượt {r}/3: Khởi chạy worker tiến trình con...")
        res = run_worker_in_subprocess(["downcasting", str(master_parquet)])
        downcast_runs.append(res)
        print(f"   -> Lượt {r}: RAM chưa tối ưu (reconstructed)={res['mem_unopt_mib']:.2f} MiB | RAM tối ưu={res['mem_opt_mib']:.2f} MiB | Thời gian={res['elapsed_seconds']:.4f}s | Peak RSS={res['peak_rss_mib']:.2f} MiB")

    # Ghi nhận trạng thái reconstructed_unoptimized
    for r_idx, res in enumerate(downcast_runs, 1):
        benchmark_rows.append({
            "experiment": "A_Dtype_Downcasting",
            "state": "reconstructed_unoptimized",
            "operation": "in_memory_profile",
            "run_id": str(r_idx),
            "rows": res["rows"],
            "columns": res["columns"],
            "dataframe_mib": round(res["mem_unopt_mib"], 2),
            "peak_rss_mib": "",  # Không áp dụng cho static profile
            "disk_mib": "",       # Không áp dụng
            "elapsed_seconds": "" # Không áp dụng
        })
    benchmark_rows.append({
        "experiment": "A_Dtype_Downcasting",
        "state": "reconstructed_unoptimized",
        "operation": "in_memory_profile",
        "run_id": "median",
        "rows": downcast_runs[0]["rows"],
        "columns": downcast_runs[0]["columns"],
        "dataframe_mib": round(float(np.median([r["mem_unopt_mib"] for r in downcast_runs])), 2),
        "peak_rss_mib": "",
        "disk_mib": "",
        "elapsed_seconds": ""
    })

    # Ghi nhận trạng thái optimized (downcast execution)
    for r_idx, res in enumerate(downcast_runs, 1):
        benchmark_rows.append({
            "experiment": "A_Dtype_Downcasting",
            "state": "optimized",
            "operation": "downcast_execution",
            "run_id": str(r_idx),
            "rows": res["rows"],
            "columns": res["columns"],
            "dataframe_mib": round(res["mem_opt_mib"], 2),
            "peak_rss_mib": round(res["peak_rss_mib"], 2),
            "disk_mib": "",
            "elapsed_seconds": round(res["elapsed_seconds"], 4)
        })
    benchmark_rows.append({
        "experiment": "A_Dtype_Downcasting",
        "state": "optimized",
        "operation": "downcast_execution",
        "run_id": "median",
        "rows": downcast_runs[0]["rows"],
        "columns": downcast_runs[0]["columns"],
        "dataframe_mib": round(float(np.median([r["mem_opt_mib"] for r in downcast_runs])), 2),
        "peak_rss_mib": round(float(np.median([r["peak_rss_mib"] for r in downcast_runs])), 2),
        "disk_mib": "",
        "elapsed_seconds": round(float(np.median([r["elapsed_seconds"] for r in downcast_runs])), 4)
    })

    # --------------------------------------------------------------------------
    # THỰC NGHIỆM B: So sánh Định dạng và I/O (CSV vs Parquet)
    # --------------------------------------------------------------------------
    print("\n--- [B] THỰC NGHIỆM ĐỊNH DẠNG VÀ I/O (3 lượt tiến trình con độc lập) ---")
    
    # 1. Ghi CSV
    write_csv_runs = []
    for r in range(1, 4):
        print(f" * [Ghi CSV] Lượt {r}/3...")
        res = run_worker_in_subprocess(["write_csv", str(master_parquet), str(bench_csv)])
        write_csv_runs.append(res)
        benchmark_rows.append({
            "experiment": "B_Format_and_IO",
            "state": "csv_benchmark",
            "operation": "write_disk",
            "run_id": str(r),
            "rows": res["rows"],
            "columns": res["columns"],
            "dataframe_mib": "",
            "peak_rss_mib": round(res["peak_rss_mib"], 2),
            "disk_mib": round(res["disk_mib"], 2),
            "elapsed_seconds": round(res["elapsed_seconds"], 4)
        })
    benchmark_rows.append({
        "experiment": "B_Format_and_IO",
        "state": "csv_benchmark",
        "operation": "write_disk",
        "run_id": "median",
        "rows": write_csv_runs[0]["rows"],
        "columns": write_csv_runs[0]["columns"],
        "dataframe_mib": "",
        "peak_rss_mib": round(float(np.median([r["peak_rss_mib"] for r in write_csv_runs])), 2),
        "disk_mib": round(float(np.median([r["disk_mib"] for r in write_csv_runs])), 2),
        "elapsed_seconds": round(float(np.median([r["elapsed_seconds"] for r in write_csv_runs])), 4)
    })

    # 2. Ghi Parquet (ghi ra bench_parquet và giữ lại để đo đọc)
    write_parquet_runs = []
    for r in range(1, 4):
        print(f" * [Ghi Parquet] Lượt {r}/3...")
        res = run_worker_in_subprocess(["write_parquet", str(master_parquet), str(bench_parquet)])
        write_parquet_runs.append(res)
        benchmark_rows.append({
            "experiment": "B_Format_and_IO",
            "state": "parquet_snappy",
            "operation": "write_disk",
            "run_id": str(r),
            "rows": res["rows"],
            "columns": res["columns"],
            "dataframe_mib": "",
            "peak_rss_mib": round(res["peak_rss_mib"], 2),
            "disk_mib": round(res["disk_mib"], 2),
            "elapsed_seconds": round(res["elapsed_seconds"], 4)
        })
    benchmark_rows.append({
        "experiment": "B_Format_and_IO",
        "state": "parquet_snappy",
        "operation": "write_disk",
        "run_id": "median",
        "rows": write_parquet_runs[0]["rows"],
        "columns": write_parquet_runs[0]["columns"],
        "dataframe_mib": "",
        "peak_rss_mib": round(float(np.median([r["peak_rss_mib"] for r in write_parquet_runs])), 2),
        "disk_mib": round(float(np.median([r["disk_mib"] for r in write_parquet_runs])), 2),
        "elapsed_seconds": round(float(np.median([r["elapsed_seconds"] for r in write_parquet_runs])), 4)
    })

    # 3. Đọc CSV (đọc chính bench_csv)
    read_csv_runs = []
    for r in range(1, 4):
        print(f" * [Đọc CSV] Lượt {r}/3...")
        res = run_worker_in_subprocess(["read_csv", str(bench_csv)])
        read_csv_runs.append(res)
        benchmark_rows.append({
            "experiment": "B_Format_and_IO",
            "state": "csv_benchmark",
            "operation": "read_disk",
            "run_id": str(r),
            "rows": res["rows"],
            "columns": res["columns"],
            "dataframe_mib": round(res["dataframe_mib"], 2),
            "peak_rss_mib": round(res["peak_rss_mib"], 2),
            "disk_mib": round(res["disk_mib"], 2),
            "elapsed_seconds": round(res["elapsed_seconds"], 4)
        })
    benchmark_rows.append({
        "experiment": "B_Format_and_IO",
        "state": "csv_benchmark",
        "operation": "read_disk",
        "run_id": "median",
        "rows": read_csv_runs[0]["rows"],
        "columns": read_csv_runs[0]["columns"],
        "dataframe_mib": round(float(np.median([r["dataframe_mib"] for r in read_csv_runs])), 2),
        "peak_rss_mib": round(float(np.median([r["peak_rss_mib"] for r in read_csv_runs])), 2),
        "disk_mib": round(float(np.median([r["disk_mib"] for r in read_csv_runs])), 2),
        "elapsed_seconds": round(float(np.median([r["elapsed_seconds"] for r in read_csv_runs])), 4)
    })

    # 4. Đọc Parquet (đọc chính bench_parquet vừa ghi)
    read_parquet_runs = []
    for r in range(1, 4):
        print(f" * [Đọc Parquet] Lượt {r}/3...")
        res = run_worker_in_subprocess(["read_parquet", str(bench_parquet)])
        read_parquet_runs.append(res)
        benchmark_rows.append({
            "experiment": "B_Format_and_IO",
            "state": "parquet_snappy",
            "operation": "read_disk",
            "run_id": str(r),
            "rows": res["rows"],
            "columns": res["columns"],
            "dataframe_mib": round(res["dataframe_mib"], 2),
            "peak_rss_mib": round(res["peak_rss_mib"], 2),
            "disk_mib": round(res["disk_mib"], 2),
            "elapsed_seconds": round(res["elapsed_seconds"], 4)
        })
    benchmark_rows.append({
        "experiment": "B_Format_and_IO",
        "state": "parquet_snappy",
        "operation": "read_disk",
        "run_id": "median",
        "rows": read_parquet_runs[0]["rows"],
        "columns": read_parquet_runs[0]["columns"],
        "dataframe_mib": round(float(np.median([r["dataframe_mib"] for r in read_parquet_runs])), 2),
        "peak_rss_mib": round(float(np.median([r["peak_rss_mib"] for r in read_parquet_runs])), 2),
        "disk_mib": round(float(np.median([r["disk_mib"] for r in read_parquet_runs])), 2),
        "elapsed_seconds": round(float(np.median([r["elapsed_seconds"] for r in read_parquet_runs])), 4)
    })

    # Kiểm chứng độc lập tính tương đương của hai phép đọc CSV vs Parquet
    verify_readers_equivalence(bench_csv, bench_parquet)

    # --------------------------------------------------------------------------
    # THỰC NGHIỆM C: So sánh Quy trình Sử dụng
    # --------------------------------------------------------------------------
    print("\n--- [C] THỰC NGHIỆM QUY TRÌNH SỬ DỤNG (3 lượt tiến trình con độc lập) ---")
    
    # 1. Quy trình nạp 5 CSV và ghép
    merge_wf_runs = []
    for r in range(1, 4):
        print(f" * [Quy trình 1: Đọc 5 CSV & Ghép] Lượt {r}/3...")
        res = run_worker_in_subprocess(["merge_workflow", str(clean_dir)])
        merge_wf_runs.append(res)
        benchmark_rows.append({
            "experiment": "C_Workflow_Comparison",
            "state": "read_5_csv_and_merge",
            "operation": "full_pipeline",
            "run_id": str(r),
            "rows": res["rows"],
            "columns": res["columns"],
            "dataframe_mib": round(res["dataframe_mib"], 2),
            "peak_rss_mib": round(res["peak_rss_mib"], 2),
            "disk_mib": "",
            "elapsed_seconds": round(res["elapsed_seconds"], 4)
        })
    benchmark_rows.append({
        "experiment": "C_Workflow_Comparison",
        "state": "read_5_csv_and_merge",
        "operation": "full_pipeline",
        "run_id": "median",
        "rows": merge_wf_runs[0]["rows"],
        "columns": merge_wf_runs[0]["columns"],
        "dataframe_mib": round(float(np.median([r["dataframe_mib"] for r in merge_wf_runs])), 2),
        "peak_rss_mib": round(float(np.median([r["peak_rss_mib"] for r in merge_wf_runs])), 2),
        "disk_mib": "",
        "elapsed_seconds": round(float(np.median([r["elapsed_seconds"] for r in merge_wf_runs])), 4)
    })

    # 2. Quy trình nạp trực tiếp Master Parquet
    parquet_wf_runs = []
    for r in range(1, 4):
        print(f" * [Quy trình 2: Đọc Master Parquet] Lượt {r}/3...")
        res = run_worker_in_subprocess(["parquet_workflow", str(master_parquet)])
        parquet_wf_runs.append(res)
        benchmark_rows.append({
            "experiment": "C_Workflow_Comparison",
            "state": "read_master_parquet",
            "operation": "full_pipeline",
            "run_id": str(r),
            "rows": res["rows"],
            "columns": res["columns"],
            "dataframe_mib": round(res["dataframe_mib"], 2),
            "peak_rss_mib": round(res["peak_rss_mib"], 2),
            "disk_mib": "",
            "elapsed_seconds": round(res["elapsed_seconds"], 4)
        })
    benchmark_rows.append({
        "experiment": "C_Workflow_Comparison",
        "state": "read_master_parquet",
        "operation": "full_pipeline",
        "run_id": "median",
        "rows": parquet_wf_runs[0]["rows"],
        "columns": parquet_wf_runs[0]["columns"],
        "dataframe_mib": round(float(np.median([r["dataframe_mib"] for r in parquet_wf_runs])), 2),
        "peak_rss_mib": round(float(np.median([r["peak_rss_mib"] for r in parquet_wf_runs])), 2),
        "disk_mib": "",
        "elapsed_seconds": round(float(np.median([r["elapsed_seconds"] for r in parquet_wf_runs])), 4)
    })

    # --------------------------------------------------------------------------
    # XUẤT BẢNG DATA_BENCHMARK.CSV VÀ DATA_BENCHMARK_METADATA.JSON
    # --------------------------------------------------------------------------
    df_benchmark = pd.DataFrame(benchmark_rows)
    cols_order = [
        "experiment", "state", "operation", "run_id",
        "rows", "columns", "dataframe_mib", "peak_rss_mib", "disk_mib", "elapsed_seconds"
    ]
    df_benchmark = df_benchmark[cols_order]
    
    # Xuất ra 2 vị trí theo yêu cầu
    out_csv_1 = output_dir / "data_benchmark.csv"
    out_csv_2 = clean_dir / "data_benchmark.csv"
    df_benchmark.to_csv(out_csv_1, index=False, encoding="utf-8-sig")
    df_benchmark.to_csv(out_csv_2, index=False, encoding="utf-8-sig")
    print(f"\n[OK] Đã xuất báo cáo chuẩn hóa: {out_csv_1}")
    print(f"[OK] Đã xuất báo cáo chuẩn hóa: {out_csv_2}")
    
    # Metadata file
    metadata = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "methodology": {
            "iterations_per_experiment": 3,
            "aggregation": "median",
            "isolation": "Fresh Python process per run isolates interpreter state and heap history; OS page cache remains shared.",
            "rss_tracking": "Sampled process RSS with a requested 5ms polling interval; short peaks may be missed and scheduling can delay samples.",
            "null_handling": "Uniform rule across all CSV readers: keep_default_na=False, na_values=[''].",
            "schema_normalization": "Parquet reader output normalized to identical contract dtypes as CSV reader, ensuring strict apples-to-apples comparison.",
            "units": {
                "memory_and_disk": "MiB (1024^2 bytes)",
                "time": "seconds (wall-clock time via time.perf_counter())"
            }
        },
        "baseline_explanation": {
            "reconstructed_unoptimized": "Baseline kiểu rộng được dựng lại (reconstructed unoptimized baseline) bằng cách ép các cột số nguyên sang int64, số thực sang float64 và chuỗi sang object trên 1.384.617 dòng của bảng master, dùng để đo lường mức tiết kiệm bộ nhớ do hợp đồng downcasting PRJ-08 mang lại."
        },
        "environment": {
            "os": f"{platform.system()} {platform.release()} ({platform.version()})",
            "processor": platform.processor(),
            "cpu_count_logical": psutil.cpu_count(logical=True),
            "cpu_count_physical": psutil.cpu_count(logical=False),
            "total_ram_gib": round(psutil.virtual_memory().total / (1024**3), 2),
            "python_version": sys.version.split()[0],
            "pandas_version": pd.__version__,
            "pyarrow_version": pa.__version__,
            "psutil_version": psutil.__version__
        },
        "cache_conditions": {
            "os_page_cache": "Warm cache: On Windows OS, operating system file system page cache is managed by OS kernel and remains active across consecutive runs without administrator flushing. Measurements represent warm-cache disk I/O.",
            "interpretation_rule": "Results represent warm-cache operating environment; no cold-cache assumptions are asserted."
        },
        "timing_scopes": {
            "A_Dtype_Downcasting": "Starts immediately before column casting loop; ends immediately upon completing full 15-column downcast.",
            "B_Format_and_IO:write_disk": "Starts immediately before df.to_csv() / df.to_parquet(); ends immediately upon file handle release.",
            "B_Format_and_IO:read_disk": "Starts immediately before pd.read_csv() / pd.read_parquet(); ends immediately upon DataFrame object instantiation and dtype contract normalization.",
            "C_Workflow_Comparison:read_5_csv_and_merge": "Starts immediately before loading 5 clean CSVs; ends immediately upon completing 4 left joins and categorical casting in memory.",
            "C_Workflow_Comparison:read_master_parquet": "Starts immediately before pd.read_parquet(); ends immediately upon DataFrame instantiation and normalization."
        },
        "files_analyzed": {
            "path_base": "thesis directory (parent of scripts/)",
            "master_parquet": report_path(master_parquet),
            "master_parquet_size_mib": round(master_parquet.stat().st_size / (1024*1024), 2),
            "master_benchmark_csv": report_path(bench_csv),
            "master_benchmark_csv_size_mib": round(bench_csv.stat().st_size / (1024*1024), 2),
            "master_benchmark_parquet": report_path(bench_parquet),
            "master_benchmark_parquet_size_mib": round(bench_parquet.stat().st_size / (1024*1024), 2)
        }
    }
    
    meta_json_1 = output_dir / "data_benchmark_metadata.json"
    meta_json_2 = clean_dir / "data_benchmark_metadata.json"
    with open(meta_json_1, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    with open(meta_json_2, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"[OK] Đã xuất siêu dữ liệu benchmark: {meta_json_1}")
    print(f"[OK] Đã xuất siêu dữ liệu benchmark: {meta_json_2}")
    
    print("\n=== HOÀN TẤT ĐO LƯỜNG 3 LƯỢT ĐỘC LẬP THEO QUY ĐỊNH ===")


# ==============================================================================
# ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    args = cli_args
    
    if args.worker:
        task = args.worker[0]
        params = args.worker[1:]
        if task == "downcasting":
            worker_downcasting(params[0])
        elif task == "write_csv":
            worker_write_csv(params[0], params[1])
        elif task == "write_parquet":
            worker_write_parquet(params[0], params[1])
        elif task == "read_csv":
            worker_read_csv(params[0])
        elif task == "read_parquet":
            worker_read_parquet(params[0])
        elif task == "merge_workflow":
            worker_merge_workflow(params[0])
        elif task == "parquet_workflow":
            worker_parquet_workflow(params[0])
        else:
            raise ValueError(f"Unknown worker task: {task}")
        sys.exit(0)
    else:
        clean_dir = args.clean_dir
        output_dir = args.output_dir
        master_parquet = clean_dir / "master_train.parquet"
        run_benchmark_suite(clean_dir, output_dir, master_parquet)
