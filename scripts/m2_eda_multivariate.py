"""Phong, mục 3.5: bảng mô tả đa biến trên reference (chạy trước hình và kiểm định 3.6).

Ma trận hiện diện ngành (crosstab), support/lift của mọi cặp ngành, pivot ngày × khung giờ
(pivot_table), tương quan Spearman/Pearson theo cặp đủ dữ liệu (corr), mức nền lift.
Ghi BAO CAO/Bao cao EDA/ban2/hashes.json để hình và kiểm định đọc đúng bảng này.
"""
import numpy as np
import pandas as pd

from project_io import check_hashes, config, path, read_json, require, write_frame, write_hashes

OUTPUT_HASHES = "BAO CAO/Bao cao EDA/ban2/hashes.json"


def presence_table(reference, baskets, departments):
    require(not baskets.order_id.duplicated().any(), 'Duplicate baskets')
    require(set(reference.order_id) == set(baskets.order_id), 'Basket set mismatch')
    ids = sorted(departments.department_id.tolist())
    require(len(ids) == len(set(ids)), 'Duplicate department IDs')
    require(set(reference.department_id) <= set(ids), 'Unknown department')
    table = pd.crosstab(reference.order_id, reference.department_id)
    table = table.reindex(index=baskets.order_id, columns=ids, fill_value=0).gt(0)
    table.index.name = 'order_id'
    table.columns = [str(int(x)) for x in ids]
    require(table.any(axis=1).all(), 'Empty basket')
    return table


def pair_summary(presence):
    # Boolean or uint8 multiplication would not preserve counts.
    values = presence.to_numpy(dtype=np.int64)
    counts = values.T @ values
    n = len(values)
    rows = []
    for i, a in enumerate(presence.columns):
        for j, b in enumerate(presence.columns):
            na, nb, nab = int(counts[i, i]), int(counts[j, j]), int(counts[i, j])
            rows.append(dict(department_a=int(a), department_b=int(b), N=n,
                             n_A=na, n_B=nb, n_AB=nab,
                             support_AB=nab/n,
                             probability_B_given_A=nab/na if na else np.nan,
                             lift_AB=nab*n/(na*nb) if na*nb else np.nan,
                             is_diagonal=i == j))
    return pd.DataFrame(rows)


def lift_percentile(lifts, lift):
    # Phân vị thực nghiệm: % cặp có lift <= lift đang xét (tính cả chính cặp đó).
    return 100*float((lifts <= lift).mean())


def correlations(baskets, columns):
    data = baskets[columns].astype('float64')
    valid = data.notna().to_numpy(dtype=np.int64)
    n = pd.DataFrame(valid.T @ valid, index=columns, columns=columns)
    results = {}
    for method in ('spearman', 'pearson'):
        result = pd.DataFrame(np.nan, index=columns, columns=columns)
        for a in columns:
            for b in columns:
                complete = data.loc[data[a].notna() & data[b].notna()]
                if len(complete) >= 2 and complete[a].nunique() > 1 and complete[b].nunique() > 1:
                    result.loc[a,b] = complete[a].corr(complete[b], method=method)
        results[method] = result
    return results, n


def time_tables(baskets, cfg):
    valid = baskets.dropna(subset=['order_dow','hour_band'])
    tables = {}
    for label, agg in [('median','median'), ('count','count')]:
        table = valid.pivot_table(index='order_dow', columns='hour_band',
                                  values='basket_size', aggfunc=agg, observed=True)
        table = table.reindex(index=range(7), columns=cfg['hour_labels'])
        if label == 'count':
            table = table.fillna(0).astype('int64')
        tables[label] = table
    rows=[]
    for band in cfg['hour_labels'] + ['missing']:
        mask = baskets.hour_band.isna() if band == 'missing' else baskets.hour_band.eq(band)
        values = baskets.loc[mask, 'basket_size']
        rows.append(dict(hour_band=band, N=len(values), denominator=len(baskets),
                         share=len(values)/len(baskets), median=values.median() if len(values) else np.nan,
                         q1=values.quantile(.25, interpolation=cfg['quantile_interpolation']) if len(values) else np.nan,
                         q3=values.quantile(.75, interpolation=cfg['quantile_interpolation']) if len(values) else np.nan,
                         small_group=len(values)<cfg['min_group_n']))
    return tables, pd.DataFrame(rows)


def main():
    cfg = config()
    foundation = check_hashes()
    folder, data = path(cfg['outputs']['ban2']), path(cfg['data_dir'])
    reference, baskets = [pd.read_parquet(data/f) for f in ('reference.parquet', 'basket_summary.parquet')]
    departments = pd.read_csv(data/'department_lookup.csv')
    require(len(baskets) == foundation['counts']['reference_baskets'], 'N mismatch')
    require(len(departments) == 21, 'Expected 21 departments')
    presence = presence_table(reference, baskets, departments)
    require(np.array_equal(presence.sum(axis=1).to_numpy(), baskets.n_departments.to_numpy()),
            'Department counts differ')
    pairs = pair_summary(presence)
    hypotheses = read_json(path(cfg['hypotheses_config']))
    for pair in hypotheses['pairs']:   # đối chiếu độc lập bằng crosstab 2×2
        a, b = pair['a'], pair['b']
        tab = pd.crosstab(presence[str(a)], presence[str(b)]).reindex(
            index=[False, True], columns=[False, True], fill_value=0)
        row = pairs.loc[(pairs.department_a == a) & (pairs.department_b == b)].iloc[0]
        require(int(tab.loc[True, True]) == row.n_AB and tab.to_numpy().sum() == len(baskets),
                'Independent crosstab mismatch')
    time, hours = time_tables(baskets, cfg)
    corr, pair_n = correlations(baskets, cfg['correlation_columns'])
    # Mức nền: vị trí lift của 3 cặp đã khóa giữa 210 cặp ngành khác nhau (I5 và 3.6).
    off = pairs.loc[pairs.department_a < pairs.department_b].dropna(subset=['lift_AB'])
    base = []
    for pair in hypotheses['pairs']:
        lift = float(off.loc[(off.department_a == pair['a']) & (off.department_b == pair['b']), 'lift_AB'].iloc[0])
        base.append(dict(hypothesis_id=pair['id'], lift_AB=lift,
                         percentile_among_pairs=lift_percentile(off.lift_AB, lift)))
    tables = {f'time_pivot_{k}.csv': v.reset_index() for k, v in time.items()}
    tables['time_pivot_small_group.csv'] = (time['count'] < cfg['min_group_n']).reset_index()
    tables['hour_band_summary.csv'] = hours
    for key, frame in corr.items():
        tables[f'correlation_{key}.csv'] = frame.rename_axis('variable').reset_index()
    tables['correlation_pair_n.csv'] = pair_n.rename_axis('variable').reset_index()
    tables['department_pair_summary.csv'] = pairs
    tables['lift_baseline.csv'] = pd.DataFrame(base).assign(
        n_pairs=len(off), n_pairs_lift_gt_1=int((off.lift_AB > 1).sum()),
        median_lift=float(off.lift_AB.median()))
    outputs = []
    for name, frame in tables.items():
        write_frame(folder/name, frame)
        outputs.append(folder/name)
    write_frame(data/'department_presence.parquet', presence.reset_index())
    outputs.append(data/'department_presence.parquet')
    check_hashes()
    write_hashes(OUTPUT_HASHES, outputs, N_baskets=len(baskets), N_rows=len(reference))
    print(folder)


if __name__ == '__main__':
    main()
