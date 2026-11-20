"""Pipeline LR/RF gọn; demo chỉ sinh dữ liệu giả, không đọc Master hoặc tập test."""
import argparse
from time import perf_counter

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from m4_test import best_f1_threshold, classification_metrics, paired_bootstrap
from project_io import atomic_write, check_hashes, path, write_frame, write_json

NUMERIC = ['candidate_popularity', 'matching_rule_count', 'max_rule_confidence',
           'max_rule_lift', 'observed_basket_size', 'same_department_count']
CATEGORY = ['candidate_department_id']
GRIDS = {'LR': [{'C': c} for c in [0.01, 0.1, 1, 10]],
         'RF': [{'max_depth': d, 'min_samples_leaf': n} for d in [10, 20] for n in [20, 100]]}


def build_pipeline(method, params=None, group='full'):
    """Chỉ 7 biến được chọn; ID/nhãn không lọt vào estimator. Bỏ nhóm dùng để diễn giải."""
    if method not in GRIDS or group not in ('full', 'no_rules', 'no_department'):
        raise ValueError('Sai phương pháp hoặc nhóm đặc trưng.')
    numeric = [c for c in NUMERIC if not (group == 'no_rules' and c in NUMERIC[1:4])
               and not (group == 'no_department' and c == 'same_department_count')]
    steps = [('impute', SimpleImputer(strategy='median', keep_empty_features=True))]
    if method == 'LR':
        steps.append(('scale', StandardScaler()))
    branches = [('numeric', Pipeline(steps), numeric)]
    if group != 'no_department':
        branches.append(('category', Pipeline([
            ('impute', SimpleImputer(strategy='most_frequent', keep_empty_features=True)),
            ('encode', OneHotEncoder(handle_unknown='ignore'))]), CATEGORY))
    estimator = (LogisticRegression(solver='lbfgs', max_iter=1000)
                 if method == 'LR' else RandomForestClassifier(
                     n_estimators=300, max_features='sqrt', random_state=42, n_jobs=-1))
    estimator.set_params(**(params or {}))
    return Pipeline([('transform', ColumnTransformer(branches)), ('model', estimator)])


def fit_grid(x_fit, y_fit, method, evaluate_validation, tolerance=0.002):
    """Callback của Vương trả recall_at_10, inference_seconds; không tự tính Recall thứ hai.

    Callback phải chấm toàn bộ validation theo lô, kể cả giỏ rỗng ứng viên.
    Trả Pipeline thắng và bảng lưới; chỉ giữ mô hình còn trong dung sai hòa.
    """
    if method not in GRIDS or tolerance < 0 or not np.isfinite(tolerance):
        raise ValueError('Sai phương pháp/dung sai.')
    rows, candidates = [], []
    for params in GRIDS[method]:
        model = build_pipeline(method, params).fit(x_fit, y_fit)
        result = evaluate_validation(model)
        recall, seconds = result['recall_at_10'], result['inference_seconds']
        if not np.isfinite([recall, seconds]).all() or not 0 <= recall <= 1 or seconds < 0:
            raise ValueError('Callback phải trả Recall [0,1] và thời gian không âm.')
        rows.append(dict(method=method, **params, recall_at_10=recall, inference_seconds=seconds))
        candidates.append((model, recall, seconds))
        best = max(r for _, r, _ in candidates)
        candidates = [(m, r, s) for m, r, s in candidates if r >= best - tolerance]
    winner = min(candidates, key=lambda item: item[2])[0]
    table = pd.DataFrame(rows)
    table['selected'] = [all(winner['model'].get_params()[k] == v for k, v in p.items())
                         for p in GRIDS[method]]
    return winner, table


def synthetic_data(n=400, seed=42):
    rng = np.random.default_rng(seed)
    x = pd.DataFrame({NUMERIC[0]: rng.uniform(0, 0.1, n), NUMERIC[1]: rng.integers(0, 5, n),
                      NUMERIC[2]: rng.uniform(0, 1, n), NUMERIC[3]: rng.uniform(0, 4, n),
                      NUMERIC[4]: rng.integers(1, 20, n), NUMERIC[5]: rng.integers(0, 5, n),
                      CATEGORY[0]: rng.integers(1, 5, n).astype(float)})
    y = (rng.random(n) < 1 / (1 + np.exp(2 - x[NUMERIC[1]] - x[NUMERIC[2]]))).astype(int)
    x.loc[::17, NUMERIC[0]] = np.nan
    x.loc[::23, CATEGORY[0]] = np.nan
    return x, y


def demo():
    check_hashes()
    folder = path('output/ch4_phong_synthetic_20261101')
    x, y = synthetic_data()
    validation, yv = synthetic_data(120, 43)
    validation.loc[0, CATEGORY[0]] = 99
    records = []
    for method in GRIDS:
        start = perf_counter()
        model = build_pipeline(method).fit(x, y)
        scores = model.predict_proba(validation)[:, 1]
        threshold = best_f1_threshold(yv, scores)
        records.append(dict(method=method, **classification_metrics(yv, scores, threshold)))
        atomic_write(folder / f'pipeline_{method.lower()}.joblib', lambda p: joblib.dump(model, p))
        restored = joblib.load(folder / f'pipeline_{method.lower()}.joblib')
        np.testing.assert_array_equal(scores, restored.predict_proba(validation)[:, 1])
        write_json(folder / f'{method.lower()}_demo.json', dict(synthetic_only=True,
                   fit_rows=len(x), validation_rows=len(validation), seconds=perf_counter() - start))
    write_frame(folder / 'classification_metrics_SYNTHETIC.csv', pd.DataFrame(records))
    # Recall dựng tay để kiểm hàm bootstrap, không phải đầu ra xếp hạng của hai classifier.
    metrics = pd.DataFrame([dict(user_id=i, order_id=i, method=m, **{'R@10': r})
                           for m, values in [('example_A', [0.5, 1, 0, 1]),
                                             ('example_B', [0, 0.5, 0, 0.5])]
                           for i, r in enumerate(values)])
    write_frame(folder / 'basket_metrics_SYNTHETIC.csv', metrics)
    write_json(folder / 'bootstrap_SYNTHETIC.json', paired_bootstrap(metrics, 'example_A', 'example_B'))
    print(f'Demo dữ liệu tự tạo hoàn thành: {folder}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo', action='store_true', required=True)
    parser.parse_args()
    demo()
