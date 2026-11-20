"""Chương 4: bảng mô tả hai tập, độ phủ luật, importance, hệ số LR và hai giỏ ví dụ trên dữ liệu thật.

Chỉ dùng giỏ fit/validation (test không được nạp) và hai Pipeline đã khóa. Importance dùng hàm của
m4_interpret.py trên 5.000 giỏ validation (seed 44, mọi ứng viên). Chạy sau m4_lock.py.

ĐỌC NHANH: sinh các bảng và hình mô tả của Chương 4 từ hai Pipeline đã khóa, chỉ trên fit/validation (test không nạp).
  Gồm: Bảng 4.2 (mô tả hai tập), độ phủ luật, importance và hình, hệ số LR, hai giỏ ví dụ (một có luật khớp, một không).
"""
import joblib
import numpy as np
import pandas as pd

from m4_classifier import CATEGORY, NUMERIC
from m4_common import basket_features, config, locked_stage, make_batches
from m4_interpret import LABELS, importance_table, lr_coefficients, sample_baskets
from project_io import check_hashes, path, plot_setup, save_figure, write_frame, write_json

FEATURES = NUMERIC + CATEGORY
REPORT = "BAO CAO/Bao cao mo hinh"


# Bảng 4.2: số giỏ, sản phẩm che, phần thuộc C, số cặp ứng viên, tỷ lệ dương.
def describe(masked, ctx, record, train):
    """Bảng 4.2 cho reference, fit, validation: số giỏ, sản phẩm che, phần thuộc C, số cặp ứng viên, tỷ lệ dương."""
    rows = [dict(split="reference", baskets=record["reference_baskets"])]
    for split in ("fit", "validation"):
        part = masked[masked.split == split]
        used = part[part.eligible]
        hidden, in_c = used.hidden.map(len), used.hidden.map(lambda h: int((ctx["pos"][h] >= 0).sum()))
        pairs = len(ctx["pid"]) - used.observed.map(lambda o: int((ctx["pos"][o] >= 0).sum()))
        rows.append(dict(split=split, baskets=len(part), one_item_baskets=int((~part.eligible).sum()), evaluated=len(used),
                         hidden=int(hidden.sum()), hidden_in_C_micro=in_c.sum() / hidden.sum(),
                         hidden_in_C_macro=(in_c / hidden).mean(), candidate_pairs=int(pairs.sum()),
                         positive_rate=in_c.sum() / pairs.sum(),
                         positive_rate_sampled=train.y.mean() if split == "fit" else None))
    return pd.DataFrame(rows)


# Hình importance: hai panel (LR, RF), cột = mức giảm AP khi hoán vị đặc trưng.
def figure(importance):
    plt, style = plot_setup()
    from matplotlib.ticker import ScalarFormatter

    class Comma(ScalarFormatter):
        """Nhãn trục số dùng dấu phẩy thập phân cho khớp lời văn (07/11)."""
        def __call__(self, x, pos=None):
            return super().__call__(x, pos).replace(".", ",")

    fig, axes = plt.subplots(2, 1, figsize=(16 / 2.54, 5.6))
    for ax, method, color in zip(axes, ["LR", "RF"], style["colors"]):
        rows = importance[importance.method == method].set_index("feature").loc[FEATURES]
        ax.barh(LABELS, rows.ap_decrease_mean, xerr=rows.ap_decrease_std, color=color, capsize=3)
        ax.invert_yaxis()
        ax.axvline(0, color="gray", linewidth=0.8)
        ax.set_title(method)
        ax.set_xlabel("Mức giảm Average Precision")
        ax.xaxis.set_major_formatter(Comma())
    fig.subplots_adjust(left=0.36, right=0.96, top=0.95, bottom=0.16, hspace=0.6)
    save_figure(plt, fig, REPORT + "/figures", "fig-importance", style)


# Giỏ ví dụ: Top-5 của bốn phương pháp, đánh dấu hit nếu nằm trong H.
def example(case, row, ctx, idx, models, names):
    """Top-5 của bốn phương pháp cho một giỏ; hit = sản phẩm nằm trong H."""
    _, X = next(make_batches(pd.DataFrame([row]), ctx, idx, 1))
    keys = {"Popularity": [X.candidate_popularity], "Rules": [X.max_rule_confidence, X.candidate_popularity],
            **{m: [model.predict_proba(X[FEATURES])[:, 1]] for m, model in models.items()}}
    out = []
    for method, key in keys.items():
        top = X.iloc[np.lexsort((X.product_id.to_numpy(), *[-np.asarray(k, float) for k in key[::-1]]))[:5]]
        out += [dict(case=case, order_id=row.order_id, method=method, rank=r + 1, product_id=p,
                     product_name=names.get(p, ""), hit=bool(h)) for r, (p, h) in enumerate(zip(top.product_id, top.y))]
    return out


# main: bảng mô tả -> độ phủ luật -> importance và hệ số LR -> hình -> hai giỏ ví dụ.
def main():
    cfg = config()
    check_hashes()
    masked, ctx, idx, record = locked_stage(cfg)
    data, report = path(cfg["data_dir"]), path(REPORT)
    write_frame(report / "dataset_description.csv", describe(
        masked, ctx, record, pd.read_parquet(data / "features_fit.parquet", columns=["y"])))
    val = masked[(masked.split == "validation") & masked.eligible]
    # Độ phủ luật: tỷ lệ giỏ validation có ít nhất một luật khớp.
    flags = np.array([basket_features(o, ctx, idx)["matching_rule_count"].any() for o in val.observed])
    write_json(report / "rule_coverage.json", dict(validation_baskets=len(val), with_matching_rule=int(flags.sum()),
                                                   share=float(flags.mean())))
    # Importance (hoán vị đặc trưng, đo bằng AP) và hệ số LR trên 5.000 giỏ validation.
    models = {m: joblib.load(data / f"pipeline_{m.lower()}.joblib") for m in ("LR", "RF")}
    sample = sample_baskets(val, 5000, cfg["seeds"]["importance"])
    X = pd.concat([x for _, x in make_batches(sample, ctx, idx, cfg["batch_size"])], ignore_index=True)
    tables, repeats, baseline = [], [], {}
    for m, model in models.items():
        table, raw, baseline[m] = importance_table(model, X, X.y.to_numpy().astype(int), m, seed=cfg["seeds"]["importance"])
        tables.append(table)
        repeats.append(raw)
    importance = pd.concat(tables, ignore_index=True)
    write_frame(report / "importance.csv", importance)
    write_frame(report / "importance_repeats.csv", pd.concat(repeats, ignore_index=True))
    write_frame(report / "lr_coefficients.csv", lr_coefficients(models["LR"]))
    write_json(report / "importance_baseline.json", dict(baskets=len(sample), candidate_rows=len(X), average_precision=baseline))
    figure(importance)
    # Hai giỏ ví dụ: một giỏ có luật khớp, một giỏ không có.
    names = pd.read_parquet(path("DATA/Data đã làm sạch/master_train.parquet"), columns=["product_id", "product_name"])
    names = names.drop_duplicates("product_id").set_index("product_id").product_name.to_dict()
    picked = {"có luật khớp": val[flags].iloc[0], "không có luật khớp": val[~flags].iloc[0]}
    write_frame(report / "examples.csv", pd.DataFrame(
        [r for case, row in picked.items() for r in example(case, row, ctx, idx, models, names)]))


if __name__ == "__main__":
    main()
