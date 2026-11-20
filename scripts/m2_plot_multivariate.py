"""Phong, mục 3.5: hình thời gian, tương quan Spearman/Pearson và lift đồng mua 21 ngành.

Chạy sau m2_eda_multivariate.py. Bảng dùng để vẽ được sao vào plot_data/ban2.
"""
import shutil

import numpy as np
import pandas as pd

from m2_eda_multivariate import OUTPUT_HASHES
from project_io import check_hashes, config, path, plot_setup, save_figure, write_frame

# Tên file ASCII, không dấu cách/ngoặc để render_pdf.py đọc đúng đường dẫn hình.
COPIED = ['time_pivot_median.csv', 'time_pivot_count.csv', 'hour_band_summary.csv',
          'correlation_spearman.csv', 'correlation_pearson.csv', 'correlation_pair_n.csv',
          'department_pair_summary.csv']


def main():
    cfg = config()
    check_hashes()
    check_hashes(OUTPUT_HASHES)
    plt, style = plot_setup()
    import seaborn as sns
    from matplotlib.ticker import FuncFormatter, ScalarFormatter

    class Comma(ScalarFormatter):
        """Nhãn trục số dùng dấu phẩy thập phân cho khớp lời văn (07/11)."""
        def __call__(self, x, pos=None):
            return super().__call__(x, pos).replace('.', ',')

    def comma(value, spec):
        return format(value, spec).replace('.', ',')

    folder, figures = path(cfg['outputs']['ban2']), cfg['outputs']['figures_ban2']
    plotdata = path(cfg['outputs']['plot_data_ban2'])
    plotdata.mkdir(parents=True, exist_ok=True)

    def save(fig, stem):
        for artist in fig.findobj():   # giữ mọi phần tử dạng vector trong PDF, kể cả colorbar
            artist.set_rasterized(False)
        save_figure(plt, fig, figures, stem, style)

    baskets = pd.read_parquet(path(cfg['data_dir'])/'basket_summary.parquet')
    n = len(baskets)
    # Chiều cao rút gọn 05/11 (rộng 6,3 in = 16 cm, chữ 12 pt); số N đầy đủ nằm ở chú thích hình.
    thousands = FuncFormatter(lambda v, _: f'{int(v):,}'.replace(',', '.'))
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.6), width_ratios=[2.2, 1], layout='constrained')
    for ax, column, values, label in [(axes[0], 'order_hour_of_day', range(24), 'Giờ đặt đơn'),
                                      (axes[1], 'order_dow', range(7), 'Mã ngày (0–6)')]:
        counts = baskets[column].value_counts().reindex(values, fill_value=0).sort_index()
        ax.bar(counts.index, counts.values, color=style['colors'][0])
        ax.set_xlabel(label)
        ax.set_xticks(list(values)[::4] if column == 'order_hour_of_day' else list(values)[::2])
        ax.yaxis.set_major_formatter(thousands)
        counts.rename('N').rename_axis(column).to_csv(plotdata/(column+'_frequency.csv'))
    axes[0].set_ylabel('Số giỏ')
    save(fig, 'fig-ref-time-frequency')

    fig, axes = plt.subplots(1, 2, figsize=(6.3, 3.9), width_ratios=[1, 1.15], layout='constrained')
    median = pd.read_csv(folder/'time_pivot_median.csv', index_col=0)
    counts = pd.read_csv(folder/'time_pivot_count.csv', index_col=0)
    labels = median.map(lambda x: '' if pd.isna(x) else comma(x, 'g')).astype(str)
    labels = labels.where(counts >= cfg['min_group_n'], labels+'*')
    sns.heatmap(median, annot=labels, fmt='', cmap='YlGnBu', mask=median.isna(), ax=axes[0],
                cbar=False)
    axes[0].set(title='(a) Median', xlabel='Khung giờ', ylabel='Mã ngày')
    axes[0].tick_params(axis='x', rotation=90)
    axes[0].tick_params(axis='y', rotation=0)
    groups = [baskets.loc[baskets.hour_band.eq(b), 'basket_size'].to_numpy() for b in cfg['hour_labels']]
    axes[1].boxplot(groups, tick_labels=cfg['hour_labels'], showfliers=True,
                    flierprops={'markersize': 2})
    axes[1].set(ylabel='Số sản phẩm/giỏ', xlabel='Khung giờ', title='(b) Kích thước giỏ')
    axes[1].tick_params(axis='x', rotation=90)
    save(fig, 'fig-ref-time-basket-size')

    names = ['Số sản phẩm', 'Số ngành', 'Số quầy', 'Khoảng cách đơn']
    for method in ['spearman', 'pearson']:
        corr = pd.read_csv(folder/f'correlation_{method}.csv', index_col=0)
        fig, ax = plt.subplots(figsize=(6.3, 3.3), layout='constrained')
        sns.heatmap(corr, vmin=-1, vmax=1, cmap='vlag', annot=corr.map(lambda v: comma(v, '.3f')),
                    fmt='', xticklabels=names, yticklabels=names, ax=ax,
                    cbar_kws={'label': method.title()})
        ax.collections[0].colorbar.ax.yaxis.set_major_formatter(Comma())
        ax.tick_params(axis='both', rotation=0)
        ax.set(xlabel='', ylabel='')
        save(fig, f'fig-ref-corr-{method}')

    pairs = pd.read_csv(folder/'department_pair_summary.csv')
    lift = pairs.pivot(index='department_a', columns='department_b',
                       values='lift_AB').sort_index().sort_index(axis=1)
    names = pd.read_csv(path(cfg['data_dir'])/'department_lookup.csv').set_index('department_id').department
    fig, ax = plt.subplots(figsize=(6.3, 5.0), layout='constrained')
    sns.heatmap(lift, mask=np.eye(len(lift), dtype=bool) | lift.isna().to_numpy(), cmap='YlGnBu',
                vmin=0, ax=ax, cbar_kws={'label': 'Lift'}, xticklabels=list(lift.columns),
                yticklabels=[f'{i} {names[i]}' for i in lift.index])
    ax.collections[0].colorbar.ax.yaxis.set_major_formatter(Comma())
    ax.set(xlabel='ID ngành B', ylabel='')
    ax.tick_params(axis='both', rotation=0)
    save(fig, 'fig-ref-department-lift')

    write_frame(plotdata/'department_labels.csv',
                pd.read_csv(path(cfg['data_dir'])/'department_lookup.csv'))
    for name in COPIED:
        shutil.copy2(folder/name, plotdata/name)
    check_hashes(OUTPUT_HASHES)
    print('BAN2 FIGURES: PNG 300 DPI + PDF vector')


if __name__ == '__main__':
    main()
