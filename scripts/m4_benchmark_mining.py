"""Chương 4: benchmark Apriori và FP-Growth trên cùng ma trận, ngưỡng và max_len.

Mỗi lượt chạy trong một tiến trình con mới (không chạy chồng); đo riêng thời gian dựng
ma trận, khai phá, sinh luật và RAM đỉnh tiến trình (psutil). Quá timeout ghi "timeout",
tiến trình lỗi ghi "error". Tương đương: cùng tập itemset, support lệch <= 1e-12.
Mỗi cấu hình ghi tệp riêng mining_benchmark_<cấu hình>.csv và itemset_equivalence_<cấu hình>.json.

  python scripts/m4_benchmark_mining.py               # cấu hình trial trong config
  python scripts/m4_benchmark_mining.py 1000 20 2     # top_n min_count max_len

ĐỌC NHANH: so Apriori với FP-Growth. Mỗi lượt chạy trong MỘT tiến trình con mới để RAM đo được không bị lượt trước làm nhiễu.
  Kết quả: thời gian từng bước, RAM đỉnh, và kiểm tra hai thuật toán cho cùng tập itemset (support lệch <= 1e-12).
"""
import json
import subprocess
import sys
import time

import pandas as pd
import psutil

from m4_common import basket_matrix, catalog, config, itemset_signature, mine, rules, worst_support_gap
from project_io import check_hashes, path, write_frame, write_json

TOLERANCE = 1e-12


# Tiến trình con: chạy MỘT thuật toán một lần, đo thời gian từng bước và RAM đỉnh, in kết quả JSON.
def worker(algorithm, top_n, min_count, max_len):
    reference = pd.read_parquet(path("DATA/Data phai sinh/M2/reference.parquet"),
                                columns=["order_id", "product_id", "department_id"])
    products = catalog(reference).product_id[:top_n]
    t0 = time.perf_counter()
    matrix = basket_matrix(reference, products)
    t1 = time.perf_counter()
    itemsets = mine(matrix, algorithm, min_count, max_len)
    t2 = time.perf_counter()
    found = rules(itemsets, len(matrix), min(config()["grid_A"]["min_confidence"]))
    t3 = time.perf_counter()
    memory = psutil.Process().memory_info()
    print(json.dumps({"matrix_s": t1 - t0, "mining_s": t2 - t1, "rules_s": t3 - t2,
                      "peak_mib": getattr(memory, "peak_wset", memory.rss) / 2**20,
                      "itemsets": len(itemsets), "rules": len(found),
                      "support": [[list(k), v] for k, v in itemset_signature(itemsets).items()]}))


# Tiến trình chính: mỗi lượt gọi một tiến trình con mới, gom kết quả rồi so tương đương itemset.
def main(top_n, min_count, max_len):
    cfg = config()
    check_hashes()
    rows, supports = [], []
    for algorithm in ("apriori", "fpgrowth"):
        for run in range(1, cfg["benchmark"]["runs"] + 1):
            row = {"algorithm": algorithm, "run": run, "top_n": top_n,
                   "min_count": min_count, "max_len": max_len, "status": "ok"}
            try:
                out = subprocess.run([sys.executable, __file__, "--worker", algorithm,
                                      str(top_n), str(min_count), str(max_len)],
                                     capture_output=True, text=True, check=True,
                                     timeout=cfg["benchmark"]["timeout_s"])
                result = json.loads(out.stdout.strip().splitlines()[-1])
                supports.append((algorithm, {tuple(k): v for k, v in result.pop("support")}))
                row.update(result)
            except subprocess.TimeoutExpired:
                row["status"] = "timeout"
            except subprocess.CalledProcessError as error:
                row.update(status="error", error=error.stderr.strip()[-300:])
            rows.append(row)
            print({k: v for k, v in row.items() if k != "error"})
    gap = (worst_support_gap([s for _, s in supports])   # mọi lượt thành công của cả hai thuật toán
           if {a for a, _ in supports} == {"apriori", "fpgrowth"} else None)
    tag = f"N{top_n}_c{min_count}_l{max_len}"
    report = path(cfg["report_dir"])
    write_frame(report / f"mining_benchmark_{tag}.csv", pd.DataFrame(rows))
    write_json(report / f"itemset_equivalence_{tag}.json", {
        "config": {"top_n": top_n, "min_count": min_count, "max_len": max_len},
        "same_itemsets": gap is not None, "max_support_gap": gap, "tolerance": TOLERANCE,
        "equivalent": gap is not None and gap <= TOLERANCE,  # False khi thiếu lượt thành công
        "python": sys.version.split()[0], "pandas": pd.__version__,
        "mlxtend": __import__("mlxtend").__version__, "psutil": psutil.__version__})


if __name__ == "__main__":
    if sys.argv[1:2] == ["--worker"]:
        worker(sys.argv[2], *map(int, sys.argv[3:6]))
    else:
        trial = config()["benchmark"]["trial"]
        args = list(map(int, sys.argv[1:4])) or [trial["top_n"], trial["min_count"], trial["max_len"]]
        main(*args)
