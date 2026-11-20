"""Chỉ số phân loại, bootstrap và chấm điểm sau khóa (cổng lock.json, bốn phương pháp, Recall@K, phân loại, bootstrap).

  python scripts/m4_test.py test                     # chấm tập test một lần, ghi vào BAO CAO/Bao cao mo hinh/
  python scripts/m4_test.py validation <thư mục>     # chạy thử cùng mã trên validation, ghi ra thư mục khác

Cổng khóa: kiểm SHA-256, hai xác nhận và mã nguồn; test_started.json chặn chạy lại kể cả khi lượt đầu lỗi.
"""
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, average_precision_score, confusion_matrix,
                             precision_recall_curve, precision_recall_fscore_support, roc_auc_score)

from m4_common import config, evaluate, locked_stage, make_batches
from project_io import check_hashes, path, plot_setup, read_json, require, save_figure, sha256, write_frame, write_json


def checked_scores(y, scores):
    y, scores = np.asarray(y), np.asarray(scores, dtype=float)
    if (y.ndim != 1 or scores.shape != y.shape or not len(y)
            or not np.isin(y, [0, 1]).all() or not np.isfinite(scores).all()
            or ((scores < 0) | (scores > 1)).any()):
        raise ValueError('Cần nhãn nhị phân và xác suất hữu hạn cùng chiều, không rỗng.')
    return y, scores


def best_f1_threshold(y_validation, scores):
    """Chỉ gọi với validation; hòa F1 chọn ngưỡng cao nhất (ít dự đoán dương)."""
    y, scores = checked_scores(y_validation, scores)
    if len(np.unique(y)) != 2:
        raise ValueError('Chọn ngưỡng cần validation có cả hai lớp.')
    precision, recall, thresholds = precision_recall_curve(y, scores)
    denominator = precision[:-1] + recall[:-1]
    f1 = np.divide(2 * precision[:-1] * recall[:-1], denominator,
                   out=np.zeros_like(denominator), where=denominator > 0)
    return float(thresholds[np.flatnonzero(f1 == f1.max())[-1]])


def classification_metrics(y, scores, threshold):
    """Toàn bộ cặp ứng viên; ROC-AUC/AP không xác định trả None, không bịa số 0."""
    y, scores = checked_scores(y, scores)
    if not np.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError('Ngưỡng phải thuộc [0, 1].')
    predicted = scores >= threshold
    precision, recall, f1, _ = precision_recall_fscore_support(
        y, predicted, average='binary', zero_division=0)
    tn, fp, fn, tp = confusion_matrix(y, predicted, labels=[0, 1]).ravel()
    return dict(n=len(y), positives=int(y.sum()), threshold=float(threshold),
                accuracy=float(accuracy_score(y, predicted)), precision=float(precision),
                recall=float(recall), f1=float(f1),
                roc_auc=float(roc_auc_score(y, scores)) if len(np.unique(y)) == 2 else None,
                average_precision=float(average_precision_score(y, scores)) if y.sum() else None,
                tn=int(tn), fp=int(fp), fn=int(fn), tp=int(tp))


def paired_bootstrap(metrics, method, baseline, repeats=2000, seed=42):
    """Ghép theo user_id/order_id; một người một giỏ. Đầu vào từ bộ metrics của Vương."""
    if not isinstance(repeats, int) or repeats < 1:
        raise ValueError('repeats phải là số nguyên dương.')
    keys = ['user_id', 'order_id']
    arrays = []
    for name in (method, baseline):
        part = metrics.loc[metrics['method'].eq(name), keys + ['R@10']]
        if (part.empty or part.isna().any().any() or part.user_id.duplicated().any()
                or part.order_id.duplicated().any()):
            raise ValueError('Mỗi phương pháp cần đúng một giỏ/người, không thiếu khóa/chỉ số.')
        arrays.append(part.set_index(keys)['R@10'].sort_index())
    if not arrays[0].index.equals(arrays[1].index):
        raise ValueError('Hai phương pháp phải có cùng tập người và giỏ; không tự bỏ giỏ.')
    values = np.column_stack([s.to_numpy(dtype=float) for s in arrays])
    if not np.isfinite(values).all() or ((values < 0) | (values > 1)).any():
        raise ValueError('Recall phải hữu hạn và thuộc [0, 1].')
    difference = values[:, 0] - values[:, 1]
    rng = np.random.default_rng(seed)
    samples = [float(rng.choice(difference, len(difference), replace=True).mean())
               for _ in range(repeats)]
    low, high = np.quantile(samples, [0.025, 0.975], method='linear')
    return dict(method=method, baseline=baseline, n_users=len(difference), repeats=repeats,
                seed=seed, difference=float(difference.mean()), ci_low=float(low),
                ci_high=float(high), improved=bool(low > 0))


KS = range(1, 11)
SHOWN = ["P@5", "R@5", "P@10", "R@10", "HR@10", "R@10_ceiling"]
CODE_FILES = ['scripts/m4_test.py', 'scripts/m4_common.py', 'scripts/m4_classifier.py',
              'scripts/project_io.py', 'requirements.txt', 'configs/m2_plot_style.json']


def checked_lock(split, out, cfg):
    """Kiểm trước khi đọc giỏ; test thật cần hai xác nhận và khóa đủ mã/nguồn."""
    require(split in ('validation', 'test'), 'Chỉ chấp nhận validation hoặc test.')
    report, out = path(cfg['report_dir']), path(out)
    lock_path = report / 'lock.json'
    lock = read_json(lock_path)
    require(bool(lock.get('files')), 'Khóa không có danh sách tệp.')
    require(lock.get('main_method') in ('Popularity', 'Rules', 'LR', 'RF'), 'Sai phương pháp chính.')
    require(all(np.isfinite(lock['f1_threshold'][m]) and 0 <= lock['f1_threshold'][m] <= 1
                for m in ('LR', 'RF')), 'Ngưỡng khóa không hợp lệ.')
    for name, digest in lock['files'].items():
        require(path(name).is_relative_to(path('.')), 'Tệp khóa nằm ngoài dự án.')
        require(sha256(path(name)) == digest, f'Tệp đã đổi sau khi khóa: {name}')
    record = check_hashes('DATA/Data phai sinh/M4/hashes.json')
    require(lock['stage_A'] == record['stage_A'], 'Cấu hình A trong lock khác hồ sơ M4.')
    if split == 'test':
        require(out == report, 'Test chỉ được ghi vào thư mục báo cáo chính thức.')
        require(lock.get('approvals') == {'Phong': True, 'Vuong': True}, 'Chưa đủ hai xác nhận khóa.')
        needed = CODE_FILES + ['configs/m4_model.json', 'DATA/Data phai sinh/M4/hashes.json',
                              'DATA/Data đã làm sạch/master_train.parquet', *record['files']]
        require(set(needed).issubset(lock['files']), 'Khóa thiếu mã nguồn hoặc đầu vào bắt buộc.')
        check_hashes()
    else:
        require(out != report, 'Validation phải xuất thư mục thử riêng.')
    require(not (out / f'results_{split}.json').exists(), 'Đã có kết quả, không ghi đè.')
    if split == 'test':
        # Tạo độc quyền trước khi nạp test; giữ dấu kể cả khi lỗi giữa chừng.
        out.mkdir(parents=True, exist_ok=True)
        with (out / 'test_started.json').open('x', encoding='utf-8') as stream:
            import json
            json.dump({'lock_sha256': sha256(lock_path)}, stream)
    return lock


def figure(recall_k, ceiling, folder, stem):
    """Hai khung chung trục K: trên là Recall trần (khoảng 0,4-0,5), dưới phóng to bốn phương pháp."""
    plt, style = plot_setup()
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(16 / 2.54, 5.4), sharex=True, height_ratios=[1, 2.4])
    top.plot(list(KS), ceiling, linestyle="--", marker="o", color="gray", label="Recall trần")
    top.set(ylim=(min(ceiling) - 0.03, max(ceiling) + 0.03))
    top.legend(loc="lower right")
    for (method, row), color in zip(recall_k.iterrows(), style["colors"]):
        bottom.plot(list(KS), row.to_numpy(), marker="o", color=color, label=method)
    bottom.set(xlabel="K", xticks=list(KS), ylim=(0, recall_k.to_numpy().max() * 1.1))
    bottom.legend(loc="upper left")
    fig.supylabel("Recall@K")
    fig.tight_layout()
    save_figure(plt, fig, folder, stem, style)


def run(split, out):
    from m4_classifier import CATEGORY, NUMERIC   # nhập tại đây: m4_classifier cũng nhập m4_test nên nhập đầu tệp sẽ tạo vòng nhập
    features = NUMERIC + CATEGORY
    cfg, report = config(), path(config()["report_dir"])
    out = path(out)
    lock = checked_lock(split, out, cfg)
    lock_digest = sha256(report / 'lock.json')

    masked, ctx, idx, _ = locked_stage(cfg, (split,))
    models = {m: joblib.load(path(cfg["data_dir"]) / f"pipeline_{m.lower()}.joblib") for m in ("LR", "RF")}
    basket, y, scores = [], [], {m: [] for m in models}
    for part, X in make_batches(masked[masked.eligible], ctx, idx, cfg["batch_size"]):
        y.append(X.y.to_numpy())
        keys = {"Popularity": [X.candidate_popularity], "Rules": [X.max_rule_confidence, X.candidate_popularity]}
        for m, model in models.items():
            scores[m].append(model.predict_proba(X[features])[:, 1])
            keys[m] = [scores[m][-1]]
        basket += [evaluate(part, X, *k, ks=KS).assign(method=m) for m, k in keys.items()]
    basket, y = pd.concat(basket, ignore_index=True), np.concatenate(y)

    # Bảng xếp hạng (trung bình vĩ mô theo giỏ) và Recall@K kèm đường trần
    mean = basket.groupby("method", sort=False).mean(numeric_only=True)
    recall_k = mean[[f"R@{k}" for k in KS]]
    base = basket[basket.method == "Popularity"]
    ceiling = [float((np.minimum(base.n_hidden_in_C, k) / base.n_hidden).mean()) for k in KS]
    # Chỉ số phân loại tại ngưỡng F1 đã khóa trên validation; toàn bộ cặp ứng viên, không lấy trung bình theo lô
    classifier = pd.DataFrame([dict(method=m, **classification_metrics(y, np.concatenate(s), lock["f1_threshold"][m]))
                               for m, s in scores.items()])
    # Kiểm định chính: phương pháp chính so với Popularity; hai so sánh sau là bổ trợ
    main = lock["main_method"]
    pairs = [(main, "Popularity"), (main, "Rules"), ("LR", "RF")]
    boot = pd.DataFrame([dict(**paired_bootstrap(basket, a, b, cfg["bootstrap_n"], cfg["seeds"]["bootstrap"]),
                              primary=(i == 0)) for i, (a, b) in enumerate(pairs)])

    write_frame(out / f"basket_metrics_{split}.csv", basket)
    write_frame(out / f"ranking_metrics_{split}.csv", mean[SHOWN].reset_index())
    ceiling_row = pd.DataFrame([dict(method="Ceiling", **{f"R@{k}": c for k, c in zip(KS, ceiling)})])
    write_frame(out / f"recall_at_k_{split}.csv", pd.concat([recall_k.reset_index(), ceiling_row], ignore_index=True))
    write_frame(out / f"classifier_metrics_{split}.csv", classifier)
    write_frame(out / f"confusion_matrix_{split}.csv", classifier[["method", "tn", "fp", "fn", "tp"]])
    write_frame(out / f"paired_bootstrap_{split}.csv", boot)
    figure(recall_k, ceiling, out / "figures", f"fig-recall-at-k-{split}")
    write_json(out / f"results_{split}.json", dict(
        split=split, baskets=int(base.shape[0]), candidate_pairs=int(len(y)), main_method=main,
        lock_locked_at=lock["locked_at"], lock_sha256=lock_digest,
        outputs={p.relative_to(out).as_posix(): sha256(p) for p in
                 sorted([*out.glob(f"*_{split}.csv"), * (out / 'figures').glob(f'fig-recall-at-k-{split}.*')])}))
    print(mean[SHOWN].round(4).to_string(), "\n", boot.round(4).to_string(index=False))


if __name__ == "__main__":
    require(sys.argv[1:2] in (["test"], ["validation"]), "Dùng: m4_test.py test | m4_test.py validation <thư mục ra>")
    run(sys.argv[1], config()["report_dir"] if sys.argv[1] == "test" else sys.argv[2])
