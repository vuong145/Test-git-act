"""Suy luận LR/RF trên 2.000 giỏ validation đầu; không fit lại hoặc mở test."""
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from project_io import check_hashes, read_json, write_frame, write_json
from m4_common import M, context, index_rules, make_batches
from m4_validate import classify
from m4_test import classification_metrics, paired_bootstrap

out = Path(__file__).parent
for manifest in ['BAO CAO/Bao cao EDA/common/hashes.json', 'DATA/Data phai sinh/M4/hashes.json',
                 'BAO CAO/Bao cao mo hinh/lock.json']:
    check_hashes(manifest)
data = ROOT / 'DATA/Data phai sinh/M4'
report = ROOT / 'BAO CAO/Bao cao mo hinh'
lock = read_json(report / 'lock.json')
stage = lock['stage_A']
val = pd.read_parquet(data / 'masked_baskets.parquet', filters=[('split', '==', 'validation')])
val = val.loc[val.eligible].sort_values('order_id').head(2000).reset_index(drop=True)
assert len(val) == 2000
products = pd.read_csv(ROOT / 'DATA/Data đã làm sạch/products.csv', usecols=['product_id', 'department_id'])
dept = np.zeros(M, dtype=int)
dept[products.product_id.to_numpy()] = products.department_id.to_numpy()
ranked = pd.read_parquet(data / 'catalog.parquet')
rules = pd.read_parquet(data / 'rules_grid.parquet')
rules = rules.loc[rules.top_n.eq(stage['top_n']) & rules.min_count.eq(stage['min_count'])
                  & rules.max_len.eq(stage['max_len']) & rules.confidence.ge(stage['min_confidence'])]
ctx = context(ranked, stage['top_n'], dept)
idx = index_rules(rules, ctx)
source = pd.read_csv(report / 'basket_metrics_validation.csv')
results, checks, all_metrics = [], [], []
for name in ['LR', 'RF']:
    model = joblib.load(data / f'pipeline_{name.lower()}.joblib')
    metrics, y, scores, seconds = classify(make_batches(val, ctx, idx, 100), model, [5, 10])
    assert np.isfinite(scores).all()
    comparison = metrics.merge(source.loc[source.method.eq(name)], on=['order_id', 'user_id'],
                               suffixes=('_phong', '_vuong'), validate='one_to_one')
    assert len(comparison) == 2000
    for metric in ['R@5', 'R@10', 'P@5', 'P@10', 'HR@10']:
        gap = float((comparison[metric+'_phong'] - comparison[metric+'_vuong']).abs().max())
        assert gap <= 1e-12, (name, metric, gap)
        checks.append(dict(method=name, metric=metric, max_abs_gap=gap))
    write_frame(out / f'{name.lower()}_validation_2000.csv', metrics)
    all_metrics.append(metrics.assign(method=name))
    results.append(dict(method=name, baskets=len(metrics), inference_seconds=seconds,
                        recall_at_10=float(metrics['R@10'].mean()),
                        **classification_metrics(y, scores, lock['f1_threshold'][name])))
write_frame(out / 'classifier_2000.csv', pd.DataFrame(results))
write_frame(out / 'comparison_2000.csv', pd.DataFrame(checks))
write_frame(out / 'selected_2000.csv', val[['order_id', 'user_id']])
write_json(out / 'bootstrap_2000_development.json', paired_bootstrap(pd.concat(all_metrics), 'RF', 'LR'))

# Mở bảng thứ hạng Vương chỉ sau khi script độc lập đã xuất Top-10.
independent = pd.read_csv(ROOT / 'output/kiem_cheo_rules_50/rankings_independent.csv')
received = ROOT / 'Gửi và Nhận/Nhận/GUI_vuong_ch4_goiA_20261104'
ranking_source = pd.read_csv(received / 'tai_lieu/rules_top10_50.csv')
rankings = independent.merge(ranking_source, on=['order_id', 'rank'], suffixes=('_phong', '_vuong'), validate='one_to_one')
assert len(rankings) == 500
assert (rankings.product_id_phong == rankings.product_id_vuong).all()
assert np.max(np.abs(rankings.score_phong - rankings.score_vuong)) <= 1e-12
write_json(out / 'classifier_verification.json', dict(passed=True, baskets=2000,
           models=['LR', 'RF'], ranking_rows_matched=500, batch_size=100,
           mode='inference_received_pipelines_no_refit', official_results=False, test_opened=False))
print(pd.DataFrame(results).to_string(index=False))
print('2.000 giỏ LR/RF khớp nguồn; 500 dòng Top-10 Rules độc lập khớp.')
