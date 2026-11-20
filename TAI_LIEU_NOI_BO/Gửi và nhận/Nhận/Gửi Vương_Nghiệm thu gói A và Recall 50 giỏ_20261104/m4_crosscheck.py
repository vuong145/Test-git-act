"""Kiểm độc lập Rules Recall@10; không gọi evaluate hoặc hàm khớp luật của Vương."""
import argparse

import numpy as np
import pandas as pd

from project_io import path, sha256, write_frame, write_json


def crosscheck(baskets, catalog, rules, metrics, top_n=1000, min_count=20,
               max_len=2, confidence=0.05, count=50):
    selected = baskets.loc[baskets.split.eq('validation') & baskets.eligible].sort_values('order_id').head(count)
    if len(selected) != count or selected.order_id.duplicated().any() or selected.user_id.duplicated().any():
        raise ValueError('Thiếu số giỏ validation yêu cầu hoặc trùng khóa.')
    cat = catalog.loc[catalog['rank'].le(top_n)]
    if len(cat) != top_n or cat.product_id.duplicated().any() or not np.isfinite(cat.popularity).all():
        raise ValueError('Danh mục không đủ Top-N hoặc khóa/độ phổ biến không hợp lệ.')
    popularity = dict(zip(cat.product_id, cat.popularity))
    chosen = rules.loc[rules.top_n.eq(top_n) & rules.min_count.eq(min_count)
                       & rules.max_len.eq(max_len) & rules.confidence.ge(confidence)]
    expected = metrics.loc[metrics.method.eq('Rules') & metrics.order_id.isin(selected.order_id)]
    if len(expected) != count or expected.order_id.duplicated().any():
        raise ValueError('Metrics phải có đúng một dòng Rules cho mỗi giỏ được kiểm.')
    expected = expected.set_index('order_id')
    rows, rankings = [], []
    for basket in selected.itertuples():
        observed, hidden = set(basket.observed), set(basket.hidden)
        if not hidden or observed & hidden:
            raise ValueError('Giỏ eligible phải có hidden không rỗng và rời observed.')
        scores = dict.fromkeys(set(popularity) - observed, 0.0)
        for rule in chosen.itertuples():
            if rule.consequent in scores and set(rule.antecedent).issubset(observed):
                scores[rule.consequent] = max(scores[rule.consequent], rule.confidence)
        top = sorted(scores, key=lambda p: (-scores[p], -popularity[p], p))[:10]
        hits = len(set(top) & hidden)
        actual = hits / len(hidden)
        original = float(expected.loc[basket.order_id, 'R@10'])
        if not np.isfinite(original) or not 0 <= original <= 1:
            raise ValueError('Recall nguồn không hợp lệ.')
        if 'user_id' in expected and expected.loc[basket.order_id, 'user_id'] != basket.user_id:
            raise ValueError('user_id nguồn khác giỏ.')
        rows.append(dict(order_id=basket.order_id, user_id=basket.user_id, hits=hits,
                         n_hidden=len(hidden), recall_independent=actual,
                         recall_source=original, difference=actual-original))
        rankings.extend(dict(order_id=basket.order_id, rank=i, product_id=p, score=scores[p])
                        for i, p in enumerate(top, 1))
    return pd.DataFrame(rows), pd.DataFrame(rankings, columns=['order_id', 'rank', 'product_id', 'score'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', required=True)
    parser.add_argument('--metrics', required=True)
    parser.add_argument('--top-n', type=int, default=1000)
    parser.add_argument('--min-count', type=int, default=20)
    parser.add_argument('--max-len', type=int, default=2)
    parser.add_argument('--confidence', type=float, default=0.05)
    args = parser.parse_args()
    files = [path(args.data_dir) / name for name in ['masked_baskets.parquet', 'catalog.parquet', 'rules_grid.parquet']]
    files.append(path(args.metrics))
    # Chỉ nạp hàng validation; tuyệt đối không tự che lại giỏ hoặc đổi phân hoạch.
    baskets = pd.read_parquet(files[0], filters=[('split', '==', 'validation')])
    result, rankings = crosscheck(baskets, pd.read_parquet(files[1]), pd.read_parquet(files[2]),
                                 pd.read_csv(files[3]), args.top_n, args.min_count, args.max_len, args.confidence)
    folder = path('output/kiem_cheo_rules_50')
    write_frame(folder / 'recall_comparison.csv', result)
    write_frame(folder / 'rankings_independent.csv', rankings)
    passed = bool(result.difference.abs().le(1e-12).all())
    write_json(folder / 'verification.json', dict(passed=passed, n=len(result), tolerance=1e-12,
               mean_independent=float(result.recall_independent.mean()),
               mean_source=float(result.recall_source.mean()), config=vars(args),
               input_hashes={str(p.relative_to(path('.'))): sha256(p) for p in files}))
    if not passed:
        raise SystemExit('Recall lệch: xem recall_comparison.csv; dừng trước bước tiếp theo.')
    print('50/50 giỏ khớp Recall@10 trong dung sai 1e-12.')


if __name__ == '__main__':
    main()
