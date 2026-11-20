"""Hai hình của Vương (mục 3.4): phân phối kích thước giỏ và mức tập trung danh mục.

Chạy sau m2_eda_summary.py. Dữ liệu vẽ lưu ở plot_data/ban1 để đối chiếu số trên hình.

ĐỌC NHANH: hai hình mục 3.4 từ các bảng đã tính. Hình 1 = phân phối kích thước giỏ (histogram + boxplot);
  Hình 2 = Top-10 ngành và đường tích lũy sản phẩm (Pareto). Dữ liệu vẽ cũng được lưu CSV để đối chiếu số trên hình.
"""
import pandas as pd

from project_io import check_hashes, config, path, plot_setup, save_figure, write_frame


def main():
    cfg = config()
    check_hashes()
    plt, style = plot_setup()
    from matplotlib.ticker import FuncFormatter
    tables, figures = path(cfg["outputs"]["tables"]), cfg["outputs"]["figures_ban1"]
    sizes = pd.read_parquet(path(cfg["data_dir"])/"basket_summary.parquet").basket_size
    dept = pd.read_csv(tables/"department_display.csv", keep_default_na=False)
    pop = pd.read_csv(tables/"product_popularity.csv", keep_default_na=False)
    top = pd.read_csv(tables/"top_n_coverage.csv")
    # Bảng dữ liệu vẽ, lưu CSV để đối chiếu số trên hình.
    histogram = sizes.value_counts().reindex(
        range(int(sizes.min()), int(sizes.max())+1), fill_value=0
    ).rename_axis("basket_size").reset_index(name="basket_count")
    histogram["basket_share"] = histogram.basket_count/len(sizes)
    for name, frame in {
        "basket_histogram": histogram, "basket_boxplot_values": sizes.to_frame(),
        "department_top10_remaining": dept,
        "product_cumulative": pop[["rank", "product_id", "row_count", "cumulative_row_share"]],
        "top_n_annotations": top,
    }.items():
        write_frame(path(cfg["outputs"]["plot_data_ban1"])/f"{name}.csv", frame)

    width, color, color2 = style["figure_width_inches"], style["colors"][0], style["colors"][1]
    percent = FuncFormatter(lambda v, _: f"{100*v:.0f}%")
    # Dấu chấm phân cách hàng nghìn cho khớp lời văn và Hình 3.4 (11/11).
    thousands = FuncFormatter(lambda v, _: f"{int(v):,}".replace(",", "."))
    n_label = f"{len(sizes):,}".replace(",", ".")
    # Hình 1: (a) histogram số giỏ theo kích thước, (b) boxplot râu 1,5 x IQR, giữ mọi giỏ.
    # Chiều cao rút gọn 05/11 (rộng giữ 16 cm, chữ 12 pt) để Chương 3 vừa ngân sách trang.
    fig, axes = plt.subplots(2, 1, figsize=(width, 3.9), height_ratios=[2.6, 1],
                             layout="constrained")
    axes[0].bar(histogram.basket_size, histogram.basket_count, width=1, color=color)
    axes[0].set(ylabel="Số giỏ", title=f"(a) Phân phối kích thước giỏ (N = {n_label})")
    axes[0].yaxis.set_major_formatter(thousands)
    axes[1].boxplot(sizes, orientation="horizontal", whis=1.5, showfliers=True,
                    patch_artist=True, boxprops={"facecolor": color2},
                    flierprops={"markersize": 3, "alpha": 0.4})
    axes[1].set(xlabel="Số sản phẩm phân biệt/giỏ", yticks=[],
                title="(b) Boxplot: râu 1,5 × IQR; giữ mọi giỏ")
    for ax in axes:
        ax.set_xlim(0.5, sizes.max()+0.5)
    save_figure(plt, fig, figures, "fig-ref-basket-distribution", style)

    # Hình 2: (a) Top-10 ngành và phần còn lại, (b) đường tích lũy sản phẩm kèm các mốc Top-N.
    fig, axes = plt.subplots(2, 1, figsize=(width, 5.1), height_ratios=[1.25, 1],
                             layout="constrained")
    axes[0].barh(dept.display_name, dept.row_share, color=color, height=0.75)
    axes[0].invert_yaxis()
    axes[0].xaxis.set_major_formatter(percent)
    axes[0].set(title="(a) Tỷ trọng dòng: Top-10 ngành và phần còn lại")
    axes[1].plot(pop["rank"], pop.cumulative_row_share, color=color2, linewidth=1.7)
    axes[1].scatter(top.n_actual, top.row_share, color=color, zorder=3)
    annotation = "Top-N → tỷ trọng dòng\n" + "\n".join(
        f"{int(r.n_requested):,}".replace(",", ".") + " → " +
        f"{100*r.row_share:.2f}%".replace(".", ",") for r in top.itertuples())
    axes[1].text(0.98, 0.04, annotation, transform=axes[1].transAxes, ha="right", va="bottom",
                 fontsize=12, bbox={"facecolor": "white", "alpha": 0.9, "edgecolor": "none"})
    axes[1].set(xlabel="Thứ hạng sản phẩm (popularity giảm dần)",
                ylabel="Tích lũy", ylim=(0, 1.02), xlim=(0, len(pop)),
                title="(b) Đường tỷ trọng dòng tích lũy")
    axes[1].yaxis.set_major_formatter(percent)
    axes[1].xaxis.set_major_formatter(thousands)
    save_figure(plt, fig, figures, "fig-ref-category-concentration", style)
    check_hashes()
    print("BAN1 FIGURES: PNG 300 DPI + PDF vector")


if __name__ == "__main__":
    main()
