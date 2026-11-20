"""Generate member-1 drafts from accepted tables; never edit the main QMD."""

from pathlib import Path

import pandas as pd

from m2_common import (
    atomic_write, digest, path, read_json, relative, require, snapshot,
    verify_hashes, write_json,
)
from m2_eda_summary import accepted_summary, branch_paths


def vi(value, digits=2):
    if pd.isna(value):
        return "---"
    return f"{value:,.{digits}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def latex_escape(value):
    return str(value).replace("_", r"\_").replace("%", r"\%").replace("&", r"\&")


def table(caption, label, headers, rows, source, widths):
    spec = "@{}" + "".join(
        rf">{{\raggedright\arraybackslash}}p{{{w}cm}}" for w in widths
    ) + "@{}"
    body = "\n".join(" & ".join(map(latex_escape, row))+r" \\" for row in rows)
    header = " & ".join(map(latex_escape, headers))+r" \\"
    return rf"""
```{{=latex}}
\begingroup
\normalsize
\setlength{{\tabcolsep}}{{3pt}}
\begin{{longtable}}{{{spec}}}
\caption{{{caption}}}\label{{{label}}}\\
\toprule
{header}
\midrule
\endfirsthead
\toprule
{header}
\midrule
\endhead
{body}
\bottomrule
\end{{longtable}}
\endgroup
```

*Nguồn: {source}. Đơn vị và mẫu số theo chú giải trong phần nội dung.*

"""


def write_text(destination, text):
    atomic_write(destination, lambda p: p.write_text(text, encoding="utf-8"))


def main():
    cfg, foundation, summary = accepted_summary()
    branch, tables = branch_paths(cfg)
    plot = read_json(branch/"plot_manifest.json")
    require(plot["status"] == "passed", "Figures not accepted")
    for key in ("inputs", "code", "outputs"):
        verify_hashes(plot[key])
    drafts = path(cfg["outputs"]["drafts"])
    s = pd.read_csv(tables/"eda_summary.csv").set_index("variable")
    overview = pd.read_csv(tables/"sample_overview.csv").set_index("metric").value
    top = pd.read_csv(tables/"top_n_coverage.csv")
    dept = pd.read_csv(tables/"department_display.csv")
    out = read_json(tables/"reference_outliers.json")
    frequencies = pd.read_csv(tables/"categorical_frequencies.csv", keep_default_na=False)
    n = int(overview["baskets"])
    row_count = int(overview["product_order_rows"])
    size = s.loc["basket_size"]
    singleton = int(overview["singleton_baskets"])
    names = {"basket_size": "Sản phẩm/giỏ", "n_departments": "Ngành/giỏ",
             "n_aisles": "Quầy/giỏ", "days_since_prior_order": "Khoảng cách (ngày)"}
    scope = f"""<!-- Bản thảo Bạn 1; tích hợp từ gốc bài sau kiểm tra chéo. -->
## Phân tích thống kê mô tả

### Phạm vi mẫu và đơn vị thống kê

Phân tích mô tả sử dụng riêng tập reference đã nghiệm thu từ Master theo phân hoạch người dùng cố định (seed 42, PCG64). Tập này gồm **{vi(n, 0)} người dùng và {vi(n, 0)} giỏ train**, với **{vi(row_count, 0)} dòng sản phẩm–đơn hàng**; quan sát được {vi(overview['products_observed'], 0)} sản phẩm, {vi(overview['departments_observed'], 0)} ngành và {vi(overview['aisles_observed'], 0)} quầy. Mỗi người chỉ có một giỏ train trong thiết kế hiện hành. Reference giữ toàn bộ thành phần của từng giỏ, kể cả giỏ một sản phẩm; không lọc Top-N trước thống kê và không dùng fit, validation hoặc test để lựa chọn phân tích.

Bảng cấp giỏ dùng một dòng mỗi đơn để mô tả kích thước, độ đa dạng và thuộc tính thời gian. Bảng cấp dòng dùng lượt xuất hiện sản phẩm trong đơn để mô tả cơ cấu danh mục. Giá trị thiếu được giữ nguyên; thống kê định lượng tính trên quan sát hợp lệ và công bố mẫu số. Dữ liệu G0 được đọc qua cổng kiểm tra hash; bảng giỏ được dựng lại từ reference để đối chiếu chính xác trước khi xuất thống kê. Nguồn quy mô là `sample_overview.csv`; quy tắc chia tập đã trình bày ở Chương 2.

### Đặc điểm thống kê của giỏ hàng

Hai bảng dưới tách thông tin chất lượng/phân tán và năm con số để bảo đảm cỡ chữ 12 pt. Độ lệch chuẩn mẫu sử dụng ddof = 1; phân vị nội suy tuyến tính. Khoảng cách ngày giữ quy tắc giới hạn mã hóa tại 30 của dữ liệu nguồn.
"""
    scope += table(
        "Số quan sát hợp lệ, tỷ lệ thiếu và mức phân tán của reference",
        "tbl-ref-quality-dispersion",
        ["Biến", "N hợp lệ", "Thiếu (%)", "Mean", "Std"],
        [[names[k], vi(r.n_valid, 0), vi(r.missing_pct), vi(r['mean']), vi(r['std'])]
         for k, r in s.iterrows()],
        "eda_summary.csv; mỗi biến có tổng cộng "+vi(n, 0)+" giỏ",
        [4.4, 2.3, 2.5, 2.3, 2.3],
    )
    scope += table(
        "Năm con số của các biến định lượng cấp giỏ reference",
        "tbl-ref-five-numbers", ["Biến", "Min", "Q1", "Median", "Q3", "Max"],
        [[names[k]]+[vi(r[c], 0) for c in ["min", "q1", "median", "q3", "max"]]
         for k, r in s.iterrows()], "eda_summary.csv",
        [4.4, 1.8, 1.8, 2.2, 1.8, 1.8],
    )
    scope += f"""Giỏ reference có trung vị {vi(size['median'], 0)} sản phẩm, trong khi trung bình là {vi(size['mean'])}; Q1 = {vi(size.q1, 0)} và Q3 = {vi(size.q3, 0)}. Độ lệch {vi(size['skew'])} và độ nhọn dư (excess kurtosis) {vi(size.kurtosis_excess)} bổ sung bằng chứng về phân phối lệch phải với phần đuôi lớn. Có {vi(singleton, 0)} giỏ một sản phẩm ({vi(100*singleton/n)}%). Kích thước quan sát trải từ {vi(size['min'], 0)} đến {vi(size['max'], 0)} sản phẩm; các số này mô tả giỏ, không xác định loại hộ gia đình hay mục đích mua hàng.

Trên riêng reference, IQR = {vi(out['iqr'], 0)}, hàng rào là [{vi(out['lower_fence'], 1)}; {vi(out['upper_fence'], 1)}]. Có {vi(out['flagged_baskets'], 0)} giỏ ({vi(out['flagged_pct'])}%) vượt hàng rào. Toàn bộ được giữ lại vì cờ thống kê không tự chứng minh lỗi giao dịch. Kết quả này có mẫu số reference, khác kiểm toán toàn Master ở mục 3.3; số liệu chi tiết nằm trong `reference_outliers.json`.

Khoảng cách đơn hàng có {vi(s.loc['days_since_prior_order','n_valid'], 0)} quan sát hợp lệ, trung vị {vi(s.loc['days_since_prior_order','median'], 0)} ngày và Q3 bằng 30. Mốc 30 có giới hạn mã hóa, nên không diễn giải thành khoảng cách thực chính xác cho mọi đơn ở ngưỡng này. Tần số ngày, giờ và nhóm giờ được xuất đầy đủ trong `categorical_frequencies.csv`, gồm các mã không có quan sát và nhóm thiếu; tỷ lệ trên toàn mẫu (`all_pct`) tách khỏi tỷ lệ trên phần hợp lệ (`valid_pct`).

"""
    missing = frequencies[(frequencies.is_missing == True) &
                          frequencies.variable.isin(["order_dow", "order_hour_of_day"])]
    scope += "Cụ thể, " + "; ".join(
        f"{'mã ngày' if r.variable == 'order_dow' else 'giờ đặt hàng'} thiếu {vi(r.count, 0)} giỏ ({vi(r.all_pct)}%)"
        for r in missing.itertuples()
    ) + ". Mã ngày giữ 0–6, không tự ánh xạ thành tên thứ. Phân tích nhóm thời gian và dashboard sẽ do nhánh đa biến thực hiện.\n\n"
    scope += """### Cơ cấu ngành/quầy và mức tập trung sản phẩm

Các phép tổng hợp nhóm theo ID ổn định; tên thiếu chỉ được hiển thị thành “Chưa có tên (ID=...)”, không làm mất nhóm. Hai bảng chi tiết `department_summary.csv` và `aisle_summary.csv` giữ đủ danh mục nguồn, báo số dòng, số giỏ, tỷ trọng dòng, độ phủ giỏ và số `reordered` hợp lệ/thiếu. Tỷ lệ mua lại quan sát được chỉ lấy số dòng có `reordered = 1` chia cho số dòng có `reordered` hợp lệ; không coi các ô thiếu là chưa mua lại.

Bảng rút gọn chọn 10 ngành có nhiều dòng nhất, phá hòa bằng ID tăng dần; phần còn lại được tổng hợp lại trên các dòng và hợp các giỏ tương ứng.
"""
    scope += table(
        "Cơ cấu ngành hàng trên reference: Top-10 và phần còn lại",
        "tbl-ref-department-structure",
        ["Ngành", "Số dòng", "Dòng (%)", "Phủ giỏ (%)"],
        [[r.display_name, vi(r.row_count, 0), vi(100*r.row_share),
          vi(100*r.basket_coverage)] for r in dept.itertuples()],
        "department_display.csv; tỷ trọng trên "+vi(row_count, 0)+
        " dòng, độ phủ trên "+vi(n, 0)+" giỏ", [5.6, 2.8, 2.8, 2.8],
    )
    first = dept.iloc[0]
    scope += f"""Ngành {first.display_name} có {vi(first.row_count, 0)} lượt xuất hiện, chiếm {vi(100*first.row_share)}% dòng và hiện diện trong {vi(first.basket_count, 0)} giỏ ({vi(100*first.basket_coverage)}%). Tỷ trọng dòng các ngành cộng thành 100%, nhưng độ phủ có thể cộng vượt 100% vì một giỏ chứa nhiều ngành. Nhóm “còn lại” phủ {vi(100*dept.iloc[-1].basket_coverage)}% giỏ; con số này được tính từ hợp giỏ, không cộng độ phủ từng ngành. Lượt xuất hiện không phải số đơn vị bán hay doanh thu. Các nhãn nguồn `other` và `missing` được giữ nguyên, với giới hạn diễn giải về nội dung ngành.

Popularity của sản phẩm là số giỏ chứa sản phẩm chia cho {vi(n, 0)} giỏ reference. Xếp hạng giảm theo popularity, phá hòa bằng ID sản phẩm tăng dần. Các mốc Top-N đã chốt trước được dùng để mô tả hai chỉ tiêu riêng: tỷ trọng dòng thuộc danh mục và tỷ lệ giỏ có ít nhất một sản phẩm thuộc danh mục.
"""
    scope += table(
        "Tỷ trọng dòng và độ phủ giỏ theo các mốc Top-N",
        "tbl-ref-top-n", ["Top-N", "Số dòng", "Dòng (%)", "Số giỏ", "Phủ giỏ (%)"],
        [[vi(r.n_actual, 0), vi(r.row_count, 0), vi(100*r.row_share),
          vi(r.basket_count, 0), vi(100*r.basket_coverage)] for r in top.itertuples()],
        "top_n_coverage.csv; mẫu số "+vi(row_count, 0)+" dòng và "+vi(n, 0)+" giỏ",
        [2, 3, 2.8, 3, 2.8],
    )
    last = top.iloc[-1]
    scope += f"""Top-{vi(last.n_actual, 0)} sản phẩm chiếm {vi(100*last.row_share)}% dòng nhưng phủ {vi(100*last.basket_coverage)}% giỏ. Vẫn còn {vi(last.outside_row_count, 0)} dòng ({vi(100*last.outside_row_share)}%) nằm ngoài nhóm này. Một giỏ được “phủ” có thể đồng thời chứa nhiều sản phẩm ngoài Top-N; vì vậy độ phủ giỏ cao không chứng minh danh mục đã giữ gần hết thành phần giỏ. Các con số chỉ cung cấp căn cứ cho lưới pilot Chương 4, chưa chốt N hoặc ngưỡng support và chưa chứng minh hiệu quả gợi ý.
"""
    figure_dir = cfg["outputs"]["figures_ban1"]
    figures = f"""<!-- Chỉ phần Bạn 1 của 3.5; đường dẫn tính từ QMD chính. -->
### Phân phối kích thước giỏ hàng

![Phân phối kích thước giỏ reference: histogram bin rộng một sản phẩm và boxplot giữ các điểm ngoài râu.](<{figure_dir}/fig-ref-basket-distribution.pdf>){{#fig-ref-basket-distribution width=16cm fig-pos=H}}

*Nguồn: basket_summary.parquet đã nghiệm thu; dữ liệu vẽ basket_histogram.csv và basket_boxplot_values.csv của nhánh Bạn 1. N = {vi(n, 0)} giỏ; hình PNG 300 DPI và PDF vector.*

Histogram thể hiện tần số từng kích thước nguyên trên toàn khoảng quan sát. Boxplot dùng râu 1,5 × IQR; các điểm ngoài râu vẫn thuộc phân tích. Trung vị {vi(size['median'], 0)}, Q1–Q3 là {vi(size.q1, 0)}–{vi(size.q3, 0)} sản phẩm; phần đuôi phải giải thích vì sao mean lớn hơn median. Các điểm trùng kích thước có thể chồng nhau trên boxplot, nên số giỏ bị gắn cờ được đọc từ bảng kiểm toán, không đếm số chấm trên hình.

### Cơ cấu ngành hàng và đường tích lũy sản phẩm

![Tỷ trọng dòng của Top-10 ngành và phần còn lại; đường tỷ trọng dòng tích lũy theo thứ hạng sản phẩm.](<{figure_dir}/fig-ref-category-concentration.pdf>){{#fig-ref-category-concentration width=16cm fig-pos=H}}

*Nguồn: department_display.csv, product_popularity.csv, top_n_coverage.csv; {vi(row_count, 0)} dòng reference. Bản PNG 300 DPI/PDF vector.*

Đường tích lũy đạt 100% trên {vi(overview['products_observed'], 0)} sản phẩm quan sát; thứ hạng theo popularity giảm dần, phá hòa bằng ID tăng dần. Các mốc Top-N chỉ mô tả tỷ trọng dòng, không phải doanh thu hay quyết định cắt danh mục. Chưa kết luận quy luật 80–20 từ hình này.
"""
    evidence = f"""# G1 — Bằng chứng I1–I3, chờ Bạn 2 kiểm tra và viết insight

Không phải bản insight cuối. Foundation SHA-256: `{summary['foundation_sha256']}`.
Canonical split: `{foundation['canonical_split_sha256']}`.
Mẫu số: {n} giỏ/người, {row_count} dòng.

| Insight | Bằng chứng | Nguồn | Giới hạn / việc Bạn 2 xác nhận |
|---|---|---|---|
| I1 | Median={size['median']}; Q1={size.q1}; Q3={size.q3}; IQR={out['iqr']}; singleton={singleton}/{n}; vượt rào={out['flagged_baskets']}/{n} | eda_summary.csv; sample_overview.csv; reference_outliers.json | Giữ mọi giỏ; không suy kiểu hộ gia đình. Bạn 2 viết hành động có thể thử. |
| I2 | produce: {int(first.row_count)}/{row_count} dòng; {int(first.basket_count)}/{n} giỏ | department_summary.csv; department_display.csv | Không suy doanh thu hoặc cộng độ phủ; đọc đủ 21 ngành trong CSV. |
| I3 | Xem toàn bộ năm mốc Top-N bên dưới | top_n_coverage.csv; product_popularity.csv | Không chốt N/support; phủ giỏ không bằng giữ đủ sản phẩm của giỏ. |

| N | Số dòng | Tỷ trọng dòng [0,1] | Số giỏ | Độ phủ giỏ [0,1] |
|---:|---:|---:|---:|---:|
"""
    evidence += "\n".join(
        f"| {int(r.n_actual)} | {int(r.row_count)} | {r.row_share!r} | {int(r.basket_count)} | {r.basket_coverage!r} |"
        for r in top.itertuples()
    )
    evidence += "\n\nƯu tiên số đầy đủ trong CSV; số trên bản thảo chỉ làm tròn khi trình bày. I4–I5, kiểm định 3.6 và insights.csv thuộc Bạn 2.\n"
    outputs = []
    for filename, text in {
        "ban1_3_4.qmd": scope,
        "ban1_3_5_hinh_1_2.qmd": figures,
        "ban1_evidence_i1_i3.md": evidence,
    }.items():
        target = drafts/filename
        write_text(target, text)
        outputs.append(target)
    # Preview is separate from the main thesis and uses its own relative paths.
    preview_header = """---
lang: vi
format:
  pdf:
    documentclass: report
    pdf-engine: xelatex
    papersize: a4
    fontsize: 12pt
    mainfont: Times New Roman
    geometry: [top=2cm, bottom=2cm, left=3cm, right=2cm]
    linestretch: 1.3
    number-sections: true
    top-level-division: chapter
    fig-cap-location: bottom
    include-in-header:
      text: |
        \\usepackage{float}
        \\usepackage{longtable}
        \\usepackage{booktabs}
        \\usepackage{array}
        \\usepackage{caption}
        \\captionsetup{font=normalsize}
        \\widowpenalty=10000
        \\clubpenalty=10000
        \\AtBeginDocument{\\renewcommand{\\tablename}{Bảng}\\renewcommand{\\figurename}{Hình}}
---

```{=latex}
\\setcounter{chapter}{2}
\\renewcommand{\\tablename}{Bảng}
\\renewcommand{\\figurename}{Hình}
```

# BẢN XEM THỬ PHẦN BẠN 1

Bản riêng để kiểm tra trình bày 3.4 và hai hình đầu 3.5. Chưa tích hợp vào bài chính; chưa nghiệm thu chung và không chứa kết quả của Bạn 2. Số bảng/hình sẽ được kiểm tra lại khi tích hợp.

```{=latex}
\\setcounter{section}{3}
\\setcounter{table}{7}
\\setcounter{figure}{1}
```

"""
    preview = preview_header + scope + "\n\\clearpage\n\n## Trực quan hóa dữ liệu và Phát hiện Insight kinh doanh\n\n" + figures.replace(
        f"<{figure_dir}/", f"<../../{figure_dir}/"
    ).replace("### Cơ cấu ngành", "\\clearpage\n\n### Cơ cấu ngành")
    target = drafts/"ban1_preview.qmd"
    write_text(target, preview)
    outputs.append(target)
    write_json(branch/"draft_manifest.json", {
        "status": "generated_peer_review_pending",
        "foundation_sha256": summary["foundation_sha256"],
        "inputs": snapshot([branch/"summary_manifest.json", branch/"plot_manifest.json"]),
        "code": snapshot([Path(__file__)]), "outputs": snapshot(outputs),
    })
    print("BAN1 DRAFTS GENERATED; main thesis untouched")


if __name__ == "__main__":
    main()
