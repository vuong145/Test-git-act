"""Three locked reference-level tests; Holm family includes untestable pairs."""
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact
from m2_common import load_foundation, path, read_json, require, digest, snapshot, write_json, write_frame
from m2_multivariate_io import verified_multivariate


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


def p_text(value):
    if pd.isna(value):return 'NA'
    return '< 2,23 × 10⁻³⁰⁸ (*)' if value==0 else f'{value:.3g}'


def main():
    cfg,foundation,folder,manifest=verified_multivariate()
    h=read_json(path(cfg['hypotheses_config']))
    require(h['adjustment']=='holm' and h['family_size']==3 and
            h['chi_square_correction'] is False and h['fisher_alternative']=='two-sided',
            'Unsupported locked testing contract')
    presence=pd.read_parquet(folder/'department_presence.parquet').set_index('order_id')
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
    destination=folder/'hypotheses';destination.mkdir(exist_ok=True)
    write_frame(destination/'hypotheses.csv',pd.DataFrame(rows))
    write_json(destination/'hypotheses_details.json',{'config':h,'tables':details,'warnings':['Zero machine p-values must be displayed as below numerical precision, never p=0.','Association is unadjusted for basket size; not causal; not externally preregistered.']})
    draft=path(cfg['outputs']['ban2']['drafts'])/'ban2_3_6.qmd'
    text='''## Kiểm định giả thuyết thống kê sơ bộ

### Giả thuyết và thiết kế

Ba cặp ngành bakery–dairy eggs, dry goods pasta–pantry và produce–meat seafood được quy định trong cấu hình trước lượt phân tích này. Đây không phải đăng ký trước độc lập; không khẳng định người thực hiện chưa từng xem dữ liệu. H0 là hai chỉ báo hiện diện ngành độc lập; H1 là có liên hệ. Mỗi quan sát là một giỏ/người trong reference, N=39.363, gồm cả giỏ không có hai ngành. Dùng Pearson Chi-square không Yates khi mọi tần số kỳ vọng ≥5; nếu bảng thưa dùng Fisher hai phía; biến hằng không kiểm định. Holm áp dụng cho họ ba cặp, alpha=0,05. Cramér’s V được tính từ thống kê Pearson không Yates, không có dấu.

### Kết quả

| Cặp ngành | N | Phương pháp | p thô | p Holm | V |
|---|---:|---|---|---|---:|
'''
    for r in rows:text+=f"| {r['pair']} | {r['N']} | {r['method']} | {p_text(r['p_raw'])} | {p_text(r['p_holm'])} | {r['cramers_v']:.3f} |\n"
    text+='\n: Kiểm định liên hệ giữa ba cặp ngành trên reference {#tbl-ban2-hypothesis-tests}\n\n(*) Giá trị p nhỏ hơn giới hạn số học được trình bày theo ngưỡng, không ghi p=0. Các số trong bảng được làm tròn để trình bày; quyết định dùng giá trị chưa làm tròn.\n\n| Cặp ngành (A / B) | P(B khi có A) | P(B khi không có A) | Chênh lệch (điểm %) | Lift |\n|---|---:|---:|---:|---:|\n'
    for r in rows:text+=f"| {r['pair']} | {r['conditional_p1']:.2%} | {r['conditional_p0']:.2%} | {r['difference_pp']:.2f} | {r['lift_AB']:.3f} |\n"
    text+='\n: Chiều và mức liên hệ giữa các ngành {#tbl-ban2-association-direction}\n\n'
    for r in rows:
        text+=f"{r['hypothesis_id']}: tần số kỳ vọng nhỏ nhất {r['expected_min']:.2f}; Pearson chi-square={r['chi2_pearson']:.3f}; df={r['df']}. Số đồng mua n11={r['n11']}, support={r['support_AB']:.2%}.\n\n"
    text+='### Diễn giải và giới hạn\n\n'
    for r in rows:text+=f"{r['pair']}: "+('bác bỏ H0 sau hiệu chỉnh Holm.' if r['reject_H0'] else 'chưa đủ bằng chứng bác bỏ H0 hoặc không kiểm định được.')+'\n\n'
    text+='Các liên hệ chưa điều chỉnh kích thước giỏ; giỏ lớn có nhiều cơ hội chứa cả hai ngành. p nhỏ không chứng minh giá trị kinh doanh lớn, quan hệ nhân quả hoặc hiệu quả gợi ý. Một giỏ/người tránh đếm lặp người, nhưng không chứng minh tính đại diện thị trường. Phân tích cấp ngành này tạo câu hỏi cho khai phá luật cấp sản phẩm ở Chương 4, chưa phải kết quả Apriori/FP-Growth. Giá trị p bị underflow được báo dưới ngưỡng số học thay vì p=0.\n\n'
    text+=f"Nguồn: `{(destination/'hypotheses.csv').relative_to(path('.')).as_posix()}`; phiên nền {manifest['run_id']}. Bảng đếm/kỳ vọng đầy đủ nằm trong hypotheses_details.json.\n"
    draft.write_text(text,encoding='utf-8')
    verified_multivariate()
    write_json(destination/'validation.json',{'status':'passed','foundation_manifest_sha256':manifest['foundation_manifest_sha256'],'inputs':snapshot([folder/'department_presence.parquet',folder/'department_pair_summary.csv',path(cfg['data_dir'])/'department_lookup.csv',path(cfg['hypotheses_config'])]),'code':snapshot([path(__file__),path('scripts/m2_multivariate_io.py')]),'outputs':snapshot([destination/'hypotheses.csv',destination/'hypotheses_details.json',draft])})
    print(pd.DataFrame(rows)[['hypothesis_id','method','p_raw','p_holm','cramers_v','difference_pp']].to_string(index=False))


if __name__=='__main__':main()
