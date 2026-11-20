"""Bạn 2: hình 3–5, hình Pearson bổ trợ và bằng chứng I4–I5."""
import os
import pandas as pd
import numpy as np
from m2_common import ROOT,config,path,read_json,write_json,write_frame,snapshot,digest,require
from m2_data_hashes import check_data_hashes


def main():
    cfg=config()
    check_data_hashes()
    folder=path(cfg['outputs']['ban2'])
    check_data_hashes(folder.relative_to(ROOT).as_posix()+'/hashes.json')
    os.environ['MPLCONFIGDIR']=str(path('BAO CAO/Bao cao EDA/common/.mplcache'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    import seaborn as sns
    style=read_json(path('configs/m2_plot_style.json'))
    font_manager.findfont(style['font_family'],fallback_to_default=False)
    plt.rcParams.update({'font.family':style['font_family'],'font.size':12,'axes.titlesize':12,'axes.labelsize':12,'xtick.labelsize':12,'ytick.labelsize':12})
    figures=path(cfg['outputs']['figures_ban2']);figures.mkdir(parents=True,exist_ok=True)
    plotdata=path(cfg['outputs']['plot_data_ban2']);plotdata.mkdir(parents=True,exist_ok=True)
    # Tên file ASCII, không dấu cách/ngoặc để render_pdf.py đọc đúng đường dẫn.
    filenames={'fig-ref-time-patterns-frequency':'fig-ref-time-frequency','fig-ref-time-patterns':'fig-ref-time-basket-size','fig-ref-correlations':'fig-ref-corr-spearman','fig-ref-correlations-pearson':'fig-ref-corr-pearson','fig-ref-department-cooccurrence':'fig-ref-department-lift'}
    outputs=[]
    def save(fig,name):
        # Matplotlib rasterizes dense colorbar meshes by default.
        # Force vector primitives throughout the PDF, including colorbars.
        for artist in fig.findobj():
            artist.set_rasterized(False)
        for ext in style['formats']:
            # Không dùng bbox_inches='tight': giữ đúng rộng 6,3 inch để chèn 16 cm không thu nhỏ chữ.
            p=figures/(filenames[name]+'.'+ext);fig.savefig(p,dpi=style['dpi']);outputs.append(p)
        plt.close(fig)
    baskets=pd.read_parquet(path(cfg['data_dir'])/'basket_summary.parquet')
    n=len(baskets)
    fig,axes=plt.subplots(2,1,figsize=(6.3,6.3),layout='constrained')
    for ax,column,values,label in [(axes[0],'order_hour_of_day',range(24),'Giờ đặt đơn'),(axes[1],'order_dow',range(7),'Mã ngày (0–6)')]:
        counts=baskets[column].value_counts().reindex(values,fill_value=0).sort_index()
        ax.bar(counts.index,counts.values,color=style['colors'][0]);ax.set_xlabel(label);ax.set_ylabel('Số giỏ')
        ax.set_title(f'N hợp lệ={int(counts.sum()):,}; thiếu={int(baskets[column].isna().sum()):,}; tổng={n:,}')
        ax.set_xticks(list(values)[::2] if column=='order_hour_of_day' else list(values))
        p=plotdata/(column+'_frequency.csv');counts.rename('N').rename_axis(column).to_csv(p);outputs.append(p)
    save(fig,'fig-ref-time-patterns-frequency')
    fig,axes2=plt.subplots(2,1,figsize=(6.3,7),layout='constrained')
    axes=[None,None,*axes2]
    median=pd.read_csv(folder/'time_pivot_median.csv',index_col=0)
    counts=pd.read_csv(folder/'time_pivot_count.csv',index_col=0)
    annotations=median.map(lambda x:'' if pd.isna(x) else f'{x:g}').astype(str)
    annotations=annotations.where(counts>=cfg['min_group_n'],annotations+'*')
    sns.heatmap(median,annot=annotations,fmt='',cmap='YlGnBu',mask=median.isna(),ax=axes[2],cbar_kws={'label':'Median số sản phẩm'})
    axes[2].set_title('Ngày × khung giờ; * N<30; ô trống: không có giỏ')
    axes[2].set_xlabel('Khung giờ');axes[2].set_ylabel('Mã ngày')
    groups=[baskets.loc[baskets.hour_band.eq(b),'basket_size'].to_numpy() for b in cfg['hour_labels']]
    axes[3].boxplot(groups,tick_labels=cfg['hour_labels'],showfliers=True,flierprops={'markersize':2})
    axes[3].set_ylabel('Số sản phẩm/giỏ');axes[3].set_xlabel('Khung giờ')
    axes[3].set_title('Giữ mọi giỏ hợp lệ; điểm ngoài râu không bị loại')
    top=max(float(baskets.basket_size.max()),1)
    for i,g in enumerate(groups):axes[3].text(i+1,top*1.08,f'N={len(g):,}',ha='center')
    axes[3].set_ylim(0,top*1.18)
    save(fig,'fig-ref-time-patterns')
    labels=['Số sản phẩm','Số ngành','Số quầy','Khoảng cách đơn']
    for method in ['spearman','pearson']:
        corr=pd.read_csv(folder/f'correlation_{method}.csv',index_col=0)
        fig,ax=plt.subplots(figsize=(6.3,5.8),layout='constrained')
        sns.heatmap(corr,vmin=-1,vmax=1,cmap='vlag',annot=True,fmt='.2f',xticklabels=labels,yticklabels=labels,ax=ax,cbar_kws={'label':method.title()})
        ax.tick_params(axis='x',rotation=35);ax.tick_params(axis='y',rotation=0)
        ax.set_xlabel('');ax.set_ylabel('')
        ax.set_title(method.title()+'; từng cặp dùng quan sát đủ dữ liệu')
        save(fig,'fig-ref-correlations'+('' if method=='spearman' else '-pearson'))
    pairs=pd.read_csv(folder/'department_pair_summary.csv')
    lift=pairs.pivot(index='department_a',columns='department_b',values='lift_AB').sort_index().sort_index(axis=1)
    mask=np.eye(len(lift),dtype=bool)|lift.isna().to_numpy()
    fig,ax=plt.subplots(figsize=(6.3,6),layout='constrained')
    sns.heatmap(lift,mask=mask,cmap='YlGnBu',vmin=0,ax=ax,cbar_kws={'label':'Lift (thang tuyến tính)'})
    ax.set_xlabel('ID ngành B');ax.set_ylabel('ID ngành A');ax.set_title(f'Đồng mua 21 ngành; N={n:,} giỏ')
    ax.tick_params(axis='both',rotation=0)
    save(fig,'fig-ref-department-cooccurrence')
    lookup=pd.read_csv(path(cfg['data_dir'])/'department_lookup.csv')
    write_frame(plotdata/'department_labels.csv',lookup);outputs.append(plotdata/'department_labels.csv')
    # Keep the exact tables used by figures beside their frequency data.
    import shutil
    for name in ['time_pivot_median.csv','time_pivot_count.csv','hour_band_summary.csv','correlation_spearman.csv','correlation_pearson.csv','correlation_pair_n.csv','department_pair_summary.csv']:
        p=plotdata/name;shutil.copy2(folder/name,p);outputs.append(p)
    draft=path(cfg['outputs']['drafts'])/'ban2';draft.mkdir(parents=True,exist_ok=True)
    text='## Trực quan hóa đa biến — phần Bạn 2\n\n'
    captions=[('fig-ref-time-patterns-frequency','Tần số giờ và mã ngày đặt đơn — phần A của nhóm hình thời gian'),('fig-ref-time-patterns','Kích thước giỏ theo ngày và khung giờ — phần B của nhóm hình thời gian'),('fig-ref-correlations','Tương quan Spearman giữa các biến định lượng'),('fig-ref-department-cooccurrence','Lift đồng mua cấp ngành trên reference')]
    for name,caption in captions:
        rel=(figures/(filenames[name]+'.png')).relative_to(path('.')).as_posix()
        text+=f'![{caption}](<{rel}>){{#{name} width=100%}}\n\nNguồn: reference G0; N={n:,} giỏ. Dữ liệu vẽ và mẫu số lưu trong hồ sơ nhánh Bạn 2.\n\n'
    complete_time=int(counts.to_numpy().sum())
    text+=f'Pivot ngày × khung giờ: N hợp lệ={complete_time:,}; thiếu ngày hoặc giờ={n-complete_time:,}. Tương quan giữa ba biến đếm dùng N={n:,}; cặp có khoảng cách đơn dùng N={int(baskets.days_since_prior_order.notna().sum()):,}. Các nhóm thiếu chỉ loại khỏi phép tính cần biến đó.\n\n'
    text+='Hình thời gian giữ riêng số thiếu; median ô trống là NA, nhóm N<30 chỉ tham khảo. Spearman là hình chính; Pearson là hình bổ trợ, không chọn hệ số lớn hơn để kết luận. Số ngành/quầy và kích thước giỏ có quan hệ cấu trúc. Heatmap ngành dùng thang tuyến tính, ẩn đường chéo và giá trị không xác định; ID tăng từ 1 đến 21, tên tương ứng trong bảng dưới. Lift cao cần đọc cùng số đồng mua và support, không chứng minh quan hệ nhân quả.\n\n| ID | Ngành |\n|---:|---|\n'
    for row in lookup.itertuples():text+=f'| {row.department_id} | {row.department} |\n'
    text+='\nĐường dẫn hình tính từ gốc project để Bạn 1 tích hợp vào QMD chính; bản thảo này không render riêng.\n'
    (draft/'ban2_3_5_hinh_3_5.qmd').write_text(text,encoding='utf-8')
    r=pairs.loc[(pairs.department_a==3)&(pairs.department_b==16)].iloc[0]
    hfile=folder/'department_pair_summary.csv'
    hours=pd.read_csv(folder/'hour_band_summary.csv')
    night=hours.loc[hours.hour_band=='18–23'].iloc[0]
    others=hours.loc[hours.hour_band.isin(cfg['hour_labels'][:3])]
    missing_hour=int(baskets.order_hour_of_day.isna().sum())
    other_text='; '.join(f"{row.hour_band}: N={int(row.N):,}, median={row.median:g}, Q1–Q3={row.q1:g}–{row.q3:g}" for row in others.itertuples())
    i4=f"Khung 18–23 có {int(night.N):,} giỏ, median {night['median']:g} sản phẩm, Q1–Q3={night.q1:g}–{night.q3:g}. Các khung khác: {other_text}. Có {missing_hour:,}/{n:,} giỏ thiếu giờ đặt đơn; các phân phối còn chồng lấn và kết quả có thể chịu ảnh hưởng của thiếu dữ liệu/thành phần người mua. Có thể đặt giả thuyết thử nghiệm giao diện gợi ý theo thời điểm; đây là khác biệt mô tả, chưa kiểm định hoặc kết luận nhân quả."
    p0=(r.n_B-r.n_AB)/(r.N-r.n_A) if r.N>r.n_A else np.nan
    delta=100*(r.probability_B_given_A-p0)
    i5=f"Bakery và dairy eggs cùng xuất hiện trong {int(r.n_AB):,}/{int(r.N):,} giỏ (support {r.support_AB:.2%}), lift={r.lift_AB:.3f}. Tỷ lệ có dairy eggs ở giỏ có bakery là {r.probability_B_given_A:.2%}, so với {p0:.2%} ở giỏ không có bakery, chênh {delta:.2f} điểm phần trăm. Có thể dùng liên hệ mô tả này để đặt giả thuyết thử nghiệm gợi ý liên ngành; chưa đánh giá ý nghĩa thống kê trong phần này. Giỏ lớn có thể làm hai ngành cùng hiện diện; chưa điều chỉnh kích thước giỏ, chưa chứng minh nhân quả, hiệu quả gợi ý hoặc tăng doanh thu."
    (draft/'ban2_3_5_insights.qmd').write_text('### I4 — Khác biệt thời điểm\n\n'+i4+'\n\n### I5 — Đồng mua ngành\n\n'+i5+'\n\nNguồn: BAO CAO/Bao cao EDA/ban2/hour_band_summary.csv, department_pair_summary.csv. I1–I3 chưa tổng hợp do thuộc bằng chứng G1 của Bạn 1.\n',encoding='utf-8')
    rel=lambda f:f.relative_to(ROOT).as_posix()
    write_frame(folder/'insights_i4_i5.csv',pd.DataFrame([{'id':'I4','text':i4,'source':rel(folder/'hour_band_summary.csv'),'N':n},{'id':'I5','text':i5,'source':rel(hfile),'N':n}]))
    check_data_hashes(folder.relative_to(ROOT).as_posix()+'/hashes.json')
    write_json(folder/'plots_validation.json',{'status':'passed','font':style['font_family'],'dpi':style['dpi'],'descriptive_pairs_sha256':digest(hfile),'code':snapshot([path(__file__)]),'style':snapshot([path('configs/m2_plot_style.json')]),'outputs':snapshot(outputs+list(draft.glob('ban2_3_5*.qmd')))})
    print(figures)


if __name__=='__main__':main()
