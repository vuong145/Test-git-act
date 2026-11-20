"""Chỉ số phân loại và bootstrap thuần; chưa mở cổng đọc test nghiên cứu."""
import numpy as np
from sklearn.metrics import (accuracy_score, average_precision_score, confusion_matrix,
                             precision_recall_curve, precision_recall_fscore_support, roc_auc_score)


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


if __name__ == '__main__':
    raise SystemExit('Chưa tích hợp lock.json: không được chấm test nghiên cứu. Chạy demo bằng m4_classifier.py --demo.')
