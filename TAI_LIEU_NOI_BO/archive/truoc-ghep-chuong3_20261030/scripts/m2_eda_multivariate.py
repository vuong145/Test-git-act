"""Bạn 2: bảng mô tả đa biến trên reference, chạy trước hình và kiểm định 3.6."""
import numpy as np
import pandas as pd
from m2_common import config, path, snapshot, write_frame, require, read_json, environment
from m2_data_hashes import check_data_hashes, write_data_hashes


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
    foundation = check_data_hashes()
    folder = path(cfg['outputs']['ban2'])
    folder.mkdir(parents=True, exist_ok=True)
    inputs=[path(cfg['data_dir'])/x for x in ('reference.parquet','basket_summary.parquet','department_lookup.csv')]
    hashes=snapshot(inputs)
    reference, baskets = [pd.read_parquet(p) for p in inputs[:2]]
    departments=pd.read_csv(inputs[2])
    require(len(baskets)==foundation['counts']['reference_baskets'], 'N mismatch')
    require(len(departments)==21, 'Expected 21 departments')
    presence=presence_table(reference,baskets,departments)
    require(np.array_equal(presence.sum(axis=1).to_numpy(),baskets.n_departments.to_numpy()), 'Department counts differ')
    pairs=pair_summary(presence)
    hypotheses=read_json(path(cfg['hypotheses_config']))
    for pair in hypotheses['pairs']:
        a,b=pair['a'],pair['b']
        tab=pd.crosstab(presence[str(a)],presence[str(b)]).reindex(index=[False,True],columns=[False,True],fill_value=0)
        row=pairs.loc[(pairs.department_a==a)&(pairs.department_b==b)].iloc[0]
        require(int(tab.loc[True,True])==row.n_AB and tab.to_numpy().sum()==len(baskets), 'Independent crosstab mismatch')
    time, hours=time_tables(baskets,cfg)
    corr, pair_n=correlations(baskets,cfg['correlation_columns'])
    outputs=[]
    def csv(name, frame, indexed=False):
        destination=folder/name
        write_frame(destination,frame.reset_index() if indexed else frame)
        outputs.append(destination)
    for key, frame in time.items():csv('time_pivot_'+key+'.csv',frame,True)
    csv('time_pivot_small_group.csv',time['count']<cfg['min_group_n'],True)
    csv('hour_band_summary.csv',hours)
    for key,frame in corr.items():csv('correlation_'+key+'.csv',frame.rename_axis('variable'),True)
    csv('correlation_pair_n.csv',pair_n.rename_axis('variable'),True)
    csv('department_pair_summary.csv',pairs)
    # Mức nền: so lift của 3 cặp đã khóa với 210 cặp ngành khác nhau (dùng cho I5 và 3.6).
    off=pairs.loc[pairs.department_a<pairs.department_b].dropna(subset=['lift_AB'])
    base=[]
    for pair in hypotheses['pairs']:
        lift=float(off.loc[(off.department_a==pair['a'])&(off.department_b==pair['b']),'lift_AB'].iloc[0])
        base.append(dict(hypothesis_id=pair['id'],lift_AB=lift,percentile_among_pairs=100*float((off.lift_AB<lift).mean())))
    csv('lift_baseline.csv',pd.DataFrame(base).assign(n_pairs=len(off),n_pairs_lift_gt_1=int((off.lift_AB>1).sum()),median_lift=float(off.lift_AB.median())))
    presence_file=path(cfg['data_dir'])/'department_presence.parquet'
    write_frame(presence_file,presence.reset_index())
    outputs.append(presence_file)
    require(snapshot(inputs)==hashes,'Inputs changed during analysis')
    check_data_hashes()
    write_data_hashes(folder/'hashes.json',outputs,inputs=hashes,
                      environment=environment(),N_baskets=len(baskets),N_rows=len(reference),
                      time_complete_baskets=len(baskets.dropna(subset=['order_dow','hour_band'])),
                      time_missing_baskets=int(baskets[['order_dow','hour_band']].isna().any(axis=1).sum()))
    print(folder)


if __name__ == '__main__':
    main()
