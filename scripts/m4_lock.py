"""Chương 4, giai đoạn C: chọn phương pháp chính trên validation và ghi lock.json (khóa trước khi mở test).

Chọn Recall@10 validation lớn nhất; hòa trong dung sai thì chi phí suy luận thấp hơn, rồi theo thứ tự
Popularity, Rules, LR, RF. lock.json ghi cấu hình, ngưỡng F1 và SHA-256 mọi tệp mà bước test phải kiểm lại.

ĐỌC NHANH: giai đoạn C. Chọn phương pháp chính trên validation rồi KHÓA bằng lock.json trước khi ai mở test.
  lock.json ghi cấu hình, ngưỡng F1 và SHA-256 của mọi tệp mà bước test phải kiểm lại; khóa xong thì không sửa code, config hay mô hình.
  Cổng của m4_test.py đòi thêm hash mã nguồn (REQUIRED) và approvals đủ hai người. approvals chỉ là true khi truyền --approve:
    python scripts/m4_lock.py                        # bản nháp, cả hai approvals = false, test chưa chạy được
    python scripts/m4_lock.py --approve Phong Vuong  # chỉ khi cả hai đã duyệt lock; từ chối nếu test đã bắt đầu
"""
import argparse
from datetime import datetime

import pandas as pd

from m4_common import CONFIG, HASHES, config
from project_io import check_hashes, path, sha256, write_json

ORDER = ["Popularity", "Rules", "LR", "RF"]
# Mã và nguồn mà cổng của m4_test.py bắt buộc phải có trong khóa (cùng danh sách CODE_FILES và các tệp nguồn của nó).
REQUIRED = ["scripts/m4_test.py", "scripts/m4_common.py", "scripts/m4_classifier.py", "scripts/project_io.py",
            "requirements.txt", "configs/m2_plot_style.json", HASHES, "DATA/Data đã làm sạch/master_train.parquet"]


def main(approved):
    cfg = config()
    record = check_hashes(HASHES)
    report = path(cfg["report_dir"])
    if (report / "test_started.json").exists():
        raise SystemExit("Test đã bắt đầu: không ghi lại lock.json.")
    methods = pd.read_csv(report / "validation_methods.csv", keep_default_na=False)
    # Chọn phương pháp chính: Recall@10 lớn nhất; hòa trong dung sai thì suy luận nhanh hơn, rồi theo thứ tự cố định.
    tied = methods[methods.recall_at_10 >= methods.recall_at_10.max() - cfg["tie_tolerance"]]
    chosen = tied.assign(order=tied.method.map(ORDER.index)).sort_values(["inference_seconds", "order"]).method.iloc[0]
    classifiers = pd.read_csv(report / "classifier_validation.csv").set_index("method")
    # Ghi lock.json kèm SHA-256 mọi tệp mà bước test phải kiểm lại.
    files = [CONFIG, *REQUIRED, *record["files"], (report / "validation_methods.csv").relative_to(path(".")).as_posix()]
    write_json(report / "lock.json", {
        "locked_at": datetime.now().isoformat(timespec="seconds"), "main_method": chosen,
        "stage_A": record["stage_A"], "validation": methods.set_index("method").to_dict("index"),
        "f1_threshold": classifiers.threshold.to_dict(), "approvals": {n: n in approved for n in ("Phong", "Vuong")},
        "files": {f: sha256(path(f)) for f in files}})
    print(methods.to_string(index=False), f"\nPhương pháp chính: {chosen}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approve", nargs="*", choices=["Phong", "Vuong"], default=[])
    main(parser.parse_args().approve)
