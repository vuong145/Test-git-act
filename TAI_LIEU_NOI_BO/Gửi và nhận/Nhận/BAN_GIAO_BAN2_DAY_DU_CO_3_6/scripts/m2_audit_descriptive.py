"""Independent audit of existing descriptive outputs; never runs section 3.6."""
import itertools
import json
from pathlib import Path
import subprocess
import sys
import zipfile
import hashlib
import re
import numpy as np
import pandas as pd
from PIL import Image
from m2_multivariate_io import verified_multivariate
from m2_common import path,read_json,verify_hashes,write_json,snapshot,digest


def main():
    cfg,foundation,folder,manifest=verified_multivariate()
    review=path('output/ra_soat_ban2_mo_ta');review.mkdir(exist_ok=True)
    tests=subprocess.run([sys.executable,str(path('tests/test_m2_multivariate.py'))],capture_output=True,text=True,encoding='utf-8')
    (review/'tests.log').write_text(tests.stdout+tests.stderr,encoding='utf-8')
    assert tests.returncode==0
    baskets=pd.read_parquet(path(cfg['data_dir'])/'basket_summary.parquet')
    reference=pd.read_parquet(path(cfg['data_dir'])/'reference.parquet')
    p=pd.read_parquet(folder/'department_presence.parquet').set_index('order_id')
    assert list(p.columns)==[str(i) for i in range(1,22)]
    assert p.dtypes.eq(bool).all() and p.index.is_unique
    sets={int(k):set(v.department_id) for k,v in reference.groupby('order_id',observed=True)}
    for order, row in p.iterrows():
        assert {int(c) for c in p.columns[row.to_numpy()]}==sets[int(order)]
    pairs=pd.read_csv(folder/'department_pair_summary.csv')
    for row in pairs.itertuples():
        aa=p[str(row.department_a)].to_numpy();bb=p[str(row.department_b)].to_numpy()
        na=int(aa.sum());nb=int(bb.sum());nab=int(np.count_nonzero(aa & bb));n=len(p)
        assert (row.N,row.n_A,row.n_B,row.n_AB)==(n,na,nb,nab)
        np.testing.assert_allclose(row.support_AB,nab/n)
        np.testing.assert_allclose(row.lift_AB,nab*n/(na*nb) if na*nb else np.nan,equal_nan=True)
        np.testing.assert_allclose(row.probability_B_given_A,nab/na if na else np.nan,equal_nan=True)
    median=pd.read_csv(folder/'time_pivot_median.csv',index_col=0)
    counts=pd.read_csv(folder/'time_pivot_count.csv',index_col=0)
    small=pd.read_csv(folder/'time_pivot_small_group.csv',index_col=0)
    for day,band in itertools.product(range(7),cfg['hour_labels']):
        values=baskets.loc[baskets.order_dow.eq(day)&baskets.hour_band.eq(band),'basket_size'].to_numpy()
        assert counts.loc[day,band]==len(values)
        np.testing.assert_allclose(median.loc[day,band],np.median(values) if len(values) else np.nan,equal_nan=True)
        assert small.loc[day,band]==(len(values)<30)
    hours=pd.read_csv(folder/'hour_band_summary.csv')
    for row in hours.itertuples():
        mask=baskets.hour_band.isna() if row.hour_band=='missing' else baskets.hour_band.eq(row.hour_band)
        values=baskets.loc[mask,'basket_size'].to_numpy()
        assert row.N==len(values) and row.denominator==len(baskets)
        np.testing.assert_allclose([row.q1,row.median,row.q3],np.quantile(values,[.25,.5,.75],method='linear') if len(values) else [np.nan]*3,equal_nan=True)
    pair_n=pd.read_csv(folder/'correlation_pair_n.csv',index_col=0)
    for method in ['pearson','spearman']:
        corr=pd.read_csv(folder/f'correlation_{method}.csv',index_col=0)
        for a,b in itertools.product(cfg['correlation_columns'],repeat=2):
            complete=baskets.loc[baskets[a].notna()&baskets[b].notna()]
            assert pair_n.loc[a,b]==len(complete)
            x,y=complete[a].astype(float),complete[b].astype(float)
            if method=='spearman':x,y=x.rank(method='average'),y.rank(method='average')
            expected=np.corrcoef(x,y)[0,1] if len(x)>=2 and x.nunique()>1 and y.nunique()>1 else np.nan
            np.testing.assert_allclose(corr.loc[a,b],expected,atol=1e-12,equal_nan=True)
    validation=read_json(folder/'plots_validation.json')
    for key in ['code','style','outputs']:verify_hashes(validation[key])
    figures=path(cfg['outputs']['ban2']['figures'])/manifest['run_id']
    assert len(list(figures.glob('*.png')))==5 and len(list(figures.glob('*.pdf')))==5
    for figure in figures.glob('*.png'):
        with Image.open(figure) as im:
            assert all(abs(v-300)<1 for v in im.info['dpi'])
    draft=path(cfg['outputs']['ban2']['drafts'])/'ban2_3_5_hinh_3_5.qmd'
    for rel in re.findall(r'!\[.*?\]\(<(.*?)>\)',draft.read_text(encoding='utf-8')):assert path(rel).is_file()
    script=path('scripts/m2_plot_multivariate.py').read_text(encoding='utf-8')
    assert 'm2_hypothesis_tests' not in script and 'hypotheses/' not in script
    insights=(draft.parent/'ban2_3_5_insights.qmd').read_text(encoding='utf-8')
    assert 'Holm' not in insights and 'bác bỏ H0' not in insights
    verified_multivariate()
    result={'status':'passed','scope':'descriptive Ban 2 only; section 3.6 excluded','tests':6,'N_baskets':len(baskets),'N_rows':len(reference),'presence_rows_checked':len(p),'department_pairs_checked':len(pairs),'time_cells_checked':28,'correlation_cells_checked':32,'time_complete_N':int(counts.to_numpy().sum()),'correlation_pair_N':pair_n.to_dict(),'foundation_unchanged':True,'plot_png_count':5,'dpi':300,'draft_image_links_valid':True,'no_hypothesis_dependency':True}
    write_json(review/'audit.json',result)
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
