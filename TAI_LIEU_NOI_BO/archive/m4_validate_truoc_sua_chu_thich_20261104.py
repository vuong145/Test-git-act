"""Chương 4: giai đoạn A (danh mục và luật) và B (LR, RF) trên validation; test không được đọc.

Giai đoạn A chọn (N, min_count, max_len, min_confidence) bằng Recall@10 của Rules; giai đoạn B gọi
fit_grid của m4_classifier.py. Đầu ra: M4/features_fit.parquet, pipeline_lr/rf.joblib và các bảng trong
BAO CAO/Bao cao mo hinh/. Với --pilot chỉ dùng pilot_baskets giỏ fit và validation, ghi vào thư mục con pilot/.

  python scripts/m4_validate.py [--pilot]

ĐỌC NHANH (vấn đáp): chọn cấu hình bằng VALIDATION, test không được đọc.
  Giai đoạn A: 24 cấu hình luật, chọn bằng Recall@10 của Rules (hòa trong dung sai 0,002 thì chọn cấu hình đơn giản hơn).
  Giai đoạn B: với cấu hình A đã chọn, dựng đặc trưng cho fit (20 mẫu âm/giỏ), chọn lưới cho LR và RF.
  Sau đó: ngưỡng F1, phép bỏ nhóm đặc trưng (no_rules, no_department), ghi bảng và hash. Giai đoạn C nằm ở m4_lock.py.
"""
import argparse
import time

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

from m4_classifier import CATEGORY, GRIDS, NUMERIC, build_pipeline, fit_grid
from m4_common import (HASHES, M, check_mask, config, context, evaluate, index_rules, make_batches,
                       sample_negatives)
from m4_test import best_f1_threshold, classification_metrics
from project_io import atomic_write, check_hashes, path, write_frame, write_hashes

FEATURES = NUMERIC + CATEGORY
DATA = "DATA/Data phai sinh/M4"


# GIAI ĐOẠN A: với mỗi bộ luật, chấm Recall@10 của Rules (kèm Popularity và trần) trên validation.
def stage_a(val, ranked, rules, dept, cfg):
    """Một dòng mỗi cấu hình (N, min_count, max_len, min_confidence); Recall@10 của Rules và của Popularity."""
    rows, size, ks = [], cfg["batch_size"], cfg["k_values"]
    for (n, count, length), group in rules.groupby(["top_n", "min_count", "max_len"]):
        ctx = context(ranked, n, dept)
        recall = {name: [] for name in ["pop", *cfg["grid_A"]["min_confidence"], "ceiling"]}
        for part, X in make_batches(val, ctx, index_rules(group, ctx), size):
            recall["pop"].append(evaluate(part, X, X.candidate_popularity, ks=ks))
            recall["ceiling"].append(recall["pop"][-1]["R@10_ceiling"])
            for c in cfg["grid_A"]["min_confidence"]:
                conf = X.max_rule_confidence.where(X.max_rule_confidence >= c, 0)
                recall[c].append(evaluate(part, X, conf, X.candidate_popularity, ks=ks)["R@10"])
        pop = pd.concat(recall["pop"])["R@10"].mean()
        for c in cfg["grid_A"]["min_confidence"]:
            rows.append(dict(top_n=n, min_count=count, max_len=length, min_confidence=c,
                             rules=int((group.confidence >= c).sum()), popularity_recall_at_10=pop,
                             rules_recall_at_10=pd.concat(recall[c]).mean(),
                             ceiling_recall_at_10=pd.concat(recall["ceiling"]).mean()))
        print(rows[-1], flush=True)
    return pd.DataFrame(rows)


# Chọn bộ luật tốt nhất; hòa trong dung sai thì ưu tiên cấu hình nhỏ và đơn giản hơn.
def choose_a(table, tolerance):
    """Recall@10 lớn nhất; hòa (trong dung sai) thì N nhỏ, min_count lớn, max_len nhỏ, min_confidence lớn."""
    tied = table[table.rules_recall_at_10 >= table.rules_recall_at_10.max() - tolerance]
    first = tied.sort_values(["top_n", "min_count", "max_len", "min_confidence"],
                             ascending=[True, False, True, False]).index[0]
    return table.loc[[first]].to_dict("records")[0]


# Chấm toàn bộ ứng viên theo lô bằng một mô hình đã huấn luyện.
def classify(batches, model, ks):
    """Chấm toàn bộ ứng viên theo lô: chỉ số theo giỏ, nhãn, điểm và thời gian (dự đoán + xếp hạng)."""
    start, metrics, y, scores = time.perf_counter(), [], [], []
    for part, X in batches:
        scores.append(model.predict_proba(X[FEATURES])[:, 1])
        metrics.append(evaluate(part, X, scores[-1], ks=ks))
        y.append(X.y.to_numpy())
    return pd.concat(metrics, ignore_index=True), np.concatenate(y), np.concatenate(scores), time.perf_counter() - start


# main: nạp dữ liệu -> giai đoạn A -> dựng đặc trưng -> giai đoạn B -> ngưỡng F1, bỏ nhóm đặc trưng -> ghi bảng và hash.
def main(pilot):
    cfg, ks = config(), config()["k_values"]
    check_hashes()
    record = check_hashes(HASHES)
    check_mask(record, cfg)
    data, report = path(cfg["data_dir"]), path(cfg["report_dir"])
    masked = pd.read_parquet(data / "masked_baskets.parquet")
    # Khối 1: nạp giỏ fit/validation (test không được nạp).
    masked = masked[masked.eligible & masked.split.isin(["fit", "validation"])]  # test không được nạp
    fit, val = (masked[masked.split == s] for s in ("fit", "validation"))
    ranked, rules = pd.read_parquet(data / "catalog.parquet"), pd.read_parquet(data / "rules_grid.parquet")
    master = pd.read_parquet(path("DATA/Data đã làm sạch/master_train.parquet"), columns=["product_id", "department_id"])
    dept = np.zeros(M, dtype=int)
    dept[master.product_id.to_numpy()] = master.department_id.to_numpy()
    if pilot:
        fit, val = fit.head(cfg["pilot_baskets"]), val.head(cfg["pilot_baskets"])
        data, report = data / "pilot", report / "pilot"
    # Khối 2 (giai đoạn A): chấm lưới luật và chọn cấu hình.
    table = stage_a(val, ranked, rules, dept, cfg)
    best = choose_a(table, cfg["tie_tolerance"])
    key = ["top_n", "min_count", "max_len", "min_confidence"]
    write_frame(report / "validation_grid_A.csv", table.assign(selected=(table[key] == pd.Series(best)[key]).all(axis=1)))
    n = best["top_n"]
    chosen = rules[(rules.top_n == n) & (rules.min_count == best["min_count"]) & (rules.max_len == best["max_len"])
                   & (rules.confidence >= best["min_confidence"])]
    # Khối 3: dựng đặc trưng cho fit (lấy mẫu âm 20/giỏ) và cho validation (giữ mọi ứng viên).
    ctx = context(ranked, n, dept)
    idx = index_rules(chosen, ctx)
    train = pd.concat([sample_negatives(p, X, cfg["negatives_per_basket"], cfg["seeds"]["negative"])
                       for p, X in make_batches(fit, ctx, idx, cfg["batch_size"])], ignore_index=True)
    write_frame(data / "features_fit.parquet", train[["order_id", "product_id", "y", *FEATURES]])
    write_frame(report / "feature_correlation.csv", train[NUMERIC].corr("spearman").rename_axis("feature").reset_index())
    batches = list(make_batches(val, ctx, idx, cfg["batch_size"]))
    x_fit, y_fit = train[FEATURES], train.y.to_numpy().astype(int)
    print(f"A: {best}; fit {len(train)} dòng, dương {y_fit.mean():.4f}", flush=True)

    def callback(model):
        metrics, _, _, seconds = classify(batches, model, ks)
        print(f"  {model['model']}: R@10={metrics['R@10'].mean():.4f} {seconds:.0f}s", flush=True)
        return {"recall_at_10": float(metrics["R@10"].mean()), "inference_seconds": seconds}

    # Khối 4: chấm Popularity và Rules; rồi với LR và RF: chọn lưới (giai đoạn B), ngưỡng F1, phép bỏ nhóm đặc trưng.
    pipelines, grids, per_basket, methods, scored = {}, [], [], [], {}
    for name, keys in [("Popularity", lambda X: [X.candidate_popularity]),
                       ("Rules", lambda X: [X.max_rule_confidence, X.candidate_popularity])]:
        start = time.perf_counter()
        metrics = pd.concat([evaluate(p, X, *keys(X), ks=ks) for p, X in batches], ignore_index=True)
        per_basket.append(metrics.assign(method=name))
        methods.append(dict(method=name, params="", recall_at_10=metrics["R@10"].mean(),
                            inference_seconds=time.perf_counter() - start))
    ablation = []
    for method in GRIDS:
        winner, grid = fit_grid(x_fit, y_fit, method, callback, cfg["tie_tolerance"])
        params = GRIDS[method][int(grid.selected.to_numpy().argmax())]
        metrics, y, scores, seconds = classify(batches, winner, ks)
        threshold = best_f1_threshold(y, scores)
        scored[method] = dict(method=method, **params, **classification_metrics(y, scores, threshold))
        per_basket.append(metrics.assign(method=method))
        methods.append(dict(method=method, params=str(params), recall_at_10=metrics["R@10"].mean(), inference_seconds=seconds))
        ablation.append(dict(method=method, group="full", recall_at_10=metrics["R@10"].mean(),
                             average_precision=average_precision_score(y, scores)))
        for group in ("no_rules", "no_department"):
            m, y, scores, _ = classify(batches, build_pipeline(method, params, group).fit(x_fit, y_fit), ks)
            ablation.append(dict(method=method, group=group, recall_at_10=m["R@10"].mean(),
                                 average_precision=average_precision_score(y, scores)))
        grids.append(grid)
        atomic_write(data / f"pipeline_{method.lower()}.joblib", lambda p: joblib.dump(winner, p))
    # Khối 5: ghi các bảng kết quả và hash (chạy thử --pilot thì không ghi hash).
    write_frame(report / "validation_grid_B.csv", pd.concat(grids, ignore_index=True))
    write_frame(report / "validation_methods.csv", pd.DataFrame(methods))
    write_frame(report / "basket_metrics_validation.csv", pd.concat(per_basket, ignore_index=True))
    write_frame(report / "classifier_validation.csv", pd.DataFrame(scored.values()))
    write_frame(report / "ablation.csv", pd.DataFrame(ablation))
    if not pilot:
        files = [data / f for f in ("masked_baskets.parquet", "catalog.parquet", "rules_grid.parquet",
                                    "features_fit.parquet", "pipeline_lr.joblib", "pipeline_rf.joblib")]
        write_hashes(HASHES, files, **{k: v for k, v in record.items() if k != "files"},
                     stage_A=best)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot", action="store_true")
    main(parser.parse_args().pilot)
