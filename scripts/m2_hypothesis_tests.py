"""Phong, mục 3.6: kiểm định ba cặp ngành đã khóa trong configs/hypotheses_config.json.

Pearson Chi-square không Yates khi mọi tần số kỳ vọng >= 5, Fisher hai phía khi bảng thưa,
biến hằng là not_testable (p=1 chỉ dùng nội bộ cho Holm). Holm tự viết cho họ 3 cặp;
Cramér's V từ chi-square không Yates. Đầu vào là reference, mỗi giỏ một người.
"""
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact

from m2_eda_multivariate import OUTPUT_HASHES
from project_io import check_hashes, config, path, read_json, require, write_frame, write_json


def holm(values):
    values=np.asarray(values,dtype=float)
    order=np.argsort(values,kind='stable')
    adjusted=np.minimum(1,np.maximum.accumulate(values[order]*np.arange(len(values),0,-1)))
    result=np.empty(len(values));result[order]=adjusted
    return result


def test_table(table, cfg):
    t=np.asarray(table)
    require(t.shape==(2,2) and np.isfinite(t).all() and (t>=0).all() and (t==np.floor(t)).all(),'Invalid counts')
    n=int(t.sum());require(n>0,'Empty table')
    n00,n01,n10,n11=map(int,t.ravel())
    result=dict(N=n,n00=n00,n01=n01,n10=n10,n11=n11,method='not_testable',
                p_raw=np.nan,chi2_pearson=np.nan,df=np.nan,fisher_odds_ratio=np.nan,
                cramers_v=np.nan,expected_min=np.nan,conditional_p1=n11/(n10+n11) if n10+n11 else np.nan,
                conditional_p0=n01/(n00+n01) if n00+n01 else np.nan,
                support_AB=n11/n,lift_AB=n11*n/((n10+n11)*(n01+n11)) if (n10+n11)*(n01+n11) else np.nan)
    expected=np.outer(t.sum(axis=1),t.sum(axis=0))/n
    result['difference_pp']=100*(result['conditional_p1']-result['conditional_p0'])
    result['expected_min']=float(expected.min())
    if (expected==0).any():return result,expected
    chi,p,df,_=chi2_contingency(t,correction=cfg['chi_square_correction'])
    result.update(chi2_pearson=float(chi),cramers_v=float(np.sqrt(chi/n)))
    if expected.min()>=cfg['minimum_expected']:
        result.update(method='chi_square',p_raw=float(p),df=int(df))
    else:
        odds,p=fisher_exact(t,alternative=cfg['fisher_alternative'])
        result.update(method='fisher',p_raw=float(p),fisher_odds_ratio=float(odds))
    return result,expected


def main():
    cfg=config()
    foundation=check_hashes()
    check_hashes(OUTPUT_HASHES)
    folder=path(cfg['outputs']['ban2'])
    h=read_json(path(cfg['hypotheses_config']))
    require(h['adjustment']=='holm' and h['family_size']==3 and
            h['chi_square_correction'] is False and h['fisher_alternative']=='two-sided',
            'Unsupported locked testing contract')
    presence=pd.read_parquet(path(cfg['data_dir'])/'department_presence.parquet').set_index('order_id')
    lookup=pd.read_csv(path(cfg['data_dir'])/'department_lookup.csv').set_index('department_id')
    pairs=pd.read_csv(folder/'department_pair_summary.csv')
    rows=[];details=[]
    for spec in h['pairs']:
        a,b=spec['a'],spec['b']
        require(lookup.loc[a,'department']==spec['a_name'] and lookup.loc[b,'department']==spec['b_name'],'ID/name mismatch')
        table=pd.crosstab(presence[str(a)],presence[str(b)]).reindex(index=[False,True],columns=[False,True],fill_value=0)
        row,expected=test_table(table.to_numpy(),h)
        require(row['N']==foundation['counts']['reference_baskets'],'Wrong N')
        require(row['n11']==int(pairs.query('department_a==@a and department_b==@b').iloc[0].n_AB),'Cooccurrence mismatch')
        row.update(hypothesis_id=spec['id'],department_A=a,department_B=b,pair=spec['a_name']+' / '+spec['b_name'])
        rows.append(row);details.append({'id':spec['id'],'observed':table.to_numpy().tolist(),'expected':expected.tolist()})
    require(len(rows)==h['family_size']==3,'Wrong family')
    adjusted=holm([r['p_raw'] if r['method']!='not_testable' else 1 for r in rows])
    for row,p in zip(rows,adjusted):
        ok=row['method']!='not_testable'
        row.update(p_holm=float(p) if ok else np.nan,status='tested' if ok else 'not_testable',reject_H0=bool(p<h['alpha']) if ok else None)
    write_frame(folder/'hypotheses.csv',pd.DataFrame(rows))
    write_json(folder/'hypotheses_details.json',{'config':h,'tables':details,'warnings':['Zero machine p-values must be displayed as below numerical precision, never p=0.','Association is unadjusted for basket size; not causal; not externally preregistered.']})
    print(pd.DataFrame(rows)[['hypothesis_id','method','p_raw','p_holm','cramers_v','difference_pp']].to_string(index=False))


if __name__=='__main__':main()
