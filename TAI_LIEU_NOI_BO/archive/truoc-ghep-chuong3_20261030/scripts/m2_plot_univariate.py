"""Two member-1 figures, with traceable plot data and a separate manifest."""

import os
from pathlib import Path

import pandas as pd

from m2_common import (
    atomic_write, digest, environment, path, read_json, relative,
    require, snapshot, verify_hashes, write_frame, write_json,
)
from m2_eda_summary import accepted_summary, branch_paths


def main():
    cfg, _, summary = accepted_summary()
    branch, tables = branch_paths(cfg)
    record_file = branch/"plot_manifest.json"
    write_json(record_file, {"status": "building"})
    write_json(branch/"run_manifest.json", {"status": "building_plots"})
    try:
        cache = branch/".mplcache"
        cache.mkdir(parents=True, exist_ok=True)
        os.environ["MPLCONFIGDIR"] = str(cache)
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib import font_manager
        from matplotlib.ticker import FuncFormatter
        from PIL import Image

        style = read_json(path("configs/m2_plot_style.json"))
        font_manager.findfont(style["font_family"], fallback_to_default=False)
        plt.rcParams.update({
            "font.family": style["font_family"],
            "font.size": style["font_size_pt"],
            "axes.titlesize": style["font_size_pt"],
            "axes.labelsize": style["font_size_pt"],
            "xtick.labelsize": style["font_size_pt"],
            "ytick.labelsize": style["font_size_pt"],
            "legend.fontsize": style["font_size_pt"],
            "pdf.fonttype": 42,
        })
        figures = path(cfg["outputs"]["figures_ban1"])
        plot_data = path(cfg["outputs"]["plot_data_ban1"])
        baskets_file = path(cfg["data_dir"])/"basket_summary.parquet"
        inputs = snapshot([
            branch/"summary_manifest.json", baskets_file,
            tables/"department_display.csv", tables/"product_popularity.csv",
            tables/"top_n_coverage.csv", path("configs/m2_plot_style.json"),
        ])
        sizes = pd.read_parquet(baskets_file).basket_size
        dept = pd.read_csv(tables/"department_display.csv", keep_default_na=False)
        pop = pd.read_csv(tables/"product_popularity.csv", keep_default_na=False)
        top = pd.read_csv(tables/"top_n_coverage.csv")
        histogram = sizes.value_counts().reindex(
            range(int(sizes.min()), int(sizes.max())+1), fill_value=0
        ).rename_axis("basket_size").reset_index(name="basket_count")
        histogram["basket_share"] = histogram.basket_count/len(sizes)
        outputs = []
        for name, frame in {
            "basket_histogram": histogram,
            "basket_boxplot_values": sizes.to_frame(),
            "department_top10_remaining": dept,
            "product_cumulative": pop[["rank", "product_id", "row_count",
                                       "cumulative_row_share"]],
            "top_n_annotations": top,
        }.items():
            target = plot_data/f"{name}.csv"
            write_frame(target, frame)
            outputs.append(target)

        def save(fig, stem):
            for extension in style["formats"]:
                target = figures/f"{stem}.{extension}"
                atomic_write(target, lambda p: fig.savefig(
                    p, format=extension, dpi=style["dpi"],
                    metadata={"CreationDate": None} if extension == "pdf" else None,
                ))
                outputs.append(target)
            with Image.open(figures/f"{stem}.png") as im:
                require(abs(im.info["dpi"][0]-300) < 1, "Wrong PNG DPI")
            plt.close(fig)

        width = style["figure_width_inches"]
        color = style["colors"][0]
        percent = FuncFormatter(lambda v, _: f"{100*v:.0f}%")
        n_label = f"{len(sizes):,}".replace(",", ".")
        fig, axes = plt.subplots(2, 1, figsize=(width, 5.8),
                                 height_ratios=[3, 1], layout="constrained")
        axes[0].bar(histogram.basket_size, histogram.basket_count,
                    width=1, color=color)
        axes[0].set(ylabel="Số giỏ", xlabel="Số sản phẩm phân biệt/giỏ",
                    title=f"(a) Phân phối kích thước giỏ (N = {n_label})")
        axes[0].set_xlim(0.5, sizes.max()+0.5)
        axes[1].boxplot(sizes, orientation="horizontal", whis=1.5,
                        showfliers=True, patch_artist=True,
                        boxprops={"facecolor": style["colors"][1]},
                        flierprops={"markersize": 3, "alpha": 0.4})
        axes[1].set(xlabel="Số sản phẩm phân biệt/giỏ", yticks=[],
                    title="(b) Boxplot: râu 1,5 × IQR; giữ mọi giỏ")
        axes[1].set_xlim(0.5, sizes.max()+0.5)
        save(fig, "fig-ref-basket-distribution")

        fig, axes = plt.subplots(2, 1, figsize=(width, 7.2),
                                 height_ratios=[1.15, 1], layout="constrained")
        axes[0].barh(dept.display_name, dept.row_share, color=color)
        axes[0].invert_yaxis()
        axes[0].xaxis.set_major_formatter(percent)
        axes[0].set(xlabel="Tỷ trọng dòng sản phẩm–đơn hàng",
                    title="(a) Top-10 ngành và phần còn lại")
        axes[1].plot(pop["rank"], pop.cumulative_row_share,
                     color=style["colors"][1], linewidth=1.7)
        axes[1].scatter(top.n_actual, top.row_share, color=color, zorder=3)
        annotation = "Top-N → tỷ trọng dòng\n" + "\n".join(
            (f"{int(r.n_requested):,}".replace(",", ".") + " → " +
             f"{100*r.row_share:.2f}%".replace(".", ","))
            for r in top.itertuples()
        )
        axes[1].text(0.98, 0.05, annotation, transform=axes[1].transAxes,
                     ha="right", va="bottom", fontsize=12,
                     bbox={"facecolor": "white", "alpha": 0.9,
                           "edgecolor": "none"})
        axes[1].set(xlabel="Thứ hạng sản phẩm (popularity giảm dần)",
                    ylabel="Tỷ trọng dòng tích lũy", ylim=(0, 1.02),
                    xlim=(0, len(pop)), title="(b) Đường tích lũy sản phẩm")
        axes[1].yaxis.set_major_formatter(percent)
        save(fig, "fig-ref-category-concentration")
        accepted_summary()
        verify_hashes(inputs)
        write_json(record_file, {
            **environment(), "status": "passed", "stage": "ban1_plots",
            "foundation_sha256": summary["foundation_sha256"],
            "inputs": inputs, "code": snapshot([Path(__file__)]),
            "outputs": snapshot(outputs), "dpi": style["dpi"],
            "font_size_pt": style["font_size_pt"],
            "figure_width_inches": width,
            "checks": {"png_dpi": True, "summary_hash_gate": True},
        })
        write_json(branch/"run_manifest.json", {
            "status": "ban1_computed_peer_review_pending",
            "foundation_sha256": summary["foundation_sha256"],
            "stages": snapshot([branch/"summary_manifest.json", record_file]),
            "pending": ["member 2 confirms G0 compatibility", "cross-review",
                        "final insights I1-I3", "combined QMD integration"],
        })
        print("BAN1 FIGURES PASSED: PNG 300 DPI and vector PDF")
    except BaseException as exc:
        failed = {"status": "failed", "error": str(exc)}
        write_json(record_file, failed)
        write_json(branch/"run_manifest.json", failed)
        raise


if __name__ == "__main__":
    main()
