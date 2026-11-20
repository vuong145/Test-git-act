"""Ban 2: reference-only descriptive tables, before plots and hypothesis tests."""
from datetime import datetime, timezone
import uuid
import numpy as np
import pandas as pd
from m2_common import (load_foundation, path, digest, snapshot, write_json,
                       write_frame, require, read_json, environment)


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
    cfg, foundation = load_foundation()
    foundation_hash = digest(path('Bao cao EDA/common/foundation_manifest.json'))
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'_'+uuid.uuid4().hex[:8]
    reports = path(cfg['outputs']['ban2']['reports'])
    folder = reports/'runs'/run_id
    folder.mkdir(parents=True, exist_ok=False)
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
    presence_file=folder/'department_presence.parquet'
    presence.reset_index().to_parquet(presence_file,index=False)
    outputs.append(presence_file)
    load_foundation()
    require(snapshot(inputs)==hashes and digest(path('Bao cao EDA/common/foundation_manifest.json'))==foundation_hash,'Inputs changed during analysis')
    canonical=path(cfg['data_dir'])/'department_presence.parquet'
    # Publish canonical derivative only after checking the full computation.
    from m2_common import atomic_write
    atomic_write(canonical,lambda p: p.write_bytes(presence_file.read_bytes()))
    manifest={**environment(),'run_id':run_id,'status':'passed','scope':'reference descriptive multivariate tables; no hypothesis tests or plots',
              'foundation_manifest_sha256':foundation_hash,'canonical_split_sha256':foundation['canonical_split_sha256'],
              'inputs':hashes,'code':snapshot([path(__file__)]),'configs':snapshot([path('configs/m2_eda.json'),path(cfg['hypotheses_config'])]),
              'outputs':snapshot(outputs+[canonical]),'N_baskets':len(baskets),'N_rows':len(reference),
              'time_complete_baskets':len(baskets.dropna(subset=['order_dow','hour_band'])),
              'time_missing_baskets':int(baskets[['order_dow','hour_band']].isna().any(axis=1).sum()),
              'checks':['all 21 departments retained','presence count matches G0','3 locked pairs independently checked by crosstab','input hashes unchanged'],
              'notes':['Counts of empty time cells are 0; their medians remain NA.','Correlation N is pairwise complete; constant/less than two observations yield NA.','No association p-values calculated; diagonal lift is not for plotting.']}
    write_json(folder/'run_manifest.json',manifest)
    write_json(reports/'run_manifest.json',{'run_id':run_id,'record':str((folder/'run_manifest.json').relative_to(path('.'))).replace('\\','/'),'sha256':digest(folder/'run_manifest.json')})
    draft=path(cfg['outputs']['ban2']['drafts']);draft.mkdir(parents=True,exist_ok=True)
    (draft/'ban2_multivariate_handoff.md').write_text(f'''# Bạn 2 — bàn giao bước phân tích đa biến

Phiên: {run_id}. Đọc trực tiếp G0, {len(baskets):,} giỏ và {len(reference):,} dòng reference. Bảng kết quả trong `{folder.relative_to(path('.')).as_posix()}`; manifest nhánh trỏ tới phiên và hash.

Đã có bảng thời gian median/count và cờ N<30; thống kê khung giờ giữ nhóm thiếu; Spearman/Pearson với N từng cặp; ma trận hiện diện đủ 21 ngành; bảng count/support/lift và xác suất có điều kiện. Ba cặp giả thuyết được đối chiếu crosstab độc lập, chưa tính kiểm định.

Ngày × khung giờ có {manifest['time_complete_baskets']:,} giỏ đủ thông tin; {manifest['time_missing_baskets']:,} giỏ thiếu ít nhất một biến thời gian không vào pivot nhưng vẫn nằm trong reference và các phân tích khác theo điều kiện hợp lệ. N=0 cho biết ô không có giỏ; median tương ứng là NA. Ô N<30 chỉ dùng tham khảo.

Đây là phần Bạn 2 chuẩn bị cho hình 3–5 và 3.6; chưa thay thế bảng 3.4 của Bạn 1. Chưa tạo hình, kiểm định hoặc kết luận insight. Bước tiếp theo dùng đúng manifest này để vẽ và kiểm định ba cặp đã khóa; I1–I3 chờ G1 của Bạn 1. Không diễn giải tương quan/lift như nhân quả; quan hệ size/ngành/quầy có thành phần cấu trúc.
''',encoding='utf-8')
    print(folder)


if __name__ == '__main__':
    main()
