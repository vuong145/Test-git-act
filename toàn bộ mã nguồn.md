# Toàn bộ mã nguồn — Tiểu luận PRJ-08

**Đề tài:** Phân tích giỏ hàng và đề xuất bán chéo trên dữ liệu Instacart quy mô lớn (PRJ-08)  
**Nhóm 01:** Lê Văn Vương (2521001118), Hoàng Thanh Phong (2521001087) · **Giảng viên:** Trần Mạnh Tường · **Lớp học phần:** 2631101190501  
**Ngày tổng hợp:** 11/11/2026 16:41 · **Số tệp:** 48 · **Tổng số dòng:** 5.318  
**Tệp đi kèm:** `nhật ký làm việc.md` (nhật ký P-D-M-V) và thư mục `2521001118_Nhom01_TieuLuan/` (mã chạy được, dữ liệu, kết quả, báo cáo PDF).

---

## Cách đọc tệp này

- Tệp gom **nguyên văn** toàn bộ mã nguồn, cấu hình và kiểm thử liên quan trực tiếp tới bài tiểu luận, lấy từ thư mục `2521001118_Nhom01_TieuLuan/` của workspace nộp kèm. Tệp gốc trong workspace là bản chạy được; tệp này để đọc và chấm.
- **Số ở đầu mỗi dòng code là số dòng trong tệp gốc** (cột `số | mã`), dùng để đối chiếu khi bài hoặc khi vấn đáp nhắc "dòng N của tệp X". Muốn chạy thì dùng tệp gốc, không chép từ đây.
- Mỗi tệp có một khung ghi chú: vai trò, mục tương ứng trong bài, người viết, đầu vào → đầu ra, các hàm chính kèm số dòng, lệnh chạy. SHA-256 (12 ký tự đầu) giúp đối chiếu tệp ở đây đúng là tệp trong workspace.
- **Tệp trong khóa thực nghiệm:** bảy tệp có ghi "Có" ở cột Khóa được ghi SHA-256 trong `BAO CAO/Bao cao mo hinh/lock.json` trước khi chấm tập test (04/11/2026). Chúng được giữ nguyên sau đó để bảo toàn bằng chứng rằng kết quả test sinh ra từ đúng mã này.
- Không gồm: mã tạm và mã cũ đã lưu trữ, tệp tự sinh (`__pycache__`), dữ liệu và kết quả.

## Môi trường và thứ tự chạy

Môi trường `.venv-m2`: Python 3.12.14, pandas 3.0.1, NumPy 2.3.5, PyArrow 26.0.0, SciPy 1.16.3, Matplotlib 3.10.8, Seaborn 0.13.2, scikit-learn 1.9.1, mlxtend 0.25.0 (đủ 23 gói ở tệp 1). Chạy từ thư mục `2521001118_Nhom01_TieuLuan/`:

```text
 1  scripts/cleaning/clean_vuong.py        # 3.3  làm sạch aisles, departments, prior
 2  scripts/cleaning/clean_phong.py        # 3.3  làm sạch products, orders, train
 3  scripts/summarize_cleaning.py          # 3.3  gộp và xác minh sáu CSV sạch
 4  scripts/m1_build_master.py             # 3.2  bảng Master
 5  scripts/m1_quality_summary.py          # 3.2  tỷ lệ thiếu, kiểm toán IQR
 6  scripts/m1_inspect_artifact.py         # 3.2  shape, info, hai chế độ đọc
 7  scripts/m1_benchmark.py                # 3.2  benchmark (chạy một mình)
 8  scripts/m2_foundation.py               # 3.4  chia tập, reference
 9  scripts/m2_profile_inputs.py           # 3.2  dấu vết đầu vào
10  scripts/m2_eda_summary.py              # 3.4  thống kê mô tả
11  scripts/m2_plot_univariate.py          # 3.5  Hình 3.2, 3.3
12  scripts/m2_eda_multivariate.py         # 3.5  bảng đa biến
13  scripts/m2_plot_multivariate.py        # 3.5  Hình 3.4–3.7
14  scripts/m2_hypothesis_tests.py         # 3.6  kiểm định H1–H3
15  scripts/m4_prepare.py                  # 4.2  che giỏ
16  scripts/m4_mining.py                   # 4.3  luật FP-Growth
17  scripts/m4_benchmark_mining.py         # 4.3  Apriori và FP-Growth
18  scripts/m4_validate.py [--pilot]       # 4.3  chọn cấu hình trên validation
19  scripts/m4_lock.py --approve ...       # 4.4  khóa trước khi mở test
20  scripts/m4_report.py                   # 4.2, 4.5  bảng mô tả, importance
21  scripts/m4_test.py test                # 4.4  chấm test MỘT LẦN (đã chạy 04/11/2026)
22  python -m unittest discover -s tests   # 57 test
23  scripts/render_pdf.py --no-open        # xuất PDF
```

## Bảng tổng quan

STT trùng với số thứ tự tiêu đề của từng tệp bên dưới (ví dụ tệp số 21 nằm ở tiêu đề "21.").

| STT | Tệp | Mục trong bài | Người viết | Khóa | Số dòng |
|---:|---|---|---|:---:|---:|
| 1 | `requirements.txt` | 2.5 | Vương | Có | 25 |
| 2 | `scripts/project_io.py` | Dùng chung (3.4–4.6) | Vương | Có | 122 |
| 3 | `scripts/m1_common.py` | 3.2 | Vương |  | 87 |
| 4 | `scripts/cleaning/common.py` | 3.3 | Vương |  | 500 |
| 5 | `scripts/cleaning/clean_vuong.py` | 3.3 | Vương |  | 23 |
| 6 | `scripts/cleaning/config_vuong.json` | 3.3 | Vương |  | 61 |
| 7 | `scripts/cleaning/clean_phong.py` | 3.3 | Phong |  | 102 |
| 8 | `scripts/cleaning/config_phong.json` | 3.3 | Phong |  | 74 |
| 9 | `scripts/summarize_cleaning.py` | 3.3 (Bảng 3.5, 3.6) | Vương |  | 98 |
| 10 | `scripts/m1_build_master.py` | 3.2 (Bảng 3.2, 3.3) | Vương |  | 271 |
| 11 | `scripts/m1_quality_summary.py` | 3.2–3.3 | Vương |  | 68 |
| 12 | `scripts/m1_inspect_artifact.py` | 3.2 | Phong |  | 44 |
| 13 | `scripts/m1_benchmark.py` | 3.2 (Bảng 3.4) | Vương |  | 788 |
| 14 | `configs/m2_eda.json` | 3.4–3.5 | Vương |  | 61 |
| 15 | `configs/m2_plot_style.json` | 3.4–3.5 | Vương | Có | 13 |
| 16 | `configs/hypotheses_config.json` | 3.6 | Phong |  | 17 |
| 17 | `scripts/m2_foundation.py` | 3.4, 4.2 | Vương |  | 153 |
| 18 | `scripts/m2_profile_inputs.py` | 3.2 | Vương |  | 45 |
| 19 | `scripts/m2_eda_summary.py` | 3.4 (Bảng 3.7–3.9) | Vương |  | 157 |
| 20 | `scripts/m2_plot_univariate.py` | 3.5 (Hình 3.2, 3.3) | Vương |  | 82 |
| 21 | `scripts/m2_eda_multivariate.py` | 3.5 | Phong |  | 141 |
| 22 | `scripts/m2_plot_multivariate.py` | 3.5 (Hình 3.4–3.7) | Phong |  | 111 |
| 23 | `scripts/m2_hypothesis_tests.py` | 3.6 (Bảng 3.10) | Phong |  | 79 |
| 24 | `configs/m4_model.json` | 4.1–4.4 | Vương | Có | 17 |
| 25 | `scripts/m4_common.py` | 4.1–4.4 | Vương | Có | 242 |
| 26 | `scripts/m4_prepare.py` | 4.2 | Vương |  | 46 |
| 27 | `scripts/m4_mining.py` | 4.3 | Vương |  | 51 |
| 28 | `scripts/m4_benchmark_mining.py` | 4.3 | Vương |  | 89 |
| 29 | `scripts/m4_classifier.py` | 4.3 | Phong | Có | 117 |
| 30 | `scripts/m4_validate.py` | 4.1, 4.3 | Vương |  | 159 |
| 31 | `scripts/m4_lock.py` | 4.4 | Vương |  | 50 |
| 32 | `scripts/m4_interpret.py` | 4.5 | Phong |  | 111 |
| 33 | `scripts/m4_report.py` | 4.2, 4.5 | Vương |  | 113 |
| 34 | `scripts/m4_test.py` | 4.4 (Bảng kết quả test, Hình 4.1) | Phong | Có | 196 |
| 35 | `scripts/render_pdf.py` | Toàn bài | Vương |  | 80 |
| 36 | `configs/render_resources.json` | Toàn bài | Vương |  | 13 |
| 37 | `tests/test_cleaning.py` | 3.3 | — |  | 116 |
| 38 | `tests/test_m2_foundation.py` | 3.4 | — |  | 100 |
| 39 | `tests/test_m2_summary.py` | 3.4 | — |  | 111 |
| 40 | `tests/test_m2_multivariate.py` | 3.5 | — |  | 64 |
| 41 | `tests/test_m2_hypotheses.py` | 3.6 | — |  | 30 |
| 42 | `tests/fixtures/m2_contingency_cases.json` | 3.6 | — |  | 12 |
| 43 | `tests/test_m4_data.py` | 4.1–4.3 | — |  | 131 |
| 44 | `tests/test_m4_model.py` | 4.3–4.4 | Phong |  | 102 |
| 45 | `tests/test_m4_interpret.py` | 4.5 | Phong |  | 61 |
| 46 | `tests/test_m4_environment.py` | 4.3 | Phong |  | 63 |
| 47 | `tests/test_m4_gate.py` | 4.4 | Phong |  | 102 |
| 48 | `tests/test_no_hard_paths.py` | — | — |  | 20 |

---

## Phần 1. Môi trường và tiện ích dùng chung

### 1. `requirements.txt`

> **Vai trò:** Khóa phiên bản 23 gói của môi trường `.venv-m2` (Python 3.12.14).  
> **Mục trong bài:** 2.5 · **Người viết:** Vương · **Tệp trong khóa thực nghiệm**  
> **Đầu vào → đầu ra:** —  
> **Ghi chú:** Mọi lượt chạy chính thức dùng đúng các phiên bản này.  
> *25 dòng · SHA-256 `79edb2c0752a…`*

```text
 1 | # Python 3.12.14. Phiên bản khóa của môi trường .venv-m2 (làm sạch, M1, M2).
 2 | contourpy==1.4.0
 3 | cycler==0.12.1
 4 | fonttools==4.68.0
 5 | kiwisolver==1.5.1
 6 | matplotlib==3.10.8
 7 | numpy==2.3.5
 8 | packaging==26.3
 9 | pandas==3.0.1
10 | pillow==13.0.0
11 | pyarrow==26.0.0
12 | pyparsing==3.3.3
13 | python-dateutil==3.0.0
14 | scipy==1.16.3
15 | seaborn==0.13.2
16 | six==1.17.0
17 | tzdata==2026.6
18 | # Cho m1_benchmark.py (đo RSS) và Chương 4; cài thêm ngày 01/11/2026, không đổi các gói trên.
19 | cloudpickle==3.1.2
20 | joblib==1.6.0
21 | mlxtend==0.25.0
22 | narwhals==2.28.0
23 | psutil==7.2.2
24 | scikit-learn==1.9.1
25 | threadpoolctl==3.7.0
```

### 2. `scripts/project_io.py`

> **Vai trò:** Đường dẫn tương đối theo thư mục bài, đọc/ghi JSON, ghi nguyên tử (tệp tạm rồi thay thế), cổng hash `write_hashes`/`check_hashes`, thiết lập hình (Times New Roman 12 pt, PNG 300 DPI + PDF vector).  
> **Mục trong bài:** Dùng chung (3.4–4.6) · **Người viết:** Vương · **Tệp trong khóa thực nghiệm**  
> **Đầu vào → đầu ra:** `configs/m2_plot_style.json` → hàm dùng chung  
> **Hàm/lớp chính (dòng):** `require` (19), `path` (24), `relative` (28), `sha256` (32), `read_json` (37), `config` (41), `atomic_write` (51), `write_json` (64), `write_frame` (69), `write_hashes` (78), `check_hashes` (82), `plot_setup` (92), `save_figure` (109)  
> **Ghi chú:** Cổng hash: `check_hashes` dừng chương trình nếu tệp đầu vào thiếu hoặc đã đổi.  
> *122 dòng · SHA-256 `d55bbb39512c…`*

```python
  1 | """Tiện ích chung cho các script M2: đường dẫn theo thư mục bài, ghi file, cổng hash.
  2 | 
  3 | ĐỌC NHANH: bộ tiện ích dùng chung cho M2 và Chương 4. Năm nhóm: (1) kiểm tra và đường dẫn; (2) đọc/ghi JSON;
  4 |   (3) ghi an toàn (tệp tạm rồi thay thế); (4) CỔNG HASH: write_hashes ghi SHA-256, check_hashes dừng nếu tệp thiếu hoặc đã đổi;
  5 |   (5) vẽ hình (font, 12 pt, PNG 300 DPI + PDF vector). Mọi đường dẫn tính từ ROOT (thư mục bài) nên là đường dẫn tương đối.
  6 | """
  7 | import hashlib
  8 | import json
  9 | import os
 10 | import tempfile
 11 | from pathlib import Path
 12 | 
 13 | # ROOT = thư mục bài; mọi đường dẫn trong code tính từ đây.
 14 | ROOT = Path(__file__).resolve().parents[1]
 15 | FOUNDATION_HASHES = "BAO CAO/Bao cao EDA/common/hashes.json"
 16 | 
 17 | 
 18 | # Nhóm 1-2: kiểm tra điều kiện, đường dẫn, đọc JSON, đọc cấu hình đã chốt.
 19 | def require(condition, message):
 20 |     if not condition:
 21 |         raise ValueError(message)
 22 | 
 23 | 
 24 | def path(value):
 25 |     return (ROOT / value).resolve()
 26 | 
 27 | 
 28 | def relative(value):
 29 |     return Path(value).resolve().relative_to(ROOT).as_posix()
 30 | 
 31 | 
 32 | def sha256(value):
 33 |     with Path(value).open("rb") as stream:
 34 |         return hashlib.file_digest(stream, "sha256").hexdigest()
 35 | 
 36 | 
 37 | def read_json(value):
 38 |     return json.loads(Path(value).read_text(encoding="utf-8"))
 39 | 
 40 | 
 41 | def config():
 42 |     """configs/m2_eda.json với các tham số đã chốt cho phép chia tập."""
 43 |     cfg = read_json(path("configs/m2_eda.json"))
 44 |     require(cfg["seed"] == 42 and cfg["rng"] == "PCG64", "Phép chia cần PCG64 seed 42")
 45 |     require(cfg["slice_order"] == ["test", "reference", "fit", "validation"], "Sai thứ tự tập")
 46 |     require(cfg["min_group_n"] == 30, "Ngưỡng báo cáo nhóm nhỏ phải là 30")
 47 |     return cfg
 48 | 
 49 | 
 50 | # Nhóm 3: ghi an toàn; lỗi giữa chừng không làm hỏng bản cũ.
 51 | def atomic_write(destination, writer):
 52 |     """Ghi vào tệp tạm cạnh đích rồi os.replace; lỗi giữa chừng không làm hỏng bản cũ."""
 53 |     destination = Path(destination)
 54 |     destination.parent.mkdir(parents=True, exist_ok=True)
 55 |     fd, name = tempfile.mkstemp(dir=destination.parent, suffix=".tmp")
 56 |     os.close(fd)
 57 |     try:
 58 |         writer(Path(name))
 59 |         os.replace(name, destination)
 60 |     finally:
 61 |         Path(name).unlink(missing_ok=True)
 62 | 
 63 | 
 64 | def write_json(destination, obj):
 65 |     atomic_write(destination, lambda p: p.write_text(
 66 |         json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8"))
 67 | 
 68 | 
 69 | def write_frame(destination, frame):
 70 |     if str(destination).endswith(".parquet"):
 71 |         atomic_write(destination, lambda p: frame.to_parquet(p, index=False))
 72 |     else:
 73 |         atomic_write(destination, lambda p: frame.to_csv(
 74 |             p, index=False, encoding="utf-8", lineterminator="\n"))
 75 | 
 76 | 
 77 | # Nhóm 4: CỔNG HASH. Script phía sau gọi check_hashes() trước khi đọc dữ liệu.
 78 | def write_hashes(destination, files, **extra):
 79 |     write_json(path(destination), {"files": {relative(p): sha256(p) for p in files}, **extra})
 80 | 
 81 | 
 82 | def check_hashes(source=FOUNDATION_HASHES):
 83 |     """Dừng nếu file ghi trong `source` bị thiếu hoặc đổi nội dung; trả về bản ghi."""
 84 |     record = read_json(path(source))
 85 |     for name, expected in record["files"].items():
 86 |         require(path(name).is_file(), f"Thiếu file: {name}")
 87 |         require(sha256(path(name)) == expected, f"File đã thay đổi: {name}")
 88 |     return record
 89 | 
 90 | 
 91 | # Nhóm 5: vẽ hình theo cấu hình chung (font, cỡ chữ, định dạng, DPI).
 92 | def plot_setup():
 93 |     """Matplotlib Agg, font và cỡ chữ theo configs/m2_plot_style.json."""
 94 |     os.environ.setdefault("MPLCONFIGDIR", str(path("BAO CAO/Bao cao EDA/common/.mplcache")))
 95 |     import matplotlib
 96 |     matplotlib.use("Agg")
 97 |     import matplotlib.pyplot as plt
 98 |     from matplotlib import font_manager
 99 |     style = read_json(path("configs/m2_plot_style.json"))
100 |     font_manager.findfont(style["font_family"], fallback_to_default=False)
101 |     size = style["font_size_pt"]
102 |     plt.rcParams.update({"font.family": style["font_family"], "font.size": size,
103 |                          "axes.titlesize": size, "axes.labelsize": size,
104 |                          "xtick.labelsize": size, "ytick.labelsize": size,
105 |                          "legend.fontsize": size, "pdf.fonttype": 42})
106 |     return plt, style
107 | 
108 | 
109 | def save_figure(plt, fig, folder, stem, style):
110 |     """Lưu PNG 300 DPI và PDF vector cùng tên; trả về danh sách file."""
111 |     from PIL import Image
112 |     files = []
113 |     for extension in style["formats"]:
114 |         target = path(folder) / f"{stem}.{extension}"
115 |         atomic_write(target, lambda p: fig.savefig(
116 |             p, format=extension, dpi=style["dpi"],
117 |             metadata={"CreationDate": None} if extension == "pdf" else None))
118 |         files.append(target)
119 |     with Image.open(path(folder) / f"{stem}.png") as image:
120 |         require(abs(image.info["dpi"][0] - style["dpi"]) < 1, "Sai DPI của PNG")
121 |     plt.close(fig)
122 |     return files
```

### 3. `scripts/m1_common.py`

> **Vai trò:** Đường dẫn và xuất bản từng tệp cho các lệnh M1.  
> **Mục trong bài:** 3.2 · **Người viết:** Vương  
> **Đầu vào → đầu ra:** —  
> **Hàm/lớp chính (dòng):** `project_path` (21), `report_path` (27), `parse_args` (32), `atomic_publish` (64)  
> **Ghi chú:** Giữ nguyên theo quyết định của nhóm.  
> *87 dòng · SHA-256 `66a5f188b445…`*

```python
 1 | """Portable paths and per-file publication shared by the M1 commands."""
 2 | 
 3 | import argparse
 4 | import hashlib
 5 | import os
 6 | from pathlib import Path
 7 | import shutil
 8 | import tempfile
 9 | 
10 | 
11 | PROJECT_ROOT = Path(__file__).resolve().parent.parent
12 | INPUT_NAMES = (
13 |     "order_products__train.csv",
14 |     "orders.csv",
15 |     "products.csv",
16 |     "aisles.csv",
17 |     "departments.csv",
18 | )
19 | 
20 | 
21 | def project_path(value):
22 |     """Resolve relative CLI paths against the project, never the shell cwd."""
23 |     path = Path(value).expanduser()
24 |     return (path if path.is_absolute() else PROJECT_ROOT / path).resolve()
25 | 
26 | 
27 | def report_path(path):
28 |     """Store relocatable paths; reports declare PROJECT_ROOT as their base."""
29 |     return Path(os.path.relpath(Path(path).resolve(), PROJECT_ROOT)).as_posix()
30 | 
31 | 
32 | def parse_args(description, *, benchmark=False):
33 |     parser = argparse.ArgumentParser(description=description)
34 |     parser.add_argument("--clean-dir", default="DATA/Data đã làm sạch",
35 |                         help="Input directory; relative to the thesis directory.")
36 |     parser.add_argument("--output-dir", default=None,
37 |                         help="Report directory; relative to the thesis directory.")
38 |     parser.add_argument("--check-inputs", action="store_true",
39 |                         help="Check paths without importing data libraries or writing files.")
40 |     if benchmark:
41 |         parser.add_argument("--worker", nargs="+", help=argparse.SUPPRESS)
42 |     else:
43 |         parser.add_argument("--chunksize", type=int, default=250000)
44 |     args = parser.parse_args()
45 |     args.clean_dir = project_path(args.clean_dir)
46 |     args.output_dir = (project_path(args.output_dir) if args.output_dir
47 |                        else args.clean_dir / "Bảng master TLCK")
48 |     if not benchmark and args.chunksize <= 0:
49 |         parser.error("--chunksize must be positive")
50 |     if args.check_inputs:
51 |         names = INPUT_NAMES + (("master_train.parquet",) if benchmark else ())
52 |         missing = [str(args.clean_dir / name) for name in names
53 |                    if not (args.clean_dir / name).is_file()]
54 |         if missing:
55 |             parser.error("Missing inputs: " + ", ".join(missing))
56 |         print(f"INPUTS OK: {args.clean_dir}")
57 |         print(f"OUTPUT DIRECTORY: {args.output_dir}")
58 |         raise SystemExit(0)
59 |     if not __debug__:
60 |         parser.error("Do not use python -O: the M1 audit requires assertions.")
61 |     return args
62 | 
63 | 
64 | def atomic_publish(source, destination):
65 |     """Copy, verify and replace one destination; not a multi-file transaction.
66 | 
67 |     A failed copy/hash check/replace leaves the previous destination intact.
68 |     The temporary file lives beside the destination to avoid cross-volume moves.
69 |     This does not promise durability against a power failure.
70 |     """
71 |     source, destination = Path(source), Path(destination)
72 |     destination.parent.mkdir(parents=True, exist_ok=True)
73 |     fd, temporary = tempfile.mkstemp(
74 |         prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent)
75 |     temporary = Path(temporary)
76 |     try:
77 |         with os.fdopen(fd, "wb") as target, source.open("rb") as origin:
78 |             shutil.copyfileobj(origin, target)
79 |             target.flush()
80 |             os.fsync(target.fileno())
81 |         with source.open("rb") as origin, temporary.open("rb") as target:
82 |             if (hashlib.file_digest(origin, "sha256").digest()
83 |                     != hashlib.file_digest(target, "sha256").digest()):
84 |                 raise OSError("Publication copy failed SHA-256 verification")
85 |         os.replace(temporary, destination)
86 |     finally:
87 |         temporary.unlink(missing_ok=True)
```

## Phần 2. Làm sạch sáu tệp dữ liệu (mục 3.3)

### 4. `scripts/cleaning/common.py`

> **Vai trò:** Lõi làm sạch: lược đồ, khóa, miền giá trị từng cột; bộ đếm `Audit`; tái dựng thứ tự theo dòng (`RowSequence`); đọc theo khối 250.000 dòng; kiểm tra đầu ra rồi mới xuất bản.  
> **Mục trong bài:** 3.3 · **Người viết:** Vương  
> **Đầu vào → đầu ra:** 6 CSV nhiễu (`DATA/Data đã làm nhiễu/`) → 6 CSV sạch (`DATA/Data đã làm sạch/`) + báo cáo kiểm toán  
> **Hàm/lớp chính (dòng):** `sha256` (55), `write_json` (60), `chunks` (64), `append_csv` (75), `read_ids` (81), `export_query` (99), `key_digest` (107), `insert` (113), `Audit` (122), `numeric` (177), `text_column` (206), `clean_frame` (224), `RowSequence` (241), `clean_dimension` (297), `clean_detail` (316), `verify_outputs` (373), `check_expected` (401), `run` (416), `cli` (495)  
> **Ghi chú:** Nguyên tắc: ô sai/thiếu thì để thiếu; khóa sai thì dừng; mọi thay đổi đều đếm; không dùng dữ liệu gốc để điền.  
> *500 dòng · SHA-256 `bc40d94d39ce…`*

```python
  1 | """Phần dùng chung của clean_vuong.py và clean_phong.py.
  2 | 
  3 | Quy tắc theo cột, bộ đếm Audit, tái dựng thứ tự theo dòng CSV, kiểm tra đầu ra và khung
  4 | chạy: hash nguồn -> làm sạch vào thư mục tạm -> đọc lại -> so bản trước -> xuất bản.
  5 | Không dùng dữ liệu gốc để điền; số kỳ vọng trong config chỉ là kiểm tra hồi quy.
  6 | 
  7 | ĐỌC NHANH (vấn đáp):
  8 |   Mục đích: làm sạch 6 CSV nhiễu mà KHÔNG xóa dòng, KHÔNG đoán, KHÔNG dùng dữ liệu gốc để điền.
  9 |   Bốn nguyên tắc: (1) ô sai/thiếu thì để thiếu; (2) khóa sai thì dừng; (3) mọi thay đổi đều được đếm (Audit);
 10 |   (4) chỉ xuất bản khi mọi kiểm tra đạt (làm trong thư mục tạm, xong mới chép sang).
 11 |   Bố cục file: Nhóm 1 tiện ích -> Nhóm 2 Audit -> Nhóm 3 quy tắc theo cột -> Nhóm 4 tái dựng thứ tự
 12 |   -> Nhóm 5 làm sạch từng loại bảng -> Nhóm 6 kiểm chứng đầu ra và khung chạy (run, cli).
 13 |   Hỏi hay gặp: vì sao đọc dạng chữ? (để pandas không tự biến 'null' thành thiếu mà ta không đếm được);
 14 |   vì sao SQLite? (nhớ hàng chục triệu khóa mà không tràn RAM); vì sao đọc theo khối 250.000 dòng? (bảng prior 32,4 triệu dòng).
 15 | """
 16 | import argparse
 17 | from collections import Counter
 18 | import csv
 19 | from datetime import datetime, timedelta, timezone
 20 | import hashlib
 21 | import json
 22 | import os
 23 | from pathlib import Path
 24 | import platform
 25 | import shutil
 26 | import sqlite3
 27 | import sys
 28 | import time
 29 | from types import SimpleNamespace
 30 | 
 31 | import numpy as np
 32 | import pandas as pd
 33 | 
 34 | # Hằng số: tên cột từng bảng (SCHEMA), cột khóa (KEYS), miền hợp lệ và kiểu của từng cột số (DOMAINS).
 35 | DETAIL = ['order_id', 'product_id', 'add_to_cart_order', 'reordered']
 36 | SCHEMA = {'aisles': ['aisle_id', 'aisle'], 'departments': ['department_id', 'department'],
 37 |           'products': ['product_id', 'product_name', 'aisle_id', 'department_id'],
 38 |           'orders': ['order_id', 'user_id', 'eval_set', 'order_number', 'order_dow',
 39 |                      'order_hour_of_day', 'days_since_prior_order'],
 40 |           'order_products__prior': DETAIL, 'order_products__train': DETAIL}
 41 | KEYS = {'aisles': ['aisle_id'], 'departments': ['department_id'],
 42 |         'products': ['product_id', 'aisle_id', 'department_id'], 'orders': ['order_id', 'user_id'],
 43 |         'order_products__prior': ['order_id', 'product_id'],
 44 |         'order_products__train': ['order_id', 'product_id']}
 45 | DOMAINS = {'order_number': (1, 100, 'Int16'), 'order_dow': (0, 6, 'Int8'),
 46 |            'order_hour_of_day': (0, 23, 'Int8'), 'days_since_prior_order': (0, 30, 'Float64'),
 47 |            'add_to_cart_order': (1, 2147483647, 'Int32'), 'reordered': (0, 1, 'Int8')}
 48 | NUMBER = r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)'
 49 | SUFFIX = NUMBER + r'\s*(?:%|[A-Za-z][A-Za-z ]*)'
 50 | GOOD = '(known=n AND distinct_n=n AND min_n=1 AND max_n=n)'   # thứ tự 1..n, không trùng/thiếu
 51 | TZ = timezone(timedelta(hours=7))
 52 | 
 53 | 
 54 | # ===== Nhóm 1: tiện ích nhỏ (hash, ghi JSON, đọc CSV theo khối, ghi nối CSV, đọc cột khóa) =====
 55 | def sha256(path):
 56 |     with Path(path).open('rb') as stream:
 57 |         return hashlib.file_digest(stream, 'sha256').hexdigest()
 58 | 
 59 | 
 60 | def write_json(path, value):
 61 |     Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
 62 | 
 63 | 
 64 | def chunks(path, size, schema=None):
 65 |     """Đọc theo khối dạng chuỗi, giữ nguyên ký hiệu thiếu cho tới khi quy tắc kiểm tra."""
 66 |     with pd.read_csv(path, dtype='string', keep_default_na=False, na_filter=False,
 67 |                      encoding='utf-8-sig', chunksize=size, skip_blank_lines=False,
 68 |                      on_bad_lines='error') as reader:
 69 |         for frame in reader:
 70 |             if schema is not None and list(frame.columns) != schema:
 71 |                 raise ValueError(f'Sai schema {path.name}: {list(frame.columns)}')
 72 |             yield frame
 73 | 
 74 | 
 75 | def append_csv(frame, path):
 76 |     first = not path.exists()
 77 |     frame.to_csv(path, mode='w' if first else 'a', header=first, index=False,
 78 |                  encoding='utf-8-sig' if first else 'utf-8', na_rep='')
 79 | 
 80 | 
 81 | def read_ids(path, column, size, unique=False):
 82 |     """Chỉ đọc cột khóa của file nhiễu để kiểm tra khóa ngoại; khóa sai thì dừng."""
 83 |     pieces = []
 84 |     for frame in pd.read_csv(path, usecols=[column], dtype='string', keep_default_na=False,
 85 |                              chunksize=size, encoding='utf-8-sig', skip_blank_lines=False):
 86 |         values = frame[column].str.strip()
 87 |         if not values.str.fullmatch(r'\d+').all():
 88 |             raise ValueError(f'{path.name}.{column}: khóa sai định dạng')
 89 |         numbers = pd.to_numeric(values, errors='raise')
 90 |         if not numbers.between(1, 2147483647).all():
 91 |             raise ValueError(f'{path.name}.{column}: khóa ngoài miền')
 92 |         pieces.append(numbers.astype('int64').to_numpy())
 93 |     result = pd.Index(np.concatenate(pieces))
 94 |     if unique and result.has_duplicates:
 95 |         raise ValueError(f'{path.name}: trùng khóa {column}')
 96 |     return result if unique else result.unique()
 97 | 
 98 | 
 99 | def export_query(db, query, path):
100 |     cursor = db.execute(query)
101 |     with path.open('w', encoding='utf-8-sig', newline='') as stream:
102 |         writer = csv.writer(stream)
103 |         writer.writerow([x[0] for x in cursor.description])
104 |         writer.writerows(cursor.fetchall())
105 | 
106 | 
107 | def key_digest(hasher, frame, table):
108 |     """Dấu vân tay của khóa đã chuẩn hóa theo đúng thứ tự dòng."""
109 |     hasher.update(frame[KEYS[table]].to_csv(index=False, header=False,
110 |                                             lineterminator='\n').encode('utf-8'))
111 | 
112 | 
113 | def insert(db, table, frame):
114 |     with db:   # khóa chính SQLite từ chối khóa trùng
115 |         db.executemany(f'INSERT INTO {table} VALUES ({",".join("?" * frame.shape[1])})',
116 |                        frame.astype(object).where(frame.notna(), None)
117 |                        .itertuples(index=False, name=None))
118 | 
119 | 
120 | # ===== Nhóm 2: Audit = sổ đếm. Mỗi ô được gán một trạng thái (hợp lệ, cắt khoảng trắng, thiếu, ngoài miền...)
121 | # rồi cộng dồn để ra các bảng 'trước và sau' của mục 3.3. Chỉ giữ tối đa 5 ví dụ cho mỗi loại lỗi. =====
122 | class Audit:
123 |     """Đếm trạng thái rời nhau theo ô và giữ tối đa 5 ví dụ mỗi quy tắc."""
124 | 
125 |     def __init__(self, folder, config):
126 |         self.folder, self.config, self.examples, self.checks = folder, config, [], {}
127 |         self.counts, self.final_counts = Counter(), Counter()
128 |         self.relational_counts, self.example_counts = Counter(), Counter()
129 | 
130 |     def tokens(self, table, column):
131 |         tokens = self.config.get('missing_tokens_by_column', {}).get(
132 |             f'{table}.{column}', self.config['missing_tokens'])
133 |         return {str(x).strip().casefold() for x in tokens}
134 | 
135 |     def example(self, table, column, status, index, raw, clean):
136 |         key = (table, column, status)
137 |         if self.example_counts[key] < 5:
138 |             self.examples.append({'table': table, 'column': column, 'status': status,
139 |                                   'record_1based': int(index) + 1, 'raw': raw, 'clean': clean})
140 |             self.example_counts[key] += 1
141 | 
142 |     def record(self, table, column, raw, clean, status):
143 |         for label, count in status.value_counts().items():
144 |             self.counts[(table, column, str(label))] += int(count)
145 |             for i in [] if label == 'valid_domain' else status[status.eq(label)].index[:5]:
146 |                 self.example(table, column, str(label), i, str(raw.loc[i]),
147 |                              '' if pd.isna(clean.loc[i]) else str(clean.loc[i]))
148 | 
149 |     def record_final(self, table, frame):
150 |         for column in SCHEMA[table]:
151 |             missing = frame[column].isna() | frame[column].eq('').fillna(False)
152 |             self.final_counts[(table, column, 'missing')] += int(missing.sum())
153 |             self.final_counts[(table, column, 'nonmissing')] += int((~missing).sum())
154 | 
155 |     def save(self):
156 |         def out(rows, columns, name):
157 |             pd.DataFrame(rows, columns=columns).to_csv(self.folder / name, index=False,
158 |                                                        encoding='utf-8-sig')
159 |         cells = ['table', 'column', 'status', 'cells']
160 |         out([(*k, n) for k, n in sorted(self.final_counts.items())], cells, 'final_column_summary.csv')
161 |         out([(*k, n) for k, n in sorted(self.counts.items())], cells, 'cleaning_summary.csv')
162 |         out([(*k, n) for k, n in sorted(self.relational_counts.items())],
163 |             ['table', 'rule', 'affected'], 'relational_summary.csv')
164 |         unusable = ['missing_token', 'invalid_format', 'suffix_unresolved', 'out_of_domain',
165 |                     'invalid_label']
166 |         out([(t, c, self.counts[(t, c, 'missing_token')],
167 |               sum(self.counts[(t, c, s)] for s in unusable),
168 |               self.final_counts[(t, c, 'missing')], self.final_counts[(t, c, 'nonmissing')])
169 |              for t, cols in SCHEMA.items() if t in self.checks for c in cols],
170 |             ['table', 'column', 'missing_tokens_before', 'unusable_after_initial_parse',
171 |              'missing_final', 'nonmissing_final'], 'before_after.csv')
172 |         out(self.examples, ['table', 'column', 'status', 'record_1based', 'raw', 'clean'],
173 |             'examples.csv')
174 | 
175 | 
176 | # ===== Nhóm 3: quy tắc làm sạch từng cột. numeric() cho cột số, text_column() cho cột chữ, clean_frame() chọn quy tắc theo tên cột. =====
177 | def numeric(raw, table, column, audit, low, high, dtype, key=False):
178 |     # Bước 1: cắt khoảng trắng; chữ như null/none/? được coi là 'thiếu' (danh sách trong config).
179 |     s = raw.str.strip()
180 |     missing = s.str.casefold().isin(audit.tokens(table, column))
181 |     # Bước 2: chỉ nhận chuỗi đúng dạng số (cột khóa chỉ nhận chữ số).
182 |     syntax = s.str.fullmatch(r'\d+' if key else NUMBER)   # khóa chỉ nhận chữ số
183 |     values = pd.to_numeric(s.where(syntax & ~missing), errors='coerce')
184 |     valid = values.notna() & values.between(low, high)
185 |     if dtype.startswith('Int'):
186 |         valid &= values.mod(1).eq(0)
187 |     # Bước 3: gán nhãn trạng thái cho từng ô để đếm lỗi; nhãn gán sau ghi đè nhãn gán trước. Ví dụ '2 %' = suffix_unresolved (không đoán).
188 |     status = pd.Series('invalid_format', index=raw.index, dtype='string')
189 |     status.loc[~missing & s.str.fullmatch(SUFFIX)] = 'suffix_unresolved'
190 |     status.loc[syntax & ~missing & ~valid] = 'out_of_domain'
191 |     status.loc[missing] = 'missing_token'
192 |     status.loc[valid] = 'valid_domain'
193 |     status.loc[valid & raw.ne(s)] = 'trimmed'
194 |     if not key:
195 |         status.loc[valid & s.str.contains('.', regex=False)] = 'numeric_format_normalized'
196 |     # Bước 4: ô sai miền thì thành thiếu (không sửa bừa); riêng cột khóa sai thì dừng cả chương trình.
197 |     clean = values.where(valid).astype(dtype)
198 |     audit.record(table, column, raw, clean, status)
199 |     if key and clean.isna().any():
200 |         raise ValueError(f'{table}.{column}: khóa không hợp lệ; dừng, không xóa/điền.')
201 |     return clean
202 | 
203 | 
204 | # Cột chữ: cắt khoảng trắng; aisle/department/eval_set đổi chữ thường; token thiếu -> thiếu;
205 | # eval_set ngoài {prior, train, test} -> thiếu (sẽ được khôi phục ở clean_phong.py).
206 | def text_column(raw, table, column, audit, lower):
207 |     s = raw.str.strip()
208 |     missing = s.str.casefold().isin(audit.tokens(table, column))
209 |     clean = (s.str.lower() if lower else s).mask(missing)
210 |     status = pd.Series('valid_domain', index=raw.index, dtype='string')
211 |     status.loc[raw.ne(s)] = 'trimmed'
212 |     if lower:
213 |         status.loc[s.ne(s.str.lower())] = 'case_normalized'
214 |     status.loc[missing] = 'missing_token'
215 |     if column == 'eval_set':
216 |         invalid = ~missing & ~clean.isin(['prior', 'train', 'test'])
217 |         status.loc[invalid] = 'invalid_label'
218 |         clean = clean.mask(invalid)
219 |     audit.record(table, column, raw, clean, status)
220 |     return clean
221 | 
222 | 
223 | # Chọn quy tắc theo tên cột: *_id -> khóa số; cột có miền trong DOMAINS -> số; còn lại -> chữ.
224 | def clean_frame(frame, table, audit):
225 |     out = pd.DataFrame(index=frame.index)
226 |     for column in frame.columns:
227 |         if column.endswith('_id'):
228 |             dtype = {'department_id': 'Int8', 'aisle_id': 'Int16'}.get(column, 'Int32')
229 |             high = {'Int8': 127, 'Int16': 32767, 'Int32': 2147483647}[dtype]
230 |             out[column] = numeric(frame[column], table, column, audit, 1, high, dtype, key=True)
231 |         elif column in DOMAINS:
232 |             out[column] = numeric(frame[column], table, column, audit, *DOMAINS[column])
233 |         else:
234 |             out[column] = text_column(frame[column], table, column, audit,
235 |                                       column in {'department', 'aisle', 'eval_set'})
236 |     return out
237 | 
238 | 
239 | # ===== Nhóm 4: tái dựng thứ tự (add_to_cart_order, order_number) theo THỨ TỰ DÒNG trong CSV.
240 | # Đây là giả định (thứ tự dòng gốc = thứ tự thật), được nêu rõ trong báo cáo; không sắp lại theo mã. =====
241 | class RowSequence:
242 |     """Đánh số nhóm liên tiếp theo thứ tự dòng CSV, giữ trạng thái qua ranh giới khối.
243 | 
244 |     Giả định thứ tự dòng gốc là thứ tự mua/thêm giỏ; không sắp lại theo mã.
245 |     Bảng SQLite từ chối nhóm xuất hiện lại ở chỗ khác trong file.
246 |     """
247 | 
248 |     def __init__(self, db, table, key, column, audit, maximum=None):
249 |         self.db, self.table, self.key, self.column = db, table, key, column
250 |         self.audit, self.maximum, self.last_key, self.last_rank = audit, maximum, None, 0
251 |         db.execute(f'CREATE TABLE groups_{table}(id INTEGER PRIMARY KEY)')
252 | 
253 |     def apply(self, frame):
254 |         ids = frame[self.key].to_numpy(dtype=np.int64)
255 |         index = np.arange(len(ids))
256 |         # starts = dòng đầu mỗi nhóm (giỏ hoặc khách); rank = vị trí trong nhóm (1, 2, 3...).
257 |         starts = np.r_[True, ids[1:] != ids[:-1]]
258 |         first = np.maximum.accumulate(np.where(starts, index, 0))
259 |         rank = index - first + 1
260 |         # Nhóm bị cắt ngang giữa hai khối: cộng tiếp thứ hạng đã đếm ở khối trước.
261 |         if self.last_key is not None and ids[0] == self.last_key:   # nhóm nối từ khối trước
262 |             rank[first == 0] += self.last_rank
263 |             starts[0] = False
264 |         # SQLite từ chối nhóm xuất hiện lại ở chỗ khác trong file: khi đó giả định thứ tự dòng sai nên dừng.
265 |         try:
266 |             self.db.executemany(f'INSERT INTO groups_{self.table} VALUES(?)',
267 |                                 ((int(x),) for x in ids[starts]))
268 |         except sqlite3.IntegrityError as exc:
269 |             raise ValueError(f'{self.table}: nhóm xuất hiện lại; dừng tái dựng thứ tự') from exc
270 |         if self.maximum is not None and (rank > self.maximum).any():
271 |             raise ValueError(f'{self.table}: thứ tự vượt giới hạn {self.maximum}')
272 |         # Phân loại từng ô: thiếu -> điền, lệch -> sửa, đúng -> giữ nguyên; chỉ để đếm cho báo cáo.
273 |         old = frame[self.column].copy()
274 |         rebuilt = pd.Series(rank, index=frame.index, dtype=old.dtype)
275 |         missing = old.isna()
276 |         masks = {'sequence_filled_unusable': missing,
277 |                  'sequence_corrected_observed': (~missing & old.ne(rebuilt)).fillna(False),
278 |                  'sequence_observed_consistent': (~missing & old.eq(rebuilt)).fillna(False)}
279 |         for rule, mask in masks.items():
280 |             self.audit.relational_counts[(self.table, rule)] += int(mask.sum())
281 |             for i in [] if rule.endswith('consistent') else mask[mask].index[:5]:
282 |                 self.audit.example(self.table, self.column, rule, i,
283 |                                    '' if pd.isna(old.loc[i]) else str(old.loc[i]), str(rebuilt.loc[i]))
284 |         frame[self.column] = rebuilt
285 |         self.last_key, self.last_rank = int(ids[-1]), int(rank[-1])
286 | 
287 |     def finish(self):
288 |         self.audit.checks.setdefault(self.table, {}).update(
289 |             sequence_policy='reconstructed_from_preserved_csv_row_order',
290 |             sequence_semantics='assumed original purchase/cart order; not independently proven',
291 |             noncontiguous_groups=0)
292 |         self.db.execute(f'DROP TABLE groups_{self.table}')
293 | 
294 | 
295 | # ===== Nhóm 5: làm sạch từng loại bảng. clean_dimension: aisles/departments/products (bảng nhỏ, nạp một lần).
296 | # clean_detail: prior/train (bảng lớn, đọc theo khối). =====
297 | def clean_dimension(table, c):
298 |     """aisles/departments/products: kiểm tra khóa chính và (với products) khóa ngoại."""
299 |     key = KEYS[table][0]
300 |     frame = clean_frame(pd.concat(list(chunks(c.files[table], 100000, c.headers[table])),
301 |                                   ignore_index=True), table, c.audit)
302 |     if frame[key].duplicated().any():
303 |         raise ValueError(f'{table}: trùng khóa chính')
304 |     for parent in ['aisles', 'departments'] if table == 'products' else []:
305 |         if not frame[KEYS[parent][0]].isin(c.references[parent]).all():
306 |             raise ValueError(f'products: khóa ngoại mồ côi {KEYS[parent][0]}')
307 |     digest = hashlib.sha256()
308 |     key_digest(digest, frame, table)
309 |     append_csv(frame, c.work / c.files[table].name)
310 |     c.audit.checks[table] = {'input_rows': len(frame), 'input_columns': c.headers[table],
311 |                              'input_key_sha256': digest.hexdigest(),
312 |                              'primary_key_unique': True, 'foreign_keys_valid': True}
313 | 
314 | 
315 | # Bảng chi tiết giỏ hàng (prior, train): kiểm khóa ngoại, khóa trùng, rồi tái dựng add_to_cart_order.
316 | def clean_detail(table, c, order_ids, product_ids):
317 |     """prior/train cùng cấu trúc: kiểm khóa ngoại, khóa trùng, tái dựng add_to_cart_order."""
318 |     audit, db, source = c.audit, c.db, table.rsplit('__', 1)[1]
319 |     db.execute('CREATE TABLE detail (order_id INTEGER, product_id INTEGER, pos INTEGER, '
320 |                'PRIMARY KEY(order_id,product_id)) WITHOUT ROWID')
321 |     count, digest = 0, hashlib.sha256()
322 |     # Vòng 1: mỗi khối -> làm sạch cột -> kiểm khóa ngoại -> tái dựng thứ tự -> ghi vào SQLite và tệp tạm.
323 |     sequence = RowSequence(db, table, 'order_id', 'add_to_cart_order', audit)
324 |     pending = c.work / (table + '.pending')
325 |     for raw in chunks(c.files[table], c.size, c.headers[table]):
326 |         frame = clean_frame(raw, table, audit)
327 |         for column, ids in [('order_id', order_ids), ('product_id', product_ids)]:
328 |             if not frame[column].isin(ids).all():
329 |                 raise ValueError(f'{table}: {column} mồ côi')
330 |         sequence.apply(frame)
331 |         insert(db, 'detail', frame[['order_id', 'product_id', 'add_to_cart_order']])
332 |         append_csv(frame, pending)
333 |         key_digest(digest, frame, table)
334 |         count += len(frame)
335 |         print(f'{table}: {count:,}', flush=True)
336 |     # Kiểm tra sau tái dựng: mỗi giỏ phải có thứ tự đúng 1..n, không trùng, không thiếu; nếu không thì dừng.
337 |     db.execute('''CREATE TABLE basket AS SELECT order_id, COUNT(*) AS n, COUNT(pos) AS known,
338 |         COUNT(DISTINCT pos) AS distinct_n, MIN(pos) AS min_n, MAX(pos) AS max_n
339 |         FROM detail GROUP BY order_id''')
340 |     with db:   # khóa chính của sources từ chối đơn vừa thuộc prior vừa thuộc train
341 |         db.execute('INSERT INTO sources SELECT order_id, ? FROM basket', (source,))
342 |     baskets, largest = db.execute('SELECT COUNT(*), MAX(n) FROM basket').fetchone()
343 |     review = db.execute(f'SELECT COUNT(*) FROM basket WHERE NOT {GOOD}').fetchone()[0]
344 |     duplicate = db.execute('SELECT COALESCE(SUM(known-distinct_n),0) FROM basket').fetchone()[0]
345 |     export_query(db, f'''SELECT order_id, n AS basket_size, known AS parsed_positions,
346 |         known-distinct_n AS duplicate_position_extra, min_n AS min_pos, max_n AS max_pos
347 |         FROM basket WHERE NOT {GOOD} ORDER BY order_id LIMIT 20''',
348 |                  audit.folder / f'{source}_basket_issue_examples.csv')
349 |     # Vòng 2: vị trí lớn hơn kích thước giỏ là vô lý -> đặt thiếu (không đoán lại).
350 |     sizes = pd.read_sql_query('SELECT order_id, n FROM basket', db).set_index('order_id')['n']
351 |     rule = (table, 'position_exceeds_basket_size')
352 |     for frame in chunks(pending, c.size, c.headers[table]):
353 |         outside = pd.to_numeric(frame['add_to_cart_order'], errors='coerce').gt(
354 |             frame['order_id'].astype('int64').map(sizes))
355 |         audit.relational_counts[rule] += int(outside.sum())
356 |         frame.loc[outside, 'add_to_cart_order'] = ''
357 |         append_csv(frame, c.work / c.files[table].name)
358 |     audit.checks[table] = {
359 |         'input_rows': count, 'input_columns': c.headers[table], 'input_key_sha256': digest.hexdigest(),
360 |         'baskets': baskets, 'largest_basket': largest, 'primary_key_unique': True,
361 |         'foreign_keys_valid': True, 'baskets_needing_position_review': review,
362 |         'duplicate_position_extra': duplicate,
363 |         'positions_exceeding_basket_size_set_missing': audit.relational_counts[rule]}
364 |     sequence.finish()
365 |     if review:
366 |         raise ValueError(f'{table}: kiểm tra thứ tự sau tái dựng không đạt')
367 |     pending.unlink()
368 |     db.execute('DROP TABLE detail')
369 |     db.execute('DROP TABLE basket')
370 | 
371 | 
372 | # ===== Nhóm 6: kiểm chứng đầu ra, so số kỳ vọng và khung chạy chung. =====
373 | def verify_outputs(tables, c):
374 |     """Đọc lại CSV cuối: đúng schema, số dòng, chuỗi khóa và thứ tự tái dựng."""
375 |     for table in tables:
376 |         digest, count, last_group, last_rank = hashlib.sha256(), 0, None, 0
377 |         for frame in chunks(c.work / c.files[table].name, c.size, c.headers[table]):
378 |             if table in {'orders', 'order_products__prior', 'order_products__train'}:
379 |                 group, col = (('user_id', 'order_number') if table == 'orders'
380 |                               else ('order_id', 'add_to_cart_order'))
381 |                 expected = frame.groupby(group, sort=False).cumcount() + 1
382 |                 if frame[group].iloc[0] == last_group:
383 |                     expected.loc[frame[group].eq(last_group)] += last_rank
384 |                 if not pd.to_numeric(frame[col], errors='coerce').eq(expected).all():
385 |                     raise ValueError(f'{table}: thứ tự CSV cuối không khớp quy tắc tái dựng')
386 |                 last_group, last_rank = frame[group].iloc[-1], int(expected.iloc[-1])
387 |                 if table == 'orders' and not frame['eval_set'].isin(['prior', 'train', 'test']).all():
388 |                     raise ValueError('eval_set cuối vẫn thiếu/sai')
389 |             key_digest(digest, frame, table)
390 |             c.audit.record_final(table, frame)
391 |             count += len(frame)
392 |         check = c.audit.checks[table]
393 |         if count != check['input_rows'] or digest.hexdigest() != check['input_key_sha256']:
394 |             raise ValueError(f'{table}: số dòng/chuỗi khóa đầu ra thay đổi')
395 |         check.update(output_rows=count, output_columns=c.headers[table],
396 |                      output_key_sha256=digest.hexdigest(), same_schema=True,
397 |                      same_row_count=True, normalized_key_sequence_preserved=True)
398 | 
399 | 
400 | # Kiểm tra hồi quy: số dòng, số giỏ, số lượt sửa phải bằng số đã ghi trong config.
401 | def check_expected(audit):
402 |     """Đối chiếu số dòng, số giỏ, số lượt sửa với config (kiểm tra hồi quy)."""
403 |     config, checks, counts = audit.config, audit.checks, audit.relational_counts
404 |     expected = [(checks[t]['output_rows'], n, t) for t, n in config.get('expected_rows', {}).items()]
405 |     expected += [(checks[t]['baskets'], n, t) for t, n in config.get('expected_baskets', {}).items()]
406 |     expected += [(counts[(t, r)], n, f'{t}.{r}') for t, rules in
407 |                  config.get('expected_sequence_actions', {}).items() for r, n in rules.items()]
408 |     expected += [(counts[('orders', r)], n, f'orders.{r}')
409 |                  for r, n in config.get('expected_eval_recoveries', {}).items()]
410 |     for observed, value, name in expected:
411 |         if observed != value:
412 |             raise ValueError(f'{name}: khác số đối chứng trong config')
413 | 
414 | 
415 | # Khung chạy chung của hai người: hash nguồn -> làm sạch vào thư mục tạm -> đọc lại kiểm tra -> so bản trước -> xuất bản.
416 | def run(config, config_dir, member, tables, steps):
417 |     """Chạy `steps(c)` của một thành viên rồi kiểm chứng và xuất bản đúng `tables`."""
418 |     started = time.perf_counter()
419 |     paths = {k: (Path(config_dir) / config[k]).resolve()
420 |              for k in ['input_dir', 'output_dir', 'report_dir']}
421 |     if paths['input_dir'] == paths['output_dir']:
422 |         raise ValueError('Thư mục đầu ra phải khác dữ liệu nguồn')
423 |     if not config.get('reconstruct_sequences_from_preserved_row_order'):
424 |         raise ValueError('Cần xác nhận giả định tái dựng thứ tự trong config')
425 |     files = {t: paths['input_dir'] / f'{t}.csv' for t in SCHEMA}
426 |     headers = {}
427 |     for table, path in files.items():
428 |         with path.open(encoding='utf-8-sig', newline='') as stream:
429 |             headers[table] = next(csv.reader(stream), [])
430 |         if sorted(headers[table]) != sorted(SCHEMA[table]):
431 |             raise ValueError(f'{path.name}: sai tên/số cột: {headers[table]}')
432 |     # Mỗi lượt chạy có thư mục báo cáo riêng theo thời điểm; mọi việc làm trong '_staging' trước.
433 |     stamp = datetime.now(TZ).strftime('%Y%m%d_%H%M%S_%f')
434 |     reports = paths['report_dir'] / stamp
435 |     work = reports / '_staging'
436 |     work.mkdir(parents=True)
437 |     paths['output_dir'].mkdir(parents=True, exist_ok=True)
438 |     audit = Audit(reports, config)
439 |     db = sqlite3.connect(work / 'audit.sqlite')
440 |     try:
441 |         inputs = {t: {'sha256': sha256(p), 'bytes': p.stat().st_size, 'filename': p.name}
442 |                   for t, p in files.items()}
443 |         for table, expected in config.get('expected_source_sha256', {}).items():
444 |             if inputs[table]['sha256'] != expected:
445 |                 raise ValueError(f'{table}: SHA-256 nguồn khác cấu hình')
446 |         references = {t: read_ids(files[t], KEYS[t][0], config['chunksize'], unique=True)
447 |                       for t in ['aisles', 'departments', 'products', 'orders']}
448 |         db.execute('CREATE TABLE sources (order_id INTEGER PRIMARY KEY, source TEXT NOT NULL)')
449 |         c = SimpleNamespace(files=files, headers=headers, work=work, db=db, audit=audit,
450 |                             size=config['chunksize'], references=references)
451 |         # Giao cho script của từng người (clean_vuong / clean_phong) làm phần làm sạch riêng.
452 |         steps(c)
453 |         verify_outputs(tables, c)
454 |         check_expected(audit)
455 |         if any(sha256(files[t]) != inputs[t]['sha256'] for t in files):
456 |             raise ValueError('Dữ liệu nguồn thay đổi trong lúc chạy')
457 |         # So hash với bản CSV trước: giống hệt từng byte = tái lập; nếu khác thì lưu bản cũ trước khi thay.
458 |         comparisons = {}
459 |         for table in tables:
460 |             previous = paths['output_dir'] / f'{table}.csv'
461 |             new, old = sha256(work / previous.name), sha256(previous) if previous.exists() else None
462 |             comparisons[table] = {'new_sha256': new, 'previous_sha256': old,
463 |                                   'byte_identical_to_previous': old == new if old else None}
464 |             if old and old != new:   # giữ bản cũ trước khi thay
465 |                 (reports / 'previous_csv').mkdir(exist_ok=True)
466 |                 shutil.copy2(previous, reports / 'previous_csv' / previous.name)
467 |         # Ghi báo cáo, rồi chỉ khi mọi kiểm tra đã đạt mới chép CSV sang thư mục chính.
468 |         audit.save()
469 |         for table in tables:   # chỉ xuất bản sau khi mọi kiểm tra đã đạt
470 |             os.replace(work / f'{table}.csv', paths['output_dir'] / f'{table}.csv')
471 |         write_json(reports / 'run_report.json', {
472 |             'status': 'completed', 'assigned_to': config['assigned_to'], 'tables_cleaned': tables,
473 |             'created_at_local': datetime.now(TZ).isoformat(),
474 |             'seconds': round(time.perf_counter() - started, 2),
475 |             'python': platform.python_version(), 'platform': platform.platform(),
476 |             'packages': {'pandas': pd.__version__, 'numpy': np.__version__},
477 |             'inputs': inputs, 'checks': audit.checks, 'output_comparison': comparisons,
478 |             'config': config, 'source_hashes_unchanged': True,
479 |             'assumptions': ['CSV rows preserve original purchase/cart encounter order.'],
480 |             'limitations': ['Sequence semantics are assumed, not independently proven.',
481 |                             'Valid-domain values may still be corrupted.',
482 |                             'Unrecoverable attributes remain missing.']})
483 |         write_json(paths['report_dir'] / 'latest.json', {'run_dir': stamp})
484 |         print(f'[{member}] HOÀN TẤT: {reports}', flush=True)
485 |         return reports
486 |     except Exception as exc:
487 |         write_json(reports / 'failure.json', {'status': 'failed', 'error': str(exc)})
488 |         raise
489 |     finally:
490 |         db.close()
491 |         shutil.rmtree(work)
492 | 
493 | 
494 | # Dòng lệnh: đọc config (mặc định config_<tên>.json) rồi gọi run().
495 | def cli(member, tables, steps):
496 |     sys.stdout.reconfigure(encoding='utf-8', errors='replace')
497 |     parser = argparse.ArgumentParser(description=f'Làm sạch có kiểm chứng: {member}')
498 |     parser.add_argument('--config', type=Path, default=Path(__file__).with_name(f'config_{member}.json'))
499 |     path = parser.parse_args().config.resolve()
500 |     run(json.loads(path.read_text(encoding='utf-8-sig')), path.parent, member, tables, steps)
```

### 5. `scripts/cleaning/clean_vuong.py`

> **Vai trò:** Khai báo thứ tự làm sạch aisles, departments, order_products__prior.  
> **Mục trong bài:** 3.3 · **Người viết:** Vương  
> **Đầu vào → đầu ra:** CSV nhiễu → CSV sạch  
> **Hàm/lớp chính (dòng):** `steps` (16)  
> **Ghi chú:** `python scripts/cleaning/clean_vuong.py`  
> *23 dòng · SHA-256 `2de40dce1397…`*

```python
 1 | """Vương: làm sạch aisles, departments và order_products__prior.
 2 | 
 3 | Chạy: python scripts/cleaning/clean_vuong.py   (cấu hình: config_vuong.json)
 4 | Khóa ngoại của prior được đối chiếu với order_id/product_id đọc trực tiếp từ
 5 | orders.csv/products.csv nhiễu; script này không làm sạch hai bảng đó.
 6 | 
 7 | ĐỌC NHANH: file này chỉ khai báo THỨ TỰ làm sạch phần của Vương; toàn bộ logic nằm trong common.py.
 8 |   Aisles và departments (bảng nhỏ) làm trước; prior (32,4 triệu dòng) làm sau vì cần đối chiếu khóa ngoại với orders/products nhiễu.
 9 | """
10 | from common import clean_detail, clean_dimension, cli
11 | 
12 | TABLES = ['aisles', 'departments', 'order_products__prior']
13 | 
14 | 
15 | # Thứ tự: 2 bảng danh mục trước, rồi bảng prior (đọc theo khối, tái dựng add_to_cart_order).
16 | def steps(c):
17 |     clean_dimension('aisles', c)
18 |     clean_dimension('departments', c)
19 |     clean_detail('order_products__prior', c, c.references['orders'], c.references['products'])
20 | 
21 | 
22 | if __name__ == '__main__':
23 |     cli('vuong', TABLES, steps)
```

### 6. `scripts/cleaning/config_vuong.json`

> **Vai trò:** Quy tắc, ký hiệu thiếu và số kỳ vọng cho ba bảng của Vương.  
> **Mục trong bài:** 3.3 · **Người viết:** Vương  
> **Đầu vào → đầu ra:** —  
> **Ghi chú:** Số kỳ vọng chỉ dùng kiểm tra hồi quy.  
> *61 dòng · SHA-256 `5adc351224c8…`*

```json
 1 | {
 2 |   "assigned_to": "Lê Văn Vương (MSSV: 2521001118)",
 3 |   "assigned_tables": [
 4 |     "aisles",
 5 |     "departments",
 6 |     "order_products__prior"
 7 |   ],
 8 |   "input_dir": "../../DATA/Data đã làm nhiễu",
 9 |   "output_dir": "../../DATA/Data đã làm sạch",
10 |   "report_dir": "../../BAO CAO/Bao cao lam sach/vuong",
11 |   "chunksize": 250000,
12 |   "missing_tokens": [
13 |     "",
14 |     "null",
15 |     "none",
16 |     "nan",
17 |     "na",
18 |     "n/a",
19 |     "?",
20 |     "-",
21 |     "chưa rõ"
22 |   ],
23 |   "missing_tokens_by_column": {
24 |     "aisles.aisle": [
25 |       "",
26 |       "null",
27 |       "none",
28 |       "nan",
29 |       "na",
30 |       "n/a",
31 |       "?",
32 |       "-",
33 |       "chưa rõ",
34 |       "unknown"
35 |     ]
36 |   },
37 |   "expected_rows": {
38 |     "aisles": 134,
39 |     "departments": 21,
40 |     "order_products__prior": 32434489
41 |   },
42 |   "expected_baskets": {
43 |     "order_products__prior": 3214874
44 |   },
45 |   "reconstruct_sequences_from_preserved_row_order": true,
46 |   "expected_source_sha256": {
47 |     "aisles": "ffa1ddce6395a6e808d239d104ab920eb20f2e169bbc538043e1e3191ce1f987",
48 |     "departments": "3d6a3f2a87ec3ccc61afea2044061017da733decda17de3beb2583dc4a1fc520",
49 |     "order_products__prior": "2cc2d226d9adcb1bd9381b681844a51d911a5ddc64910def71379e9b32d4f8c3",
50 |     "order_products__train": "37530a6ecdbe40ebbd923b2b294580dd2cfd414285659b2df71363389b696071",
51 |     "orders": "fbbbc436ddffefc7f609a540916e9728e81d86b8105bbaff79f3cb4dbc76269b",
52 |     "products": "c02c3f5c7ddbbf83b87b8b360923d81ca3a1d9fd83c6e719123cdc9d077fb7ba"
53 |   },
54 |   "expected_sequence_actions": {
55 |     "order_products__prior": {
56 |       "sequence_filled_unusable": 6005160,
57 |       "sequence_corrected_observed": 762067,
58 |       "sequence_observed_consistent": 25667262
59 |     }
60 |   }
61 | }
```

### 7. `scripts/cleaning/clean_phong.py`

> **Vai trò:** Làm sạch products, orders, order_products__train; tái dựng `order_number`, khôi phục `eval_set` theo tư cách thành viên (bảng SQLite `sources`).  
> **Mục trong bài:** 3.3 · **Người viết:** Phong  
> **Đầu vào → đầu ra:** CSV nhiễu → CSV sạch  
> **Hàm/lớp chính (dòng):** `clean_orders` (19), `finalize_orders` (49), `steps` (86)  
> **Ghi chú:** `python scripts/cleaning/clean_phong.py`  
> *102 dòng · SHA-256 `c828660adc52…`*

```python
  1 | """Phong: làm sạch products, orders và order_products__train.
  2 | 
  3 | Chạy: python scripts/cleaning/clean_phong.py   (cấu hình: config_phong.json)
  4 | Tái dựng order_number theo khách và khôi phục eval_set: đơn có trong prior là 'prior',
  5 | trong train là 'train', còn lại là 'test' khi mỗi khách có đúng một đơn cuối ngoài prior.
  6 | Chỉ đọc cột order_id của prior nhiễu để làm việc này, không sửa bảng prior.
  7 | """
  8 | from collections import Counter
  9 | import hashlib
 10 | 
 11 | import pandas as pd
 12 | 
 13 | from common import (GOOD, RowSequence, append_csv, chunks, clean_detail, clean_dimension,
 14 |                     clean_frame, cli, export_query, insert, key_digest, read_ids)
 15 | 
 16 | TABLES = ['products', 'orders', 'order_products__train']
 17 | 
 18 | 
 19 | def clean_orders(c):
 20 |     db, audit = c.db, c.audit
 21 |     db.execute('CREATE TABLE orders (order_id INTEGER PRIMARY KEY, '
 22 |                'user_id INTEGER NOT NULL, order_number INTEGER)')
 23 |     count, digest = 0, hashlib.sha256()
 24 |     sequence = RowSequence(db, 'orders', 'user_id', 'order_number', audit, maximum=100)
 25 |     for raw in chunks(c.files['orders'], c.size, c.headers['orders']):
 26 |         frame = clean_frame(raw, 'orders', audit)
 27 |         sequence.apply(frame)
 28 |         insert(db, 'orders', frame[['order_id', 'user_id', 'order_number']])
 29 |         append_csv(frame, c.work / 'orders.pending')
 30 |         key_digest(digest, frame, 'orders')
 31 |         count += len(frame)
 32 |         print(f'orders: {count:,}', flush=True)
 33 |     sequence.finish()
 34 |     db.execute('''CREATE TEMP TABLE histories AS SELECT user_id, COUNT(*) AS n,
 35 |         COUNT(order_number) AS known, COUNT(DISTINCT order_number) AS distinct_n,
 36 |         MIN(order_number) AS min_n, MAX(order_number) AS max_n FROM orders GROUP BY user_id''')
 37 |     audit.checks['orders'] = {
 38 |         'input_rows': count, 'input_columns': c.headers['orders'],
 39 |         'input_key_sha256': digest.hexdigest(), 'primary_key_unique': True,
 40 |         **audit.checks.get('orders', {}),
 41 |         'users': db.execute('SELECT COUNT(*) FROM histories').fetchone()[0],
 42 |         'users_needing_sequence_review': db.execute(
 43 |             f'SELECT COUNT(*) FROM histories WHERE NOT {GOOD}').fetchone()[0]}
 44 |     export_query(db, f'SELECT * FROM histories WHERE NOT {GOOD} ORDER BY user_id LIMIT 20',
 45 |                  audit.folder / 'history_issue_examples.csv')
 46 |     return pd.Index(pd.read_sql_query('SELECT order_id FROM orders', db)['order_id'])
 47 | 
 48 | 
 49 | def finalize_orders(c):
 50 |     """Gán eval_set theo bảng sources; test = đơn cuối không thuộc prior/train."""
 51 |     db, audit, config = c.db, c.audit, c.audit.config
 52 |     db.execute("""CREATE TEMP TABLE partition_check AS SELECT o.user_id, COUNT(*) AS n,
 53 |         SUM(CASE WHEN s.source='prior' THEN 0 ELSE 1 END) AS nonprior,
 54 |         MAX(CASE WHEN s.source='prior' THEN NULL ELSE o.order_number END) AS final_n
 55 |         FROM orders o LEFT JOIN sources s ON o.order_id=s.order_id GROUP BY o.user_id""")
 56 |     bad, users = db.execute('SELECT SUM(nonprior<>1 OR final_n<>n), COUNT(*) '
 57 |                             'FROM partition_check').fetchone()
 58 |     n_test = db.execute('SELECT COUNT(*) FROM orders o LEFT JOIN sources s '
 59 |                         'ON o.order_id=s.order_id WHERE s.order_id IS NULL').fetchone()[0]
 60 |     if bad:
 61 |         raise ValueError(f'{bad} khách không có đúng một đơn cuối ngoài prior; không suy ra test')
 62 |     if config.get('expected_users', users) != users or config.get('expected_test_orders', n_test) != n_test:
 63 |         raise ValueError('Số khách hoặc số đơn test khác báo cáo kiểm tra')
 64 |     sources = pd.read_sql_query('SELECT order_id, source FROM sources', db).set_index('order_id')['source']
 65 |     totals = Counter()
 66 |     for frame in chunks(c.work / 'orders.pending', c.size, c.headers['orders']):
 67 |         source = frame['order_id'].astype('int64').map(sources)
 68 |         target, old = source.fillna('test'), frame['eval_set']
 69 |         if (old.ne('') & old.ne(target)).any():
 70 |             raise ValueError('Nhãn eval_set quan sát được mâu thuẫn phân chia; cần kiểm tra lại nguồn')
 71 |         for rule, mask in {'eval_recovered_prior': source.eq('prior') & old.eq(''),
 72 |                            'eval_recovered_train': source.eq('train') & old.eq(''),
 73 |                            'eval_inferred_test': source.isna() & old.eq(''),
 74 |                            'eval_observed_consistent': old.eq(target)}.items():
 75 |             audit.relational_counts[('orders', rule)] += int(mask.sum())
 76 |         frame['eval_set'] = target
 77 |         totals.update(target.value_counts().to_dict())
 78 |         append_csv(frame, c.work / 'orders.csv')
 79 |     audit.checks['orders'].update(
 80 |         final_eval_set_counts=dict(totals), prior_train_disjoint=True,
 81 |         users_with_invalid_final_partition=bad, test_orders=n_test,
 82 |         test_inference='complete audited files, neither source, exactly one final order per user')
 83 |     (c.work / 'orders.pending').unlink()
 84 | 
 85 | 
 86 | def steps(c):
 87 |     if not c.audit.config.get('infer_test_from_complete_partition'):
 88 |         raise ValueError('Cần bật kiểm chứng phân chia đầy đủ để suy luận test')
 89 |     clean_dimension('products', c)
 90 |     order_ids = clean_orders(c)
 91 |     prior = read_ids(c.files['order_products__prior'], 'order_id', c.size)   # chỉ cột khóa
 92 |     if not prior.isin(order_ids).all():
 93 |         raise ValueError('prior: order_id mồ côi')
 94 |     insert(c.db, 'sources', pd.DataFrame({'order_id': prior, 'source': 'prior'}))
 95 |     c.audit.checks['prior_dependency'] = {'unique_orders': len(prior),
 96 |                                           'order_foreign_keys_valid': True}
 97 |     clean_detail('order_products__train', c, order_ids, c.references['products'])
 98 |     finalize_orders(c)
 99 | 
100 | 
101 | if __name__ == '__main__':
102 |     cli('phong', TABLES, steps)
```

### 8. `scripts/cleaning/config_phong.json`

> **Vai trò:** Quy tắc, ký hiệu thiếu và số kỳ vọng cho ba bảng của Phong.  
> **Mục trong bài:** 3.3 · **Người viết:** Phong  
> **Đầu vào → đầu ra:** —  
> *74 dòng · SHA-256 `f80ad90f004b…`*

```json
 1 | {
 2 |   "assigned_to": "Hoàng Thanh Phong (MSSV: 2521001087)",
 3 |   "assigned_tables": [
 4 |     "products",
 5 |     "orders",
 6 |     "order_products__train"
 7 |   ],
 8 |   "input_dir": "../../DATA/Data đã làm nhiễu",
 9 |   "output_dir": "../../DATA/Data đã làm sạch",
10 |   "report_dir": "../../BAO CAO/Bao cao lam sach/phong",
11 |   "chunksize": 250000,
12 |   "missing_tokens": [
13 |     "",
14 |     "null",
15 |     "none",
16 |     "nan",
17 |     "na",
18 |     "n/a",
19 |     "?",
20 |     "-",
21 |     "chưa rõ"
22 |   ],
23 |   "missing_tokens_by_column": {
24 |     "products.product_name": [
25 |       "",
26 |       "null",
27 |       "none",
28 |       "nan",
29 |       "na",
30 |       "n/a",
31 |       "?",
32 |       "-",
33 |       "chưa rõ",
34 |       "unknown"
35 |     ]
36 |   },
37 |   "expected_rows": {
38 |     "products": 49688,
39 |     "orders": 3421083,
40 |     "order_products__train": 1384617
41 |   },
42 |   "expected_baskets": {
43 |     "order_products__train": 131209
44 |   },
45 |   "reconstruct_sequences_from_preserved_row_order": true,
46 |   "infer_test_from_complete_partition": true,
47 |   "expected_source_sha256": {
48 |     "aisles": "ffa1ddce6395a6e808d239d104ab920eb20f2e169bbc538043e1e3191ce1f987",
49 |     "departments": "3d6a3f2a87ec3ccc61afea2044061017da733decda17de3beb2583dc4a1fc520",
50 |     "order_products__prior": "2cc2d226d9adcb1bd9381b681844a51d911a5ddc64910def71379e9b32d4f8c3",
51 |     "order_products__train": "37530a6ecdbe40ebbd923b2b294580dd2cfd414285659b2df71363389b696071",
52 |     "orders": "fbbbc436ddffefc7f609a540916e9728e81d86b8105bbaff79f3cb4dbc76269b",
53 |     "products": "c02c3f5c7ddbbf83b87b8b360923d81ca3a1d9fd83c6e719123cdc9d077fb7ba"
54 |   },
55 |   "expected_test_orders": 75000,
56 |   "expected_users": 206209,
57 |   "expected_sequence_actions": {
58 |     "orders": {
59 |       "sequence_filled_unusable": 1233938,
60 |       "sequence_corrected_observed": 4773,
61 |       "sequence_observed_consistent": 2182372
62 |     },
63 |     "order_products__train": {
64 |       "sequence_filled_unusable": 525773,
65 |       "sequence_corrected_observed": 67880,
66 |       "sequence_observed_consistent": 790964
67 |     }
68 |   },
69 |   "expected_eval_recoveries": {
70 |     "eval_recovered_prior": 764250,
71 |     "eval_recovered_train": 31140,
72 |     "eval_inferred_test": 17939
73 |   }
74 | }
```

### 9. `scripts/summarize_cleaning.py`

> **Vai trò:** Gộp báo cáo hai người, đối chiếu SHA-256 sáu CSV với hồ sơ lượt chạy, nối thử train với bốn bảng cha.  
> **Mục trong bài:** 3.3 (Bảng 3.5, 3.6) · **Người viết:** Vương  
> **Đầu vào → đầu ra:** báo cáo `BAO CAO/Bao cao lam sach/{vuong,phong}/` → `before_after.csv`, `relational_summary.csv`, `verification.json`  
> **Hàm/lớp chính (dòng):** `sha256` (24), `main` (29)  
> **Ghi chú:** `python scripts/summarize_cleaning.py`  
> *98 dòng · SHA-256 `baafbbdecf68…`*

```python
 1 | """Gộp báo cáo làm sạch của hai thành viên và xác minh sáu CSV đã xuất bản.
 2 | 
 3 | Chạy sau clean_vuong.py và clean_phong.py. Đối chiếu SHA-256 của CSV hiện tại với
 4 | new_sha256 trong run_report.json của lượt được latest.json trỏ tới; kiểm tra nguồn
 5 | nhiễu không đổi; nối thử train với orders/products/aisles/departments.
 6 | 
 7 | ĐỌC NHANH: gộp kết quả làm sạch của hai người và CHỨNG MINH sáu CSV sạch đúng là sản phẩm của các lượt đã kiểm chứng.
 8 |   Bốn khối: (1) đọc báo cáo mới nhất của từng người, so hash CSV; (2) nguồn nhiễu không đổi;
 9 |   (3) nối thử train với orders/products/aisles/departments để chắc khóa ngoại khớp; (4) gộp bảng và ghi verification.json.
10 |   Đầu ra chính: before_after.csv (Bảng 'trước và sau'), relational_summary.csv, comparison_previous.csv, verification.json.
11 | """
12 | from datetime import datetime, timedelta, timezone
13 | import hashlib
14 | import json
15 | from pathlib import Path
16 | 
17 | import pandas as pd
18 | 
19 | ROOT = Path(__file__).resolve().parent.parent
20 | REPORTS = ROOT / 'BAO CAO' / 'Bao cao lam sach'
21 | DATA = ROOT / 'DATA' / 'Data đã làm sạch'
22 | 
23 | 
24 | def sha256(path):
25 |     with path.open('rb') as stream:
26 |         return hashlib.file_digest(stream, 'sha256').hexdigest()
27 | 
28 | 
29 | def main():
30 |     runs, checks, comparisons, before_after, actions, sources = {}, {}, [], [], [], None
31 |     # Khối 1: mỗi người một báo cáo lượt chạy mới nhất; hai người phải dùng cùng nguồn nhiễu; hash CSV hiện tại phải khớp lượt đã kiểm chứng.
32 |     for member in ['vuong', 'phong']:
33 |         latest = json.loads((REPORTS / member / 'latest.json').read_text('utf-8'))
34 |         folder = REPORTS / member / latest['run_dir']
35 |         report = json.loads((folder / 'run_report.json').read_text('utf-8'))
36 |         if report['status'] != 'completed':
37 |             raise ValueError(f'{member}: chưa hoàn tất')
38 |         if sources is not None and sources != report['inputs']:
39 |             raise ValueError('Hai thành viên dùng nguồn khác nhau')
40 |         sources = report['inputs']
41 |         runs[member] = {'report': folder.relative_to(ROOT).as_posix(),
42 |                         'seconds': report['seconds'], 'packages': report['packages'],
43 |                         'python': report['python'], 'finished_at': report['created_at_local']}
44 |         for table in report['tables_cleaned']:
45 |             comparison = report['output_comparison'][table]
46 |             if sha256(DATA / f'{table}.csv') != comparison['new_sha256']:
47 |                 raise ValueError(f'{table}: CSV hiện tại khác đầu ra đã kiểm chứng')
48 |             checks[table] = report['checks'][table]
49 |             comparisons.append({'table': table, **comparison})
50 |         before_after.append(pd.read_csv(folder / 'before_after.csv'))
51 |         actions.append(pd.read_csv(folder / 'relational_summary.csv'))
52 |     # Khối 2: file nhiễu gốc không được thay đổi sau khi chạy làm sạch.
53 |     for table, manifest in sources.items():
54 |         if sha256(ROOT / 'DATA' / 'Data đã làm nhiễu' / manifest['filename']) != manifest['sha256']:
55 |             raise ValueError(f'{table}: nguồn đã thay đổi sau khi chạy')
56 | 
57 |     # Kiểm tra toàn vẹn bằng phép nối nhiều–một; chưa phải bảng Master.
58 |     # Khối 3: nối thử train với các bảng khác (many_to_one): không đổi số dòng, không khóa ngoại thiếu.
59 |     train = pd.read_csv(DATA / 'order_products__train.csv', usecols=['order_id', 'product_id'])
60 |     orders = pd.read_csv(DATA / 'orders.csv', usecols=['order_id', 'user_id', 'eval_set'])
61 |     joined = train.merge(orders, on='order_id', how='left', validate='many_to_one')
62 |     if joined.user_id.isna().any() or not joined.eval_set.eq('train').all():
63 |         raise ValueError('Chi tiết train không khớp orders')
64 |     joined = joined.merge(pd.read_csv(DATA / 'products.csv',
65 |                                       usecols=['product_id', 'aisle_id', 'department_id']),
66 |                           on='product_id', how='left', validate='many_to_one')
67 |     for table, key in [('aisles', 'aisle_id'), ('departments', 'department_id')]:
68 |         parent = pd.read_csv(DATA / f'{table}.csv', usecols=[key]).assign(_found=True)
69 |         joined = joined.merge(parent, on=key, how='left', validate='many_to_one')
70 |         if joined['_found'].isna().any():
71 |             raise ValueError(f'Khóa ngoại thiếu trong {table}')
72 |         joined = joined.drop(columns='_found')
73 |     if len(joined) != len(train) or len(joined) < 1000000:
74 |         raise ValueError('Merge làm thay đổi số dòng hoặc không đủ 1 triệu dòng')
75 |     checks['train_merge'] = {
76 |         'rows': len(joined), 'baskets': int(joined.order_id.nunique()),
77 |         'users': int(joined.user_id.nunique()), 'many_to_one_validated': True,
78 |         'at_least_100000': True, 'at_least_1000000': True, 'all_foreign_keys_matched': True}
79 | 
80 |     # Khối 4: gộp báo cáo hai người và ghi verification.json (trạng thái 'verified').
81 |     pd.concat(before_after, ignore_index=True).to_csv(
82 |         REPORTS / 'before_after.csv', index=False, encoding='utf-8-sig')
83 |     pd.concat(actions, ignore_index=True).to_csv(
84 |         REPORTS / 'relational_summary.csv', index=False, encoding='utf-8-sig')
85 |     pd.DataFrame(comparisons).to_csv(REPORTS / 'comparison_previous.csv',
86 |                                      index=False, encoding='utf-8-sig')
87 |     result = {'status': 'verified', 'runs': runs, 'checks': checks,
88 |               'source_files_unchanged': True, 'published_output_hashes_match_runs': True,
89 |               'comparison_previous': comparisons,
90 |               'verified_at': datetime.now(timezone(timedelta(hours=7))).isoformat()}
91 |     (REPORTS / 'verification.json').write_text(
92 |         json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
93 |     print(f"VERIFIED: 6 CSV; train merge {len(joined):,} dòng, "
94 |           f"{joined.order_id.nunique():,} giỏ")
95 | 
96 | 
97 | if __name__ == '__main__':
98 |     main()
```

## Phần 3. Bảng Master, chất lượng và tối ưu bộ nhớ (mục 3.2)

### 10. `scripts/m1_build_master.py`

> **Vai trò:** Ghép train với orders, products, aisles, departments bằng `merge(how="left", validate="many_to_one", indicator=True)` theo sáu khối; thu hẹp kiểu sau khi kiểm miền; ghi Parquet tạm, đọc lại, chạy 13 tiêu chí rồi xuất bản bằng `os.replace`.  
> **Mục trong bài:** 3.2 (Bảng 3.2, 3.3) · **Người viết:** Vương  
> **Đầu vào → đầu ra:** 5 CSV sạch → `DATA/Data đã làm sạch/master_train.parquet` + `join_audit.csv`, `master_schema.csv`, `master_verification.json`  
> **Hàm/lớp chính (dòng):** `read` (73), `key_hash` (78), `audit_downcasting` (87), `load_right_tables` (123), `build` (137)  
> **Ghi chú:** Dòng `before = pd.concat(...)` và `after = pd.read_parquet(...)` là bước đối soát từng ô (đọc toàn bảng có chủ đích).  
> *271 dòng · SHA-256 `6c653ae7a101…`*

```python
  1 | """Tạo bảng Master train (M1): 4 phép ghép trái nhiều–một, kiểm tra và xuất bản Parquet.
  2 | 
  3 | Mỗi khối train lần lượt ghép orders, products, aisles, departments bằng
  4 | merge(how="left", validate="many_to_one", indicator=True). Dừng nếu có dòng
  5 | left_only, đổi số dòng, đổi chuỗi cặp khóa (order_id, product_id) hoặc sinh cột _x/_y.
  6 | Trước khi thu hẹp kiểu: kiểm tra miền số nguyên và Float64 -> Float32 không mất giá trị.
  7 | Ghi master_train.tmp.parquet, đọc lại bằng dtype_backend="numpy_nullable", chạy 13
  8 | tiêu chí rồi mới xuất bản. Đầu ra:
  9 |   DATA/Data đã làm sạch/master_train.parquet
 10 |   DATA/Data đã làm sạch/Bảng master TLCK/{join_audit,master_schema,master_dictionary}.csv
 11 |   DATA/Data đã làm sạch/Bảng master TLCK/master_verification.json
 12 | 
 13 | ĐỌC NHANH (vấn đáp):
 14 |   Mục đích: tạo bảng Master 1.384.617 dòng x 15 cột để làm bài toán hoàn thiện giỏ (chỉ lấy đơn train: mỗi khách đúng một đơn).
 15 |   Năm bước: (1) kiểm tra trước khi thu hẹp kiểu; (2) nạp 4 bảng bên phải; (3) ghép từng khối train với 4 bảng;
 16 |   (4) ghi Parquet tạm, đọc lại, chạy 13 tiêu chí; (5) xuất bản nguyên tử và ghi các bảng bằng chứng.
 17 |   Vì sao left merge + validate='many_to_one'? Giữ mọi dòng train và chặn việc nhân dòng khi bảng kia trùng khóa.
 18 |   Vì sao Parquet và thu hẹp kiểu? RAM giảm 88,16%, tệp nhỏ hơn CSV 7,75 lần (số đo trong m1_benchmark.py).
 19 | """
 20 | import hashlib
 21 | import json
 22 | import sys
 23 | import time
 24 | 
 25 | from m1_common import atomic_publish, parse_args, report_path
 26 | 
 27 | import numpy as np
 28 | import pandas as pd
 29 | import pyarrow as pa
 30 | import pyarrow.parquet as pq
 31 | 
 32 | # Số kỳ vọng của Master, dùng cho tiêu chí kiểm tra cuối.
 33 | ROWS, BASKETS = 1384617, 131209
 34 | CATEGORIES = ["eval_set", "product_name", "aisle", "department"]
 35 | # Hợp đồng 15 cột: tên, kiểu lưu trữ gọn (int8/int16/int32...) và cột nào được phép thiếu (nullable).
 36 | SCHEMA = pa.schema([
 37 |     pa.field("order_id", pa.int32(), nullable=False),
 38 |     pa.field("product_id", pa.int32(), nullable=False),
 39 |     pa.field("add_to_cart_order", pa.int16(), nullable=False),
 40 |     pa.field("reordered", pa.int8(), nullable=True),
 41 |     pa.field("user_id", pa.int32(), nullable=False),
 42 |     pa.field("eval_set", pa.dictionary(pa.int8(), pa.string()), nullable=False),
 43 |     pa.field("order_number", pa.int16(), nullable=False),
 44 |     pa.field("order_dow", pa.int8(), nullable=True),
 45 |     pa.field("order_hour_of_day", pa.int8(), nullable=True),
 46 |     pa.field("days_since_prior_order", pa.float32(), nullable=True),
 47 |     pa.field("product_name", pa.dictionary(pa.int32(), pa.string()), nullable=True),
 48 |     pa.field("aisle_id", pa.int16(), nullable=False),
 49 |     pa.field("department_id", pa.int8(), nullable=False),
 50 |     pa.field("aisle", pa.dictionary(pa.int16(), pa.string()), nullable=True),
 51 |     pa.field("department", pa.dictionary(pa.int8(), pa.string()), nullable=False),
 52 | ])
 53 | COLUMNS = SCHEMA.names
 54 | # Kiểu đọc CSV theo từng bảng; cột có thể thiếu dùng kiểu cho phép thiếu (Int8, Float32).
 55 | DTYPES = {
 56 |     "orders": {"order_id": "int32", "user_id": "int32", "eval_set": "string",
 57 |                "order_number": "int16", "order_dow": "Int8", "order_hour_of_day": "Int8",
 58 |                "days_since_prior_order": "Float32"},
 59 |     "products": {"product_id": "int32", "product_name": "string",
 60 |                  "aisle_id": "int16", "department_id": "int8"},
 61 |     "aisles": {"aisle_id": "int16", "aisle": "string"},
 62 |     "departments": {"department_id": "int8", "department": "string"},
 63 |     "order_products__train": {"order_id": "int32", "product_id": "int32",
 64 |                               "add_to_cart_order": "int16", "reordered": "Int8"},
 65 | }
 66 | # 4 phép ghép theo thứ tự: orders (order_id), products (product_id), aisles (aisle_id), departments (department_id).
 67 | JOINS = [("1_orders", "orders", "order_id"), ("2_products", "products", "product_id"),
 68 |          ("3_aisles", "aisles", "aisle_id"), ("4_departments", "departments", "department_id")]
 69 | LIMITS = {"int8": (-128, 127), "Int8": (-128, 127), "int16": (-32768, 32767),
 70 |           "int32": (-2147483648, 2147483647)}
 71 | 
 72 | 
 73 | def read(clean_dir, table, **kwargs):
 74 |     return pd.read_csv(clean_dir / f"{table}.csv", keep_default_na=False, na_values=[""], **kwargs)
 75 | 
 76 | 
 77 | # SHA-256 của chuỗi cặp (order_id, product_id): bằng chứng phép ghép không đổi số dòng và thứ tự dòng.
 78 | def key_hash(order_id, product_id):
 79 |     """SHA-256 của chuỗi cặp khóa theo đúng thứ tự dòng."""
 80 |     h = hashlib.sha256()
 81 |     for o, p in zip(order_id, product_id):
 82 |         h.update(f"{o},{p}\n".encode("utf-8"))
 83 |     return h.hexdigest()
 84 | 
 85 | 
 86 | # BƯỚC 1: kiểm tra trước khi thu hẹp kiểu: giá trị nằm trong miền kiểu mới, không có số lẻ, Float64 -> Float32 không mất giá trị.
 87 | def audit_downcasting(clean_dir):
 88 |     """Kiểm tra trước khi thu hẹp kiểu: miền, số lẻ, null và Float64 -> Float32."""
 89 |     orders = read(clean_dir, "orders", usecols=list(DTYPES["orders"]))
 90 |     s64 = pd.to_numeric(orders["days_since_prior_order"], errors="coerce")
 91 |     s32 = s64.astype("Float32")
 92 |     valid = s64.notna()
 93 |     max_diff = float((s64[valid] - s32[valid].astype("float64")).abs().max())
 94 |     same_nulls = bool(s64.isna().equals(s32.isna()))
 95 |     result = {"days_since_prior_order": {
 96 |         "source_dtype": "float64", "target_dtype": "Float32", "total_rows": len(s64),
 97 |         "valid_count": int(valid.sum()), "null_count": int(s64.isna().sum()),
 98 |         "min_value": float(s64.min()), "max_value": float(s64.max()),
 99 |         "max_abs_diff": max_diff, "null_positions_preserved": same_nulls,
100 |         "is_safe_to_downcast": max_diff == 0.0 and same_nulls}}
101 |     assert result["days_since_prior_order"]["is_safe_to_downcast"], "Float32 làm sai lệch giá trị"
102 |     frames = {"orders": orders, "train": read(clean_dir, "order_products__train"),
103 |               "products": read(clean_dir, "products")}
104 |     checks = [(t, frames[t], col, dt, dt.startswith("Int")) for t, name in
105 |               [("orders", "orders"), ("train", "order_products__train"), ("products", "products")]
106 |               for col, dt in DTYPES[name].items() if dt in LIMITS]
107 |     for table, frame, column, target, nullable in checks:
108 |         s = pd.to_numeric(frame[column], errors="coerce")
109 |         values, nulls = s.dropna(), int(s.isna().sum())
110 |         assert nullable or nulls == 0, f"[{table}.{column}] có {nulls} null nhưng {target} không cho phép"
111 |         odd = int(((values % 1) != 0).sum())
112 |         assert odd == 0, f"[{table}.{column}] có {odd} giá trị lẻ thập phân"
113 |         low, high = LIMITS[target]
114 |         c_min, c_max = float(values.min()), float(values.max())
115 |         assert low <= c_min and c_max <= high, f"[{table}.{column}] tràn miền {target}"
116 |         result[f"{table}.{column}"] = {"target_dtype": target, "min_val": c_min,
117 |                                        "max_val": c_max, "null_count": nulls,
118 |                                        "non_integer_count": odd, "fits_domain": True}
119 |     return result
120 | 
121 | 
122 | # BƯỚC 2: nạp 4 bảng bên phải (orders chỉ giữ các đơn có trong train); khóa không được thiếu hoặc trùng.
123 | def load_right_tables(clean_dir, train_orders):
124 |     chunks = read(clean_dir, "orders", dtype=DTYPES["orders"], chunksize=250000)
125 |     orders = pd.concat([m for c in chunks if not (m := c[c["order_id"].isin(train_orders)]).empty],
126 |                        ignore_index=True)
127 |     tables = {"orders": orders}
128 |     for name in ["products", "aisles", "departments"]:
129 |         tables[name] = read(clean_dir, name, dtype=DTYPES[name])
130 |     for name, key in [(n, k) for _, n, k in JOINS]:
131 |         assert tables[name][key].notna().all(), f"{name}.{key} có null"
132 |         assert not tables[name][key].duplicated().any(), f"{name}.{key} bị trùng"
133 |     return tables
134 | 
135 | 
136 | # BƯỚC 3-5: ghép từng khối, ghi Parquet tạm, đọc lại, chạy 13 tiêu chí, rồi mới xuất bản.
137 | def build(clean_dir, output_dir, chunksize):
138 |     output_dir.mkdir(parents=True, exist_ok=True)
139 |     tmp, final = clean_dir / "master_train.tmp.parquet", clean_dir / "master_train.parquet"
140 |     pre_audit = audit_downcasting(clean_dir)
141 |     inputs = {}
142 |     for name in ["order_products__train", "orders", "products", "aisles", "departments"]:
143 |         path = clean_dir / f"{name}.csv"
144 |         with open(path, "rb") as f:
145 |             inputs[path.name] = {"path": report_path(path), "size_bytes": path.stat().st_size,
146 |                                  "sha256": hashlib.file_digest(f, "sha256").hexdigest()}
147 |     ids = read(clean_dir, "order_products__train", usecols=["order_id", "product_id"])
148 |     expected_rows, input_hash = len(ids), key_hash(ids["order_id"], ids["product_id"])
149 |     right = load_right_tables(clean_dir, set(ids["order_id"].unique()))
150 |     del ids
151 |     tmp.unlink(missing_ok=True)
152 |     audit, written, raw_dtypes = [], [], {}
153 |     # Mỗi khối train: ghép lần lượt 4 bảng; dừng ngay nếu có dòng không khớp, đổi số dòng, lệch thứ tự khóa hoặc sinh cột _x/_y.
154 |     with pq.ParquetWriter(str(tmp), schema=SCHEMA, compression="snappy") as writer:
155 |         for number, frame in enumerate(read(clean_dir, "order_products__train",
156 |                                             dtype=DTYPES["order_products__train"],
157 |                                             chunksize=chunksize), start=1):
158 |             chunk_hash = key_hash(frame["order_id"], frame["product_id"])
159 |             for step, table, key in JOINS:
160 |                 merged = frame.merge(right[table], on=key, how="left", validate="many_to_one",
161 |                                      indicator=True, sort=False)
162 |                 unmatched = int((merged["_merge"] == "left_only").sum())
163 |                 same = key_hash(merged["order_id"], merged["product_id"]) == chunk_hash
164 |                 assert unmatched == 0, f"Khối {number}, {step}: {unmatched} dòng không khớp"
165 |                 assert len(merged) == len(frame), f"Khối {number}, {step}: đổi số dòng"
166 |                 assert same, f"Khối {number}, {step}: lệch chuỗi cặp khóa"
167 |                 assert not any(c.endswith(("_x", "_y")) for c in merged.columns), "Cột _x/_y"
168 |                 audit.append({"chunk_id": number, "step": step, "right_table": table,
169 |                               "join_key": key, "rows_before": len(frame),
170 |                               "rows_after": len(merged), "unmatched_rows": unmatched,
171 |                               "key_sequence_preserved": same})
172 |                 frame = merged.drop(columns=["_merge"])
173 |             assert set(frame.columns) == set(COLUMNS), f"Khối {number}: sai tập cột"
174 |             frame = frame[COLUMNS]
175 |             if number == 1:
176 |                 raw_dtypes = {c: str(frame[c].dtype) for c in COLUMNS}
177 |             for column in CATEGORIES:
178 |                 frame[column] = frame[column].astype("category")
179 |             written.append(frame.copy())
180 |             writer.write_table(pa.Table.from_pandas(frame, schema=SCHEMA, preserve_index=False))
181 |             print(f" - Khối {number}: {sum(map(len, written)):,}/{expected_rows:,} dòng")
182 | 
183 |     # Đọc lại tệp tạm bằng kiểu numpy_nullable rồi đối chiếu với bản trước khi ghi.
184 |     before = pd.concat(written, ignore_index=True)
185 |     del written
186 |     after = pd.read_parquet(tmp, dtype_backend="numpy_nullable")
187 |     per_user = after.groupby("user_id")["order_id"].nunique()
188 |     # 13 tiêu chí: đủ số dòng/cột, đủ 131.209 giỏ và khách, mỗi khách một đơn train, không trùng/thiếu khóa, nội dung không đổi.
189 |     checks = {
190 |         "row_count_exact_1384617": len(after) == ROWS,
191 |         "column_count_exact_15": after.shape[1] == 15,
192 |         "columns_match_contract": list(after.columns) == COLUMNS,
193 |         "distinct_orders_131209": int(after["order_id"].nunique()) == BASKETS,
194 |         "distinct_users_131209": int(after["user_id"].nunique()) == BASKETS,
195 |         "one_train_order_per_user": bool((per_user == 1).all()),
196 |         "missing_keys_count_zero": not after[["order_id", "product_id", "user_id"]].isna().any().any(),
197 |         "duplicate_key_pairs_zero": not after.duplicated(subset=["order_id", "product_id"]).any(),
198 |         "eval_set_all_train": set(after["eval_set"].dropna().unique()) == {"train"}
199 |                               and after["eval_set"].isna().sum() == 0,
200 |         "key_pairs_and_sequence_preserved": key_hash(after["order_id"], after["product_id"]) == input_hash,
201 |     }
202 |     # So từng cột: vị trí thiếu và giá trị trước/sau khi ghi phải giống hệt.
203 |     columns = {}
204 |     for col in COLUMNS:
205 |         b, a = before[col], after[col]
206 |         mask_b, mask_a = b.isna(), a.isna()
207 |         same_mask = bool(mask_b.equals(mask_a))
208 |         vb, va = b.loc[~mask_b], a.loc[~mask_a]
209 |         if col in CATEGORIES:
210 |             vb, va = vb.astype(str), va.astype(str)
211 |         same_values = bool(np.array_equal(vb.to_numpy(), va.to_numpy()))
212 |         assert same_mask and same_values, f"Cột {col}: giá trị hoặc vị trí thiếu thay đổi"
213 |         columns[col] = {"column": col, "raw_merged_dtype": raw_dtypes.get(col, "unknown"),
214 |                         "dtype_before_write": str(b.dtype), "dtype_after_read": str(a.dtype),
215 |                         "pyarrow_storage_type": str(SCHEMA.field(col).type),
216 |                         "missing_before": int(mask_b.sum()), "missing_after": int(mask_a.sum()),
217 |                         "missing_mask_preserved": same_mask, "values_preserved": same_values}
218 |     checks["content_preserved_before_after"] = all(c["values_preserved"] for c in columns.values())
219 |     checks["missing_positions_preserved_before_after"] = all(
220 |         c["missing_mask_preserved"] for c in columns.values())
221 |     bad_labels = {"Unknown", "unknown", "nan", "<NA>", "None"}
222 |     checks["category_labels_and_nulls_valid"] = not any(
223 |         bad_labels & set(after[c].cat.categories) for c in CATEGORIES)
224 |     checks = {k: bool(v) for k, v in checks.items()}
225 |     failed = [k for k, v in checks.items() if not v]
226 |     assert not failed, f"Kiểm tra cuối không đạt: {failed}"
227 | 
228 |     atomic_publish(tmp, final)   # chỉ xuất bản sau khi 13 tiêu chí đều đạt
229 |     tmp.unlink()
230 |     with open(final, "rb") as f:
231 |         final_sha = hashlib.file_digest(f, "sha256").hexdigest()
232 |     # Xuất các bảng bằng chứng: join_audit.csv, master_schema.csv, master_dictionary.csv, master_verification.json.
233 |     audit = pd.DataFrame(audit)
234 |     totals = [{"chunk_id": "TOTAL_SUMMARY", "step": step, "right_table": table, "join_key": key,
235 |                **{c: int(audit.loc[audit.step == step, c].sum())
236 |                   for c in ["rows_before", "rows_after", "unmatched_rows"]},
237 |                "key_sequence_preserved": bool(audit.loc[audit.step == step,
238 |                                                         "key_sequence_preserved"].all())}
239 |               for step, table, key in JOINS]
240 |     pd.concat([audit, pd.DataFrame(totals)], ignore_index=True).to_csv(
241 |         output_dir / "join_audit.csv", index=False, encoding="utf-8-sig")
242 |     pd.DataFrame([{k: v for k, v in c.items()} for c in columns.values()]).to_csv(
243 |         output_dir / "master_schema.csv", index=False, encoding="utf-8-sig")
244 |     pd.DataFrame([{"column_name": c, "pandas_dtype_read": v["dtype_after_read"],
245 |                    "pyarrow_type": v["pyarrow_storage_type"], "missing_count": v["missing_after"],
246 |                    "missing_pct": round(v["missing_after"] / ROWS * 100, 2)}
247 |                   for c, v in columns.items()]).to_csv(
248 |         output_dir / "master_dictionary.csv", index=False, encoding="utf-8-sig")
249 |     size = final.stat().st_size
250 |     report = {
251 |         "status": "PASSED", "path_base": "thesis directory (parent of scripts/)",
252 |         "inputs": inputs, "pre_downcasting_audit": pre_audit,
253 |         "master_size": {"rows": len(after), "columns": len(after.columns),
254 |                         "distinct_orders": BASKETS, "distinct_users": BASKETS,
255 |                         "train_orders_per_user": 1},
256 |         "checks": checks, "column_verifications": columns,
257 |         "file_info": {"primary_file": report_path(final), "size_bytes": size,
258 |                       "size_mb": round(size / (1024 * 1024), 2),
259 |                       "compression": "snappy", "sha256": final_sha},
260 |         "environment": {"python": sys.version.split()[0], "pandas": pd.__version__,
261 |                         "pyarrow": pa.__version__, "numpy": np.__version__},
262 |         "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
263 |     with open(output_dir / "master_verification.json", "w", encoding="utf-8") as f:
264 |         json.dump(report, f, indent=2, ensure_ascii=False)
265 |     print(f"MASTER PASSED: {len(after):,} dòng; {final}")
266 | 
267 | 
268 | if __name__ == "__main__":
269 |     sys.stdout.reconfigure(encoding="utf-8")
270 |     args = parse_args("Build and verify the PRJ-08 Master table")
271 |     build(args.clean_dir, args.output_dir, args.chunksize)
```

### 11. `scripts/m1_quality_summary.py`

> **Vai trò:** Tỷ lệ thiếu theo bảng nguồn và kiểm toán IQR kích thước giỏ trên toàn Master (chỉ mô tả, không lọc).  
> **Mục trong bài:** 3.2–3.3 · **Người viết:** Vương  
> **Đầu vào → đầu ra:** CSV sạch, Master → `missingness_summary.csv`, `basket_quality_summary.json`  
> **Hàm/lớp chính (dòng):** `digest` (21), `main` (26)  
> **Ghi chú:** `python scripts/m1_quality_summary.py`  
> *68 dòng · SHA-256 `240f8a784a46…`*

```python
 1 | """Tỷ lệ thiếu theo bảng nguồn và kiểm toán IQR kích thước giỏ trên toàn Master train.
 2 | 
 3 | Chạy sau summarize_cleaning.py và m1_build_master.py. Đây là kiểm toán cấu trúc,
 4 | không dùng ngưỡng IQR để lọc mẫu hay chọn mô hình (EDA mô hình chỉ dùng reference).
 5 | 
 6 | ĐỌC NHANH: hai bảng chất lượng cho mục 3.2-3.3. (1) Tỷ lệ thiếu theo bảng nguồn (trước/sau làm sạch);
 7 |   (2) kiểm toán IQR kích thước giỏ trên toàn Master: CHỈ để mô tả, KHÔNG dùng để lọc dòng hay chọn mô hình.
 8 | """
 9 | from datetime import datetime, timezone
10 | import hashlib
11 | import json
12 | from pathlib import Path
13 | 
14 | import pandas as pd
15 | 
16 | ROOT = Path(__file__).resolve().parents[1]
17 | REPORTS = ROOT / "BAO CAO/Bao cao lam sach"
18 | MASTER = ROOT / "DATA/Data đã làm sạch/master_train.parquet"
19 | 
20 | 
21 | def digest(path):
22 |     with path.open("rb") as stream:
23 |         return hashlib.file_digest(stream, "sha256").hexdigest()
24 | 
25 | 
26 | def main():
27 |     # Khối 1: tỷ lệ thiếu theo bảng nguồn, từ before_after.csv.
28 |     before = REPORTS / "before_after.csv"
29 |     sources = {p.relative_to(ROOT).as_posix(): digest(p) for p in (MASTER, before)}
30 |     missing = pd.read_csv(before)
31 |     total = missing["missing_final"] + missing["nonmissing_final"]
32 |     if total.le(0).any():
33 |         raise ValueError("Empty source table in quality report")
34 |     missing["rows"] = total
35 |     missing["missing_before_pct"] = 100 * missing["missing_tokens_before"] / total
36 |     missing["missing_final_pct"] = 100 * missing["missing_final"] / total
37 |     # Khối 2: IQR của kích thước giỏ trên Master; giỏ vượt hàng rào chỉ bị đánh dấu, vẫn giữ lại.
38 |     master = pd.read_parquet(MASTER, columns=["order_id", "product_id"])
39 |     if master.isna().any().any() or master.duplicated().any():
40 |         raise ValueError("Missing or duplicated basket-product keys")
41 |     sizes = master.groupby("order_id", observed=True).size()
42 |     q1, q3 = sizes.quantile([0.25, 0.75]).tolist()
43 |     iqr = q3 - q1
44 |     lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
45 |     flagged = sizes.lt(lower) | sizes.gt(upper)
46 |     # Báo cáo kèm hash nguồn và hash script để truy vết.
47 |     report = {
48 |         "created_at": datetime.now(timezone.utc).isoformat(),
49 |         "scope": "full train Master; structural quality audit only",
50 |         "source_sha256": sources, "script_sha256": digest(Path(__file__)),
51 |         "pandas_version": pd.__version__, "rows": len(master), "baskets": len(sizes),
52 |         "minimum": int(sizes.min()), "maximum": int(sizes.max()),
53 |         "q1": q1, "q3": q3, "iqr": iqr, "lower_fence": lower, "upper_fence": upper,
54 |         "quantile_interpolation": "linear", "flagged_baskets": int(flagged.sum()),
55 |         "flagged_pct": 100 * float(flagged.mean()),
56 |         "decision": "retain; statistical flag alone is not an invalid-record rule",
57 |         "limitations": "No household inference; no model tuning on full Master. "
58 |                        "Model-directed EDA must use reference after splitting."}
59 |     if {name: digest(ROOT / name) for name in sources} != sources:
60 |         raise ValueError("Source changed during quality audit")
61 |     missing.to_csv(REPORTS / "missingness_summary.csv", index=False, encoding="utf-8-sig")
62 |     (REPORTS / "basket_quality_summary.json").write_text(
63 |         json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
64 |     print(json.dumps(report, ensure_ascii=True, indent=2))
65 | 
66 | 
67 | if __name__ == "__main__":
68 |     main()
```

### 12. `scripts/m1_inspect_artifact.py`

> **Vai trò:** Chỉ đọc Master: `shape`, `info(memory_usage="deep")`, `isna().mean()*100`, so hai chế độ đọc.  
> **Mục trong bài:** 3.2 · **Người viết:** Phong  
> **Đầu vào → đầu ra:** Master → `master_info.txt`, `master_read_modes.*`  
> **Hàm/lớp chính (dòng):** `main` (14)  
> **Ghi chú:** `python scripts/m1_inspect_artifact.py`  
> *44 dòng · SHA-256 `5f239fc848c5…`*

```python
 1 | """Read-only structural inspection of the inherited M1 artifact, not a benchmark."""
 2 | from pathlib import Path
 3 | import hashlib
 4 | import io
 5 | import json
 6 | import platform
 7 | 
 8 | import pandas as pd
 9 | import pyarrow
10 | 
11 | ROOT = Path(__file__).resolve().parents[1]
12 | 
13 | 
14 | def main():
15 |     source = ROOT / "DATA/Data đã làm sạch/master_train.parquet"
16 |     before = hashlib.sha256(source.read_bytes()).hexdigest()
17 |     ordinary = pd.read_parquet(source)
18 |     nullable = pd.read_parquet(source, dtype_backend="numpy_nullable")
19 |     pd.testing.assert_frame_equal(ordinary, nullable, check_dtype=False, check_exact=True,
20 |                                   check_categorical=False)
21 |     assert ordinary.isna().equals(nullable.isna())
22 |     report = ROOT / "DATA/Data đã làm sạch/Bảng master TLCK"
23 |     report.mkdir(exist_ok=True)
24 |     buffer = io.StringIO()
25 |     nullable.info(buf=buffer, memory_usage="deep")
26 |     (report / "master_info.txt").write_text(buffer.getvalue(), encoding="utf-8")
27 |     missing = pd.DataFrame({"missing": nullable.isna().sum(),
28 |                             "missing_pct": nullable.isna().mean() * 100,
29 |                             "default_dtype": ordinary.dtypes.astype(str),
30 |                             "nullable_dtype": nullable.dtypes.astype(str)})
31 |     missing.index.name = "column"
32 |     missing.to_csv(report / "master_read_modes.csv", encoding="utf-8", lineterminator="\n")
33 |     result = {"scope": "structural artifact audit; full Master; not behavioral EDA or benchmark",
34 |               "master_sha256": before, "shape": list(nullable.shape),
35 |               "default_and_nullable_values_equal": True, "missing_masks_equal": True,
36 |               "python": platform.python_version(), "pandas": pd.__version__,
37 |               "pyarrow": pyarrow.__version__,
38 |               "source_unchanged": before == hashlib.sha256(source.read_bytes()).hexdigest()}
39 |     (report / "master_read_modes.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
40 |     print(json.dumps(result))
41 | 
42 | 
43 | if __name__ == "__main__":
44 |     main()
```

### 13. `scripts/m1_benchmark.py`

> **Vai trò:** Benchmark ba lượt, mỗi lượt một tiến trình con: thu hẹp kiểu, ghi/đọc CSV và Parquet, tái sử dụng Master; đo thời gian (`perf_counter`) và RSS đỉnh (`psutil`, 5 ms).  
> **Mục trong bài:** 3.2 (Bảng 3.4) · **Người viết:** Vương  
> **Đầu vào → đầu ra:** CSV sạch, Master → `data_benchmark.csv`, `data_benchmark_metadata.json`  
> **Hàm/lớp chính (dòng):** `normalize_parquet_dtypes` (80), `SubprocessPeakTracker` (92), `worker_downcasting` (133), `worker_write_csv` (170), `worker_write_parquet` (193), `worker_read_csv` (217), `worker_read_parquet` (239), `worker_merge_workflow` (263), `worker_parquet_workflow` (319), `run_worker_in_subprocess` (342), `verify_readers_equivalence` (355), `run_benchmark_suite` (398)  
> **Ghi chú:** Chạy một mình: `python scripts/m1_benchmark.py`. Giữ nguyên theo quyết định của nhóm.  
> *788 dòng · SHA-256 `71a18ddadb48…`*

```python
  1 | """
  2 | Benchmark Resource Optimization for PRJ-08 (Milestone M1) with Strict 3-Run Subprocess Isolation.
  3 | 
  4 | Implements:
  5 | - Subprocess isolation for every single measurement run to eliminate heap memory contamination.
  6 | - Continuous RSS monitoring during execution via dedicated background polling thread (every 5ms).
  7 | - Explicit timing scope measurement (wall time in seconds via time.perf_counter()).
  8 | - Uniform null handling (keep_default_na=False, na_values=[""]) across all CSV read branches.
  9 | - Uniform output dtypes between CSV and Parquet readers to ensure apples-to-apples comparison.
 10 | - Consistent benchmark artifacts: Write Parquet and Read Parquet operate on the EXACT SAME file (master_benchmark.parquet).
 11 | - Reconstructed unoptimized baseline clearly labeled and described in metadata.
 12 | - Explicit cache condition disclosure (Windows OS page cache / warm-cache transparency).
 13 | - Standardized units: MiB (1024^2 bytes) and seconds.
 14 | - Missing/inapplicable metrics left empty (not 0).
 15 | - Records Run 1, Run 2, Run 3 and computes Median.
 16 | 
 17 | Outputs:
 18 | - data_benchmark.csv (with columns: experiment, state, operation, run_id, rows, columns, dataframe_mib, peak_rss_mib, disk_mib, elapsed_seconds)
 19 | - data_benchmark_metadata.json (system info, timing scopes, cache condition, artifact specs)
 20 | """
 21 | import os
 22 | import gc
 23 | import sys
 24 | import time
 25 | import json
 26 | import platform
 27 | import threading
 28 | import subprocess
 29 | from pathlib import Path
 30 | from m1_common import parse_args, report_path
 31 | 
 32 | if hasattr(sys.stdout, "reconfigure"):
 33 |     sys.stdout.reconfigure(encoding="utf-8")
 34 | if __name__ == "__main__":
 35 |     cli_args = parse_args("Milestone M1 Benchmark Runner", benchmark=True)
 36 | 
 37 | import psutil
 38 | import numpy as np
 39 | import pandas as pd
 40 | import pyarrow as pa
 41 | import pyarrow.parquet as pq
 42 | 
 43 | MASTER_COLUMNS = [
 44 |     "order_id",
 45 |     "product_id",
 46 |     "add_to_cart_order",
 47 |     "reordered",
 48 |     "user_id",
 49 |     "eval_set",
 50 |     "order_number",
 51 |     "order_dow",
 52 |     "order_hour_of_day",
 53 |     "days_since_prior_order",
 54 |     "product_name",
 55 |     "aisle_id",
 56 |     "department_id",
 57 |     "aisle",
 58 |     "department",
 59 | ]
 60 | 
 61 | OPTIMIZED_DTYPES = {
 62 |     "order_id": "int32",
 63 |     "product_id": "int32",
 64 |     "add_to_cart_order": "int16",
 65 |     "reordered": "Int8",
 66 |     "user_id": "int32",
 67 |     "eval_set": "category",
 68 |     "order_number": "int16",
 69 |     "order_dow": "Int8",
 70 |     "order_hour_of_day": "Int8",
 71 |     "days_since_prior_order": "Float32",
 72 |     "product_name": "category",
 73 |     "aisle_id": "int16",
 74 |     "department_id": "int8",
 75 |     "aisle": "category",
 76 |     "department": "category",
 77 | }
 78 | 
 79 | 
 80 | def normalize_parquet_dtypes(df: pd.DataFrame) -> pd.DataFrame:
 81 |     """Đưa các cột nguyên không null từ Int32/Int16/Int8 nullable về int32/int16/int8 thuần chuẩn để đồng nhất tuyệt đối với CSV."""
 82 |     df["order_id"] = df["order_id"].astype("int32")
 83 |     df["product_id"] = df["product_id"].astype("int32")
 84 |     df["add_to_cart_order"] = df["add_to_cart_order"].astype("int16")
 85 |     df["user_id"] = df["user_id"].astype("int32")
 86 |     df["order_number"] = df["order_number"].astype("int16")
 87 |     df["aisle_id"] = df["aisle_id"].astype("int16")
 88 |     df["department_id"] = df["department_id"].astype("int8")
 89 |     return df
 90 | 
 91 | 
 92 | class SubprocessPeakTracker:
 93 |     def __init__(self, interval=0.005):
 94 |         self.interval = interval
 95 |         self.process = psutil.Process(os.getpid())
 96 |         self.peak_rss = self.process.memory_info().rss
 97 |         self._stop_event = threading.Event()
 98 |         self._thread = None
 99 | 
100 |     def _monitor(self):
101 |         while not self._stop_event.is_set():
102 |             try:
103 |                 rss = self.process.memory_info().rss
104 |                 if rss > self.peak_rss:
105 |                     self.peak_rss = rss
106 |             except Exception:
107 |                 pass
108 |             time.sleep(self.interval)
109 | 
110 |     def __enter__(self):
111 |         gc.collect()
112 |         self.peak_rss = self.process.memory_info().rss
113 |         self._stop_event.clear()
114 |         self._thread = threading.Thread(target=self._monitor, daemon=True)
115 |         self._thread.start()
116 |         return self
117 | 
118 |     def __exit__(self, exc_type, exc_val, exc_tb):
119 |         self._stop_event.set()
120 |         if self._thread:
121 |             self._thread.join(timeout=0.5)
122 |         rss = self.process.memory_info().rss
123 |         if rss > self.peak_rss:
124 |             self.peak_rss = rss
125 | 
126 |     def get_peak_mib(self):
127 |         return self.peak_rss / (1024 * 1024)
128 | 
129 | 
130 | # ==============================================================================
131 | # WORKER ROUTINES (Executed in an isolated fresh subprocess for each single run)
132 | # ==============================================================================
133 | def worker_downcasting(master_parquet_path: str):
134 |     df_raw = pd.read_parquet(master_parquet_path, dtype_backend="numpy_nullable")
135 |     df_unopt = pd.DataFrame()
136 |     for col in MASTER_COLUMNS:
137 |         s = df_raw[col]
138 |         if col in ["order_id", "product_id", "add_to_cart_order", "user_id", "order_number", "aisle_id", "department_id"]:
139 |             df_unopt[col] = s.astype("int64")
140 |         elif col in ["reordered", "order_dow", "order_hour_of_day", "days_since_prior_order"]:
141 |             df_unopt[col] = s.astype("float64")
142 |         else:
143 |             df_unopt[col] = s.astype("object")
144 |             
145 |     mem_unopt_mib = df_unopt.memory_usage(deep=True).sum() / (1024 * 1024)
146 |     del df_raw
147 |     gc.collect()
148 |     
149 |     with SubprocessPeakTracker() as tracker:
150 |         t0 = time.perf_counter()
151 |         df_opt = pd.DataFrame()
152 |         for col in MASTER_COLUMNS:
153 |             df_opt[col] = df_unopt[col].astype(OPTIMIZED_DTYPES[col])
154 |         elapsed = time.perf_counter() - t0
155 |         
156 |     mem_opt_mib = df_opt.memory_usage(deep=True).sum() / (1024 * 1024)
157 |     peak_mib = tracker.get_peak_mib()
158 |     
159 |     res = {
160 |         "mem_unopt_mib": mem_unopt_mib,
161 |         "mem_opt_mib": mem_opt_mib,
162 |         "elapsed_seconds": elapsed,
163 |         "peak_rss_mib": peak_mib,
164 |         "rows": len(df_opt),
165 |         "columns": len(df_opt.columns),
166 |     }
167 |     print("__BENCHMARK_RESULT__" + json.dumps(res))
168 | 
169 | 
170 | def worker_write_csv(master_parquet_path: str, target_csv_path: str):
171 |     df = pd.read_parquet(master_parquet_path, dtype_backend="numpy_nullable")
172 |     p_csv = Path(target_csv_path)
173 |     if p_csv.exists():
174 |         p_csv.unlink()
175 |         
176 |     with SubprocessPeakTracker() as tracker:
177 |         t0 = time.perf_counter()
178 |         df.to_csv(p_csv, index=False, encoding="utf-8")
179 |         elapsed = time.perf_counter() - t0
180 |         
181 |     peak_mib = tracker.get_peak_mib()
182 |     disk_mib = p_csv.stat().st_size / (1024 * 1024)
183 |     res = {
184 |         "disk_mib": disk_mib,
185 |         "elapsed_seconds": elapsed,
186 |         "peak_rss_mib": peak_mib,
187 |         "rows": len(df),
188 |         "columns": len(df.columns),
189 |     }
190 |     print("__BENCHMARK_RESULT__" + json.dumps(res))
191 | 
192 | 
193 | def worker_write_parquet(master_parquet_path: str, target_parquet_path: str):
194 |     df = pd.read_parquet(master_parquet_path, dtype_backend="numpy_nullable")
195 |     p_parq = Path(target_parquet_path)
196 |     if p_parq.exists():
197 |         p_parq.unlink()
198 |         
199 |     with SubprocessPeakTracker() as tracker:
200 |         t0 = time.perf_counter()
201 |         df.to_parquet(p_parq, compression="snappy", index=False)
202 |         elapsed = time.perf_counter() - t0
203 |         
204 |     peak_mib = tracker.get_peak_mib()
205 |     disk_mib = p_parq.stat().st_size / (1024 * 1024)
206 |     # Giữ nguyên tệp để worker_read_parquet đọc chính tệp đối chứng này!
207 |     res = {
208 |         "disk_mib": disk_mib,
209 |         "elapsed_seconds": elapsed,
210 |         "peak_rss_mib": peak_mib,
211 |         "rows": len(df),
212 |         "columns": len(df.columns),
213 |     }
214 |     print("__BENCHMARK_RESULT__" + json.dumps(res))
215 | 
216 | 
217 | def worker_read_csv(target_csv_path: str):
218 |     p_csv = Path(target_csv_path)
219 |     disk_mib = p_csv.stat().st_size / (1024 * 1024)
220 |     
221 |     with SubprocessPeakTracker() as tracker:
222 |         t0 = time.perf_counter()
223 |         df = pd.read_csv(p_csv, dtype=OPTIMIZED_DTYPES, keep_default_na=False, na_values=[""])
224 |         elapsed = time.perf_counter() - t0
225 |         
226 |     peak_mib = tracker.get_peak_mib()
227 |     df_mib = df.memory_usage(deep=True).sum() / (1024 * 1024)
228 |     res = {
229 |         "dataframe_mib": df_mib,
230 |         "disk_mib": disk_mib,
231 |         "elapsed_seconds": elapsed,
232 |         "peak_rss_mib": peak_mib,
233 |         "rows": len(df),
234 |         "columns": len(df.columns),
235 |     }
236 |     print("__BENCHMARK_RESULT__" + json.dumps(res))
237 | 
238 | 
239 | def worker_read_parquet(target_parquet_path: str):
240 |     p_parq = Path(target_parquet_path)
241 |     disk_mib = p_parq.stat().st_size / (1024 * 1024)
242 |     
243 |     with SubprocessPeakTracker() as tracker:
244 |         t0 = time.perf_counter()
245 |         df = pd.read_parquet(p_parq, dtype_backend="numpy_nullable")
246 |         # Chuẩn hóa về đúng contract schema để đồng nhất kiểu dữ liệu và bộ nhớ với nhánh CSV
247 |         df = normalize_parquet_dtypes(df)
248 |         elapsed = time.perf_counter() - t0
249 |         
250 |     peak_mib = tracker.get_peak_mib()
251 |     df_mib = df.memory_usage(deep=True).sum() / (1024 * 1024)
252 |     res = {
253 |         "dataframe_mib": df_mib,
254 |         "disk_mib": disk_mib,
255 |         "elapsed_seconds": elapsed,
256 |         "peak_rss_mib": peak_mib,
257 |         "rows": len(df),
258 |         "columns": len(df.columns),
259 |     }
260 |     print("__BENCHMARK_RESULT__" + json.dumps(res))
261 | 
262 | 
263 | def worker_merge_workflow(clean_dir_path: str):
264 |     clean_dir = Path(clean_dir_path)
265 |     with SubprocessPeakTracker() as tracker:
266 |         t0 = time.perf_counter()
267 |         df_train = pd.read_csv(
268 |             clean_dir / "order_products__train.csv",
269 |             dtype={"order_id": "int32", "product_id": "int32", "add_to_cart_order": "int16", "reordered": "Int8"},
270 |             keep_default_na=False,
271 |             na_values=[""]
272 |         )
273 |         df_orders = pd.read_csv(
274 |             clean_dir / "orders.csv",
275 |             dtype={"order_id": "int32", "user_id": "int32", "eval_set": "string", "order_number": "int16", "order_dow": "Int8", "order_hour_of_day": "Int8", "days_since_prior_order": "Float32"},
276 |             keep_default_na=False,
277 |             na_values=[""]
278 |         )
279 |         df_products = pd.read_csv(
280 |             clean_dir / "products.csv",
281 |             dtype={"product_id": "int32", "product_name": "string", "aisle_id": "int16", "department_id": "int8"},
282 |             keep_default_na=False,
283 |             na_values=[""]
284 |         )
285 |         df_aisles = pd.read_csv(
286 |             clean_dir / "aisles.csv",
287 |             dtype={"aisle_id": "int16", "aisle": "string"},
288 |             keep_default_na=False,
289 |             na_values=[""]
290 |         )
291 |         df_departments = pd.read_csv(
292 |             clean_dir / "departments.csv",
293 |             dtype={"department_id": "int8", "department": "string"},
294 |             keep_default_na=False,
295 |             na_values=[""]
296 |         )
297 |         
298 |         m1 = df_train.merge(df_orders[df_orders["order_id"].isin(df_train["order_id"])], on="order_id", how="left")
299 |         m2 = m1.merge(df_products, on="product_id", how="left")
300 |         m3 = m2.merge(df_aisles, on="aisle_id", how="left")
301 |         m4 = m3.merge(df_departments, on="department_id", how="left")
302 |         
303 |         for c in ["eval_set", "product_name", "aisle", "department"]:
304 |             m4[c] = m4[c].astype("category")
305 |         elapsed = time.perf_counter() - t0
306 |         
307 |     peak_mib = tracker.get_peak_mib()
308 |     df_mib = m4.memory_usage(deep=True).sum() / (1024 * 1024)
309 |     res = {
310 |         "dataframe_mib": df_mib,
311 |         "elapsed_seconds": elapsed,
312 |         "peak_rss_mib": peak_mib,
313 |         "rows": len(m4),
314 |         "columns": len(m4.columns),
315 |     }
316 |     print("__BENCHMARK_RESULT__" + json.dumps(res))
317 | 
318 | 
319 | def worker_parquet_workflow(master_parquet_path: str):
320 |     p_parq = Path(master_parquet_path)
321 |     with SubprocessPeakTracker() as tracker:
322 |         t0 = time.perf_counter()
323 |         df = pd.read_parquet(p_parq, dtype_backend="numpy_nullable")
324 |         df = normalize_parquet_dtypes(df)
325 |         elapsed = time.perf_counter() - t0
326 |         
327 |     peak_mib = tracker.get_peak_mib()
328 |     df_mib = df.memory_usage(deep=True).sum() / (1024 * 1024)
329 |     res = {
330 |         "dataframe_mib": df_mib,
331 |         "elapsed_seconds": elapsed,
332 |         "peak_rss_mib": peak_mib,
333 |         "rows": len(df),
334 |         "columns": len(df.columns),
335 |     }
336 |     print("__BENCHMARK_RESULT__" + json.dumps(res))
337 | 
338 | 
339 | # ==============================================================================
340 | # SUBPROCESS EXECUTION RUNNER
341 | # ==============================================================================
342 | def run_worker_in_subprocess(worker_cmd_args: list):
343 |     """Executes a worker in a fresh, isolated Python subprocess and captures JSON output."""
344 |     full_cmd = [sys.executable, str(Path(__file__).resolve()), "--worker"] + worker_cmd_args
345 |     proc = subprocess.run(
346 |         full_cmd, capture_output=True, text=True, encoding="utf-8", check=True)
347 |     out_lines = proc.stdout.splitlines()
348 |     for line in out_lines:
349 |         if line.startswith("__BENCHMARK_RESULT__"):
350 |             json_str = line.replace("__BENCHMARK_RESULT__", "")
351 |             return json.loads(json_str)
352 |     raise RuntimeError(f"Worker did not output benchmark result! Raw output: {proc.stdout}\nStderr: {proc.stderr}")
353 | 
354 | 
355 | def verify_readers_equivalence(csv_path: Path, parquet_path: Path):
356 |     """Kiểm chứng độc lập ngoài khoảng thời gian đo: hai cách đọc trả về cùng một dữ liệu chính xác."""
357 |     print("\n--- KIỂM CHỨNG ĐỘC LẬP TÍNH TƯƠNG ĐƯƠNG CỦA HAI PHÉP ĐỌC BENCHMARK ---")
358 |     df_c = pd.read_csv(csv_path, dtype=OPTIMIZED_DTYPES, keep_default_na=False, na_values=[""])
359 |     df_p = pd.read_parquet(parquet_path, dtype_backend="numpy_nullable")
360 |     df_p = normalize_parquet_dtypes(df_p)
361 |     
362 |     assert len(df_c) == len(df_p), f"Lệch số dòng: CSV={len(df_c)}, Parquet={len(df_p)}"
363 |     assert list(df_c.columns) == list(df_p.columns), "Lệch danh sách cột!"
364 |     
365 |     for col in MASTER_COLUMNS:
366 |         dt_c = str(df_c[col].dtype)
367 |         dt_p = str(df_p[col].dtype)
368 |         assert dt_c == dt_p, f"Cột {col}: Lệch dtype giữa CSV ({dt_c}) và Parquet ({dt_p})!"
369 |         
370 |         mask_c = df_c[col].isna()
371 |         mask_p = df_p[col].isna()
372 |         assert mask_c.equals(mask_p), f"Cột {col}: Lệch vị trí null giữa CSV và Parquet!"
373 |         
374 |         if col in ["eval_set", "product_name", "aisle", "department"]:
375 |             vc = df_c.loc[~mask_c, col].astype(str).to_numpy()
376 |             vp = df_p.loc[~mask_p, col].astype(str).to_numpy()
377 |             assert np.array_equal(vc, vp), f"Cột {col}: Lệch giá trị category giữa CSV và Parquet!"
378 |         elif col == "days_since_prior_order":
379 |             vc = df_c.loc[~mask_c, col].to_numpy()
380 |             vp = df_p.loc[~mask_p, col].to_numpy()
381 |             assert np.array_equal(vc, vp), f"Cột {col}: Lệch giá trị float!"
382 |         else:
383 |             vc = df_c.loc[~mask_c, col].to_numpy()
384 |             vp = df_p.loc[~mask_p, col].to_numpy()
385 |             assert np.array_equal(vc, vp), f"Cột {col}: Lệch giá trị int!"
386 |             
387 |     mem_c = df_c.memory_usage(deep=True).sum() / (1024 * 1024)
388 |     mem_p = df_p.memory_usage(deep=True).sum() / (1024 * 1024)
389 |     print(f" [OK] Xác thực hoàn tất: Cả hai phép đọc trả về đúng 100% từng giá trị, cùng vị trí thiếu, cùng 15 dtypes chuẩn.")
390 |     print(f"      Bộ nhớ DataFrame CSV: {mem_c:.2f} MiB | Bộ nhớ DataFrame Parquet: {mem_p:.2f} MiB.")
391 |     del df_c, df_p
392 |     gc.collect()
393 | 
394 | 
395 | # ==============================================================================
396 | # MAIN BENCHMARK CONTROLLER (3 Runs with Subprocess Isolation)
397 | # ==============================================================================
398 | def run_benchmark_suite(clean_dir: Path, output_dir: Path, master_parquet: Path):
399 |     output_dir.mkdir(parents=True, exist_ok=True)
400 |     bench_csv = output_dir / "master_benchmark.csv"
401 |     bench_parquet = output_dir / "master_benchmark.parquet"
402 |     
403 |     # 0. Đảm bảo file CSV đối chứng được tạo trước nếu chưa có
404 |     if not bench_csv.exists():
405 |         print(f"Khởi tạo tệp Master CSV đối chứng: {bench_csv.name}...")
406 |         df_init = pd.read_parquet(master_parquet, dtype_backend="numpy_nullable")
407 |         df_init.to_csv(bench_csv, index=False, encoding="utf-8")
408 |         del df_init
409 |         gc.collect()
410 |         
411 |     benchmark_rows = []
412 |     
413 |     # --------------------------------------------------------------------------
414 |     # THỰC NGHIỆM A: Bộ nhớ trước–sau tối ưu Dtype
415 |     # --------------------------------------------------------------------------
416 |     print("\n--- [A] THỰC NGHIỆM TỐI ƯU KIỂU DỮ LIỆU (3 lượt tiến trình con độc lập) ---")
417 |     downcast_runs = []
418 |     for r in range(1, 4):
419 |         print(f" * Lượt {r}/3: Khởi chạy worker tiến trình con...")
420 |         res = run_worker_in_subprocess(["downcasting", str(master_parquet)])
421 |         downcast_runs.append(res)
422 |         print(f"   -> Lượt {r}: RAM chưa tối ưu (reconstructed)={res['mem_unopt_mib']:.2f} MiB | RAM tối ưu={res['mem_opt_mib']:.2f} MiB | Thời gian={res['elapsed_seconds']:.4f}s | Peak RSS={res['peak_rss_mib']:.2f} MiB")
423 | 
424 |     # Ghi nhận trạng thái reconstructed_unoptimized
425 |     for r_idx, res in enumerate(downcast_runs, 1):
426 |         benchmark_rows.append({
427 |             "experiment": "A_Dtype_Downcasting",
428 |             "state": "reconstructed_unoptimized",
429 |             "operation": "in_memory_profile",
430 |             "run_id": str(r_idx),
431 |             "rows": res["rows"],
432 |             "columns": res["columns"],
433 |             "dataframe_mib": round(res["mem_unopt_mib"], 2),
434 |             "peak_rss_mib": "",  # Không áp dụng cho static profile
435 |             "disk_mib": "",       # Không áp dụng
436 |             "elapsed_seconds": "" # Không áp dụng
437 |         })
438 |     benchmark_rows.append({
439 |         "experiment": "A_Dtype_Downcasting",
440 |         "state": "reconstructed_unoptimized",
441 |         "operation": "in_memory_profile",
442 |         "run_id": "median",
443 |         "rows": downcast_runs[0]["rows"],
444 |         "columns": downcast_runs[0]["columns"],
445 |         "dataframe_mib": round(float(np.median([r["mem_unopt_mib"] for r in downcast_runs])), 2),
446 |         "peak_rss_mib": "",
447 |         "disk_mib": "",
448 |         "elapsed_seconds": ""
449 |     })
450 | 
451 |     # Ghi nhận trạng thái optimized (downcast execution)
452 |     for r_idx, res in enumerate(downcast_runs, 1):
453 |         benchmark_rows.append({
454 |             "experiment": "A_Dtype_Downcasting",
455 |             "state": "optimized",
456 |             "operation": "downcast_execution",
457 |             "run_id": str(r_idx),
458 |             "rows": res["rows"],
459 |             "columns": res["columns"],
460 |             "dataframe_mib": round(res["mem_opt_mib"], 2),
461 |             "peak_rss_mib": round(res["peak_rss_mib"], 2),
462 |             "disk_mib": "",
463 |             "elapsed_seconds": round(res["elapsed_seconds"], 4)
464 |         })
465 |     benchmark_rows.append({
466 |         "experiment": "A_Dtype_Downcasting",
467 |         "state": "optimized",
468 |         "operation": "downcast_execution",
469 |         "run_id": "median",
470 |         "rows": downcast_runs[0]["rows"],
471 |         "columns": downcast_runs[0]["columns"],
472 |         "dataframe_mib": round(float(np.median([r["mem_opt_mib"] for r in downcast_runs])), 2),
473 |         "peak_rss_mib": round(float(np.median([r["peak_rss_mib"] for r in downcast_runs])), 2),
474 |         "disk_mib": "",
475 |         "elapsed_seconds": round(float(np.median([r["elapsed_seconds"] for r in downcast_runs])), 4)
476 |     })
477 | 
478 |     # --------------------------------------------------------------------------
479 |     # THỰC NGHIỆM B: So sánh Định dạng và I/O (CSV vs Parquet)
480 |     # --------------------------------------------------------------------------
481 |     print("\n--- [B] THỰC NGHIỆM ĐỊNH DẠNG VÀ I/O (3 lượt tiến trình con độc lập) ---")
482 |     
483 |     # 1. Ghi CSV
484 |     write_csv_runs = []
485 |     for r in range(1, 4):
486 |         print(f" * [Ghi CSV] Lượt {r}/3...")
487 |         res = run_worker_in_subprocess(["write_csv", str(master_parquet), str(bench_csv)])
488 |         write_csv_runs.append(res)
489 |         benchmark_rows.append({
490 |             "experiment": "B_Format_and_IO",
491 |             "state": "csv_benchmark",
492 |             "operation": "write_disk",
493 |             "run_id": str(r),
494 |             "rows": res["rows"],
495 |             "columns": res["columns"],
496 |             "dataframe_mib": "",
497 |             "peak_rss_mib": round(res["peak_rss_mib"], 2),
498 |             "disk_mib": round(res["disk_mib"], 2),
499 |             "elapsed_seconds": round(res["elapsed_seconds"], 4)
500 |         })
501 |     benchmark_rows.append({
502 |         "experiment": "B_Format_and_IO",
503 |         "state": "csv_benchmark",
504 |         "operation": "write_disk",
505 |         "run_id": "median",
506 |         "rows": write_csv_runs[0]["rows"],
507 |         "columns": write_csv_runs[0]["columns"],
508 |         "dataframe_mib": "",
509 |         "peak_rss_mib": round(float(np.median([r["peak_rss_mib"] for r in write_csv_runs])), 2),
510 |         "disk_mib": round(float(np.median([r["disk_mib"] for r in write_csv_runs])), 2),
511 |         "elapsed_seconds": round(float(np.median([r["elapsed_seconds"] for r in write_csv_runs])), 4)
512 |     })
513 | 
514 |     # 2. Ghi Parquet (ghi ra bench_parquet và giữ lại để đo đọc)
515 |     write_parquet_runs = []
516 |     for r in range(1, 4):
517 |         print(f" * [Ghi Parquet] Lượt {r}/3...")
518 |         res = run_worker_in_subprocess(["write_parquet", str(master_parquet), str(bench_parquet)])
519 |         write_parquet_runs.append(res)
520 |         benchmark_rows.append({
521 |             "experiment": "B_Format_and_IO",
522 |             "state": "parquet_snappy",
523 |             "operation": "write_disk",
524 |             "run_id": str(r),
525 |             "rows": res["rows"],
526 |             "columns": res["columns"],
527 |             "dataframe_mib": "",
528 |             "peak_rss_mib": round(res["peak_rss_mib"], 2),
529 |             "disk_mib": round(res["disk_mib"], 2),
530 |             "elapsed_seconds": round(res["elapsed_seconds"], 4)
531 |         })
532 |     benchmark_rows.append({
533 |         "experiment": "B_Format_and_IO",
534 |         "state": "parquet_snappy",
535 |         "operation": "write_disk",
536 |         "run_id": "median",
537 |         "rows": write_parquet_runs[0]["rows"],
538 |         "columns": write_parquet_runs[0]["columns"],
539 |         "dataframe_mib": "",
540 |         "peak_rss_mib": round(float(np.median([r["peak_rss_mib"] for r in write_parquet_runs])), 2),
541 |         "disk_mib": round(float(np.median([r["disk_mib"] for r in write_parquet_runs])), 2),
542 |         "elapsed_seconds": round(float(np.median([r["elapsed_seconds"] for r in write_parquet_runs])), 4)
543 |     })
544 | 
545 |     # 3. Đọc CSV (đọc chính bench_csv)
546 |     read_csv_runs = []
547 |     for r in range(1, 4):
548 |         print(f" * [Đọc CSV] Lượt {r}/3...")
549 |         res = run_worker_in_subprocess(["read_csv", str(bench_csv)])
550 |         read_csv_runs.append(res)
551 |         benchmark_rows.append({
552 |             "experiment": "B_Format_and_IO",
553 |             "state": "csv_benchmark",
554 |             "operation": "read_disk",
555 |             "run_id": str(r),
556 |             "rows": res["rows"],
557 |             "columns": res["columns"],
558 |             "dataframe_mib": round(res["dataframe_mib"], 2),
559 |             "peak_rss_mib": round(res["peak_rss_mib"], 2),
560 |             "disk_mib": round(res["disk_mib"], 2),
561 |             "elapsed_seconds": round(res["elapsed_seconds"], 4)
562 |         })
563 |     benchmark_rows.append({
564 |         "experiment": "B_Format_and_IO",
565 |         "state": "csv_benchmark",
566 |         "operation": "read_disk",
567 |         "run_id": "median",
568 |         "rows": read_csv_runs[0]["rows"],
569 |         "columns": read_csv_runs[0]["columns"],
570 |         "dataframe_mib": round(float(np.median([r["dataframe_mib"] for r in read_csv_runs])), 2),
571 |         "peak_rss_mib": round(float(np.median([r["peak_rss_mib"] for r in read_csv_runs])), 2),
572 |         "disk_mib": round(float(np.median([r["disk_mib"] for r in read_csv_runs])), 2),
573 |         "elapsed_seconds": round(float(np.median([r["elapsed_seconds"] for r in read_csv_runs])), 4)
574 |     })
575 | 
576 |     # 4. Đọc Parquet (đọc chính bench_parquet vừa ghi)
577 |     read_parquet_runs = []
578 |     for r in range(1, 4):
579 |         print(f" * [Đọc Parquet] Lượt {r}/3...")
580 |         res = run_worker_in_subprocess(["read_parquet", str(bench_parquet)])
581 |         read_parquet_runs.append(res)
582 |         benchmark_rows.append({
583 |             "experiment": "B_Format_and_IO",
584 |             "state": "parquet_snappy",
585 |             "operation": "read_disk",
586 |             "run_id": str(r),
587 |             "rows": res["rows"],
588 |             "columns": res["columns"],
589 |             "dataframe_mib": round(res["dataframe_mib"], 2),
590 |             "peak_rss_mib": round(res["peak_rss_mib"], 2),
591 |             "disk_mib": round(res["disk_mib"], 2),
592 |             "elapsed_seconds": round(res["elapsed_seconds"], 4)
593 |         })
594 |     benchmark_rows.append({
595 |         "experiment": "B_Format_and_IO",
596 |         "state": "parquet_snappy",
597 |         "operation": "read_disk",
598 |         "run_id": "median",
599 |         "rows": read_parquet_runs[0]["rows"],
600 |         "columns": read_parquet_runs[0]["columns"],
601 |         "dataframe_mib": round(float(np.median([r["dataframe_mib"] for r in read_parquet_runs])), 2),
602 |         "peak_rss_mib": round(float(np.median([r["peak_rss_mib"] for r in read_parquet_runs])), 2),
603 |         "disk_mib": round(float(np.median([r["disk_mib"] for r in read_parquet_runs])), 2),
604 |         "elapsed_seconds": round(float(np.median([r["elapsed_seconds"] for r in read_parquet_runs])), 4)
605 |     })
606 | 
607 |     # Kiểm chứng độc lập tính tương đương của hai phép đọc CSV vs Parquet
608 |     verify_readers_equivalence(bench_csv, bench_parquet)
609 | 
610 |     # --------------------------------------------------------------------------
611 |     # THỰC NGHIỆM C: So sánh Quy trình Sử dụng
612 |     # --------------------------------------------------------------------------
613 |     print("\n--- [C] THỰC NGHIỆM QUY TRÌNH SỬ DỤNG (3 lượt tiến trình con độc lập) ---")
614 |     
615 |     # 1. Quy trình nạp 5 CSV và ghép
616 |     merge_wf_runs = []
617 |     for r in range(1, 4):
618 |         print(f" * [Quy trình 1: Đọc 5 CSV & Ghép] Lượt {r}/3...")
619 |         res = run_worker_in_subprocess(["merge_workflow", str(clean_dir)])
620 |         merge_wf_runs.append(res)
621 |         benchmark_rows.append({
622 |             "experiment": "C_Workflow_Comparison",
623 |             "state": "read_5_csv_and_merge",
624 |             "operation": "full_pipeline",
625 |             "run_id": str(r),
626 |             "rows": res["rows"],
627 |             "columns": res["columns"],
628 |             "dataframe_mib": round(res["dataframe_mib"], 2),
629 |             "peak_rss_mib": round(res["peak_rss_mib"], 2),
630 |             "disk_mib": "",
631 |             "elapsed_seconds": round(res["elapsed_seconds"], 4)
632 |         })
633 |     benchmark_rows.append({
634 |         "experiment": "C_Workflow_Comparison",
635 |         "state": "read_5_csv_and_merge",
636 |         "operation": "full_pipeline",
637 |         "run_id": "median",
638 |         "rows": merge_wf_runs[0]["rows"],
639 |         "columns": merge_wf_runs[0]["columns"],
640 |         "dataframe_mib": round(float(np.median([r["dataframe_mib"] for r in merge_wf_runs])), 2),
641 |         "peak_rss_mib": round(float(np.median([r["peak_rss_mib"] for r in merge_wf_runs])), 2),
642 |         "disk_mib": "",
643 |         "elapsed_seconds": round(float(np.median([r["elapsed_seconds"] for r in merge_wf_runs])), 4)
644 |     })
645 | 
646 |     # 2. Quy trình nạp trực tiếp Master Parquet
647 |     parquet_wf_runs = []
648 |     for r in range(1, 4):
649 |         print(f" * [Quy trình 2: Đọc Master Parquet] Lượt {r}/3...")
650 |         res = run_worker_in_subprocess(["parquet_workflow", str(master_parquet)])
651 |         parquet_wf_runs.append(res)
652 |         benchmark_rows.append({
653 |             "experiment": "C_Workflow_Comparison",
654 |             "state": "read_master_parquet",
655 |             "operation": "full_pipeline",
656 |             "run_id": str(r),
657 |             "rows": res["rows"],
658 |             "columns": res["columns"],
659 |             "dataframe_mib": round(res["dataframe_mib"], 2),
660 |             "peak_rss_mib": round(res["peak_rss_mib"], 2),
661 |             "disk_mib": "",
662 |             "elapsed_seconds": round(res["elapsed_seconds"], 4)
663 |         })
664 |     benchmark_rows.append({
665 |         "experiment": "C_Workflow_Comparison",
666 |         "state": "read_master_parquet",
667 |         "operation": "full_pipeline",
668 |         "run_id": "median",
669 |         "rows": parquet_wf_runs[0]["rows"],
670 |         "columns": parquet_wf_runs[0]["columns"],
671 |         "dataframe_mib": round(float(np.median([r["dataframe_mib"] for r in parquet_wf_runs])), 2),
672 |         "peak_rss_mib": round(float(np.median([r["peak_rss_mib"] for r in parquet_wf_runs])), 2),
673 |         "disk_mib": "",
674 |         "elapsed_seconds": round(float(np.median([r["elapsed_seconds"] for r in parquet_wf_runs])), 4)
675 |     })
676 | 
677 |     # --------------------------------------------------------------------------
678 |     # XUẤT BẢNG DATA_BENCHMARK.CSV VÀ DATA_BENCHMARK_METADATA.JSON
679 |     # --------------------------------------------------------------------------
680 |     df_benchmark = pd.DataFrame(benchmark_rows)
681 |     cols_order = [
682 |         "experiment", "state", "operation", "run_id",
683 |         "rows", "columns", "dataframe_mib", "peak_rss_mib", "disk_mib", "elapsed_seconds"
684 |     ]
685 |     df_benchmark = df_benchmark[cols_order]
686 |     
687 |     # Xuất ra 2 vị trí theo yêu cầu
688 |     out_csv_1 = output_dir / "data_benchmark.csv"
689 |     out_csv_2 = clean_dir / "data_benchmark.csv"
690 |     df_benchmark.to_csv(out_csv_1, index=False, encoding="utf-8-sig")
691 |     df_benchmark.to_csv(out_csv_2, index=False, encoding="utf-8-sig")
692 |     print(f"\n[OK] Đã xuất báo cáo chuẩn hóa: {out_csv_1}")
693 |     print(f"[OK] Đã xuất báo cáo chuẩn hóa: {out_csv_2}")
694 |     
695 |     # Metadata file
696 |     metadata = {
697 |         "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
698 |         "methodology": {
699 |             "iterations_per_experiment": 3,
700 |             "aggregation": "median",
701 |             "isolation": "Fresh Python process per run isolates interpreter state and heap history; OS page cache remains shared.",
702 |             "rss_tracking": "Sampled process RSS with a requested 5ms polling interval; short peaks may be missed and scheduling can delay samples.",
703 |             "null_handling": "Uniform rule across all CSV readers: keep_default_na=False, na_values=[''].",
704 |             "schema_normalization": "Parquet reader output normalized to identical contract dtypes as CSV reader, ensuring strict apples-to-apples comparison.",
705 |             "units": {
706 |                 "memory_and_disk": "MiB (1024^2 bytes)",
707 |                 "time": "seconds (wall-clock time via time.perf_counter())"
708 |             }
709 |         },
710 |         "baseline_explanation": {
711 |             "reconstructed_unoptimized": "Baseline kiểu rộng được dựng lại (reconstructed unoptimized baseline) bằng cách ép các cột số nguyên sang int64, số thực sang float64 và chuỗi sang object trên 1.384.617 dòng của bảng master, dùng để đo lường mức tiết kiệm bộ nhớ do hợp đồng downcasting PRJ-08 mang lại."
712 |         },
713 |         "environment": {
714 |             "os": f"{platform.system()} {platform.release()} ({platform.version()})",
715 |             "processor": platform.processor(),
716 |             "cpu_count_logical": psutil.cpu_count(logical=True),
717 |             "cpu_count_physical": psutil.cpu_count(logical=False),
718 |             "total_ram_gib": round(psutil.virtual_memory().total / (1024**3), 2),
719 |             "python_version": sys.version.split()[0],
720 |             "pandas_version": pd.__version__,
721 |             "pyarrow_version": pa.__version__,
722 |             "psutil_version": psutil.__version__
723 |         },
724 |         "cache_conditions": {
725 |             "os_page_cache": "Warm cache: On Windows OS, operating system file system page cache is managed by OS kernel and remains active across consecutive runs without administrator flushing. Measurements represent warm-cache disk I/O.",
726 |             "interpretation_rule": "Results represent warm-cache operating environment; no cold-cache assumptions are asserted."
727 |         },
728 |         "timing_scopes": {
729 |             "A_Dtype_Downcasting": "Starts immediately before column casting loop; ends immediately upon completing full 15-column downcast.",
730 |             "B_Format_and_IO:write_disk": "Starts immediately before df.to_csv() / df.to_parquet(); ends immediately upon file handle release.",
731 |             "B_Format_and_IO:read_disk": "Starts immediately before pd.read_csv() / pd.read_parquet(); ends immediately upon DataFrame object instantiation and dtype contract normalization.",
732 |             "C_Workflow_Comparison:read_5_csv_and_merge": "Starts immediately before loading 5 clean CSVs; ends immediately upon completing 4 left joins and categorical casting in memory.",
733 |             "C_Workflow_Comparison:read_master_parquet": "Starts immediately before pd.read_parquet(); ends immediately upon DataFrame instantiation and normalization."
734 |         },
735 |         "files_analyzed": {
736 |             "path_base": "thesis directory (parent of scripts/)",
737 |             "master_parquet": report_path(master_parquet),
738 |             "master_parquet_size_mib": round(master_parquet.stat().st_size / (1024*1024), 2),
739 |             "master_benchmark_csv": report_path(bench_csv),
740 |             "master_benchmark_csv_size_mib": round(bench_csv.stat().st_size / (1024*1024), 2),
741 |             "master_benchmark_parquet": report_path(bench_parquet),
742 |             "master_benchmark_parquet_size_mib": round(bench_parquet.stat().st_size / (1024*1024), 2)
743 |         }
744 |     }
745 |     
746 |     meta_json_1 = output_dir / "data_benchmark_metadata.json"
747 |     meta_json_2 = clean_dir / "data_benchmark_metadata.json"
748 |     with open(meta_json_1, "w", encoding="utf-8") as f:
749 |         json.dump(metadata, f, indent=2, ensure_ascii=False)
750 |     with open(meta_json_2, "w", encoding="utf-8") as f:
751 |         json.dump(metadata, f, indent=2, ensure_ascii=False)
752 |     print(f"[OK] Đã xuất siêu dữ liệu benchmark: {meta_json_1}")
753 |     print(f"[OK] Đã xuất siêu dữ liệu benchmark: {meta_json_2}")
754 |     
755 |     print("\n=== HOÀN TẤT ĐO LƯỜNG 3 LƯỢT ĐỘC LẬP THEO QUY ĐỊNH ===")
756 | 
757 | 
758 | # ==============================================================================
759 | # ENTRY POINT
760 | # ==============================================================================
761 | if __name__ == "__main__":
762 |     args = cli_args
763 |     
764 |     if args.worker:
765 |         task = args.worker[0]
766 |         params = args.worker[1:]
767 |         if task == "downcasting":
768 |             worker_downcasting(params[0])
769 |         elif task == "write_csv":
770 |             worker_write_csv(params[0], params[1])
771 |         elif task == "write_parquet":
772 |             worker_write_parquet(params[0], params[1])
773 |         elif task == "read_csv":
774 |             worker_read_csv(params[0])
775 |         elif task == "read_parquet":
776 |             worker_read_parquet(params[0])
777 |         elif task == "merge_workflow":
778 |             worker_merge_workflow(params[0])
779 |         elif task == "parquet_workflow":
780 |             worker_parquet_workflow(params[0])
781 |         else:
782 |             raise ValueError(f"Unknown worker task: {task}")
783 |         sys.exit(0)
784 |     else:
785 |         clean_dir = args.clean_dir
786 |         output_dir = args.output_dir
787 |         master_parquet = clean_dir / "master_train.parquet"
788 |         run_benchmark_suite(clean_dir, output_dir, master_parquet)
```

## Phần 4. Chia tập, thống kê mô tả, trực quan hóa và kiểm định (mục 3.4–3.6)

### 14. `configs/m2_eda.json`

> **Vai trò:** Đường dẫn vào/ra, khung giờ, ngưỡng nhóm nhỏ (30 giỏ) của M2.  
> **Mục trong bài:** 3.4–3.5 · **Người viết:** Vương  
> **Đầu vào → đầu ra:** —  
> *61 dòng · SHA-256 `f00865789fb5…`*

```json
 1 | {
 2 |   "contract_version": 1,
 3 |   "master": "DATA/Data đã làm sạch/master_train.parquet",
 4 |   "clean_dir": "DATA/Data đã làm sạch",
 5 |   "data_dir": "DATA/Data phai sinh/M2",
 6 |   "report_dir": "BAO CAO/Bao cao EDA/common",
 7 |   "hypotheses_config": "configs/hypotheses_config.json",
 8 |   "min_group_n": 30,
 9 |   "outputs": {
10 |     "tables": "BAO CAO/Bao cao EDA",
11 |     "ban1": "BAO CAO/Bao cao EDA/ban1",
12 |     "ban2": "BAO CAO/Bao cao EDA/ban2",
13 |     "figures": "BAO CAO/Bao cao EDA/figures",
14 |     "plot_data": "BAO CAO/Bao cao EDA/plot_data",
15 |     "drafts": "drafts/m2",
16 |     "figures_ban1": "BAO CAO/Bao cao EDA/figures/ban1",
17 |     "figures_ban2": "BAO CAO/Bao cao EDA/figures/ban2",
18 |     "plot_data_ban1": "BAO CAO/Bao cao EDA/plot_data/ban1",
19 |     "plot_data_ban2": "BAO CAO/Bao cao EDA/plot_data/ban2"
20 |   },
21 |   "seed": 42,
22 |   "rng": "PCG64",
23 |   "split_rule": "test=ceil(N/5);validation=floor(N/5);reference=floor(remaining/2);fit=remainder",
24 |   "slice_order": [
25 |     "test",
26 |     "reference",
27 |     "fit",
28 |     "validation"
29 |   ],
30 |   "expected_one_basket_per_user": true,
31 |   "quantile_interpolation": "linear",
32 |   "std_ddof": 1,
33 |   "kurtosis": "excess",
34 |   "iqr_multiplier": 1.5,
35 |   "hour_bins": [
36 |     0,
37 |     6,
38 |     12,
39 |     18,
40 |     24
41 |   ],
42 |   "hour_labels": [
43 |     "00–05",
44 |     "06–11",
45 |     "12–17",
46 |     "18–23"
47 |   ],
48 |   "top_n_grid": [
49 |     10,
50 |     50,
51 |     100,
52 |     500,
53 |     1000
54 |   ],
55 |   "correlation_columns": [
56 |     "basket_size",
57 |     "n_departments",
58 |     "n_aisles",
59 |     "days_since_prior_order"
60 |   ]
61 | }
```

### 15. `configs/m2_plot_style.json`

> **Vai trò:** Phông, cỡ chữ 12 pt, DPI 300, định dạng PNG + PDF, bảng màu.  
> **Mục trong bài:** 3.4–3.5 · **Người viết:** Vương · **Tệp trong khóa thực nghiệm**  
> **Đầu vào → đầu ra:** —  
> **Ghi chú:** Tệp trong khóa thực nghiệm.  
> *13 dòng · SHA-256 `8d1d3bdfb8b2…`*

```json
 1 | {
 2 |   "contract_version": 1,
 3 |   "font_family": "Times New Roman",
 4 |   "font_size_pt": 12,
 5 |   "dpi": 300,
 6 |   "formats": ["png", "pdf"],
 7 |   "figure_width_inches": 6.3,
 8 |   "colors": ["#264653", "#2A9D8F", "#E9C46A", "#E76F51"],
 9 |   "department_order": "department_id ascending; all 21 IDs",
10 |   "missing_color": "#D9D9D9",
11 |   "display_decimals": 2,
12 |   "note": "Validate text at final print size; split panels rather than shrink text. No figures generated in G0."
13 | }
```

### 16. `configs/hypotheses_config.json`

> **Vai trò:** Ba cặp ngành H1–H3 cố định trước lượt kiểm định, mức ý nghĩa 0,05.  
> **Mục trong bài:** 3.6 · **Người viết:** Phong  
> **Đầu vào → đầu ra:** —  
> **Ghi chú:** Giữ nguyên theo quyết định của nhóm.  
> *17 dòng · SHA-256 `468fe9e5dd7c…`*

```json
 1 | {
 2 |   "contract_version": 1,
 3 |   "stage": "locked before M2 cooccurrence analysis; not external preregistration",
 4 |   "alpha": 0.05,
 5 |   "adjustment": "holm",
 6 |   "family_size": 3,
 7 |   "minimum_expected": 5,
 8 |   "chi_square_correction": false,
 9 |   "fisher_alternative": "two-sided",
10 |   "constant_variable": "not_testable; use p=1 internally for Holm only; report NA",
11 |   "effect_size": "sqrt(uncorrected Pearson chi2 / N)",
12 |   "pairs": [
13 |     {"id": "H1", "a": 3, "a_name": "bakery", "b": 16, "b_name": "dairy eggs", "reason": "Possible complementary breakfast categories; not an observed result"},
14 |     {"id": "H2", "a": 9, "a_name": "dry goods pasta", "b": 13, "b_name": "pantry", "reason": "Possible main ingredients and pantry complements; not an observed result"},
15 |     {"id": "H3", "a": 4, "a_name": "produce", "b": 12, "b_name": "meat seafood", "reason": "Possible vegetable and protein meal components; not an observed result"}
16 |   ]
17 | }
```

### 17. `scripts/m2_foundation.py`

> **Vai trò:** Chia người dùng thành reference/fit/validation/test (PCG64 seed 42; test = ceil(N/5), validation = floor(N/5), reference = floor(phần còn lại/2)); tạo reference và bảng giỏ; ghi `common/hashes.json`.  
> **Mục trong bài:** 3.4, 4.2 · **Người viết:** Vương  
> **Đầu vào → đầu ra:** Master → `DATA/Data phai sinh/M2/*.parquet`  
> **Hàm/lớp chính (dòng):** `make_split` (32), `canonical_split_sha256` (49), `validate_master` (55), `build_baskets` (71), `check_sources` (96), `main` (110)  
> **Ghi chú:** `python scripts/m2_foundation.py`  
> *153 dòng · SHA-256 `727de62c59b4…`*

```python
  1 | """Nền M2 (G0): chia tập theo người dùng, tạo reference và bảng giỏ; không làm EDA.
  2 | 
  3 | 1. Kiểm tra Master và 6 CSV sạch khớp hồ sơ M1/làm sạch (master_verification.json,
  4 |    verification.json).
  5 | 2. validate_master; make_split (PCG64 seed 42, test=ceil(N/5), validation=floor(N/5),
  6 |    reference=floor(phần còn lại/2), fit=phần còn lại); tái lập khi đảo thứ tự ID.
  7 | 3. Ghi split_manifest.parquet, reference.parquet, basket_summary.parquet,
  8 |    department_lookup.csv vào DATA/Data phai sinh/M2/.
  9 | 4. Ghi BAO CAO/Bao cao EDA/common/hashes.json: SHA-256 các file trên, số đếm, dtype
 10 |    thực đọc của reference. Script phía sau gọi project_io.check_hashes() trước khi đọc.
 11 | 
 12 | ĐỌC NHANH (vấn đáp):
 13 |   Mục đích: chia 131.209 người dùng thành 4 tập (reference 30%, fit 30%, validation 20%, test 20%) và tạo bảng giỏ cho EDA.
 14 |   Vì sao chia theo NGƯỜI, không theo dòng? Một người ở hai tập sẽ làm mô hình học lại chính họ (rò rỉ thông tin).
 15 |   Vì sao có hashes.json? Mọi script sau phải kiểm hash trước khi đọc: dữ liệu bị sửa là dừng.
 16 |   Tái lập: chia lại với danh sách ID đảo ngược phải ra đúng kết quả cũ.
 17 | """
 18 | import hashlib
 19 | 
 20 | import numpy as np
 21 | import pandas as pd
 22 | 
 23 | from project_io import (FOUNDATION_HASHES, config, path, read_json, relative, require,
 24 |                         sha256, write_frame, write_hashes)
 25 | 
 26 | # Sáu CSV sạch phải khớp hash đã ghi lúc làm sạch.
 27 | CLEAN = ("aisles", "departments", "products", "orders",
 28 |          "order_products__prior", "order_products__train")
 29 | 
 30 | 
 31 | # CHIA TẬP: xáo ID người dùng bằng PCG64 seed 42 rồi cắt thành test, reference, fit, validation.
 32 | def make_split(users, seed=42):
 33 |     values = np.asarray(sorted(users), dtype=np.int64)
 34 |     require(len(values) == len(np.unique(values)), "Duplicate user IDs")
 35 |     n = len(values)
 36 |     require(n >= 5, "At least five users needed")
 37 |     # test = làm tròn lên N/5; validation = làm tròn xuống N/5; phần còn lại chia đôi cho reference và fit.
 38 |     n_test, n_validation = (n + 4) // 5, n // 5
 39 |     remaining = n - n_test - n_validation
 40 |     counts = {"test": n_test, "reference": remaining // 2,
 41 |               "fit": remaining - remaining // 2, "validation": n_validation}
 42 |     shuffled = np.random.Generator(np.random.PCG64(seed)).permutation(values)
 43 |     labels = [label for label, count in counts.items() for _ in range(count)]
 44 |     return pd.DataFrame({"user_id": shuffled, "split": labels}).sort_values(
 45 |         "user_id").reset_index(drop=True)
 46 | 
 47 | 
 48 | # Dấu vân tay của bảng chia tập (sắp theo user_id) để chứng minh chia tập không đổi.
 49 | def canonical_split_sha256(split):
 50 |     text = split.sort_values("user_id").to_csv(index=False, lineterminator="\n")
 51 |     return hashlib.sha256(text.encode("utf-8")).hexdigest()
 52 | 
 53 | 
 54 | # Kiểm tra Master: không thiếu khóa, không trùng cặp, mỗi người đúng một giỏ, chỉ có train, mỗi quầy thuộc một ngành.
 55 | def validate_master(frame):
 56 |     keys = ["order_id", "product_id", "user_id", "aisle_id", "department_id"]
 57 |     require(not frame[keys].isna().any().any(), "Missing identifiers")
 58 |     require(all(pd.api.types.is_integer_dtype(frame[k]) for k in keys),
 59 |             "Identifiers must have integer dtype")
 60 |     require(not frame.duplicated(["order_id", "product_id"]).any(), "Duplicate order/product key")
 61 |     pairs = frame[["user_id", "order_id"]].drop_duplicates()
 62 |     require(not pairs.user_id.duplicated().any(), "Multiple baskets per user")
 63 |     require(not pairs.order_id.duplicated().any(), "Multiple users per order")
 64 |     require(frame.eval_set.eq("train").all(), "Master must contain train only")
 65 |     require(frame.groupby("aisle_id", observed=True).department_id.nunique().le(1).all(),
 66 |             "Aisle maps to multiple departments")
 67 |     return pairs
 68 | 
 69 | 
 70 | # Gom dòng sản phẩm thành bảng giỏ: kích thước giỏ, số ngành, số quầy, ngày, giờ và khung giờ (hour_band).
 71 | def build_baskets(reference, cfg):
 72 |     validate_master(reference)
 73 |     attributes = ["user_id", "order_dow", "order_hour_of_day", "days_since_prior_order"]
 74 |     grouped = reference.groupby("order_id", observed=True, sort=True)
 75 |     require(grouped[attributes].nunique(dropna=False).le(1).all().all(),
 76 |             "Conflicting order attributes, including missing values")
 77 |     baskets = grouped.agg(basket_size=("product_id", "nunique"),
 78 |                           n_departments=("department_id", "nunique"),
 79 |                           n_aisles=("aisle_id", "nunique")).reset_index()
 80 |     attributes_frame = reference[["order_id"] + attributes].drop_duplicates("order_id")
 81 |     baskets = baskets.join(attributes_frame.set_index("order_id"),
 82 |                            on="order_id", validate="one_to_one")
 83 |     for column, low, high in (("order_dow", 0, 6), ("order_hour_of_day", 0, 23),
 84 |                               ("days_since_prior_order", 0, 30)):
 85 |         require(baskets[column].dropna().between(low, high).all(), f"Invalid domain: {column}")
 86 |     baskets["hour_band"] = pd.cut(
 87 |         baskets.order_hour_of_day.astype("float64"), bins=cfg["hour_bins"],
 88 |         labels=cfg["hour_labels"], right=False, ordered=True)
 89 |     require(baskets.basket_size.sum() == len(reference), "Basket row mismatch")
 90 |     require((baskets.n_departments.ge(1) & baskets.n_departments.le(baskets.n_aisles) &
 91 |              baskets.n_aisles.le(baskets.basket_size)).all(), "Invalid basket counts")
 92 |     return baskets.sort_values("order_id").reset_index(drop=True)
 93 | 
 94 | 
 95 | # Cổng đầu vào: Master và 6 CSV sạch phải khớp hash của M1 và của bước làm sạch.
 96 | def check_sources(cfg):
 97 |     """Master và CSV sạch phải khớp hash đã ghi ở M1 và ở bước làm sạch."""
 98 |     m1 = read_json(path(cfg["clean_dir"]) / "Bảng master TLCK" / "master_verification.json")
 99 |     require(m1["status"] == "PASSED", "M1 chưa đạt")
100 |     require(sha256(path(cfg["master"])) == m1["file_info"]["sha256"], "Master khác hồ sơ M1")
101 |     clean = read_json(path("BAO CAO/Bao cao lam sach/verification.json"))
102 |     require(clean["status"] == "verified", "Làm sạch chưa được xác minh")
103 |     recorded = {r["table"]: r["new_sha256"] for r in clean["comparison_previous"]}
104 |     for name in CLEAN:
105 |         require(sha256(path(cfg["clean_dir"]) / f"{name}.csv") == recorded[name],
106 |                 f"CSV khác hồ sơ làm sạch: {name}")
107 | 
108 | 
109 | # main: kiểm nguồn -> chia tập -> lấy reference -> dựng bảng giỏ -> ghi 4 tệp -> ghi hashes.json (cổng cho mọi script sau).
110 | def main():
111 |     cfg = config()
112 |     data = path(cfg["data_dir"])
113 |     check_sources(cfg)
114 |     master = pd.read_parquet(path(cfg["master"]))
115 |     pairs = validate_master(master)
116 |     split = make_split(pairs.user_id, cfg["seed"])
117 |     pd.testing.assert_frame_equal(split, make_split(pairs.user_id.iloc[::-1], cfg["seed"]))
118 |     require(set(split.user_id) == set(pairs.user_id), "Split does not cover population")
119 |     users = split.loc[split.split.eq("reference"), "user_id"]
120 |     reference = master.loc[master.user_id.isin(users)].sort_values(
121 |         ["order_id", "product_id"]).reset_index(drop=True)
122 |     require(reference.user_id.nunique() == len(users), "Missing reference users")
123 |     baskets = build_baskets(reference, cfg)
124 |     lookup = pd.read_csv(path(cfg["clean_dir"]) / "departments.csv",
125 |                          keep_default_na=False).sort_values("department_id")
126 |     require(lookup.department_id.tolist() == list(range(1, 22)), "Expected department IDs 1..21")
127 |     require(reference.department_id.isin(lookup.department_id).all(), "Unknown department")
128 |     names = lookup.set_index("department_id").department.to_dict()
129 |     require(names[21] == "missing", "Literal missing must be preserved")
130 |     for pair in read_json(path(cfg["hypotheses_config"]))["pairs"]:
131 |         require(names[pair["a"]] == pair["a_name"] and names[pair["b"]] == pair["b_name"],
132 |                 "Hypothesis ID/name mismatch")
133 |     outputs = {"split_manifest.parquet": split, "reference.parquet": reference,
134 |                "basket_summary.parquet": baskets, "department_lookup.csv": lookup}
135 |     for name, frame in outputs.items():
136 |         write_frame(data / name, frame)
137 |         if name.endswith(".parquet"):   # đọc lại để chắc nội dung và dtype không đổi
138 |             pd.testing.assert_frame_equal(frame, pd.read_parquet(data / name))
139 |     counts = {"master_rows": len(master), "users": len(pairs), "reference_rows": len(reference),
140 |               "split_users": {str(k): int(v) for k, v in split.split.value_counts().items()},
141 |               "reference_baskets": len(baskets),
142 |               "reference_users": int(baskets.user_id.nunique()), "departments": len(lookup)}
143 |     write_hashes(FOUNDATION_HASHES,
144 |                  [path(cfg["master"])] + [data / n for n in outputs] + [path(cfg["hypotheses_config"])],
145 |                  counts=counts, canonical_split_sha256=canonical_split_sha256(split),
146 |                  reference_dtypes={k: str(v) for k, v in reference.dtypes.items()},
147 |                  basket_dtypes={k: str(v) for k, v in baskets.dtypes.items()},
148 |                  parquet_reader="pd.read_parquet mặc định, không đổi dtype_backend")
149 |     print(counts, relative(path(FOUNDATION_HASHES)))
150 | 
151 | 
152 | if __name__ == "__main__":
153 |     main()
```

### 18. `scripts/m2_profile_inputs.py`

> **Vai trò:** Dấu vết kiểm tra đầu vào: `shape`, `info`, tỷ lệ thiếu, `describe()`.  
> **Mục trong bài:** 3.2 · **Người viết:** Vương  
> **Đầu vào → đầu ra:** Master, reference → `common/profile/`  
> **Hàm/lớp chính (dòng):** `missing_table` (16), `main` (23)  
> *45 dòng · SHA-256 `087d200bc9a5…`*

```python
 1 | """Dấu vết kiểm tra đầu vào: shape, info(memory_usage="deep"), isna().mean()*100, describe().
 2 | 
 3 | Tách tỷ lệ thiếu cấp dòng Master (train) khỏi cấp giỏ reference. Không thay thế EDA 3.4–3.6.
 4 | Đầu ra: BAO CAO/Bao cao EDA/common/profile/.
 5 | 
 6 | ĐỌC NHANH: ghi dấu vết kiểm tra đầu vào (shape, info, tỷ lệ thiếu, describe) cho mục 3.2; mẫu số ghi rõ là dòng Master hay giỏ reference.
 7 | """
 8 | import io
 9 | 
10 | import pandas as pd
11 | 
12 | from project_io import check_hashes, config, path, write_frame, write_json
13 | 
14 | 
15 | # Bảng tỷ lệ thiếu theo cột, ghi rõ mẫu số và đơn vị.
16 | def missing_table(frame, unit):
17 |     return pd.DataFrame({"column": frame.columns, "missing": frame.isna().sum().values,
18 |                          "missing_pct": (frame.isna().mean() * 100).values,
19 |                          "denominator": len(frame), "unit": unit})
20 | 
21 | 
22 | # main: kiểm hash -> ghi info/thiếu/describe của Master và của bảng giỏ reference.
23 | def main():
24 |     cfg = config()
25 |     record = check_hashes()
26 |     folder = path("BAO CAO/Bao cao EDA/common/profile")
27 |     master = pd.read_parquet(path(cfg["master"]))
28 |     buffer = io.StringIO()
29 |     master.info(buf=buffer, memory_usage="deep")
30 |     folder.mkdir(parents=True, exist_ok=True)
31 |     (folder / "master_info.txt").write_text(buffer.getvalue(), encoding="utf-8")
32 |     write_frame(folder / "master_missing.csv", missing_table(master, "train product-order row"))
33 |     baskets = pd.read_parquet(path(cfg["data_dir"]) / "basket_summary.parquet")
34 |     write_frame(folder / "reference_missing.csv", missing_table(baskets, "reference basket"))
35 |     write_frame(folder / "reference_describe.csv",
36 |                 baskets[cfg["correlation_columns"]].describe().reset_index())
37 |     write_json(folder / "inspection.json", {
38 |         "scope": "Basic inspection trace, not completed section 3.4",
39 |         "master_shape": list(master.shape), "reference_baskets_shape": list(baskets.shape),
40 |         "canonical_split_sha256": record["canonical_split_sha256"]})
41 |     print(master.shape, baskets.shape)
42 | 
43 | 
44 | if __name__ == "__main__":
45 |     main()
```

### 19. `scripts/m2_eda_summary.py`

> **Vai trò:** Thống kê mô tả trên reference: 4 biến cấp giỏ, tần số ngày giờ, ngoại lai IQR (đánh dấu, giữ 100% giỏ), ngành, quầy, độ phổ biến, độ phủ Top-N.  
> **Mục trong bài:** 3.4 (Bảng 3.7–3.9) · **Người viết:** Vương  
> **Đầu vào → đầu ra:** reference → 8 CSV trong `BAO CAO/Bao cao EDA/` + `reference_outliers.json`  
> **Hàm/lớp chính (dòng):** `display_name` (19), `group_summary` (24), `department_display` (47), `summarize` (60), `main` (141)  
> **Ghi chú:** `python scripts/m2_eda_summary.py`  
> *157 dòng · SHA-256 `512adacc032b…`*

```python
  1 | """Vương, mục 3.4: thống kê mô tả trên reference -> 8 CSV và reference_outliers.json.
  2 | 
  3 | Mẫu số ghi ở từng bảng: giỏ, dòng sản phẩm–đơn hoặc dòng có reordered hợp lệ.
  4 | Giữ đủ danh mục (cả nhóm 0 dòng và mã chưa có tên); không lọc Top-N trong reference.
  5 | 
  6 | ĐỌC NHANH: tạo 8 bảng thống kê mô tả của mục 3.4 trên tập reference (không đụng test).
  7 |   Năm phần trong summarize(): (1) mô tả 4 biến; (2) tần số ngày giờ; (3) ngoại lai IQR (chỉ đánh dấu, giữ 100% giỏ);
  8 |   (4) ngành, quầy, độ phổ biến sản phẩm; (5) độ phủ Top-N = tỷ lệ giỏ có ít nhất một sản phẩm trong Top-N.
  9 |   Mọi con số trong lời văn mục 3.4 được chép từ các CSV này.
 10 | """
 11 | import numpy as np
 12 | import pandas as pd
 13 | 
 14 | from m2_foundation import build_baskets
 15 | from project_io import check_hashes, config, path, require, write_frame, write_json
 16 | 
 17 | 
 18 | # Sản phẩm/quầy chưa có tên thì hiện 'Chưa có tên (ID=...)' để không mất dòng.
 19 | def display_name(value, identifier):
 20 |     return f"Chưa có tên (ID={identifier})" if pd.isna(value) or not str(value).strip() else str(value)
 21 | 
 22 | 
 23 | # Bảng theo ngành hoặc quầy: số dòng, số giỏ, tỷ lệ mua lại; giữ đủ danh mục kể cả mã 0 dòng.
 24 | def group_summary(reference, lookup, key, label, n_baskets):
 25 |     """Theo ngành/quầy, giữ đủ danh mục nguồn kể cả mã không xuất hiện."""
 26 |     require(not lookup[key].duplicated().any() and reference[key].isin(lookup[key]).all(),
 27 |             "Lookup ID trùng hoặc lạ")
 28 |     counts = reference.groupby(key, observed=True).agg(
 29 |         row_count=("order_id", "size"), basket_count=("order_id", "nunique"),
 30 |         reordered_valid=("reordered", "count"), reordered_yes=("reordered", "sum")).reset_index()
 31 |     r = lookup[[key, label]].merge(counts, on=key, how="left", validate="one_to_one"
 32 |                                    ).sort_values(key).reset_index(drop=True)
 33 |     for column in counts.columns.drop(key):
 34 |         r[column] = r[column].fillna(0).astype("int64")
 35 |     r["display_name"] = [display_name(v, i) for i, v in zip(r[key], r[label])]
 36 |     r["reordered_missing"] = r.row_count - r.reordered_valid
 37 |     r["row_share"] = r.row_count / len(reference)
 38 |     r["basket_coverage"] = r.basket_count / n_baskets
 39 |     r["observed_reorder_rate"] = r.reordered_yes / r.reordered_valid.replace(0, np.nan)
 40 |     r["reordered_missing_pct"] = 100 * r.reordered_missing / r.row_count.replace(0, np.nan)
 41 |     require(r.row_count.sum() == len(reference) and r.basket_count.le(n_baskets).all(),
 42 |             f"Mất dòng hoặc độ phủ sai: {label}")
 43 |     return r
 44 | 
 45 | 
 46 | # Top-10 ngành cộng một dòng 'các ngành còn lại', dùng cho hình 2.
 47 | def department_display(reference, departments, n_baskets):
 48 |     """Top-10 ngành theo số dòng và một dòng gộp các ngành còn lại (độ phủ tính theo hợp)."""
 49 |     top = departments.sort_values(["row_count", "department_id"], ascending=[False, True]).head(10)
 50 |     top = top.assign(group_key=top.department_id.astype(str))
 51 |     others = reference.loc[~reference.department_id.isin(top.department_id)]
 52 |     rest = pd.DataFrame([{"group_key": "remaining", "display_name": "Các ngành còn lại",
 53 |                           "row_count": len(others), "row_share": len(others) / len(reference),
 54 |                           "basket_count": others.order_id.nunique(),
 55 |                           "basket_coverage": others.order_id.nunique() / n_baskets}])
 56 |     return pd.concat([top[rest.columns], rest], ignore_index=True)
 57 | 
 58 | 
 59 | # Tính toàn bộ 8 bảng của mục 3.4.
 60 | def summarize(reference, baskets, departments, aisles, products, cfg):
 61 |     require(len(reference) > 0, "Empty reference")
 62 |     pd.testing.assert_frame_equal(baskets, build_baskets(reference, cfg), check_exact=True)
 63 |     n, rule = len(baskets), cfg["quantile_interpolation"]
 64 |     overview = {"users": baskets.user_id.nunique(), "baskets": n, "product_order_rows": len(reference),
 65 |                 "products_observed": reference.product_id.nunique(),
 66 |                 "departments_observed": reference.department_id.nunique(),
 67 |                 "aisles_observed": reference.aisle_id.nunique(),
 68 |                 "singleton_baskets": int(baskets.basket_size.eq(1).sum())}
 69 |     # (1) Mô tả 4 biến định lượng: trung bình, độ lệch chuẩn mẫu, phân vị, độ lệch, độ nhọn vượt chuẩn.
 70 |     rows = []
 71 |     for column in cfg["correlation_columns"]:   # std mẫu (ddof=1), kurtosis vượt chuẩn
 72 |         s = baskets[column].dropna().astype("float64")
 73 |         q = s.quantile([0.25, 0.5, 0.75], interpolation=rule)
 74 |         varied = s.nunique() > 1
 75 |         rows.append({"variable": column, "n_total": n, "n_valid": len(s), "n_missing": n - len(s),
 76 |                      "missing_pct": 100 * (n-len(s))/n, "mean": s.mean(), "std": s.std(ddof=1),
 77 |                      "min": s.min(), "q1": q.loc[0.25], "median": q.loc[0.5], "q3": q.loc[0.75],
 78 |                      "max": s.max(), "skew": s.skew() if len(s) >= 3 and varied else np.nan,
 79 |                      "kurtosis_excess": s.kurt() if len(s) >= 4 and varied else np.nan})
 80 |     # (2) Tần số theo ngày, giờ, khung giờ: có hàng NA riêng và hai mẫu số (cả mẫu / chỉ giá trị hợp lệ).
 81 |     frequencies = []
 82 |     for column, domain in {"order_dow": range(7), "order_hour_of_day": range(24),
 83 |                            "hour_band": cfg["hour_labels"]}.items():
 84 |         s = baskets[column]
 85 |         valid = int(s.notna().sum())
 86 |         for value in [*domain, None]:   # None = dòng NA
 87 |             count = int(s.eq(value).sum()) if value is not None else n - valid
 88 |             frequencies.append({"variable": column, "value": "NA" if value is None else str(value),
 89 |                                 "is_missing": value is None, "count": count, "n_total": n,
 90 |                                 "n_valid": valid, "all_pct": 100 * count/n,
 91 |                                 "valid_pct": 100 * count/valid if valid and value is not None else np.nan})
 92 |     # (3) Ngoại lai kích thước giỏ theo IQR: chỉ đánh dấu, quyết định giữ lại 100% giỏ.
 93 |     sizes = baskets.basket_size
 94 |     q1, q3 = sizes.quantile([0.25, 0.75], interpolation=rule)
 95 |     iqr = float(q3-q1)
 96 |     lower, upper = float(q1-cfg["iqr_multiplier"]*iqr), float(q3+cfg["iqr_multiplier"]*iqr)
 97 |     flagged = int((sizes.lt(lower) | sizes.gt(upper)).sum())
 98 |     outliers = {"scope": "reference baskets only", "n_baskets": n, "q1": float(q1), "q3": float(q3),
 99 |                 "iqr": iqr, "lower_fence": lower, "upper_fence": upper, "flagged_baskets": flagged,
100 |                 "flagged_rate": flagged/n, "flagged_pct": 100*flagged/n,
101 |                 "decision": "retain all baskets", "quantile_interpolation": rule}
102 |     # (4) Ngành, quầy, độ phổ biến sản phẩm (xếp theo số giỏ chứa, hòa thì theo product_id).
103 |     dept = group_summary(reference, departments, "department_id", "department", n)
104 |     pop = reference.groupby("product_id", observed=True).agg(
105 |         basket_count=("order_id", "nunique"), row_count=("order_id", "size")).reset_index()
106 |     require(pop.basket_count.eq(pop.row_count).all(), "Duplicate product/giỏ")
107 |     require(pop.product_id.isin(products.product_id).all(), "Unknown product")
108 |     pop = pop.merge(products[["product_id", "product_name"]], on="product_id", how="left",
109 |                     validate="one_to_one")
110 |     pop["display_name"] = [display_name(v, i) for i, v in zip(pop.product_id, pop.product_name)]
111 |     pop = pop.sort_values(["basket_count", "product_id"], ascending=[False, True]).reset_index(drop=True)
112 |     pop["popularity"] = pop.basket_count/n
113 |     pop["rank"] = np.arange(1, len(pop)+1)
114 |     pop["row_share"] = pop.row_count/len(reference)
115 |     pop["cumulative_row_share"] = pop.row_share.cumsum()
116 |     # (5) Độ phủ Top-N: hợp các giỏ có chứa sản phẩm trong Top-N (không cộng các popularity).
117 |     top_rows = []
118 |     for requested in cfg["top_n_grid"]:   # độ phủ là hợp các giỏ, không cộng popularity
119 |         ids = pop.head(requested).product_id
120 |         subset = reference.loc[reference.product_id.isin(ids)]
121 |         count = subset.order_id.nunique()
122 |         top_rows.append({"n_requested": requested, "n_actual": len(ids), "row_count": len(subset),
123 |                          "row_share": len(subset)/len(reference), "basket_count": count,
124 |                          "basket_coverage": count/n, "n_rows_total": len(reference),
125 |                          "n_baskets_total": n, "outside_row_count": len(reference)-len(subset),
126 |                          "outside_row_share": 1-len(subset)/len(reference)})
127 |     top = pd.DataFrame(top_rows)
128 |     require(top.basket_coverage.is_monotonic_increasing and top.row_share.is_monotonic_increasing,
129 |             "Top-N không tăng dần")
130 |     tables = {"sample_overview": pd.DataFrame({"metric": overview.keys(), "value": overview.values()}),
131 |               "eda_summary": pd.DataFrame(rows), "categorical_frequencies": pd.DataFrame(frequencies),
132 |               "department_summary": dept,
133 |               "aisle_summary": group_summary(reference, aisles, "aisle_id", "aisle", n),
134 |               "product_popularity": pop, "top_n_coverage": top,
135 |               "department_display": department_display(reference, dept, n)}
136 |     require(np.isclose(tables["department_display"].row_share.sum(), 1), "Top-10 + phần còn lại ≠ 100%")
137 |     return tables, outliers
138 | 
139 | 
140 | # main: kiểm hash -> nạp reference và bảng tra -> summarize -> ghi 8 CSV và reference_outliers.json.
141 | def main():
142 |     cfg = config()
143 |     check_hashes()
144 |     data, clean = path(cfg["data_dir"]), path(cfg["clean_dir"])
145 |     reference, baskets = (pd.read_parquet(data/f) for f in ("reference.parquet", "basket_summary.parquet"))
146 |     lookups = (pd.read_csv(p, keep_default_na=False) for p in
147 |                (data/"department_lookup.csv", clean/"aisles.csv", clean/"products.csv"))
148 |     tables, outliers = summarize(reference, baskets, *lookups, cfg)
149 |     output = path(cfg["outputs"]["tables"])
150 |     for name, frame in tables.items():
151 |         write_frame(output/f"{name}.csv", frame)
152 |     write_json(output/"reference_outliers.json", outliers)
153 |     print("EDA SUMMARY:", {k: len(v) for k, v in tables.items()})
154 | 
155 | 
156 | if __name__ == "__main__":
157 |     main()
```

### 20. `scripts/m2_plot_univariate.py`

> **Vai trò:** Hình phân phối kích thước giỏ (histogram + boxplot) và tập trung danh mục (Top-10 ngành + đường tích lũy).  
> **Mục trong bài:** 3.5 (Hình 3.2, 3.3) · **Người viết:** Vương  
> **Đầu vào → đầu ra:** bảng 3.4 → `figures/ban1/*.pdf|png`, `plot_data/ban1/`  
> **Hàm/lớp chính (dòng):** `main` (13)  
> **Ghi chú:** Rộng 6,3 inch = 16 cm nên chữ đúng 12 pt khi chèn.  
> *82 dòng · SHA-256 `12a3842a2c82…`*

```python
 1 | """Hai hình của Vương (mục 3.4): phân phối kích thước giỏ và mức tập trung danh mục.
 2 | 
 3 | Chạy sau m2_eda_summary.py. Dữ liệu vẽ lưu ở plot_data/ban1 để đối chiếu số trên hình.
 4 | 
 5 | ĐỌC NHANH: hai hình mục 3.4 từ các bảng đã tính. Hình 1 = phân phối kích thước giỏ (histogram + boxplot);
 6 |   Hình 2 = Top-10 ngành và đường tích lũy sản phẩm (Pareto). Dữ liệu vẽ cũng được lưu CSV để đối chiếu số trên hình.
 7 | """
 8 | import pandas as pd
 9 | 
10 | from project_io import check_hashes, config, path, plot_setup, save_figure, write_frame
11 | 
12 | 
13 | def main():
14 |     cfg = config()
15 |     check_hashes()
16 |     plt, style = plot_setup()
17 |     from matplotlib.ticker import FuncFormatter
18 |     tables, figures = path(cfg["outputs"]["tables"]), cfg["outputs"]["figures_ban1"]
19 |     sizes = pd.read_parquet(path(cfg["data_dir"])/"basket_summary.parquet").basket_size
20 |     dept = pd.read_csv(tables/"department_display.csv", keep_default_na=False)
21 |     pop = pd.read_csv(tables/"product_popularity.csv", keep_default_na=False)
22 |     top = pd.read_csv(tables/"top_n_coverage.csv")
23 |     # Bảng dữ liệu vẽ, lưu CSV để đối chiếu số trên hình.
24 |     histogram = sizes.value_counts().reindex(
25 |         range(int(sizes.min()), int(sizes.max())+1), fill_value=0
26 |     ).rename_axis("basket_size").reset_index(name="basket_count")
27 |     histogram["basket_share"] = histogram.basket_count/len(sizes)
28 |     for name, frame in {
29 |         "basket_histogram": histogram, "basket_boxplot_values": sizes.to_frame(),
30 |         "department_top10_remaining": dept,
31 |         "product_cumulative": pop[["rank", "product_id", "row_count", "cumulative_row_share"]],
32 |         "top_n_annotations": top,
33 |     }.items():
34 |         write_frame(path(cfg["outputs"]["plot_data_ban1"])/f"{name}.csv", frame)
35 | 
36 |     width, color, color2 = style["figure_width_inches"], style["colors"][0], style["colors"][1]
37 |     percent = FuncFormatter(lambda v, _: f"{100*v:.0f}%")
38 |     # Dấu chấm phân cách hàng nghìn cho khớp lời văn và Hình 3.4 (11/11).
39 |     thousands = FuncFormatter(lambda v, _: f"{int(v):,}".replace(",", "."))
40 |     n_label = f"{len(sizes):,}".replace(",", ".")
41 |     # Hình 1: (a) histogram số giỏ theo kích thước, (b) boxplot râu 1,5 x IQR, giữ mọi giỏ.
42 |     # Chiều cao rút gọn 05/11 (rộng giữ 16 cm, chữ 12 pt) để Chương 3 vừa ngân sách trang.
43 |     fig, axes = plt.subplots(2, 1, figsize=(width, 3.9), height_ratios=[2.6, 1],
44 |                              layout="constrained")
45 |     axes[0].bar(histogram.basket_size, histogram.basket_count, width=1, color=color)
46 |     axes[0].set(ylabel="Số giỏ", title=f"(a) Phân phối kích thước giỏ (N = {n_label})")
47 |     axes[0].yaxis.set_major_formatter(thousands)
48 |     axes[1].boxplot(sizes, orientation="horizontal", whis=1.5, showfliers=True,
49 |                     patch_artist=True, boxprops={"facecolor": color2},
50 |                     flierprops={"markersize": 3, "alpha": 0.4})
51 |     axes[1].set(xlabel="Số sản phẩm phân biệt/giỏ", yticks=[],
52 |                 title="(b) Boxplot: râu 1,5 × IQR; giữ mọi giỏ")
53 |     for ax in axes:
54 |         ax.set_xlim(0.5, sizes.max()+0.5)
55 |     save_figure(plt, fig, figures, "fig-ref-basket-distribution", style)
56 | 
57 |     # Hình 2: (a) Top-10 ngành và phần còn lại, (b) đường tích lũy sản phẩm kèm các mốc Top-N.
58 |     fig, axes = plt.subplots(2, 1, figsize=(width, 5.1), height_ratios=[1.25, 1],
59 |                              layout="constrained")
60 |     axes[0].barh(dept.display_name, dept.row_share, color=color, height=0.75)
61 |     axes[0].invert_yaxis()
62 |     axes[0].xaxis.set_major_formatter(percent)
63 |     axes[0].set(title="(a) Tỷ trọng dòng: Top-10 ngành và phần còn lại")
64 |     axes[1].plot(pop["rank"], pop.cumulative_row_share, color=color2, linewidth=1.7)
65 |     axes[1].scatter(top.n_actual, top.row_share, color=color, zorder=3)
66 |     annotation = "Top-N → tỷ trọng dòng\n" + "\n".join(
67 |         f"{int(r.n_requested):,}".replace(",", ".") + " → " +
68 |         f"{100*r.row_share:.2f}%".replace(".", ",") for r in top.itertuples())
69 |     axes[1].text(0.98, 0.04, annotation, transform=axes[1].transAxes, ha="right", va="bottom",
70 |                  fontsize=12, bbox={"facecolor": "white", "alpha": 0.9, "edgecolor": "none"})
71 |     axes[1].set(xlabel="Thứ hạng sản phẩm (popularity giảm dần)",
72 |                 ylabel="Tích lũy", ylim=(0, 1.02), xlim=(0, len(pop)),
73 |                 title="(b) Đường tỷ trọng dòng tích lũy")
74 |     axes[1].yaxis.set_major_formatter(percent)
75 |     axes[1].xaxis.set_major_formatter(thousands)
76 |     save_figure(plt, fig, figures, "fig-ref-category-concentration", style)
77 |     check_hashes()
78 |     print("BAN1 FIGURES: PNG 300 DPI + PDF vector")
79 | 
80 | 
81 | if __name__ == "__main__":
82 |     main()
```

### 21. `scripts/m2_eda_multivariate.py`

> **Vai trò:** Ma trận hiện diện ngành (`crosstab`), support/lift mọi cặp ngành, `pivot_table` ngày × khung giờ, tương quan Spearman/Pearson, mức nền lift; ghi `ban2/hashes.json`.  
> **Mục trong bài:** 3.5 · **Người viết:** Phong  
> **Đầu vào → đầu ra:** reference → `BAO CAO/Bao cao EDA/ban2/*.csv`  
> **Hàm/lớp chính (dòng):** `presence_table` (15), `pair_summary` (29), `lift_percentile` (47), `correlations` (52), `time_tables` (68), `main` (90)  
> **Ghi chú:** `python scripts/m2_eda_multivariate.py`  
> *141 dòng · SHA-256 `b819de2d6856…`*

```python
  1 | """Phong, mục 3.5: bảng mô tả đa biến trên reference (chạy trước hình và kiểm định 3.6).
  2 | 
  3 | Ma trận hiện diện ngành (crosstab), support/lift của mọi cặp ngành, pivot ngày × khung giờ
  4 | (pivot_table), tương quan Spearman/Pearson theo cặp đủ dữ liệu (corr), mức nền lift.
  5 | Ghi BAO CAO/Bao cao EDA/ban2/hashes.json để hình và kiểm định đọc đúng bảng này.
  6 | """
  7 | import numpy as np
  8 | import pandas as pd
  9 | 
 10 | from project_io import check_hashes, config, path, read_json, require, write_frame, write_hashes
 11 | 
 12 | OUTPUT_HASHES = "BAO CAO/Bao cao EDA/ban2/hashes.json"
 13 | 
 14 | 
 15 | def presence_table(reference, baskets, departments):
 16 |     require(not baskets.order_id.duplicated().any(), 'Duplicate baskets')
 17 |     require(set(reference.order_id) == set(baskets.order_id), 'Basket set mismatch')
 18 |     ids = sorted(departments.department_id.tolist())
 19 |     require(len(ids) == len(set(ids)), 'Duplicate department IDs')
 20 |     require(set(reference.department_id) <= set(ids), 'Unknown department')
 21 |     table = pd.crosstab(reference.order_id, reference.department_id)
 22 |     table = table.reindex(index=baskets.order_id, columns=ids, fill_value=0).gt(0)
 23 |     table.index.name = 'order_id'
 24 |     table.columns = [str(int(x)) for x in ids]
 25 |     require(table.any(axis=1).all(), 'Empty basket')
 26 |     return table
 27 | 
 28 | 
 29 | def pair_summary(presence):
 30 |     # Boolean or uint8 multiplication would not preserve counts.
 31 |     values = presence.to_numpy(dtype=np.int64)
 32 |     counts = values.T @ values
 33 |     n = len(values)
 34 |     rows = []
 35 |     for i, a in enumerate(presence.columns):
 36 |         for j, b in enumerate(presence.columns):
 37 |             na, nb, nab = int(counts[i, i]), int(counts[j, j]), int(counts[i, j])
 38 |             rows.append(dict(department_a=int(a), department_b=int(b), N=n,
 39 |                              n_A=na, n_B=nb, n_AB=nab,
 40 |                              support_AB=nab/n,
 41 |                              probability_B_given_A=nab/na if na else np.nan,
 42 |                              lift_AB=nab*n/(na*nb) if na*nb else np.nan,
 43 |                              is_diagonal=i == j))
 44 |     return pd.DataFrame(rows)
 45 | 
 46 | 
 47 | def lift_percentile(lifts, lift):
 48 |     # Phân vị thực nghiệm: % cặp có lift <= lift đang xét (tính cả chính cặp đó).
 49 |     return 100*float((lifts <= lift).mean())
 50 | 
 51 | 
 52 | def correlations(baskets, columns):
 53 |     data = baskets[columns].astype('float64')
 54 |     valid = data.notna().to_numpy(dtype=np.int64)
 55 |     n = pd.DataFrame(valid.T @ valid, index=columns, columns=columns)
 56 |     results = {}
 57 |     for method in ('spearman', 'pearson'):
 58 |         result = pd.DataFrame(np.nan, index=columns, columns=columns)
 59 |         for a in columns:
 60 |             for b in columns:
 61 |                 complete = data.loc[data[a].notna() & data[b].notna()]
 62 |                 if len(complete) >= 2 and complete[a].nunique() > 1 and complete[b].nunique() > 1:
 63 |                     result.loc[a,b] = complete[a].corr(complete[b], method=method)
 64 |         results[method] = result
 65 |     return results, n
 66 | 
 67 | 
 68 | def time_tables(baskets, cfg):
 69 |     valid = baskets.dropna(subset=['order_dow','hour_band'])
 70 |     tables = {}
 71 |     for label, agg in [('median','median'), ('count','count')]:
 72 |         table = valid.pivot_table(index='order_dow', columns='hour_band',
 73 |                                   values='basket_size', aggfunc=agg, observed=True)
 74 |         table = table.reindex(index=range(7), columns=cfg['hour_labels'])
 75 |         if label == 'count':
 76 |             table = table.fillna(0).astype('int64')
 77 |         tables[label] = table
 78 |     rows=[]
 79 |     for band in cfg['hour_labels'] + ['missing']:
 80 |         mask = baskets.hour_band.isna() if band == 'missing' else baskets.hour_band.eq(band)
 81 |         values = baskets.loc[mask, 'basket_size']
 82 |         rows.append(dict(hour_band=band, N=len(values), denominator=len(baskets),
 83 |                          share=len(values)/len(baskets), median=values.median() if len(values) else np.nan,
 84 |                          q1=values.quantile(.25, interpolation=cfg['quantile_interpolation']) if len(values) else np.nan,
 85 |                          q3=values.quantile(.75, interpolation=cfg['quantile_interpolation']) if len(values) else np.nan,
 86 |                          small_group=len(values)<cfg['min_group_n']))
 87 |     return tables, pd.DataFrame(rows)
 88 | 
 89 | 
 90 | def main():
 91 |     cfg = config()
 92 |     foundation = check_hashes()
 93 |     folder, data = path(cfg['outputs']['ban2']), path(cfg['data_dir'])
 94 |     reference, baskets = [pd.read_parquet(data/f) for f in ('reference.parquet', 'basket_summary.parquet')]
 95 |     departments = pd.read_csv(data/'department_lookup.csv')
 96 |     require(len(baskets) == foundation['counts']['reference_baskets'], 'N mismatch')
 97 |     require(len(departments) == 21, 'Expected 21 departments')
 98 |     presence = presence_table(reference, baskets, departments)
 99 |     require(np.array_equal(presence.sum(axis=1).to_numpy(), baskets.n_departments.to_numpy()),
100 |             'Department counts differ')
101 |     pairs = pair_summary(presence)
102 |     hypotheses = read_json(path(cfg['hypotheses_config']))
103 |     for pair in hypotheses['pairs']:   # đối chiếu độc lập bằng crosstab 2×2
104 |         a, b = pair['a'], pair['b']
105 |         tab = pd.crosstab(presence[str(a)], presence[str(b)]).reindex(
106 |             index=[False, True], columns=[False, True], fill_value=0)
107 |         row = pairs.loc[(pairs.department_a == a) & (pairs.department_b == b)].iloc[0]
108 |         require(int(tab.loc[True, True]) == row.n_AB and tab.to_numpy().sum() == len(baskets),
109 |                 'Independent crosstab mismatch')
110 |     time, hours = time_tables(baskets, cfg)
111 |     corr, pair_n = correlations(baskets, cfg['correlation_columns'])
112 |     # Mức nền: vị trí lift của 3 cặp đã khóa giữa 210 cặp ngành khác nhau (I5 và 3.6).
113 |     off = pairs.loc[pairs.department_a < pairs.department_b].dropna(subset=['lift_AB'])
114 |     base = []
115 |     for pair in hypotheses['pairs']:
116 |         lift = float(off.loc[(off.department_a == pair['a']) & (off.department_b == pair['b']), 'lift_AB'].iloc[0])
117 |         base.append(dict(hypothesis_id=pair['id'], lift_AB=lift,
118 |                          percentile_among_pairs=lift_percentile(off.lift_AB, lift)))
119 |     tables = {f'time_pivot_{k}.csv': v.reset_index() for k, v in time.items()}
120 |     tables['time_pivot_small_group.csv'] = (time['count'] < cfg['min_group_n']).reset_index()
121 |     tables['hour_band_summary.csv'] = hours
122 |     for key, frame in corr.items():
123 |         tables[f'correlation_{key}.csv'] = frame.rename_axis('variable').reset_index()
124 |     tables['correlation_pair_n.csv'] = pair_n.rename_axis('variable').reset_index()
125 |     tables['department_pair_summary.csv'] = pairs
126 |     tables['lift_baseline.csv'] = pd.DataFrame(base).assign(
127 |         n_pairs=len(off), n_pairs_lift_gt_1=int((off.lift_AB > 1).sum()),
128 |         median_lift=float(off.lift_AB.median()))
129 |     outputs = []
130 |     for name, frame in tables.items():
131 |         write_frame(folder/name, frame)
132 |         outputs.append(folder/name)
133 |     write_frame(data/'department_presence.parquet', presence.reset_index())
134 |     outputs.append(data/'department_presence.parquet')
135 |     check_hashes()
136 |     write_hashes(OUTPUT_HASHES, outputs, N_baskets=len(baskets), N_rows=len(reference))
137 |     print(folder)
138 | 
139 | 
140 | if __name__ == '__main__':
141 |     main()
```

### 22. `scripts/m2_plot_multivariate.py`

> **Vai trò:** Hình tần số giờ/ngày, kích thước giỏ theo thời gian, heatmap Spearman, heatmap lift 21 ngành.  
> **Mục trong bài:** 3.5 (Hình 3.4–3.7) · **Người viết:** Phong  
> **Đầu vào → đầu ra:** bảng ban2 → `figures/ban2/*.pdf|png`, `plot_data/ban2/`  
> **Hàm/lớp chính (dòng):** `main` (19)  
> *111 dòng · SHA-256 `b909d5218626…`*

```python
  1 | """Phong, mục 3.5: hình thời gian, tương quan Spearman/Pearson và lift đồng mua 21 ngành.
  2 | 
  3 | Chạy sau m2_eda_multivariate.py. Bảng dùng để vẽ được sao vào plot_data/ban2.
  4 | """
  5 | import shutil
  6 | 
  7 | import numpy as np
  8 | import pandas as pd
  9 | 
 10 | from m2_eda_multivariate import OUTPUT_HASHES
 11 | from project_io import check_hashes, config, path, plot_setup, save_figure, write_frame
 12 | 
 13 | # Tên file ASCII, không dấu cách/ngoặc để render_pdf.py đọc đúng đường dẫn hình.
 14 | COPIED = ['time_pivot_median.csv', 'time_pivot_count.csv', 'hour_band_summary.csv',
 15 |           'correlation_spearman.csv', 'correlation_pearson.csv', 'correlation_pair_n.csv',
 16 |           'department_pair_summary.csv']
 17 | 
 18 | 
 19 | def main():
 20 |     cfg = config()
 21 |     check_hashes()
 22 |     check_hashes(OUTPUT_HASHES)
 23 |     plt, style = plot_setup()
 24 |     import seaborn as sns
 25 |     from matplotlib.ticker import FuncFormatter, ScalarFormatter
 26 | 
 27 |     class Comma(ScalarFormatter):
 28 |         """Nhãn trục số dùng dấu phẩy thập phân cho khớp lời văn (07/11)."""
 29 |         def __call__(self, x, pos=None):
 30 |             return super().__call__(x, pos).replace('.', ',')
 31 | 
 32 |     def comma(value, spec):
 33 |         return format(value, spec).replace('.', ',')
 34 | 
 35 |     folder, figures = path(cfg['outputs']['ban2']), cfg['outputs']['figures_ban2']
 36 |     plotdata = path(cfg['outputs']['plot_data_ban2'])
 37 |     plotdata.mkdir(parents=True, exist_ok=True)
 38 | 
 39 |     def save(fig, stem):
 40 |         for artist in fig.findobj():   # giữ mọi phần tử dạng vector trong PDF, kể cả colorbar
 41 |             artist.set_rasterized(False)
 42 |         save_figure(plt, fig, figures, stem, style)
 43 | 
 44 |     baskets = pd.read_parquet(path(cfg['data_dir'])/'basket_summary.parquet')
 45 |     n = len(baskets)
 46 |     # Chiều cao rút gọn 05/11 (rộng 6,3 in = 16 cm, chữ 12 pt); số N đầy đủ nằm ở chú thích hình.
 47 |     thousands = FuncFormatter(lambda v, _: f'{int(v):,}'.replace(',', '.'))
 48 |     fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.6), width_ratios=[2.2, 1], layout='constrained')
 49 |     for ax, column, values, label in [(axes[0], 'order_hour_of_day', range(24), 'Giờ đặt đơn'),
 50 |                                       (axes[1], 'order_dow', range(7), 'Mã ngày (0–6)')]:
 51 |         counts = baskets[column].value_counts().reindex(values, fill_value=0).sort_index()
 52 |         ax.bar(counts.index, counts.values, color=style['colors'][0])
 53 |         ax.set_xlabel(label)
 54 |         ax.set_xticks(list(values)[::4] if column == 'order_hour_of_day' else list(values)[::2])
 55 |         ax.yaxis.set_major_formatter(thousands)
 56 |         counts.rename('N').rename_axis(column).to_csv(plotdata/(column+'_frequency.csv'))
 57 |     axes[0].set_ylabel('Số giỏ')
 58 |     save(fig, 'fig-ref-time-frequency')
 59 | 
 60 |     fig, axes = plt.subplots(1, 2, figsize=(6.3, 3.9), width_ratios=[1, 1.15], layout='constrained')
 61 |     median = pd.read_csv(folder/'time_pivot_median.csv', index_col=0)
 62 |     counts = pd.read_csv(folder/'time_pivot_count.csv', index_col=0)
 63 |     labels = median.map(lambda x: '' if pd.isna(x) else comma(x, 'g')).astype(str)
 64 |     labels = labels.where(counts >= cfg['min_group_n'], labels+'*')
 65 |     sns.heatmap(median, annot=labels, fmt='', cmap='YlGnBu', mask=median.isna(), ax=axes[0],
 66 |                 cbar=False)
 67 |     axes[0].set(title='(a) Median', xlabel='Khung giờ', ylabel='Mã ngày')
 68 |     axes[0].tick_params(axis='x', rotation=90)
 69 |     axes[0].tick_params(axis='y', rotation=0)
 70 |     groups = [baskets.loc[baskets.hour_band.eq(b), 'basket_size'].to_numpy() for b in cfg['hour_labels']]
 71 |     axes[1].boxplot(groups, tick_labels=cfg['hour_labels'], showfliers=True,
 72 |                     flierprops={'markersize': 2})
 73 |     axes[1].set(ylabel='Số sản phẩm/giỏ', xlabel='Khung giờ', title='(b) Kích thước giỏ')
 74 |     axes[1].tick_params(axis='x', rotation=90)
 75 |     save(fig, 'fig-ref-time-basket-size')
 76 | 
 77 |     names = ['Số sản phẩm', 'Số ngành', 'Số quầy', 'Khoảng cách đơn']
 78 |     for method in ['spearman', 'pearson']:
 79 |         corr = pd.read_csv(folder/f'correlation_{method}.csv', index_col=0)
 80 |         fig, ax = plt.subplots(figsize=(6.3, 3.3), layout='constrained')
 81 |         sns.heatmap(corr, vmin=-1, vmax=1, cmap='vlag', annot=corr.map(lambda v: comma(v, '.3f')),
 82 |                     fmt='', xticklabels=names, yticklabels=names, ax=ax,
 83 |                     cbar_kws={'label': method.title()})
 84 |         ax.collections[0].colorbar.ax.yaxis.set_major_formatter(Comma())
 85 |         ax.tick_params(axis='both', rotation=0)
 86 |         ax.set(xlabel='', ylabel='')
 87 |         save(fig, f'fig-ref-corr-{method}')
 88 | 
 89 |     pairs = pd.read_csv(folder/'department_pair_summary.csv')
 90 |     lift = pairs.pivot(index='department_a', columns='department_b',
 91 |                        values='lift_AB').sort_index().sort_index(axis=1)
 92 |     names = pd.read_csv(path(cfg['data_dir'])/'department_lookup.csv').set_index('department_id').department
 93 |     fig, ax = plt.subplots(figsize=(6.3, 5.0), layout='constrained')
 94 |     sns.heatmap(lift, mask=np.eye(len(lift), dtype=bool) | lift.isna().to_numpy(), cmap='YlGnBu',
 95 |                 vmin=0, ax=ax, cbar_kws={'label': 'Lift'}, xticklabels=list(lift.columns),
 96 |                 yticklabels=[f'{i} {names[i]}' for i in lift.index])
 97 |     ax.collections[0].colorbar.ax.yaxis.set_major_formatter(Comma())
 98 |     ax.set(xlabel='ID ngành B', ylabel='')
 99 |     ax.tick_params(axis='both', rotation=0)
100 |     save(fig, 'fig-ref-department-lift')
101 | 
102 |     write_frame(plotdata/'department_labels.csv',
103 |                 pd.read_csv(path(cfg['data_dir'])/'department_lookup.csv'))
104 |     for name in COPIED:
105 |         shutil.copy2(folder/name, plotdata/name)
106 |     check_hashes(OUTPUT_HASHES)
107 |     print('BAN2 FIGURES: PNG 300 DPI + PDF vector')
108 | 
109 | 
110 | if __name__ == '__main__':
111 |     main()
```

### 23. `scripts/m2_hypothesis_tests.py`

> **Vai trò:** Chi-square không Yates (Fisher nếu bảng thưa), Holm tự viết cho họ ba kiểm định, Cramér's V.  
> **Mục trong bài:** 3.6 (Bảng 3.10) · **Người viết:** Phong  
> **Đầu vào → đầu ra:** reference, `hypotheses_config.json` → `ban2/hypotheses.csv`, `hypotheses_details.json`  
> **Hàm/lớp chính (dòng):** `holm` (15), `test_table` (23), `main` (47)  
> **Ghi chú:** `python scripts/m2_hypothesis_tests.py`  
> *79 dòng · SHA-256 `ad0935a9d4c5…`*

```python
 1 | """Phong, mục 3.6: kiểm định ba cặp ngành đã khóa trong configs/hypotheses_config.json.
 2 | 
 3 | Pearson Chi-square không Yates khi mọi tần số kỳ vọng >= 5, Fisher hai phía khi bảng thưa,
 4 | biến hằng là not_testable (p=1 chỉ dùng nội bộ cho Holm). Holm tự viết cho họ 3 cặp;
 5 | Cramér's V từ chi-square không Yates. Đầu vào là reference, mỗi giỏ một người.
 6 | """
 7 | import numpy as np
 8 | import pandas as pd
 9 | from scipy.stats import chi2_contingency, fisher_exact
10 | 
11 | from m2_eda_multivariate import OUTPUT_HASHES
12 | from project_io import check_hashes, config, path, read_json, require, write_frame, write_json
13 | 
14 | 
15 | def holm(values):
16 |     values=np.asarray(values,dtype=float)
17 |     order=np.argsort(values,kind='stable')
18 |     adjusted=np.minimum(1,np.maximum.accumulate(values[order]*np.arange(len(values),0,-1)))
19 |     result=np.empty(len(values));result[order]=adjusted
20 |     return result
21 | 
22 | 
23 | def test_table(table, cfg):
24 |     t=np.asarray(table)
25 |     require(t.shape==(2,2) and np.isfinite(t).all() and (t>=0).all() and (t==np.floor(t)).all(),'Invalid counts')
26 |     n=int(t.sum());require(n>0,'Empty table')
27 |     n00,n01,n10,n11=map(int,t.ravel())
28 |     result=dict(N=n,n00=n00,n01=n01,n10=n10,n11=n11,method='not_testable',
29 |                 p_raw=np.nan,chi2_pearson=np.nan,df=np.nan,fisher_odds_ratio=np.nan,
30 |                 cramers_v=np.nan,expected_min=np.nan,conditional_p1=n11/(n10+n11) if n10+n11 else np.nan,
31 |                 conditional_p0=n01/(n00+n01) if n00+n01 else np.nan,
32 |                 support_AB=n11/n,lift_AB=n11*n/((n10+n11)*(n01+n11)) if (n10+n11)*(n01+n11) else np.nan)
33 |     expected=np.outer(t.sum(axis=1),t.sum(axis=0))/n
34 |     result['difference_pp']=100*(result['conditional_p1']-result['conditional_p0'])
35 |     result['expected_min']=float(expected.min())
36 |     if (expected==0).any():return result,expected
37 |     chi,p,df,_=chi2_contingency(t,correction=cfg['chi_square_correction'])
38 |     result.update(chi2_pearson=float(chi),cramers_v=float(np.sqrt(chi/n)))
39 |     if expected.min()>=cfg['minimum_expected']:
40 |         result.update(method='chi_square',p_raw=float(p),df=int(df))
41 |     else:
42 |         odds,p=fisher_exact(t,alternative=cfg['fisher_alternative'])
43 |         result.update(method='fisher',p_raw=float(p),fisher_odds_ratio=float(odds))
44 |     return result,expected
45 | 
46 | 
47 | def main():
48 |     cfg=config()
49 |     foundation=check_hashes()
50 |     check_hashes(OUTPUT_HASHES)
51 |     folder=path(cfg['outputs']['ban2'])
52 |     h=read_json(path(cfg['hypotheses_config']))
53 |     require(h['adjustment']=='holm' and h['family_size']==3 and
54 |             h['chi_square_correction'] is False and h['fisher_alternative']=='two-sided',
55 |             'Unsupported locked testing contract')
56 |     presence=pd.read_parquet(path(cfg['data_dir'])/'department_presence.parquet').set_index('order_id')
57 |     lookup=pd.read_csv(path(cfg['data_dir'])/'department_lookup.csv').set_index('department_id')
58 |     pairs=pd.read_csv(folder/'department_pair_summary.csv')
59 |     rows=[];details=[]
60 |     for spec in h['pairs']:
61 |         a,b=spec['a'],spec['b']
62 |         require(lookup.loc[a,'department']==spec['a_name'] and lookup.loc[b,'department']==spec['b_name'],'ID/name mismatch')
63 |         table=pd.crosstab(presence[str(a)],presence[str(b)]).reindex(index=[False,True],columns=[False,True],fill_value=0)
64 |         row,expected=test_table(table.to_numpy(),h)
65 |         require(row['N']==foundation['counts']['reference_baskets'],'Wrong N')
66 |         require(row['n11']==int(pairs.query('department_a==@a and department_b==@b').iloc[0].n_AB),'Cooccurrence mismatch')
67 |         row.update(hypothesis_id=spec['id'],department_A=a,department_B=b,pair=spec['a_name']+' / '+spec['b_name'])
68 |         rows.append(row);details.append({'id':spec['id'],'observed':table.to_numpy().tolist(),'expected':expected.tolist()})
69 |     require(len(rows)==h['family_size']==3,'Wrong family')
70 |     adjusted=holm([r['p_raw'] if r['method']!='not_testable' else 1 for r in rows])
71 |     for row,p in zip(rows,adjusted):
72 |         ok=row['method']!='not_testable'
73 |         row.update(p_holm=float(p) if ok else np.nan,status='tested' if ok else 'not_testable',reject_H0=bool(p<h['alpha']) if ok else None)
74 |     write_frame(folder/'hypotheses.csv',pd.DataFrame(rows))
75 |     write_json(folder/'hypotheses_details.json',{'config':h,'tables':details,'warnings':['Zero machine p-values must be displayed as below numerical precision, never p=0.','Association is unadjusted for basket size; not causal; not externally preregistered.']})
76 |     print(pd.DataFrame(rows)[['hypothesis_id','method','p_raw','p_holm','cramers_v','difference_pp']].to_string(index=False))
77 | 
78 | 
79 | if __name__=='__main__':main()
```

## Phần 5. Mô hình hóa và đánh giá (Chương 4)

### 24. `configs/m4_model.json`

> **Vai trò:** Seed (che 42, mẫu âm 43, importance 44, bootstrap 42), lưới A (luật) và B (LR, RF), dung sai 0,002, 20 mẫu âm.  
> **Mục trong bài:** 4.1–4.4 · **Người viết:** Vương · **Tệp trong khóa thực nghiệm**  
> **Đầu vào → đầu ra:** —  
> **Ghi chú:** Tệp trong khóa thực nghiệm. Demo đổi tham số chỉ làm trên bản sao của thư mục bài.  
> *17 dòng · SHA-256 `1350c3ebc27b…`*

```json
 1 | {
 2 |   "data_dir": "DATA/Data phai sinh/M4",
 3 |   "report_dir": "BAO CAO/Bao cao mo hinh",
 4 |   "seeds": {"mask": 42, "negative": 43, "importance": 44, "bootstrap": 42},
 5 |   "hidden_share": 0.2,
 6 |   "k_values": [5, 10],
 7 |   "grid_A": {"top_n": [500, 1000, 2000], "min_count": [20, 50],
 8 |              "min_confidence": [0.05, 0.10], "max_len": [2, 3]},
 9 |   "grid_B": {"lr_C": [0.01, 0.1, 1, 10],
10 |              "rf_max_depth": [10, 20], "rf_min_samples_leaf": [20, 100], "rf_n_estimators": 300},
11 |   "tie_tolerance": 0.002,
12 |   "negatives_per_basket": 20,
13 |   "batch_size": 2000,
14 |   "pilot_baskets": 2000,
15 |   "bootstrap_n": 2000,
16 |   "benchmark": {"runs": 3, "timeout_s": 900, "trial": {"top_n": 500, "min_count": 50, "max_len": 2}}
17 | }
```

### 25. `scripts/m4_common.py`

> **Vai trò:** Nền Chương 4: phép che h = min(k−1, max(1, ⌊0,2k⌋)), danh mục C, ma trận giỏ, khai phá Apriori/FP-Growth, luật, 7 đặc trưng ứng viên, mẫu âm, Recall@K/Precision@K, `locked_stage`.  
> **Mục trong bài:** 4.1–4.4 · **Người viết:** Vương · **Tệp trong khóa thực nghiệm**  
> **Đầu vào → đầu ra:** Master, reference → hàm dùng chung  
> **Hàm/lớp chính (dòng):** `config` (27), `mask_params` (31), `check_mask` (35), `baskets` (41), `mask` (53), `catalog` (65), `basket_matrix` (79), `mine` (91), `rules` (99), `itemset_signature` (114), `max_support_gap` (120), `worst_support_gap` (125), `context` (135), `index_rules` (144), `basket_features` (155), `make_batches` (185), `sample_negatives` (197), `evaluate` (208), `locked_stage` (227)  
> **Ghi chú:** Mọi thống kê học từ reference; giỏ fit/validation/test chỉ được che.  
> *242 dòng · SHA-256 `bed59411f67f…`*

```python
  1 | """Hàm dùng chung Chương 4 (phần Vương): giỏ, phép che, danh mục C, khai phá luật.
  2 | 
  3 | Mọi thống kê học từ reference; giỏ fit/validation/test chỉ được che, không dùng để học luật.
  4 | 
  5 | ĐỌC NHANH (vấn đáp). File này là NỀN của Chương 4, sáu nhóm theo thứ tự dùng:
  6 |   1. Giỏ và phép che: baskets, mask (che h = min(k-1, max(1, floor(0,2k))) sản phẩm, seed + order_id).
  7 |   2. Danh mục C và luật: catalog (xếp sản phẩm theo độ phổ biến), basket_matrix, mine (Apriori/FP-Growth), rules.
  8 |   3. So sánh Apriori và FP-Growth: cùng tập itemset, support lệch <= 1e-12.
  9 |   4. Đặc trưng ứng viên: index_rules + basket_features (tra luật bằng tìm kiếm nhị phân, ứng viên không khớp luật = 0).
 10 |   5. Chấm điểm: make_batches (lô giỏ), sample_negatives (20 mẫu âm/giỏ), evaluate (P@k, R@k, HR@10, trần Recall@10).
 11 |   6. locked_stage: nạp lại cấu hình giai đoạn A đã chọn, CHỈ fit/validation, test không được nạp.
 12 |   Ba ý quan trọng: hàm đặc trưng chỉ dùng phần quan sát O, không dùng phần bị che H; ứng viên = C trừ O;
 13 |   mọi phương pháp xếp hạng cùng một quy tắc hòa (product_id tăng).
 14 | """
 15 | import numpy as np
 16 | import pandas as pd
 17 | from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
 18 | from scipy import sparse
 19 | 
 20 | from project_io import check_hashes, path, read_json, require
 21 | 
 22 | # Đường dẫn cấu hình và tệp hash của Chương 4.
 23 | CONFIG = "configs/m4_model.json"
 24 | HASHES = "DATA/Data phai sinh/M4/hashes.json"
 25 | 
 26 | 
 27 | def config():
 28 |     return read_json(path(CONFIG))
 29 | 
 30 | 
 31 | def mask_params(cfg):
 32 |     return {"seed": cfg["seeds"]["mask"], "hidden_share": cfg["hidden_share"]}
 33 | 
 34 | 
 35 | def check_mask(record, cfg):
 36 |     """Dừng nếu phép che đã lưu không được tạo từ tham số che trong config hiện tại."""
 37 |     require(record.get("mask") == mask_params(cfg), "Phép che đã lưu khác config; chạy lại m4_prepare.py")
 38 | 
 39 | 
 40 | # ===== Nhóm 1: dựng giỏ và phép che =====
 41 | def baskets(master, split, splits):
 42 |     """Một dòng mỗi giỏ của các tập `splits`; `items` là danh sách product_id tăng dần."""
 43 |     users = split.loc[split.split.isin(splits)].set_index("user_id").split
 44 |     rows = master.loc[master.user_id.isin(users.index), ["order_id", "user_id", "product_id"]]
 45 |     out = (rows.sort_values(["order_id", "product_id"])
 46 |            .groupby("order_id", sort=True).agg(user_id=("user_id", "first"),
 47 |                                                items=("product_id", list)).reset_index())
 48 |     out["split"] = out.user_id.map(users).astype(str)
 49 |     require(not out.user_id.duplicated().any(), "Mỗi người dùng phải có đúng một giỏ")
 50 |     return out
 51 | 
 52 | 
 53 | def mask(items, order_id, seed=42, share=0.2):
 54 |     """Che h = min(k-1, max(1, floor(share*k))) sản phẩm; giỏ k < 2 không che (Chương 2)."""
 55 |     k = len(items)
 56 |     if k < 2:
 57 |         return list(items), []
 58 |     h = min(k - 1, max(1, int(np.floor(share * k))))
 59 |     hidden = np.random.default_rng([seed, order_id]).choice(np.asarray(items), h, replace=False)
 60 |     hidden = sorted(int(x) for x in hidden)
 61 |     return [int(x) for x in items if x not in hidden], hidden
 62 | 
 63 | 
 64 | # ===== Nhóm 2: danh mục C và khai phá luật (chỉ học trên reference) =====
 65 | def catalog(reference):
 66 |     """Mọi sản phẩm của reference, xếp theo số giỏ chứa giảm dần, phá hòa product_id tăng.
 67 | 
 68 |     Danh mục C với Top-N là các dòng rank <= N. Mẫu số popularity là toàn bộ giỏ reference.
 69 |     """
 70 |     n_baskets = reference.order_id.nunique()
 71 |     out = (reference.groupby("product_id").agg(n_ref=("order_id", "nunique"),
 72 |                                                department_id=("department_id", "first"))
 73 |            .reset_index().sort_values(["n_ref", "product_id"], ascending=[False, True]))
 74 |     out["popularity"] = out.n_ref / n_baskets
 75 |     out["rank"] = np.arange(1, len(out) + 1)
 76 |     return out.reset_index(drop=True)
 77 | 
 78 | 
 79 | def basket_matrix(reference, products):
 80 |     """Ma trận Boolean thưa: hàng = mọi giỏ reference (kể cả giỏ không có sản phẩm nào của C)."""
 81 |     rows, order_ids = pd.factorize(reference.order_id, sort=True)
 82 |     column = pd.Index(products)
 83 |     keep = column.get_indexer(reference.product_id) >= 0
 84 |     data = sparse.csr_matrix((np.ones(keep.sum(), dtype=bool),
 85 |                               (rows[keep], column.get_indexer(reference.product_id[keep]))),
 86 |                              shape=(len(order_ids), len(column)))
 87 |     # mlxtend yêu cầu tên cột chuỗi với DataFrame thưa; kết quả đổi lại về int.
 88 |     return pd.DataFrame.sparse.from_spmatrix(data, columns=[str(int(p)) for p in products])
 89 | 
 90 | 
 91 | def mine(matrix, algorithm, min_count, max_len):
 92 |     """Itemset phổ biến với support >= min_count/N; cùng đầu vào cho Apriori và FP-Growth."""
 93 |     support = min_count / len(matrix)
 94 |     if algorithm == "apriori":  # mặc định cần ~14 GB RAM ở N=500 (lượt thử 01/11); low_memory cho cùng kết quả
 95 |         return apriori(matrix, min_support=support, use_colnames=True, max_len=max_len, low_memory=True)
 96 |     return fpgrowth(matrix, min_support=support, use_colnames=True, max_len=max_len)
 97 | 
 98 | 
 99 | def rules(itemsets, n_baskets, min_confidence):
100 |     """Luật hậu đề một sản phẩm, kèm số giỏ đếm được để báo cùng tỷ lệ."""
101 |     found = association_rules(itemsets, num_itemsets=n_baskets, metric="confidence",
102 |                               min_threshold=min_confidence)
103 |     found = found.loc[found.consequents.map(len) == 1]
104 |     out = pd.DataFrame({
105 |         "antecedent": found.antecedents.map(lambda s: sorted(int(x) for x in s)),
106 |         "consequent": found.consequents.map(lambda s: int(next(iter(s)))),
107 |         "n_antecedent": (found["antecedent support"] * n_baskets).round().astype(int),
108 |         "n_both": (found.support * n_baskets).round().astype(int),
109 |         **{c: found[c] for c in ["support", "confidence", "lift", "leverage", "conviction"]}})
110 |     return out.sort_values(["consequent", "confidence"], ascending=[True, False]).reset_index(drop=True)
111 | 
112 | 
113 | # ===== Nhóm 3: so sánh Apriori và FP-Growth =====
114 | def itemset_signature(itemsets):
115 |     """{itemset đã sắp: support chưa làm tròn} để so Apriori và FP-Growth."""
116 |     return {tuple(sorted(int(x) for x in s)): float(v)
117 |             for s, v in zip(itemsets.itemsets, itemsets.support)}
118 | 
119 | 
120 | def max_support_gap(a, b):
121 |     """Sai số support lớn nhất giữa hai kết quả; None nếu tập itemset khác nhau."""
122 |     return max((abs(a[k] - b[k]) for k in a), default=0.0) if a.keys() == b.keys() else None
123 | 
124 | 
125 | def worst_support_gap(runs):
126 |     """Sai số lớn nhất của mọi lượt so với lượt đầu; None nếu rỗng hoặc có lượt khác tập itemset."""
127 |     gaps = [max_support_gap(runs[0], r) for r in runs] if runs else [None]
128 |     return None if None in gaps else max(gaps)
129 | 
130 | 
131 | # ===== Nhóm 4: đặc trưng ứng viên (khớp luật bằng tìm kiếm nhị phân) =====
132 | M = 1 << 16  # product_id < 65.536: khóa luật = đầu tiên * M + thứ hai (0 nếu chỉ một sản phẩm)
133 | 
134 | 
135 | def context(ranked, n, dept):
136 |     """C = Top-n của danh mục theo thứ tự xếp hạng; pos[product_id] là vị trí trong C (-1 nếu ngoài C)."""
137 |     top = ranked[ranked["rank"] <= n]
138 |     pos = np.full(M, -1)
139 |     pos[top.product_id] = np.arange(len(top))
140 |     return {"pid": top.product_id.to_numpy(), "pop": top.popularity.to_numpy(),
141 |             "dept": top.department_id.to_numpy(), "pos": pos, "all_dept": dept}
142 | 
143 | 
144 | def index_rules(found, ctx):
145 |     """Chỉ mục luật theo tiền đề: các luật cùng tiền đề nằm liền nhau trong cons/conf/lift."""
146 |     key = found.antecedent.map(lambda s: s[0] * M + (s[1] if len(s) > 1 else 0)).to_numpy()
147 |     order = np.argsort(key, kind="stable")
148 |     unique, start = np.unique(key[order], return_index=True)
149 |     return {"uk": unique, "start": start, "end": np.append(start[1:], len(key)),
150 |             "pairs": bool((found.antecedent.map(len) > 1).any()),
151 |             "cons": ctx["pos"][found.consequent.to_numpy()][order],
152 |             "conf": found.confidence.to_numpy()[order], "lift": found.lift.to_numpy()[order]}
153 | 
154 | 
155 | def basket_features(observed, ctx, idx):
156 |     """Bảy đặc trưng của mọi ứng viên trong C trừ O theo thứ tự danh mục; chỉ dùng O, không dùng H."""
157 |     obs = np.asarray(observed, dtype=np.int64)
158 |     # Bước 1: sản phẩm quan sát nằm trong C; khóa tiền đề một sản phẩm = a*M, cặp = a*M + b.
159 |     inside = obs[ctx["pos"][obs] >= 0]
160 |     keys = inside * M
161 |     if idx["pairs"] and len(inside) > 1:
162 |         i, j = np.triu_indices(len(inside), 1)
163 |         keys = np.append(keys, inside[i] * M + inside[j])
164 |     # Bước 2: tra khóa tiền đề trong chỉ mục luật bằng tìm kiếm nhị phân.
165 |     loc = np.searchsorted(idx["uk"], keys).clip(max=len(idx["uk"]) - 1)
166 |     loc = loc[idx["uk"][loc] == keys]
167 |     rows = np.concatenate([np.arange(idx["start"][k], idx["end"][k]) for k in loc] or [np.empty(0, int)])
168 |     # Bước 3: mỗi ứng viên: đếm số luật khớp, lấy confidence và lift LỚN NHẤT; không khớp luật nào thì bằng 0 (không để thiếu).
169 |     n, cons = len(ctx["pid"]), idx["cons"][rows]
170 |     count, conf, lift = np.bincount(cons, minlength=n).astype(float), np.zeros(n), np.zeros(n)
171 |     np.maximum.at(conf, cons, idx["conf"][rows])
172 |     np.maximum.at(lift, cons, idx["lift"][rows])
173 |     # Bước 4: loại sản phẩm đã có trong giỏ khỏi ứng viên (C trừ O).
174 |     keep = np.ones(n, bool)
175 |     keep[ctx["pos"][inside]] = False
176 |     same = np.bincount(ctx["all_dept"][obs], minlength=22)[ctx["dept"]]
177 |     features = {"product_id": ctx["pid"], "candidate_popularity": ctx["pop"], "matching_rule_count": count,
178 |                 "max_rule_confidence": conf, "max_rule_lift": lift,
179 |                 "observed_basket_size": np.full(n, float(len(obs))), "same_department_count": same.astype(float),
180 |                 "candidate_department_id": ctx["dept"].astype(float)}
181 |     return {name: value[keep] for name, value in features.items()}
182 | 
183 | 
184 | # ===== Nhóm 5: chấm điểm xếp hạng =====
185 | def make_batches(frame, ctx, idx, size):
186 |     """Sinh (giỏ, bảng ứng viên) theo lô; X có đặc trưng, `basket` (chỉ số trong lô) và nhãn `y` (thuộc H)."""
187 |     for start in range(0, len(frame), size):
188 |         part = frame.iloc[start:start + size].reset_index(drop=True)
189 |         feats = [basket_features(o, ctx, idx) for o in part.observed]
190 |         X = pd.DataFrame({c: np.concatenate([f[c] for f in feats]) for c in feats[0]})
191 |         X["basket"] = np.repeat(np.arange(len(part)), [len(f["product_id"]) for f in feats])
192 |         hidden = np.concatenate([b * M + np.asarray(h, dtype=np.int64) for b, h in enumerate(part.hidden)])
193 |         X["y"] = np.isin(X.basket.to_numpy() * M + X.product_id.to_numpy(), hidden)
194 |         yield part, X
195 | 
196 | 
197 | def sample_negatives(part, X, n, seed):
198 |     """Giữ mọi dòng dương và tối đa n dòng âm mỗi giỏ (RNG riêng theo order_id, không hoàn lại)."""
199 |     y, edges = X.y.to_numpy(), np.searchsorted(X.basket.to_numpy(), np.arange(len(part) + 1))
200 |     keep = [np.flatnonzero(y)]
201 |     for b, order_id in enumerate(part.order_id):
202 |         negative = np.flatnonzero(~y[edges[b]:edges[b + 1]]) + edges[b]
203 |         keep.append(np.random.default_rng([seed, order_id]).choice(negative, min(n, len(negative)), replace=False))
204 |     out = X.iloc[np.sort(np.concatenate(keep))]
205 |     return out.assign(order_id=part.order_id.to_numpy()[out.basket.to_numpy()])
206 | 
207 | 
208 | def evaluate(part, X, *keys, ks=(5, 10)):
209 |     """Chỉ số theo giỏ của một phương pháp; `keys` là các khóa giảm dần theo thứ tự ưu tiên, hòa thì product_id tăng."""
210 |     # Xếp hạng trong từng giỏ theo các khóa giảm dần; hòa thì product_id tăng.
211 |     order = np.lexsort((X.product_id.to_numpy(), *[-np.asarray(k, float) for k in keys[::-1]], X.basket.to_numpy()))
212 |     basket, hit = X.basket.to_numpy()[order], X.y.to_numpy()[order]
213 |     place = np.arange(len(order)) - np.searchsorted(basket, basket)
214 |     n, h = len(part), part.hidden.map(len).to_numpy()
215 |     out = part[["order_id", "user_id"]].copy()
216 |     out["n_hidden"], out["n_hidden_in_C"] = h, np.bincount(X.basket.to_numpy()[X.y.to_numpy()], minlength=n)
217 |     # P@k = trúng/k; R@k = trúng/|H| (|H| gồm cả sản phẩm ngoài C); trần Recall@10 = min(|H giao C|, 10)/|H|.
218 |     for k in ks:
219 |         hits = np.bincount(basket[hit & (place < k)], minlength=n)
220 |         out[f"hits@{k}"], out[f"P@{k}"], out[f"R@{k}"] = hits, hits / k, hits / h
221 |     out[f"HR@{ks[-1]}"] = (out[f"hits@{ks[-1]}"] > 0).astype(float)
222 |     out[f"R@{ks[-1]}_ceiling"] = np.minimum(out.n_hidden_in_C, ks[-1]) / h
223 |     return out
224 | 
225 | 
226 | # ===== Nhóm 6: nạp lại cấu hình giai đoạn A đã chọn (test KHÔNG được nạp) =====
227 | def locked_stage(cfg, splits=("fit", "validation")):
228 |     """Giỏ của các tập `splits` (mặc định fit/validation, test không được nạp), ngữ cảnh và chỉ mục luật của cấu hình A đã chọn.
229 | 
230 |     Chỉ bước chấm test sau khóa (m4_test.py) được truyền splits=("test",)."""
231 |     record = check_hashes(HASHES)
232 |     check_mask(record, cfg)
233 |     data, a = path(cfg["data_dir"]), record["stage_A"]
234 |     masked = pd.read_parquet(data / "masked_baskets.parquet", filters=[("split", "in", list(splits))])
235 |     found = pd.read_parquet(data / "rules_grid.parquet")
236 |     found = found[(found.top_n == a["top_n"]) & (found.min_count == a["min_count"]) & (found.max_len == a["max_len"])
237 |                   & (found.confidence >= a["min_confidence"])]
238 |     master = pd.read_parquet(path("DATA/Data đã làm sạch/master_train.parquet"), columns=["product_id", "department_id"])
239 |     dept = np.zeros(M, dtype=int)
240 |     dept[master.product_id.to_numpy()] = master.department_id.to_numpy()
241 |     ctx = context(pd.read_parquet(data / "catalog.parquet"), a["top_n"], dept)
242 |     return masked, ctx, index_rules(found, ctx), record
```

### 26. `scripts/m4_prepare.py`

> **Vai trò:** Dựng giỏ fit/validation/test từ Master và che một lần (chỉ phụ thuộc seed và order_id).  
> **Mục trong bài:** 4.2 · **Người viết:** Vương  
> **Đầu vào → đầu ra:** Master, `split_manifest.parquet` → `M4/masked_baskets.parquet`  
> **Hàm/lớp chính (dòng):** `main` (19)  
> **Ghi chú:** `python scripts/m4_prepare.py`  
> *46 dòng · SHA-256 `f6272b4e4d55…`*

```python
 1 | """Chương 4, bước chuẩn bị: dựng giỏ fit/validation/test từ Master và che giỏ cố định.
 2 | 
 3 | Đầu ra DATA/Data phai sinh/M4/masked_baskets.parquet: order_id, user_id, split,
 4 | basket_size, observed, hidden, eligible (k >= 2). Phép che chỉ dùng seed và order_id,
 5 | không xem nội dung tập nào để chọn; mọi phương pháp đọc cùng tệp này.
 6 | M4/hashes.json ghi kèm tham số che để bước sau từ chối phép che lệch config.
 7 | 
 8 | ĐỌC NHANH: bước đầu Chương 4. Dựng giỏ fit/validation/test từ Master và CHE sản phẩm một lần duy nhất.
 9 |   Phép che chỉ phụ thuộc seed và order_id, nên mọi phương pháp đọc cùng một tệp che; tham số che được ghi vào hashes.json.
10 | """
11 | import pandas as pd
12 | 
13 | from m4_common import HASHES, baskets, config, mask, mask_params
14 | from project_io import check_hashes, path, require, write_frame, write_hashes
15 | 
16 | M2 = "DATA/Data phai sinh/M2"
17 | 
18 | 
19 | def main():
20 |     cfg = config()
21 |     foundation = check_hashes()
22 |     split = pd.read_parquet(path(M2) / "split_manifest.parquet")
23 |     master = pd.read_parquet(path("DATA/Data đã làm sạch/master_train.parquet"),
24 |                              columns=["order_id", "user_id", "product_id"])
25 |     # Bước 1: dựng giỏ của fit/validation/test từ Master theo bảng chia tập.
26 |     out = baskets(master, split, ["fit", "validation", "test"])
27 |     # Bước 2: che sản phẩm; cùng một giỏ luôn bị che giống nhau (seed + order_id).
28 |     masked = [mask(i, o, cfg["seeds"]["mask"], cfg["hidden_share"])
29 |               for i, o in zip(out["items"], out.order_id)]
30 |     out["basket_size"] = out["items"].map(len)
31 |     out["observed"], out["hidden"] = [m[0] for m in masked], [m[1] for m in masked]
32 |     out["eligible"] = out.basket_size >= 2
33 |     out = out.drop(columns="items")
34 |     # Bước 3: kiểm tra đủ giỏ và che đúng, rồi ghi tệp, hash và tham số che.
35 |     require(len(out) == split.split.ne("reference").sum(), "Thiếu giỏ so với phân hoạch")
36 |     require((out.observed.map(len) + out.hidden.map(len) == out.basket_size).all(), "Che sai")
37 |     target = path(cfg["data_dir"]) / "masked_baskets.parquet"
38 |     write_frame(target, out)
39 |     write_hashes(HASHES, [target], mask=mask_params(cfg),
40 |                  g0_split_sha256=foundation["canonical_split_sha256"])
41 |     print(out.groupby("split").agg(baskets=("order_id", "size"), eligible=("eligible", "sum"),
42 |                                    hidden=("hidden", lambda s: s.map(len).sum())))
43 | 
44 | 
45 | if __name__ == "__main__":
46 |     main()
```

### 27. `scripts/m4_mining.py`

> **Vai trò:** Danh mục C và luật FP-Growth cho 12 tổ hợp (N, min_count, max_len) trên reference.  
> **Mục trong bài:** 4.3 · **Người viết:** Vương  
> **Đầu vào → đầu ra:** reference → `M4/catalog.parquet`, `M4/rules_grid.parquet`  
> **Hàm/lớp chính (dòng):** `main` (22)  
> **Ghi chú:** `python scripts/m4_mining.py`  
> *51 dòng · SHA-256 `2aa0810906ef…`*

```python
 1 | """Chương 4: danh mục C và luật kết hợp trên reference cho lưới giai đoạn A.
 2 | 
 3 | catalog.parquet: mọi sản phẩm reference đã xếp hạng (C với Top-N là rank <= N).
 4 | rules_grid.parquet: luật FP-Growth cho mỗi (top_n, min_count, max_len), confidence
 5 | >= ngưỡng thấp nhất của lưới; ngưỡng cao hơn lọc khi chấm validation.
 6 | Apriori chỉ chạy trong m4_benchmark_mining.py để so sánh và kiểm tra tương đương.
 7 | Chạy sau m4_prepare.py; cập nhật M4/hashes.json (giữ tham số che, thêm lưới A).
 8 | 
 9 | ĐỌC NHANH: học danh mục C và luật kết hợp CHỈ trên reference. Chạy FP-Growth cho 12 tổ hợp (N, min_count, max_len) của giai đoạn A.
10 |   Apriori không chạy ở đây (chỉ dùng trong benchmark để so sánh).
11 | """
12 | import itertools
13 | 
14 | import pandas as pd
15 | 
16 | from m4_common import HASHES, basket_matrix, catalog, check_mask, config, mine, rules
17 | from project_io import check_hashes, path, write_frame, write_hashes
18 | 
19 | M2 = "DATA/Data phai sinh/M2"
20 | 
21 | 
22 | def main():
23 |     cfg = config()
24 |     grid = cfg["grid_A"]
25 |     check_hashes()
26 |     record = check_hashes(HASHES)
27 |     check_mask(record, cfg)
28 |     reference = pd.read_parquet(path(M2) / "reference.parquet",
29 |                                 columns=["order_id", "product_id", "department_id"])
30 |     # Xếp hạng toàn bộ sản phẩm reference theo độ phổ biến -> danh mục C.
31 |     ranked = catalog(reference)
32 |     n = reference.order_id.nunique()
33 |     found = []
34 |     # Mỗi tổ hợp: dựng ma trận giỏ x sản phẩm của Top-N, khai phá FP-Growth, sinh luật với confidence >= ngưỡng thấp nhất của lưới.
35 |     for top_n, min_count, max_len in itertools.product(grid["top_n"], grid["min_count"], grid["max_len"]):
36 |         matrix = basket_matrix(reference, ranked.product_id[:top_n])
37 |         r = rules(mine(matrix, "fpgrowth", min_count, max_len), n, min(grid["min_confidence"]))
38 |         found.append(r.assign(top_n=top_n, min_count=min_count, max_len=max_len))
39 |         print(f"N={top_n} min_count={min_count} max_len={max_len}: {len(r)} luật")
40 |     # Ghi danh mục, bảng luật và cập nhật hash (giữ tham số che).
41 |     data = path(cfg["data_dir"])
42 |     write_frame(data / "catalog.parquet", ranked)
43 |     write_frame(data / "rules_grid.parquet", pd.concat(found, ignore_index=True))
44 |     write_hashes(HASHES, [data / f for f in ("masked_baskets.parquet", "catalog.parquet",
45 |                                              "rules_grid.parquet")],
46 |                  mask=record["mask"], g0_split_sha256=record["g0_split_sha256"],
47 |                  grid_A=grid, reference_baskets=n)
48 | 
49 | 
50 | if __name__ == "__main__":
51 |     main()
```

### 28. `scripts/m4_benchmark_mining.py`

> **Vai trò:** So Apriori và FP-Growth trên cùng ma trận và ngưỡng, mỗi lượt một tiến trình con; kiểm cùng itemset, support lệch ≤ 1e-12.  
> **Mục trong bài:** 4.3 · **Người viết:** Vương  
> **Đầu vào → đầu ra:** reference → `mining_benchmark_*.csv`, `itemset_equivalence_*.json`  
> **Hàm/lớp chính (dòng):** `worker` (29), `main` (48)  
> **Ghi chú:** `python scripts/m4_benchmark_mining.py 1000 20 2`  
> *89 dòng · SHA-256 `69b5696bc6c7…`*

```python
 1 | """Chương 4: benchmark Apriori và FP-Growth trên cùng ma trận, ngưỡng và max_len.
 2 | 
 3 | Mỗi lượt chạy trong một tiến trình con mới (không chạy chồng); đo riêng thời gian dựng
 4 | ma trận, khai phá, sinh luật và RAM đỉnh tiến trình (psutil). Quá timeout ghi "timeout",
 5 | tiến trình lỗi ghi "error". Tương đương: cùng tập itemset, support lệch <= 1e-12.
 6 | Mỗi cấu hình ghi tệp riêng mining_benchmark_<cấu hình>.csv và itemset_equivalence_<cấu hình>.json.
 7 | 
 8 |   python scripts/m4_benchmark_mining.py               # cấu hình trial trong config
 9 |   python scripts/m4_benchmark_mining.py 1000 20 2     # top_n min_count max_len
10 | 
11 | ĐỌC NHANH: so Apriori với FP-Growth. Mỗi lượt chạy trong MỘT tiến trình con mới để RAM đo được không bị lượt trước làm nhiễu.
12 |   Kết quả: thời gian từng bước, RAM đỉnh, và kiểm tra hai thuật toán cho cùng tập itemset (support lệch <= 1e-12).
13 | """
14 | import json
15 | import subprocess
16 | import sys
17 | import time
18 | 
19 | import pandas as pd
20 | import psutil
21 | 
22 | from m4_common import basket_matrix, catalog, config, itemset_signature, mine, rules, worst_support_gap
23 | from project_io import check_hashes, path, write_frame, write_json
24 | 
25 | TOLERANCE = 1e-12
26 | 
27 | 
28 | # Tiến trình con: chạy MỘT thuật toán một lần, đo thời gian từng bước và RAM đỉnh, in kết quả JSON.
29 | def worker(algorithm, top_n, min_count, max_len):
30 |     reference = pd.read_parquet(path("DATA/Data phai sinh/M2/reference.parquet"),
31 |                                 columns=["order_id", "product_id", "department_id"])
32 |     products = catalog(reference).product_id[:top_n]
33 |     t0 = time.perf_counter()
34 |     matrix = basket_matrix(reference, products)
35 |     t1 = time.perf_counter()
36 |     itemsets = mine(matrix, algorithm, min_count, max_len)
37 |     t2 = time.perf_counter()
38 |     found = rules(itemsets, len(matrix), min(config()["grid_A"]["min_confidence"]))
39 |     t3 = time.perf_counter()
40 |     memory = psutil.Process().memory_info()
41 |     print(json.dumps({"matrix_s": t1 - t0, "mining_s": t2 - t1, "rules_s": t3 - t2,
42 |                       "peak_mib": getattr(memory, "peak_wset", memory.rss) / 2**20,
43 |                       "itemsets": len(itemsets), "rules": len(found),
44 |                       "support": [[list(k), v] for k, v in itemset_signature(itemsets).items()]}))
45 | 
46 | 
47 | # Tiến trình chính: mỗi lượt gọi một tiến trình con mới, gom kết quả rồi so tương đương itemset.
48 | def main(top_n, min_count, max_len):
49 |     cfg = config()
50 |     check_hashes()
51 |     rows, supports = [], []
52 |     for algorithm in ("apriori", "fpgrowth"):
53 |         for run in range(1, cfg["benchmark"]["runs"] + 1):
54 |             row = {"algorithm": algorithm, "run": run, "top_n": top_n,
55 |                    "min_count": min_count, "max_len": max_len, "status": "ok"}
56 |             try:
57 |                 out = subprocess.run([sys.executable, __file__, "--worker", algorithm,
58 |                                       str(top_n), str(min_count), str(max_len)],
59 |                                      capture_output=True, text=True, check=True,
60 |                                      timeout=cfg["benchmark"]["timeout_s"])
61 |                 result = json.loads(out.stdout.strip().splitlines()[-1])
62 |                 supports.append((algorithm, {tuple(k): v for k, v in result.pop("support")}))
63 |                 row.update(result)
64 |             except subprocess.TimeoutExpired:
65 |                 row["status"] = "timeout"
66 |             except subprocess.CalledProcessError as error:
67 |                 row.update(status="error", error=error.stderr.strip()[-300:])
68 |             rows.append(row)
69 |             print({k: v for k, v in row.items() if k != "error"})
70 |     gap = (worst_support_gap([s for _, s in supports])   # mọi lượt thành công của cả hai thuật toán
71 |            if {a for a, _ in supports} == {"apriori", "fpgrowth"} else None)
72 |     tag = f"N{top_n}_c{min_count}_l{max_len}"
73 |     report = path(cfg["report_dir"])
74 |     write_frame(report / f"mining_benchmark_{tag}.csv", pd.DataFrame(rows))
75 |     write_json(report / f"itemset_equivalence_{tag}.json", {
76 |         "config": {"top_n": top_n, "min_count": min_count, "max_len": max_len},
77 |         "same_itemsets": gap is not None, "max_support_gap": gap, "tolerance": TOLERANCE,
78 |         "equivalent": gap is not None and gap <= TOLERANCE,  # False khi thiếu lượt thành công
79 |         "python": sys.version.split()[0], "pandas": pd.__version__,
80 |         "mlxtend": __import__("mlxtend").__version__, "psutil": psutil.__version__})
81 | 
82 | 
83 | if __name__ == "__main__":
84 |     if sys.argv[1:2] == ["--worker"]:
85 |         worker(sys.argv[2], *map(int, sys.argv[3:6]))
86 |     else:
87 |         trial = config()["benchmark"]["trial"]
88 |         args = list(map(int, sys.argv[1:4])) or [trial["top_n"], trial["min_count"], trial["max_len"]]
89 |         main(*args)
```

### 29. `scripts/m4_classifier.py`

> **Vai trò:** `Pipeline` + `ColumnTransformer` (chuẩn hóa số, one-hot ngành) cho Logistic Regression và Random Forest; `fit_grid` chọn tham số.  
> **Mục trong bài:** 4.3 · **Người viết:** Phong · **Tệp trong khóa thực nghiệm**  
> **Đầu vào → đầu ra:** đặc trưng fit → Pipeline  
> **Hàm/lớp chính (dòng):** `build_pipeline` (25), `fit_grid` (46), `synthetic_data` (72), `demo` (84)  
> **Ghi chú:** `--demo` chỉ dùng dữ liệu tự tạo.  
> *117 dòng · SHA-256 `ac9f4a565b7a…`*

```python
  1 | """Pipeline LR/RF gọn; demo chỉ sinh dữ liệu giả, không đọc Master hoặc tập test."""
  2 | import argparse
  3 | from time import perf_counter
  4 | 
  5 | import joblib
  6 | import numpy as np
  7 | import pandas as pd
  8 | from sklearn.compose import ColumnTransformer
  9 | from sklearn.ensemble import RandomForestClassifier
 10 | from sklearn.impute import SimpleImputer
 11 | from sklearn.linear_model import LogisticRegression
 12 | from sklearn.pipeline import Pipeline
 13 | from sklearn.preprocessing import OneHotEncoder, StandardScaler
 14 | 
 15 | from m4_test import best_f1_threshold, classification_metrics, paired_bootstrap
 16 | from project_io import atomic_write, check_hashes, path, write_frame, write_json
 17 | 
 18 | NUMERIC = ['candidate_popularity', 'matching_rule_count', 'max_rule_confidence',
 19 |            'max_rule_lift', 'observed_basket_size', 'same_department_count']
 20 | CATEGORY = ['candidate_department_id']
 21 | GRIDS = {'LR': [{'C': c} for c in [0.01, 0.1, 1, 10]],
 22 |          'RF': [{'max_depth': d, 'min_samples_leaf': n} for d in [10, 20] for n in [20, 100]]}
 23 | 
 24 | 
 25 | def build_pipeline(method, params=None, group='full'):
 26 |     """Chỉ 7 biến được chọn; ID/nhãn không lọt vào estimator. Bỏ nhóm dùng để diễn giải."""
 27 |     if method not in GRIDS or group not in ('full', 'no_rules', 'no_department'):
 28 |         raise ValueError('Sai phương pháp hoặc nhóm đặc trưng.')
 29 |     numeric = [c for c in NUMERIC if not (group == 'no_rules' and c in NUMERIC[1:4])
 30 |                and not (group == 'no_department' and c == 'same_department_count')]
 31 |     steps = [('impute', SimpleImputer(strategy='median', keep_empty_features=True))]
 32 |     if method == 'LR':
 33 |         steps.append(('scale', StandardScaler()))
 34 |     branches = [('numeric', Pipeline(steps), numeric)]
 35 |     if group != 'no_department':
 36 |         branches.append(('category', Pipeline([
 37 |             ('impute', SimpleImputer(strategy='most_frequent', keep_empty_features=True)),
 38 |             ('encode', OneHotEncoder(handle_unknown='ignore'))]), CATEGORY))
 39 |     estimator = (LogisticRegression(solver='lbfgs', max_iter=1000)
 40 |                  if method == 'LR' else RandomForestClassifier(
 41 |                      n_estimators=300, max_features='sqrt', random_state=42, n_jobs=-1))
 42 |     estimator.set_params(**(params or {}))
 43 |     return Pipeline([('transform', ColumnTransformer(branches)), ('model', estimator)])
 44 | 
 45 | 
 46 | def fit_grid(x_fit, y_fit, method, evaluate_validation, tolerance=0.002):
 47 |     """Callback của Vương trả recall_at_10, inference_seconds; không tự tính Recall thứ hai.
 48 | 
 49 |     Callback phải chấm toàn bộ validation theo lô, kể cả giỏ rỗng ứng viên.
 50 |     Trả Pipeline thắng và bảng lưới; chỉ giữ mô hình còn trong dung sai hòa.
 51 |     """
 52 |     if method not in GRIDS or tolerance < 0 or not np.isfinite(tolerance):
 53 |         raise ValueError('Sai phương pháp/dung sai.')
 54 |     rows, candidates = [], []
 55 |     for params in GRIDS[method]:
 56 |         model = build_pipeline(method, params).fit(x_fit, y_fit)
 57 |         result = evaluate_validation(model)
 58 |         recall, seconds = result['recall_at_10'], result['inference_seconds']
 59 |         if not np.isfinite([recall, seconds]).all() or not 0 <= recall <= 1 or seconds < 0:
 60 |             raise ValueError('Callback phải trả Recall [0,1] và thời gian không âm.')
 61 |         rows.append(dict(method=method, **params, recall_at_10=recall, inference_seconds=seconds))
 62 |         candidates.append((model, recall, seconds))
 63 |         best = max(r for _, r, _ in candidates)
 64 |         candidates = [(m, r, s) for m, r, s in candidates if r >= best - tolerance]
 65 |     winner = min(candidates, key=lambda item: item[2])[0]
 66 |     table = pd.DataFrame(rows)
 67 |     table['selected'] = [all(winner['model'].get_params()[k] == v for k, v in p.items())
 68 |                          for p in GRIDS[method]]
 69 |     return winner, table
 70 | 
 71 | 
 72 | def synthetic_data(n=400, seed=42):
 73 |     rng = np.random.default_rng(seed)
 74 |     x = pd.DataFrame({NUMERIC[0]: rng.uniform(0, 0.1, n), NUMERIC[1]: rng.integers(0, 5, n),
 75 |                       NUMERIC[2]: rng.uniform(0, 1, n), NUMERIC[3]: rng.uniform(0, 4, n),
 76 |                       NUMERIC[4]: rng.integers(1, 20, n), NUMERIC[5]: rng.integers(0, 5, n),
 77 |                       CATEGORY[0]: rng.integers(1, 5, n).astype(float)})
 78 |     y = (rng.random(n) < 1 / (1 + np.exp(2 - x[NUMERIC[1]] - x[NUMERIC[2]]))).astype(int)
 79 |     x.loc[::17, NUMERIC[0]] = np.nan
 80 |     x.loc[::23, CATEGORY[0]] = np.nan
 81 |     return x, y
 82 | 
 83 | 
 84 | def demo():
 85 |     check_hashes()
 86 |     folder = path('output/ch4_phong_synthetic_20261101')
 87 |     x, y = synthetic_data()
 88 |     validation, yv = synthetic_data(120, 43)
 89 |     validation.loc[0, CATEGORY[0]] = 99
 90 |     records = []
 91 |     for method in GRIDS:
 92 |         start = perf_counter()
 93 |         model = build_pipeline(method).fit(x, y)
 94 |         scores = model.predict_proba(validation)[:, 1]
 95 |         threshold = best_f1_threshold(yv, scores)
 96 |         records.append(dict(method=method, **classification_metrics(yv, scores, threshold)))
 97 |         atomic_write(folder / f'pipeline_{method.lower()}.joblib', lambda p: joblib.dump(model, p))
 98 |         restored = joblib.load(folder / f'pipeline_{method.lower()}.joblib')
 99 |         np.testing.assert_array_equal(scores, restored.predict_proba(validation)[:, 1])
100 |         write_json(folder / f'{method.lower()}_demo.json', dict(synthetic_only=True,
101 |                    fit_rows=len(x), validation_rows=len(validation), seconds=perf_counter() - start))
102 |     write_frame(folder / 'classification_metrics_SYNTHETIC.csv', pd.DataFrame(records))
103 |     # Recall dựng tay để kiểm hàm bootstrap, không phải đầu ra xếp hạng của hai classifier.
104 |     metrics = pd.DataFrame([dict(user_id=i, order_id=i, method=m, **{'R@10': r})
105 |                            for m, values in [('example_A', [0.5, 1, 0, 1]),
106 |                                              ('example_B', [0, 0.5, 0, 0.5])]
107 |                            for i, r in enumerate(values)])
108 |     write_frame(folder / 'basket_metrics_SYNTHETIC.csv', metrics)
109 |     write_json(folder / 'bootstrap_SYNTHETIC.json', paired_bootstrap(metrics, 'example_A', 'example_B'))
110 |     print(f'Demo dữ liệu tự tạo hoàn thành: {folder}')
111 | 
112 | 
113 | if __name__ == '__main__':
114 |     parser = argparse.ArgumentParser(description=__doc__)
115 |     parser.add_argument('--demo', action='store_true', required=True)
116 |     parser.parse_args()
117 |     demo()
```

### 30. `scripts/m4_validate.py`

> **Vai trò:** Giai đoạn A (24 cấu hình luật) và B (LR, RF) trên validation, ngưỡng F1, phép bỏ nhóm đặc trưng.  
> **Mục trong bài:** 4.1, 4.3 · **Người viết:** Vương  
> **Đầu vào → đầu ra:** giỏ đã che, luật → `features_fit.parquet`, `pipeline_lr/rf.joblib`, `validation_grid_A/B.csv`, `validation_methods.csv`, `ablation.csv`  
> **Hàm/lớp chính (dòng):** `stage_a` (33), `choose_a` (56), `classify` (65), `main` (76)  
> **Ghi chú:** Tập test được nạp cùng tệp che nhưng bị loại ngay sau khi đọc, không tham gia chọn cấu hình. `--pilot` cho chạy thử nhanh.  
> *159 dòng · SHA-256 `42f0025371fa…`*

```python
  1 | """Chương 4: giai đoạn A (danh mục và luật) và B (LR, RF) trên validation; test bị loại ngay sau khi đọc, không tham gia chọn cấu hình.
  2 | 
  3 | Giai đoạn A chọn (N, min_count, max_len, min_confidence) bằng Recall@10 của Rules; giai đoạn B gọi
  4 | fit_grid của m4_classifier.py. Đầu ra: M4/features_fit.parquet, pipeline_lr/rf.joblib và các bảng trong
  5 | BAO CAO/Bao cao mo hinh/. Với --pilot chỉ dùng pilot_baskets giỏ fit và validation, ghi vào thư mục con pilot/.
  6 | 
  7 |   python scripts/m4_validate.py [--pilot]
  8 | 
  9 | ĐỌC NHANH (vấn đáp): chọn cấu hình bằng VALIDATION; test bị loại ngay sau khi đọc, không tham gia chọn cấu hình.
 10 |   Giai đoạn A: 24 cấu hình luật, chọn bằng Recall@10 của Rules (hòa trong dung sai 0,002 thì chọn cấu hình đơn giản hơn).
 11 |   Giai đoạn B: với cấu hình A đã chọn, dựng đặc trưng cho fit (20 mẫu âm/giỏ), chọn lưới cho LR và RF.
 12 |   Sau đó: ngưỡng F1, phép bỏ nhóm đặc trưng (no_rules, no_department), ghi bảng và hash. Giai đoạn C nằm ở m4_lock.py.
 13 | """
 14 | import argparse
 15 | import time
 16 | 
 17 | import joblib
 18 | import numpy as np
 19 | import pandas as pd
 20 | from sklearn.metrics import average_precision_score
 21 | 
 22 | from m4_classifier import CATEGORY, GRIDS, NUMERIC, build_pipeline, fit_grid
 23 | from m4_common import (HASHES, M, check_mask, config, context, evaluate, index_rules, make_batches,
 24 |                        sample_negatives)
 25 | from m4_test import best_f1_threshold, classification_metrics
 26 | from project_io import atomic_write, check_hashes, path, write_frame, write_hashes
 27 | 
 28 | FEATURES = NUMERIC + CATEGORY
 29 | DATA = "DATA/Data phai sinh/M4"
 30 | 
 31 | 
 32 | # GIAI ĐOẠN A: với mỗi bộ luật, chấm Recall@10 của Rules (kèm Popularity và trần) trên validation.
 33 | def stage_a(val, ranked, rules, dept, cfg):
 34 |     """Một dòng mỗi cấu hình (N, min_count, max_len, min_confidence); Recall@10 của Rules và của Popularity."""
 35 |     rows, size, ks = [], cfg["batch_size"], cfg["k_values"]
 36 |     for (n, count, length), group in rules.groupby(["top_n", "min_count", "max_len"]):
 37 |         ctx = context(ranked, n, dept)
 38 |         recall = {name: [] for name in ["pop", *cfg["grid_A"]["min_confidence"], "ceiling"]}
 39 |         for part, X in make_batches(val, ctx, index_rules(group, ctx), size):
 40 |             recall["pop"].append(evaluate(part, X, X.candidate_popularity, ks=ks))
 41 |             recall["ceiling"].append(recall["pop"][-1]["R@10_ceiling"])
 42 |             for c in cfg["grid_A"]["min_confidence"]:
 43 |                 conf = X.max_rule_confidence.where(X.max_rule_confidence >= c, 0)
 44 |                 recall[c].append(evaluate(part, X, conf, X.candidate_popularity, ks=ks)["R@10"])
 45 |         pop = pd.concat(recall["pop"])["R@10"].mean()
 46 |         for c in cfg["grid_A"]["min_confidence"]:
 47 |             rows.append(dict(top_n=n, min_count=count, max_len=length, min_confidence=c,
 48 |                              rules=int((group.confidence >= c).sum()), popularity_recall_at_10=pop,
 49 |                              rules_recall_at_10=pd.concat(recall[c]).mean(),
 50 |                              ceiling_recall_at_10=pd.concat(recall["ceiling"]).mean()))
 51 |         print(rows[-1], flush=True)
 52 |     return pd.DataFrame(rows)
 53 | 
 54 | 
 55 | # Chọn bộ luật tốt nhất; hòa trong dung sai thì ưu tiên cấu hình nhỏ và đơn giản hơn.
 56 | def choose_a(table, tolerance):
 57 |     """Recall@10 lớn nhất; hòa (trong dung sai) thì N nhỏ, min_count lớn, max_len nhỏ, min_confidence lớn."""
 58 |     tied = table[table.rules_recall_at_10 >= table.rules_recall_at_10.max() - tolerance]
 59 |     first = tied.sort_values(["top_n", "min_count", "max_len", "min_confidence"],
 60 |                              ascending=[True, False, True, False]).index[0]
 61 |     return table.loc[[first]].to_dict("records")[0]
 62 | 
 63 | 
 64 | # Chấm toàn bộ ứng viên theo lô bằng một mô hình đã huấn luyện.
 65 | def classify(batches, model, ks):
 66 |     """Chấm toàn bộ ứng viên theo lô: chỉ số theo giỏ, nhãn, điểm và thời gian (dự đoán + xếp hạng)."""
 67 |     start, metrics, y, scores = time.perf_counter(), [], [], []
 68 |     for part, X in batches:
 69 |         scores.append(model.predict_proba(X[FEATURES])[:, 1])
 70 |         metrics.append(evaluate(part, X, scores[-1], ks=ks))
 71 |         y.append(X.y.to_numpy())
 72 |     return pd.concat(metrics, ignore_index=True), np.concatenate(y), np.concatenate(scores), time.perf_counter() - start
 73 | 
 74 | 
 75 | # main: nạp dữ liệu -> giai đoạn A -> dựng đặc trưng -> giai đoạn B -> ngưỡng F1, bỏ nhóm đặc trưng -> ghi bảng và hash.
 76 | def main(pilot):
 77 |     cfg, ks = config(), config()["k_values"]
 78 |     check_hashes()
 79 |     record = check_hashes(HASHES)
 80 |     check_mask(record, cfg)
 81 |     data, report = path(cfg["data_dir"]), path(cfg["report_dir"])
 82 |     masked = pd.read_parquet(data / "masked_baskets.parquet")
 83 |     # Khối 1: đọc tệp giỏ che (có cả test), giữ ngay fit/validation; test bị loại ngay sau khi đọc.
 84 |     masked = masked[masked.eligible & masked.split.isin(["fit", "validation"])]  # test bị loại tại đây, không tham gia chọn cấu hình
 85 |     fit, val = (masked[masked.split == s] for s in ("fit", "validation"))
 86 |     ranked, rules = pd.read_parquet(data / "catalog.parquet"), pd.read_parquet(data / "rules_grid.parquet")
 87 |     master = pd.read_parquet(path("DATA/Data đã làm sạch/master_train.parquet"), columns=["product_id", "department_id"])
 88 |     dept = np.zeros(M, dtype=int)
 89 |     dept[master.product_id.to_numpy()] = master.department_id.to_numpy()
 90 |     if pilot:
 91 |         fit, val = fit.head(cfg["pilot_baskets"]), val.head(cfg["pilot_baskets"])
 92 |         data, report = data / "pilot", report / "pilot"
 93 |     # Khối 2 (giai đoạn A): chấm lưới luật và chọn cấu hình.
 94 |     table = stage_a(val, ranked, rules, dept, cfg)
 95 |     best = choose_a(table, cfg["tie_tolerance"])
 96 |     key = ["top_n", "min_count", "max_len", "min_confidence"]
 97 |     write_frame(report / "validation_grid_A.csv", table.assign(selected=(table[key] == pd.Series(best)[key]).all(axis=1)))
 98 |     n = best["top_n"]
 99 |     chosen = rules[(rules.top_n == n) & (rules.min_count == best["min_count"]) & (rules.max_len == best["max_len"])
100 |                    & (rules.confidence >= best["min_confidence"])]
101 |     # Khối 3: dựng đặc trưng cho fit (lấy mẫu âm 20/giỏ) và cho validation (giữ mọi ứng viên).
102 |     ctx = context(ranked, n, dept)
103 |     idx = index_rules(chosen, ctx)
104 |     train = pd.concat([sample_negatives(p, X, cfg["negatives_per_basket"], cfg["seeds"]["negative"])
105 |                        for p, X in make_batches(fit, ctx, idx, cfg["batch_size"])], ignore_index=True)
106 |     write_frame(data / "features_fit.parquet", train[["order_id", "product_id", "y", *FEATURES]])
107 |     write_frame(report / "feature_correlation.csv", train[NUMERIC].corr("spearman").rename_axis("feature").reset_index())
108 |     batches = list(make_batches(val, ctx, idx, cfg["batch_size"]))
109 |     x_fit, y_fit = train[FEATURES], train.y.to_numpy().astype(int)
110 |     print(f"A: {best}; fit {len(train)} dòng, dương {y_fit.mean():.4f}", flush=True)
111 | 
112 |     def callback(model):
113 |         metrics, _, _, seconds = classify(batches, model, ks)
114 |         print(f"  {model['model']}: R@10={metrics['R@10'].mean():.4f} {seconds:.0f}s", flush=True)
115 |         return {"recall_at_10": float(metrics["R@10"].mean()), "inference_seconds": seconds}
116 | 
117 |     # Khối 4: chấm Popularity và Rules; rồi với LR và RF: chọn lưới (giai đoạn B), ngưỡng F1, phép bỏ nhóm đặc trưng.
118 |     pipelines, grids, per_basket, methods, scored = {}, [], [], [], {}
119 |     for name, keys in [("Popularity", lambda X: [X.candidate_popularity]),
120 |                        ("Rules", lambda X: [X.max_rule_confidence, X.candidate_popularity])]:
121 |         start = time.perf_counter()
122 |         metrics = pd.concat([evaluate(p, X, *keys(X), ks=ks) for p, X in batches], ignore_index=True)
123 |         per_basket.append(metrics.assign(method=name))
124 |         methods.append(dict(method=name, params="", recall_at_10=metrics["R@10"].mean(),
125 |                             inference_seconds=time.perf_counter() - start))
126 |     ablation = []
127 |     for method in GRIDS:
128 |         winner, grid = fit_grid(x_fit, y_fit, method, callback, cfg["tie_tolerance"])
129 |         params = GRIDS[method][int(grid.selected.to_numpy().argmax())]
130 |         metrics, y, scores, seconds = classify(batches, winner, ks)
131 |         threshold = best_f1_threshold(y, scores)
132 |         scored[method] = dict(method=method, **params, **classification_metrics(y, scores, threshold))
133 |         per_basket.append(metrics.assign(method=method))
134 |         methods.append(dict(method=method, params=str(params), recall_at_10=metrics["R@10"].mean(), inference_seconds=seconds))
135 |         ablation.append(dict(method=method, group="full", recall_at_10=metrics["R@10"].mean(),
136 |                              average_precision=average_precision_score(y, scores)))
137 |         for group in ("no_rules", "no_department"):
138 |             m, y, scores, _ = classify(batches, build_pipeline(method, params, group).fit(x_fit, y_fit), ks)
139 |             ablation.append(dict(method=method, group=group, recall_at_10=m["R@10"].mean(),
140 |                                  average_precision=average_precision_score(y, scores)))
141 |         grids.append(grid)
142 |         atomic_write(data / f"pipeline_{method.lower()}.joblib", lambda p: joblib.dump(winner, p))
143 |     # Khối 5: ghi các bảng kết quả và hash (chạy thử --pilot thì không ghi hash).
144 |     write_frame(report / "validation_grid_B.csv", pd.concat(grids, ignore_index=True))
145 |     write_frame(report / "validation_methods.csv", pd.DataFrame(methods))
146 |     write_frame(report / "basket_metrics_validation.csv", pd.concat(per_basket, ignore_index=True))
147 |     write_frame(report / "classifier_validation.csv", pd.DataFrame(scored.values()))
148 |     write_frame(report / "ablation.csv", pd.DataFrame(ablation))
149 |     if not pilot:
150 |         files = [data / f for f in ("masked_baskets.parquet", "catalog.parquet", "rules_grid.parquet",
151 |                                     "features_fit.parquet", "pipeline_lr.joblib", "pipeline_rf.joblib")]
152 |         write_hashes(HASHES, files, **{k: v for k, v in record.items() if k != "files"},
153 |                      stage_A=best)
154 | 
155 | 
156 | if __name__ == "__main__":
157 |     parser = argparse.ArgumentParser(description=__doc__)
158 |     parser.add_argument("--pilot", action="store_true")
159 |     main(parser.parse_args().pilot)
```

### 31. `scripts/m4_lock.py`

> **Vai trò:** Chọn phương pháp chính theo Recall@10 validation và ghi `lock.json` (cấu hình, ngưỡng, SHA-256 các tệp) trước khi mở test.  
> **Mục trong bài:** 4.4 · **Người viết:** Vương  
> **Đầu vào → đầu ra:** kết quả validation → `lock.json`  
> **Hàm/lớp chính (dòng):** `main` (26)  
> **Ghi chú:** `python scripts/m4_lock.py --approve Phong Vuong`  
> *50 dòng · SHA-256 `c2973caa1865…`*

```python
 1 | """Chương 4, giai đoạn C: chọn phương pháp chính trên validation và ghi lock.json (khóa trước khi mở test).
 2 | 
 3 | Chọn Recall@10 validation lớn nhất; hòa trong dung sai thì chi phí suy luận thấp hơn, rồi theo thứ tự
 4 | Popularity, Rules, LR, RF. lock.json ghi cấu hình, ngưỡng F1 và SHA-256 mọi tệp mà bước test phải kiểm lại.
 5 | 
 6 | ĐỌC NHANH: giai đoạn C. Chọn phương pháp chính trên validation rồi KHÓA bằng lock.json trước khi ai mở test.
 7 |   lock.json ghi cấu hình, ngưỡng F1 và SHA-256 của mọi tệp mà bước test phải kiểm lại; khóa xong thì không sửa code, config hay mô hình.
 8 |   Cổng của m4_test.py đòi thêm hash mã nguồn (REQUIRED) và approvals đủ hai người. approvals chỉ là true khi truyền --approve:
 9 |     python scripts/m4_lock.py                        # bản nháp, cả hai approvals = false, test chưa chạy được
10 |     python scripts/m4_lock.py --approve Phong Vuong  # chỉ khi cả hai đã duyệt lock; từ chối nếu test đã bắt đầu
11 | """
12 | import argparse
13 | from datetime import datetime
14 | 
15 | import pandas as pd
16 | 
17 | from m4_common import CONFIG, HASHES, config
18 | from project_io import check_hashes, path, sha256, write_json
19 | 
20 | ORDER = ["Popularity", "Rules", "LR", "RF"]
21 | # Mã và nguồn mà cổng của m4_test.py bắt buộc phải có trong khóa (cùng danh sách CODE_FILES và các tệp nguồn của nó).
22 | REQUIRED = ["scripts/m4_test.py", "scripts/m4_common.py", "scripts/m4_classifier.py", "scripts/project_io.py",
23 |             "requirements.txt", "configs/m2_plot_style.json", HASHES, "DATA/Data đã làm sạch/master_train.parquet"]
24 | 
25 | 
26 | def main(approved):
27 |     cfg = config()
28 |     record = check_hashes(HASHES)
29 |     report = path(cfg["report_dir"])
30 |     if (report / "test_started.json").exists():
31 |         raise SystemExit("Test đã bắt đầu: không ghi lại lock.json.")
32 |     methods = pd.read_csv(report / "validation_methods.csv", keep_default_na=False)
33 |     # Chọn phương pháp chính: Recall@10 lớn nhất; hòa trong dung sai thì suy luận nhanh hơn, rồi theo thứ tự cố định.
34 |     tied = methods[methods.recall_at_10 >= methods.recall_at_10.max() - cfg["tie_tolerance"]]
35 |     chosen = tied.assign(order=tied.method.map(ORDER.index)).sort_values(["inference_seconds", "order"]).method.iloc[0]
36 |     classifiers = pd.read_csv(report / "classifier_validation.csv").set_index("method")
37 |     # Ghi lock.json kèm SHA-256 mọi tệp mà bước test phải kiểm lại.
38 |     files = [CONFIG, *REQUIRED, *record["files"], (report / "validation_methods.csv").relative_to(path(".")).as_posix()]
39 |     write_json(report / "lock.json", {
40 |         "locked_at": datetime.now().isoformat(timespec="seconds"), "main_method": chosen,
41 |         "stage_A": record["stage_A"], "validation": methods.set_index("method").to_dict("index"),
42 |         "f1_threshold": classifiers.threshold.to_dict(), "approvals": {n: n in approved for n in ("Phong", "Vuong")},
43 |         "files": {f: sha256(path(f)) for f in files}})
44 |     print(methods.to_string(index=False), f"\nPhương pháp chính: {chosen}")
45 | 
46 | 
47 | if __name__ == "__main__":
48 |     parser = argparse.ArgumentParser(description=__doc__)
49 |     parser.add_argument("--approve", nargs="*", choices=["Phong", "Vuong"], default=[])
50 |     main(parser.parse_args().approve)
```

### 32. `scripts/m4_interpret.py`

> **Vai trò:** Permutation importance (mức giảm Average Precision) và hệ số LR.  
> **Mục trong bài:** 4.5 · **Người viết:** Phong  
> **Đầu vào → đầu ra:** Pipeline → hàm dùng chung  
> **Hàm/lớp chính (dòng):** `sample_baskets` (17), `importance_table` (26), `lr_coefficients` (43), `figures` (55), `demo` (81)  
> **Ghi chú:** `--demo` chỉ dùng dữ liệu tự tạo.  
> *111 dòng · SHA-256 `13aaef754905…`*

```python
  1 | """Importance LR/RF, hệ số LR và hình mẫu; CLI chỉ chạy dữ liệu tự tạo."""
  2 | import argparse
  3 | 
  4 | import numpy as np
  5 | import pandas as pd
  6 | from sklearn.inspection import permutation_importance
  7 | from sklearn.metrics import average_precision_score
  8 | 
  9 | from m4_classifier import CATEGORY, NUMERIC, build_pipeline, synthetic_data
 10 | from project_io import check_hashes, path, plot_setup, save_figure, write_frame, write_json
 11 | 
 12 | LABELS = ['Độ phổ biến', 'Số luật khớp', 'Confidence lớn nhất', 'Lift lớn nhất',
 13 |           'Cỡ giỏ quan sát', 'Số món cùng ngành', 'Ngành ứng viên']
 14 | FOLDER = 'output/ch4_phong_importance_20261101'
 15 | 
 16 | 
 17 | def sample_baskets(frame, n=5000, seed=44):
 18 |     """Chọn giỏ, giữ toàn bộ dòng ứng viên; frame chỉ chứa validation do bên gọi bảo đảm."""
 19 |     if n < 1 or frame.empty or frame.order_id.isna().any():
 20 |         raise ValueError('Cần dữ liệu không rỗng, order_id đầy đủ và n dương.')
 21 |     ids = np.sort(frame.order_id.unique())
 22 |     chosen = np.random.default_rng(seed).choice(ids, min(n, len(ids)), replace=False)
 23 |     return frame.loc[frame.order_id.isin(chosen)].copy()
 24 | 
 25 | 
 26 | def importance_table(model, x, y, method, repeats=10, seed=44):
 27 |     """Hoán vị cột gốc trước OneHot: ngành là một biến; không fit lại Pipeline."""
 28 |     x = x[NUMERIC + CATEGORY]
 29 |     if set(np.unique(y)) != {0, 1} or repeats < 1:
 30 |         raise ValueError('Importance cần hai lớp và số lần lặp dương.')
 31 |     result = permutation_importance(model, x, y, scoring='average_precision',
 32 |                                     n_repeats=repeats, random_state=seed, n_jobs=1)
 33 |     table = pd.DataFrame({'method': method, 'feature': x.columns,
 34 |                           'ap_decrease_mean': result.importances_mean,
 35 |                           'ap_decrease_std': result.importances_std})
 36 |     raw = pd.DataFrame(result.importances, index=x.columns).rename_axis('feature')
 37 |     raw.columns = np.arange(1, repeats + 1)
 38 |     raw = raw.stack().rename_axis(['feature', 'repeat']).rename('ap_decrease').reset_index()
 39 |     raw.insert(0, 'method', method)
 40 |     return table, raw, float(average_precision_score(y, model.predict_proba(x)[:, 1]))
 41 | 
 42 | 
 43 | def lr_coefficients(model):
 44 |     """Hệ số đúng thứ tự sau biến đổi; sáu biến số theo 1 SD, ngành theo cột OneHot."""
 45 |     estimator = model['model']
 46 |     if not hasattr(estimator, 'coef_') or estimator.coef_.shape[0] != 1:
 47 |         raise ValueError('Cần Pipeline LR nhị phân đã fit.')
 48 |     names = model['transform'].get_feature_names_out()
 49 |     table = pd.DataFrame({'feature': names, 'coefficient': estimator.coef_[0]})
 50 |     table['kind'] = np.where(table.feature.str.startswith('numeric__'), 'numeric_1_sd', 'onehot')
 51 |     return pd.concat([table, pd.DataFrame([{'feature': 'intercept',
 52 |                      'coefficient': float(estimator.intercept_[0]), 'kind': 'intercept'}])], ignore_index=True)
 53 | 
 54 | 
 55 | def figures(importance, coefficients):
 56 |     plt, style = plot_setup()
 57 |     fig, axes = plt.subplots(2, 1, figsize=(16 / 2.54, 9.0))
 58 |     for ax, method, color in zip(axes, ['LR', 'RF'], style['colors']):
 59 |         rows = importance.loc[importance.method.eq(method)].set_index('feature').loc[NUMERIC + CATEGORY]
 60 |         ax.barh(LABELS, rows.ap_decrease_mean, xerr=rows.ap_decrease_std, color=color, capsize=3)
 61 |         ax.invert_yaxis()
 62 |         ax.axvline(0, color='gray', linewidth=0.8)
 63 |         ax.set_title(method)
 64 |         ax.set_xlabel('Mức giảm Average Precision')
 65 |     fig.suptitle('Permutation importance LR và RF\nDỮ LIỆU TỰ TẠO', fontsize=12)
 66 |     fig.text(0.5, 0.02, 'Thanh sai số: ±1 SD của 10 lần hoán vị; seed 44.', ha='center', fontsize=12)
 67 |     fig.subplots_adjust(left=0.36, right=0.96, top=0.88, bottom=0.10, hspace=0.48)
 68 |     save_figure(plt, fig, FOLDER + '/figures', 'Hinh_mau_1_Importance_LR_RF', style)
 69 |     numeric = coefficients.loc[coefficients.kind.eq('numeric_1_sd')]
 70 |     fig, ax = plt.subplots(figsize=(16 / 2.54, 5.2))
 71 |     ax.barh(LABELS[:6], numeric.coefficient, color=style['colors'][0])
 72 |     ax.invert_yaxis()
 73 |     ax.axvline(0, color='gray', linewidth=0.8)
 74 |     ax.set_xlabel('Hệ số LR (biến số đã chuẩn hóa)')
 75 |     ax.set_title('Hệ số LR của sáu biến số\nDỮ LIỆU TỰ TẠO', fontsize=12)
 76 |     fig.text(0.5, 0.03, 'Dấu hệ số không thể hiện quan hệ nhân quả.', ha='center', fontsize=12)
 77 |     fig.subplots_adjust(left=0.36, right=0.96, top=0.84, bottom=0.20)
 78 |     save_figure(plt, fig, FOLDER + '/figures', 'Hinh_mau_2_He_so_LR', style)
 79 | 
 80 | 
 81 | def demo():
 82 |     check_hashes()
 83 |     x, y = synthetic_data(800, 42)
 84 |     validation, yv = synthetic_data(400, 43)
 85 |     tables, raw, baselines = [], [], {}
 86 |     for method in ['LR', 'RF']:
 87 |         model = build_pipeline(method).fit(x, y)
 88 |         before = model.predict_proba(validation)
 89 |         table, runs, baselines[method] = importance_table(model, validation, yv, method)
 90 |         np.testing.assert_array_equal(before, model.predict_proba(validation))
 91 |         tables.append(table)
 92 |         raw.append(runs)
 93 |         if method == 'LR':
 94 |             coefficients = lr_coefficients(model)
 95 |     importance = pd.concat(tables, ignore_index=True)
 96 |     write_frame(path(FOLDER) / 'importance_SYNTHETIC.csv', importance)
 97 |     write_frame(path(FOLDER) / 'importance_repeats_SYNTHETIC.csv', pd.concat(raw, ignore_index=True))
 98 |     write_frame(path(FOLDER) / 'lr_coefficients_SYNTHETIC.csv', coefficients)
 99 |     write_json(path(FOLDER) / 'demo_metadata.json', dict(synthetic_only=True, fit_rows=len(x),
100 |                validation_rows=len(validation), fit_seed=42, validation_seed=43, importance_seed=44,
101 |                repeats=10, scoring='average_precision', std_ddof=0, baseline_ap=baselines,
102 |                note='400 dòng tự tạo, không phải mẫu 5.000 giỏ validation nghiên cứu.'))
103 |     figures(importance, coefficients)
104 |     print('Đã xuất bảng và hai cặp hình mẫu tại ' + FOLDER)
105 | 
106 | 
107 | if __name__ == '__main__':
108 |     parser = argparse.ArgumentParser(description=__doc__)
109 |     parser.add_argument('--demo', action='store_true', required=True)
110 |     parser.parse_args()
111 |     demo()
```

### 33. `scripts/m4_report.py`

> **Vai trò:** Bảng mô tả hai tập, độ phủ luật, importance (5.000 giỏ validation), hệ số LR, hai giỏ ví dụ, hình importance; không nạp test.  
> **Mục trong bài:** 4.2, 4.5 · **Người viết:** Vương  
> **Đầu vào → đầu ra:** Pipeline đã khóa, fit/validation → `dataset_description.csv`, `importance.csv`, `lr_coefficients.csv`, `examples.csv`, `fig-importance.*`  
> **Hàm/lớp chính (dòng):** `describe` (23), `figure` (40), `example` (63), `main` (77)  
> **Ghi chú:** `python scripts/m4_report.py`  
> *113 dòng · SHA-256 `f9ef4f84c176…`*

```python
  1 | """Chương 4: bảng mô tả hai tập, độ phủ luật, importance, hệ số LR và hai giỏ ví dụ trên dữ liệu thật.
  2 | 
  3 | Chỉ dùng giỏ fit/validation (test không được nạp) và hai Pipeline đã khóa. Importance dùng hàm của
  4 | m4_interpret.py trên 5.000 giỏ validation (seed 44, mọi ứng viên). Chạy sau m4_lock.py.
  5 | 
  6 | ĐỌC NHANH: sinh các bảng và hình mô tả của Chương 4 từ hai Pipeline đã khóa, chỉ trên fit/validation (test không nạp).
  7 |   Gồm: Bảng 4.2 (mô tả hai tập), độ phủ luật, importance và hình, hệ số LR, hai giỏ ví dụ (một có luật khớp, một không).
  8 | """
  9 | import joblib
 10 | import numpy as np
 11 | import pandas as pd
 12 | 
 13 | from m4_classifier import CATEGORY, NUMERIC
 14 | from m4_common import basket_features, config, locked_stage, make_batches
 15 | from m4_interpret import LABELS, importance_table, lr_coefficients, sample_baskets
 16 | from project_io import check_hashes, path, plot_setup, save_figure, write_frame, write_json
 17 | 
 18 | FEATURES = NUMERIC + CATEGORY
 19 | REPORT = "BAO CAO/Bao cao mo hinh"
 20 | 
 21 | 
 22 | # Bảng 4.2: số giỏ, sản phẩm che, phần thuộc C, số cặp ứng viên, tỷ lệ dương.
 23 | def describe(masked, ctx, record, train):
 24 |     """Bảng 4.2 cho reference, fit, validation: số giỏ, sản phẩm che, phần thuộc C, số cặp ứng viên, tỷ lệ dương."""
 25 |     rows = [dict(split="reference", baskets=record["reference_baskets"])]
 26 |     for split in ("fit", "validation"):
 27 |         part = masked[masked.split == split]
 28 |         used = part[part.eligible]
 29 |         hidden, in_c = used.hidden.map(len), used.hidden.map(lambda h: int((ctx["pos"][h] >= 0).sum()))
 30 |         pairs = len(ctx["pid"]) - used.observed.map(lambda o: int((ctx["pos"][o] >= 0).sum()))
 31 |         rows.append(dict(split=split, baskets=len(part), one_item_baskets=int((~part.eligible).sum()), evaluated=len(used),
 32 |                          hidden=int(hidden.sum()), hidden_in_C_micro=in_c.sum() / hidden.sum(),
 33 |                          hidden_in_C_macro=(in_c / hidden).mean(), candidate_pairs=int(pairs.sum()),
 34 |                          positive_rate=in_c.sum() / pairs.sum(),
 35 |                          positive_rate_sampled=train.y.mean() if split == "fit" else None))
 36 |     return pd.DataFrame(rows)
 37 | 
 38 | 
 39 | # Hình importance: hai panel (LR, RF), cột = mức giảm AP khi hoán vị đặc trưng.
 40 | def figure(importance):
 41 |     plt, style = plot_setup()
 42 |     from matplotlib.ticker import ScalarFormatter
 43 | 
 44 |     class Comma(ScalarFormatter):
 45 |         """Nhãn trục số dùng dấu phẩy thập phân cho khớp lời văn (07/11)."""
 46 |         def __call__(self, x, pos=None):
 47 |             return super().__call__(x, pos).replace(".", ",")
 48 | 
 49 |     fig, axes = plt.subplots(2, 1, figsize=(16 / 2.54, 5.6))
 50 |     for ax, method, color in zip(axes, ["LR", "RF"], style["colors"]):
 51 |         rows = importance[importance.method == method].set_index("feature").loc[FEATURES]
 52 |         ax.barh(LABELS, rows.ap_decrease_mean, xerr=rows.ap_decrease_std, color=color, capsize=3)
 53 |         ax.invert_yaxis()
 54 |         ax.axvline(0, color="gray", linewidth=0.8)
 55 |         ax.set_title(method)
 56 |         ax.set_xlabel("Mức giảm Average Precision")
 57 |         ax.xaxis.set_major_formatter(Comma())
 58 |     fig.subplots_adjust(left=0.36, right=0.96, top=0.95, bottom=0.16, hspace=0.6)
 59 |     save_figure(plt, fig, REPORT + "/figures", "fig-importance", style)
 60 | 
 61 | 
 62 | # Giỏ ví dụ: Top-5 của bốn phương pháp, đánh dấu hit nếu nằm trong H.
 63 | def example(case, row, ctx, idx, models, names):
 64 |     """Top-5 của bốn phương pháp cho một giỏ; hit = sản phẩm nằm trong H."""
 65 |     _, X = next(make_batches(pd.DataFrame([row]), ctx, idx, 1))
 66 |     keys = {"Popularity": [X.candidate_popularity], "Rules": [X.max_rule_confidence, X.candidate_popularity],
 67 |             **{m: [model.predict_proba(X[FEATURES])[:, 1]] for m, model in models.items()}}
 68 |     out = []
 69 |     for method, key in keys.items():
 70 |         top = X.iloc[np.lexsort((X.product_id.to_numpy(), *[-np.asarray(k, float) for k in key[::-1]]))[:5]]
 71 |         out += [dict(case=case, order_id=row.order_id, method=method, rank=r + 1, product_id=p,
 72 |                      product_name=names.get(p, ""), hit=bool(h)) for r, (p, h) in enumerate(zip(top.product_id, top.y))]
 73 |     return out
 74 | 
 75 | 
 76 | # main: bảng mô tả -> độ phủ luật -> importance và hệ số LR -> hình -> hai giỏ ví dụ.
 77 | def main():
 78 |     cfg = config()
 79 |     check_hashes()
 80 |     masked, ctx, idx, record = locked_stage(cfg)
 81 |     data, report = path(cfg["data_dir"]), path(REPORT)
 82 |     write_frame(report / "dataset_description.csv", describe(
 83 |         masked, ctx, record, pd.read_parquet(data / "features_fit.parquet", columns=["y"])))
 84 |     val = masked[(masked.split == "validation") & masked.eligible]
 85 |     # Độ phủ luật: tỷ lệ giỏ validation có ít nhất một luật khớp.
 86 |     flags = np.array([basket_features(o, ctx, idx)["matching_rule_count"].any() for o in val.observed])
 87 |     write_json(report / "rule_coverage.json", dict(validation_baskets=len(val), with_matching_rule=int(flags.sum()),
 88 |                                                    share=float(flags.mean())))
 89 |     # Importance (hoán vị đặc trưng, đo bằng AP) và hệ số LR trên 5.000 giỏ validation.
 90 |     models = {m: joblib.load(data / f"pipeline_{m.lower()}.joblib") for m in ("LR", "RF")}
 91 |     sample = sample_baskets(val, 5000, cfg["seeds"]["importance"])
 92 |     X = pd.concat([x for _, x in make_batches(sample, ctx, idx, cfg["batch_size"])], ignore_index=True)
 93 |     tables, repeats, baseline = [], [], {}
 94 |     for m, model in models.items():
 95 |         table, raw, baseline[m] = importance_table(model, X, X.y.to_numpy().astype(int), m, seed=cfg["seeds"]["importance"])
 96 |         tables.append(table)
 97 |         repeats.append(raw)
 98 |     importance = pd.concat(tables, ignore_index=True)
 99 |     write_frame(report / "importance.csv", importance)
100 |     write_frame(report / "importance_repeats.csv", pd.concat(repeats, ignore_index=True))
101 |     write_frame(report / "lr_coefficients.csv", lr_coefficients(models["LR"]))
102 |     write_json(report / "importance_baseline.json", dict(baskets=len(sample), candidate_rows=len(X), average_precision=baseline))
103 |     figure(importance)
104 |     # Hai giỏ ví dụ: một giỏ có luật khớp, một giỏ không có.
105 |     names = pd.read_parquet(path("DATA/Data đã làm sạch/master_train.parquet"), columns=["product_id", "product_name"])
106 |     names = names.drop_duplicates("product_id").set_index("product_id").product_name.to_dict()
107 |     picked = {"có luật khớp": val[flags].iloc[0], "không có luật khớp": val[~flags].iloc[0]}
108 |     write_frame(report / "examples.csv", pd.DataFrame(
109 |         [r for case, row in picked.items() for r in example(case, row, ctx, idx, models, names)]))
110 | 
111 | 
112 | if __name__ == "__main__":
113 |     main()
```

### 34. `scripts/m4_test.py`

> **Vai trò:** Cổng khóa (kiểm SHA-256 mọi tệp trong `lock.json`, hai xác nhận), chấm test một lần cho bốn phương pháp: Recall@K, Precision@K, chỉ số phân loại, bootstrap ghép cặp 2.000 lần.  
> **Mục trong bài:** 4.4 (Bảng kết quả test, Hình 4.1) · **Người viết:** Phong · **Tệp trong khóa thực nghiệm**  
> **Đầu vào → đầu ra:** giỏ test đã che, `lock.json` → `results_test.json`, `ranking_metrics_test.csv`, `paired_bootstrap_test.csv`, `fig-recall-at-k-test.*`  
> **Hàm/lớp chính (dòng):** `checked_scores` (22), `best_f1_threshold` (31), `classification_metrics` (43), `paired_bootstrap` (60), `checked_lock` (93), `figure` (127), `run` (143)  
> **Ghi chú:** Đã chạy một lần ngày 04/11/2026; `test_started.json` chặn chạy lại.  
> *196 dòng · SHA-256 `e9e2e4f7a439…`*

```python
  1 | """Chỉ số phân loại, bootstrap và chấm điểm sau khóa (cổng lock.json, bốn phương pháp, Recall@K, phân loại, bootstrap).
  2 | 
  3 |   python scripts/m4_test.py test                     # chấm tập test một lần, ghi vào BAO CAO/Bao cao mo hinh/
  4 |   python scripts/m4_test.py validation <thư mục>     # chạy thử cùng mã trên validation, ghi ra thư mục khác
  5 | 
  6 | Cổng khóa: kiểm SHA-256, hai xác nhận và mã nguồn; test_started.json chặn chạy lại kể cả khi lượt đầu lỗi.
  7 | Nếu máy hỏng: giữ mọi dấu/log; chỉ hai bên cùng duyệt mới được đổi tên dấu sang
  8 | test_started_failed_<ngày giờ>.json khi chưa có bất kỳ kết quả test nào. Không tự xóa dấu.
  9 | """
 10 | import sys
 11 | 
 12 | import joblib
 13 | import numpy as np
 14 | import pandas as pd
 15 | from sklearn.metrics import (accuracy_score, average_precision_score, confusion_matrix,
 16 |                              precision_recall_curve, precision_recall_fscore_support, roc_auc_score)
 17 | 
 18 | from m4_common import config, evaluate, locked_stage, make_batches
 19 | from project_io import check_hashes, path, plot_setup, read_json, require, save_figure, sha256, write_frame, write_json
 20 | 
 21 | 
 22 | def checked_scores(y, scores):
 23 |     y, scores = np.asarray(y), np.asarray(scores, dtype=float)
 24 |     if (y.ndim != 1 or scores.shape != y.shape or not len(y)
 25 |             or not np.isin(y, [0, 1]).all() or not np.isfinite(scores).all()
 26 |             or ((scores < 0) | (scores > 1)).any()):
 27 |         raise ValueError('Cần nhãn nhị phân và xác suất hữu hạn cùng chiều, không rỗng.')
 28 |     return y, scores
 29 | 
 30 | 
 31 | def best_f1_threshold(y_validation, scores):
 32 |     """Chỉ gọi với validation; hòa F1 chọn ngưỡng cao nhất (ít dự đoán dương)."""
 33 |     y, scores = checked_scores(y_validation, scores)
 34 |     if len(np.unique(y)) != 2:
 35 |         raise ValueError('Chọn ngưỡng cần validation có cả hai lớp.')
 36 |     precision, recall, thresholds = precision_recall_curve(y, scores)
 37 |     denominator = precision[:-1] + recall[:-1]
 38 |     f1 = np.divide(2 * precision[:-1] * recall[:-1], denominator,
 39 |                    out=np.zeros_like(denominator), where=denominator > 0)
 40 |     return float(thresholds[np.flatnonzero(f1 == f1.max())[-1]])
 41 | 
 42 | 
 43 | def classification_metrics(y, scores, threshold):
 44 |     """Toàn bộ cặp ứng viên; ROC-AUC/AP không xác định trả None, không bịa số 0."""
 45 |     y, scores = checked_scores(y, scores)
 46 |     if not np.isfinite(threshold) or not 0 <= threshold <= 1:
 47 |         raise ValueError('Ngưỡng phải thuộc [0, 1].')
 48 |     predicted = scores >= threshold
 49 |     precision, recall, f1, _ = precision_recall_fscore_support(
 50 |         y, predicted, average='binary', zero_division=0)
 51 |     tn, fp, fn, tp = confusion_matrix(y, predicted, labels=[0, 1]).ravel()
 52 |     return dict(n=len(y), positives=int(y.sum()), threshold=float(threshold),
 53 |                 accuracy=float(accuracy_score(y, predicted)), precision=float(precision),
 54 |                 recall=float(recall), f1=float(f1),
 55 |                 roc_auc=float(roc_auc_score(y, scores)) if len(np.unique(y)) == 2 else None,
 56 |                 average_precision=float(average_precision_score(y, scores)) if y.sum() else None,
 57 |                 tn=int(tn), fp=int(fp), fn=int(fn), tp=int(tp))
 58 | 
 59 | 
 60 | def paired_bootstrap(metrics, method, baseline, repeats=2000, seed=42):
 61 |     """Ghép theo user_id/order_id; một người một giỏ. Đầu vào từ bộ metrics của Vương."""
 62 |     if not isinstance(repeats, int) or repeats < 1:
 63 |         raise ValueError('repeats phải là số nguyên dương.')
 64 |     keys = ['user_id', 'order_id']
 65 |     arrays = []
 66 |     for name in (method, baseline):
 67 |         part = metrics.loc[metrics['method'].eq(name), keys + ['R@10']]
 68 |         if (part.empty or part.isna().any().any() or part.user_id.duplicated().any()
 69 |                 or part.order_id.duplicated().any()):
 70 |             raise ValueError('Mỗi phương pháp cần đúng một giỏ/người, không thiếu khóa/chỉ số.')
 71 |         arrays.append(part.set_index(keys)['R@10'].sort_index())
 72 |     if not arrays[0].index.equals(arrays[1].index):
 73 |         raise ValueError('Hai phương pháp phải có cùng tập người và giỏ; không tự bỏ giỏ.')
 74 |     values = np.column_stack([s.to_numpy(dtype=float) for s in arrays])
 75 |     if not np.isfinite(values).all() or ((values < 0) | (values > 1)).any():
 76 |         raise ValueError('Recall phải hữu hạn và thuộc [0, 1].')
 77 |     difference = values[:, 0] - values[:, 1]
 78 |     rng = np.random.default_rng(seed)
 79 |     samples = [float(rng.choice(difference, len(difference), replace=True).mean())
 80 |                for _ in range(repeats)]
 81 |     low, high = np.quantile(samples, [0.025, 0.975], method='linear')
 82 |     return dict(method=method, baseline=baseline, n_users=len(difference), repeats=repeats,
 83 |                 seed=seed, difference=float(difference.mean()), ci_low=float(low),
 84 |                 ci_high=float(high), improved=bool(low > 0))
 85 | 
 86 | 
 87 | KS = range(1, 11)
 88 | SHOWN = ["P@5", "R@5", "P@10", "R@10", "HR@10", "R@10_ceiling"]
 89 | CODE_FILES = ['scripts/m4_test.py', 'scripts/m4_common.py', 'scripts/m4_classifier.py',
 90 |               'scripts/project_io.py', 'requirements.txt', 'configs/m2_plot_style.json']
 91 | 
 92 | 
 93 | def checked_lock(split, out, cfg):
 94 |     """Kiểm trước khi đọc giỏ; test thật cần hai xác nhận và khóa đủ mã/nguồn."""
 95 |     require(split in ('validation', 'test'), 'Chỉ chấp nhận validation hoặc test.')
 96 |     report, out = path(cfg['report_dir']), path(out)
 97 |     lock_path = report / 'lock.json'
 98 |     lock = read_json(lock_path)
 99 |     require(bool(lock.get('files')), 'Khóa không có danh sách tệp.')
100 |     require(lock.get('main_method') in ('Popularity', 'Rules', 'LR', 'RF'), 'Sai phương pháp chính.')
101 |     require(all(np.isfinite(lock['f1_threshold'][m]) and 0 <= lock['f1_threshold'][m] <= 1
102 |                 for m in ('LR', 'RF')), 'Ngưỡng khóa không hợp lệ.')
103 |     for name, digest in lock['files'].items():
104 |         require(path(name).is_relative_to(path('.')), 'Tệp khóa nằm ngoài dự án.')
105 |         require(sha256(path(name)) == digest, f'Tệp đã đổi sau khi khóa: {name}')
106 |     record = check_hashes('DATA/Data phai sinh/M4/hashes.json')
107 |     require(lock['stage_A'] == record['stage_A'], 'Cấu hình A trong lock khác hồ sơ M4.')
108 |     if split == 'test':
109 |         require(out == report, 'Test chỉ được ghi vào thư mục báo cáo chính thức.')
110 |         require(lock.get('approvals') == {'Phong': True, 'Vuong': True}, 'Chưa đủ hai xác nhận khóa.')
111 |         needed = CODE_FILES + ['configs/m4_model.json', 'DATA/Data phai sinh/M4/hashes.json',
112 |                               'DATA/Data đã làm sạch/master_train.parquet', *record['files']]
113 |         require(set(needed).issubset(lock['files']), 'Khóa thiếu mã nguồn hoặc đầu vào bắt buộc.')
114 |         check_hashes()
115 |     else:
116 |         require(out != report, 'Validation phải xuất thư mục thử riêng.')
117 |     require(not (out / f'results_{split}.json').exists(), 'Đã có kết quả, không ghi đè.')
118 |     if split == 'test':
119 |         # Tạo độc quyền trước khi nạp test; giữ dấu kể cả khi lỗi giữa chừng.
120 |         out.mkdir(parents=True, exist_ok=True)
121 |         with (out / 'test_started.json').open('x', encoding='utf-8') as stream:
122 |             import json
123 |             json.dump({'lock_sha256': sha256(lock_path)}, stream)
124 |     return lock
125 | 
126 | 
127 | def figure(recall_k, ceiling, folder, stem):
128 |     """Hai khung chung trục K: trên là Recall trần (khoảng 0,4-0,5), dưới phóng to bốn phương pháp."""
129 |     plt, style = plot_setup()
130 |     fig, (top, bottom) = plt.subplots(2, 1, figsize=(16 / 2.54, 5.4), sharex=True, height_ratios=[1, 2.4])
131 |     top.plot(list(KS), ceiling, linestyle="--", marker="o", color="gray", label="Recall trần")
132 |     top.set(ylim=(min(ceiling) - 0.03, max(ceiling) + 0.03))
133 |     top.legend(loc="lower right")
134 |     for (method, row), color in zip(recall_k.iterrows(), style["colors"]):
135 |         bottom.plot(list(KS), row.to_numpy(), marker="o", color=color, label=method)
136 |     bottom.set(xlabel="K", xticks=list(KS), ylim=(0, recall_k.to_numpy().max() * 1.1))
137 |     bottom.legend(loc="upper left")
138 |     fig.supylabel("Recall@K")
139 |     fig.tight_layout()
140 |     save_figure(plt, fig, folder, stem, style)
141 | 
142 | 
143 | def run(split, out):
144 |     from m4_classifier import CATEGORY, NUMERIC   # nhập tại đây: m4_classifier cũng nhập m4_test nên nhập đầu tệp sẽ tạo vòng nhập
145 |     features = NUMERIC + CATEGORY
146 |     cfg, report = config(), path(config()["report_dir"])
147 |     out = path(out)
148 |     lock = checked_lock(split, out, cfg)
149 |     lock_digest = sha256(report / 'lock.json')
150 | 
151 |     masked, ctx, idx, _ = locked_stage(cfg, (split,))
152 |     models = {m: joblib.load(path(cfg["data_dir"]) / f"pipeline_{m.lower()}.joblib") for m in ("LR", "RF")}
153 |     models['RF'].named_steps['model'].set_params(n_jobs=1)  # cố định thứ tự cộng xác suất; không ghi lại mô hình
154 |     basket, y, scores = [], [], {m: [] for m in models}
155 |     for part, X in make_batches(masked[masked.eligible], ctx, idx, cfg["batch_size"]):
156 |         y.append(X.y.to_numpy())
157 |         keys = {"Popularity": [X.candidate_popularity], "Rules": [X.max_rule_confidence, X.candidate_popularity]}
158 |         for m, model in models.items():
159 |             scores[m].append(model.predict_proba(X[features])[:, 1])
160 |             keys[m] = [scores[m][-1]]
161 |         basket += [evaluate(part, X, *k, ks=KS).assign(method=m) for m, k in keys.items()]
162 |     basket, y = pd.concat(basket, ignore_index=True), np.concatenate(y)
163 | 
164 |     # Bảng xếp hạng (trung bình vĩ mô theo giỏ) và Recall@K kèm đường trần
165 |     mean = basket.groupby("method", sort=False).mean(numeric_only=True)
166 |     recall_k = mean[[f"R@{k}" for k in KS]]
167 |     base = basket[basket.method == "Popularity"]
168 |     ceiling = [float((np.minimum(base.n_hidden_in_C, k) / base.n_hidden).mean()) for k in KS]
169 |     # Chỉ số phân loại tại ngưỡng F1 đã khóa trên validation; toàn bộ cặp ứng viên, không lấy trung bình theo lô
170 |     classifier = pd.DataFrame([dict(method=m, **classification_metrics(y, np.concatenate(s), lock["f1_threshold"][m]))
171 |                                for m, s in scores.items()])
172 |     # Kiểm định chính: phương pháp chính so với Popularity; hai so sánh sau là bổ trợ
173 |     main = lock["main_method"]
174 |     pairs = [(main, "Popularity"), (main, "Rules"), ("LR", "RF")]
175 |     boot = pd.DataFrame([dict(**paired_bootstrap(basket, a, b, cfg["bootstrap_n"], cfg["seeds"]["bootstrap"]),
176 |                               primary=(i == 0)) for i, (a, b) in enumerate(pairs)])
177 | 
178 |     write_frame(out / f"basket_metrics_{split}.csv", basket)
179 |     write_frame(out / f"ranking_metrics_{split}.csv", mean[SHOWN].reset_index())
180 |     ceiling_row = pd.DataFrame([dict(method="Ceiling", **{f"R@{k}": c for k, c in zip(KS, ceiling)})])
181 |     write_frame(out / f"recall_at_k_{split}.csv", pd.concat([recall_k.reset_index(), ceiling_row], ignore_index=True))
182 |     write_frame(out / f"classifier_metrics_{split}.csv", classifier)
183 |     write_frame(out / f"confusion_matrix_{split}.csv", classifier[["method", "tn", "fp", "fn", "tp"]])
184 |     write_frame(out / f"paired_bootstrap_{split}.csv", boot)
185 |     figure(recall_k, ceiling, out / "figures", f"fig-recall-at-k-{split}")
186 |     write_json(out / f"results_{split}.json", dict(
187 |         split=split, baskets=int(base.shape[0]), candidate_pairs=int(len(y)), main_method=main,
188 |         lock_locked_at=lock["locked_at"], lock_sha256=lock_digest,
189 |         outputs={p.relative_to(out).as_posix(): sha256(p) for p in
190 |                  sorted([*out.glob(f"*_{split}.csv"), * (out / 'figures').glob(f'fig-recall-at-k-{split}.*')])}))
191 |     print(mean[SHOWN].round(4).to_string(), "\n", boot.round(4).to_string(index=False))
192 | 
193 | 
194 | if __name__ == "__main__":
195 |     require(sys.argv[1:2] in (["test"], ["validation"]), "Dùng: m4_test.py test | m4_test.py validation <thư mục ra>")
196 |     run(sys.argv[1], config()["report_dir"] if sys.argv[1] == "test" else sys.argv[2])
```

## Phần 6. Xuất báo cáo

### 35. `scripts/render_pdf.py`

> **Vai trò:** Render QMD bằng Quarto/XeLaTeX trong thư mục tạm; chỉ thay PDF khi render thành công.  
> **Mục trong bài:** Toàn bài · **Người viết:** Vương  
> **Đầu vào → đầu ra:** QMD, `assets/`, `references.bib` → PDF  
> **Hàm/lớp chính (dòng):** `resources` (18), `main` (37)  
> **Ghi chú:** `python scripts/render_pdf.py --no-open`  
> *80 dòng · SHA-256 `c1ca47d04115…`*

```python
 1 | """Xuất PDF bằng Quarto trong thư mục tạm; chỉ thay PDF cũ khi render thành công."""
 2 | import argparse
 3 | import json
 4 | import os
 5 | from pathlib import Path
 6 | import re
 7 | import shutil
 8 | import subprocess
 9 | import sys
10 | import tempfile
11 | import time
12 | 
13 | ROOT = Path(__file__).resolve().parent.parent
14 | SOURCE = ROOT / '2521001118_Nhom01_TieuLuan.qmd'
15 | LOG = ROOT / 'BAO CAO/Bao cao lam sach/logs/render_pdf.log'
16 | 
17 | 
18 | def resources(text):
19 |     """File khai báo trong configs/render_resources.json và file QMD trỏ tới (hình, bảng)."""
20 |     spec = json.loads((ROOT / 'configs/render_resources.json').read_text(encoding='utf-8'))
21 |     files = set(spec.get('files', []))
22 |     for pattern in spec.get('globs', []):
23 |         files.update(p.relative_to(ROOT).as_posix() for p in ROOT.glob(pattern) if p.is_file())
24 |     found = re.findall(r'!\[[^\]]*\]\(([^\n)]+)\)', text)
25 |     found += re.findall(r'\\(?:includegraphics|VerbatimInput|input)(?:\[[^\]]*\])?\{([^}]+)\}', text)
26 |     found += re.findall(r'''(?:read_csv|read_json|read_parquet|open)\(\s*["']([^"']+)["']''', text)
27 |     files.update(v.strip().strip('<>') for v in found if not v.startswith(('http', 'data:')))
28 |     for name in sorted(files):
29 |         path = (ROOT / name).resolve()
30 |         if not path.is_relative_to(ROOT) or not path.is_file():
31 |             raise FileNotFoundError(f'Thiếu tài nguyên hoặc nằm ngoài thư mục bài: {name}')
32 |         if path.stat().st_size > spec.get('max_file_bytes', 10 * 1024 * 1024):
33 |             raise ValueError(f'Tài nguyên quá lớn, cần xuất bảng nhẹ: {name}')
34 |         yield path
35 | 
36 | 
37 | def main():
38 |     sys.stdout.reconfigure(encoding='utf-8')
39 |     args = argparse.ArgumentParser(description='Xuất PDF bằng Quarto/XeLaTeX')
40 |     args.add_argument('--no-open', action='store_true')
41 |     args = args.parse_args()
42 |     candidates = [Path(os.environ.get('ProgramFiles', 'C:/Program Files')),
43 |                   Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs']
44 |     quarto = shutil.which('quarto') or next(
45 |         (str(p) for p in (b / 'Quarto/bin/quarto.exe' for b in candidates) if p.exists()), None)
46 |     if not quarto:
47 |         raise RuntimeError('Không tìm thấy Quarto CLI')
48 |     target, build = SOURCE.with_suffix('.pdf'), ROOT / (SOURCE.stem + '.build.pdf')
49 |     started = time.perf_counter()
50 |     # Quarto có thể xóa PDF cùng tên nguồn, nên render bản sao trong thư mục tạm.
51 |     with tempfile.TemporaryDirectory(prefix='quarto-build-', dir=ROOT,
52 |                                      ignore_cleanup_errors=True) as directory:
53 |         staging = Path(directory)
54 |         for name in [SOURCE.name, 'references.bib']:
55 |             shutil.copy2(ROOT / name, staging / name)
56 |         for name in ['styles', 'assets']:
57 |             shutil.copytree(ROOT / name, staging / name)
58 |         for path in resources(SOURCE.read_text(encoding='utf-8')):
59 |             (staging / path.relative_to(ROOT)).parent.mkdir(parents=True, exist_ok=True)
60 |             shutil.copy2(path, staging / path.relative_to(ROOT))
61 |         process = subprocess.run([quarto, 'render', SOURCE.name, '--to', 'pdf', '--output', build.name],
62 |                                  cwd=staging, capture_output=True, text=True, encoding='utf-8',
63 |                                  errors='replace')
64 |         if process.returncode == 0 and (staging / build.name).exists():
65 |             os.replace(staging / build.name, build)
66 |     LOG.parent.mkdir(parents=True, exist_ok=True)
67 |     LOG.write_text((process.stdout or '') + (process.stderr or ''), encoding='utf-8')
68 |     if process.returncode or not build.exists():
69 |         raise RuntimeError(f'Render thất bại; xem {LOG.relative_to(ROOT)}; PDF cũ được giữ')
70 |     try:
71 |         os.replace(build, target)
72 |     except PermissionError as exc:
73 |         raise PermissionError(f'PDF đang mở ở chương trình khác; bản mới lưu tại {build}') from exc
74 |     print(f'THÀNH CÔNG: {target}; {time.perf_counter() - started:.2f} giây')
75 |     if not args.no_open and hasattr(os, 'startfile'):
76 |         os.startfile(target)
77 | 
78 | 
79 | if __name__ == '__main__':
80 |     main()
```

### 36. `configs/render_resources.json`

> **Vai trò:** Danh sách tài nguyên nhẹ được chép vào thư mục render.  
> **Mục trong bài:** Toàn bài · **Người viết:** Vương  
> **Đầu vào → đầu ra:** —  
> *13 dòng · SHA-256 `9307deec8b6c…`*

```json
 1 | {
 2 |   "max_file_bytes": 10485760,
 3 |   "files": [],
 4 |   "globs": [
 5 |     "BAO CAO/Bao cao EDA/figures/**/*.png",
 6 |     "BAO CAO/Bao cao EDA/figures/**/*.pdf",
 7 |     "BAO CAO/Bao cao EDA/figures/**/*.svg",
 8 |     "BAO CAO/Bao cao EDA/*.csv",
 9 |     "BAO CAO/Bao cao EDA/*.json",
10 |     "BAO CAO/Bao cao EDA/*.tex"
11 |   ],
12 |   "note": "Only referenced/declared light resources are staged. Add explicit light exports from DATA/Data phai sinh to files; never copy the full data tree."
13 | }
```

## Phần 7. Kiểm thử tự động (57 test)

### 37. `tests/test_cleaning.py`

> **Vai trò:** Phân vùng, khóa ngoại, ranh giới khối (đổi kích thước khối không đổi byte đầu ra).  
> **Mục trong bài:** 3.3 · **Người viết:** —  
> **Đầu vào → đầu ra:** dữ liệu dựng tay  
> **Hàm/lớp chính (dòng):** `CleaningTests` (22)  
> *116 dòng · SHA-256 `60aa684b2f15…`*

```python
  1 | """Regression checks for partitions, foreign keys and chunk boundaries."""
  2 | import contextlib
  3 | import io
  4 | import json
  5 | from pathlib import Path
  6 | import sys
  7 | import shutil
  8 | import sqlite3
  9 | import uuid
 10 | import unittest
 11 | 
 12 | import pandas as pd
 13 | 
 14 | TESTS = Path(__file__).resolve().parent
 15 | CLEANING = TESTS.parent / 'scripts/cleaning'
 16 | sys.path.insert(0, str(CLEANING))
 17 | import clean_phong  # noqa: E402
 18 | import clean_vuong  # noqa: E402
 19 | from common import run  # noqa: E402
 20 | 
 21 | 
 22 | class CleaningTests(unittest.TestCase):
 23 |     def setUp(self):
 24 |         self.root = TESTS / ('tmp_' + uuid.uuid4().hex)
 25 |         self.root.mkdir()
 26 |         self.addCleanup(self.remove_fixture)
 27 |         self.raw = self.root / 'raw'
 28 |         self.raw.mkdir()
 29 |         tables = {
 30 |             'aisles': {'aisle_id': [1], 'aisle': ['unknown']},
 31 |             'departments': {'department_id': [1], 'department': [' Food ']},
 32 |             'products': {'product_id': [1, 2], 'product_name': ['unknown', 'Milk'],
 33 |                          'aisle_id': [1, 1], 'department_id': [1, 1]},
 34 |             'orders': {'order_id': [1, 2, 3, 4], 'user_id': [10, 10, 20, 20],
 35 |                        'eval_set': ['', 'train', 'prior', ''],
 36 |                        'order_number': ['', 8, 1, 2], 'order_dow': [0, 9, 2, 3],
 37 |                        'order_hour_of_day': [1, 2, 3, 4],
 38 |                        'days_since_prior_order': ['', 7, '', 5]},
 39 |             'order_products__prior': {'order_id': [1, 1, 3],
 40 |                                       'product_id': [1, 2, 2],
 41 |                                       'add_to_cart_order': ['', 9, 1],
 42 |                                       'reordered': [0, '?', 0]},
 43 |             'order_products__train': {'order_id': [2, 2], 'product_id': [1, 2],
 44 |                                       'add_to_cart_order': ['', 8],
 45 |                                       'reordered': [1, 1]},
 46 |         }
 47 |         for table, data in tables.items():
 48 |             pd.DataFrame(data).to_csv(self.raw / f'{table}.csv', index=False)
 49 | 
 50 |     def remove_fixture(self):
 51 |         assert self.root.resolve().parent == TESTS
 52 |         shutil.rmtree(self.root)
 53 | 
 54 |     def run_clean(self, member, size=2):
 55 |         module = clean_vuong if member == 'vuong' else clean_phong
 56 |         config = json.loads((CLEANING / f'config_{member}.json').read_text('utf-8'))
 57 |         config = {k: v for k, v in config.items() if not k.startswith('expected_')}
 58 |         config.update(input_dir=str(self.raw), output_dir=str(self.root / 'clean'),
 59 |                       report_dir=str(self.root / 'reports' / member), chunksize=size)
 60 |         with contextlib.redirect_stdout(io.StringIO()):
 61 |             return run(config, CLEANING, member, module.TABLES, module.steps)
 62 | 
 63 |     def test_both_members_independent_of_chunk_size_and_order(self):
 64 |         baseline = None
 65 |         for size in [1, 2, 3, 100]:
 66 |             for member in ['phong', 'vuong']:
 67 |                 report = self.run_clean(member, size)
 68 |                 result = json.loads((report / 'run_report.json').read_text('utf-8'))
 69 |                 self.assertTrue(result['source_hashes_unchanged'])
 70 |                 before_after = pd.read_csv(report / 'before_after.csv')
 71 |                 self.assertEqual(len(before_after['table'].unique()), 3)
 72 |                 self.assertTrue((before_after['nonmissing_final'] > 0).any())
 73 |             output = {p.name: p.read_bytes() for p in (self.root / 'clean').glob('*.csv')}
 74 |             if baseline is None:
 75 |                 baseline = output
 76 |             self.assertEqual(output, baseline)
 77 |         orders = pd.read_csv(self.root / 'clean/orders.csv')
 78 |         self.assertEqual(orders.eval_set.tolist(), ['prior', 'train', 'prior', 'test'])
 79 |         self.assertEqual(orders.order_number.tolist(), [1, 2, 1, 2])
 80 |         self.assertTrue(pd.isna(orders.loc[1, 'order_dow']))
 81 |         prior = pd.read_csv(self.root / 'clean/order_products__prior.csv')
 82 |         self.assertEqual(prior.add_to_cart_order.tolist(), [1, 2, 1])
 83 |         self.assertTrue(pd.isna(prior.loc[1, 'reordered']))
 84 |         products = pd.read_csv(self.root / 'clean/products.csv')
 85 |         self.assertTrue(pd.isna(products.loc[0, 'product_name']))
 86 | 
 87 |     def test_orphan_prior_key_rejected_without_overwriting_output(self):
 88 |         self.run_clean('vuong')
 89 |         path = self.root / 'clean/order_products__prior.csv'
 90 |         previous = path.read_bytes()
 91 |         raw = pd.read_csv(self.raw / path.name)
 92 |         raw.loc[0, 'product_id'] = 999
 93 |         raw.to_csv(self.raw / path.name, index=False)
 94 |         with self.assertRaisesRegex(ValueError, 'mồ côi'):
 95 |             self.run_clean('vuong')
 96 |         self.assertEqual(previous, path.read_bytes())
 97 | 
 98 |     def test_partition_overlap_rejected(self):
 99 |         path = self.raw / 'order_products__prior.csv'
100 |         frame = pd.read_csv(path)
101 |         frame.loc[0, 'order_id'] = 2
102 |         frame.to_csv(path, index=False)
103 |         with self.assertRaises(sqlite3.IntegrityError):
104 |             self.run_clean('phong')
105 |         self.assertFalse((self.root / 'clean/orders.csv').exists())
106 | 
107 |     def test_noncontiguous_basket_rejected(self):
108 |         path = self.raw / 'order_products__prior.csv'
109 |         frame = pd.read_csv(path).iloc[[0, 2, 1]]
110 |         frame.to_csv(path, index=False)
111 |         with self.assertRaisesRegex(ValueError, 'nhóm xuất hiện lại'):
112 |             self.run_clean('vuong', 1)
113 | 
114 | 
115 | if __name__ == '__main__':
116 |     unittest.main(verbosity=2)
```

### 38. `tests/test_m2_foundation.py`

> **Vai trò:** Chia tập, tái lập khi đảo thứ tự ID.  
> **Mục trong bài:** 3.4 · **Người viết:** —  
> **Đầu vào → đầu ra:** dữ liệu dựng tay  
> **Hàm/lớp chính (dòng):** `fixture` (16), `FoundationTests` (27)  
> *100 dòng · SHA-256 `4b00d39e18e6…`*

```python
  1 | """Small, hand-checkable G0 fixtures. No writes to the production dataset."""
  2 | 
  3 | import sys
  4 | import tempfile
  5 | import unittest
  6 | from pathlib import Path
  7 | 
  8 | import pandas as pd
  9 | 
 10 | sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
 11 | from m2_foundation import (build_baskets, canonical_split_sha256 as canonical_manifest,
 12 |                            make_split, validate_master)
 13 | from project_io import atomic_write, config
 14 | 
 15 | 
 16 | def fixture():
 17 |     return pd.DataFrame({
 18 |         "order_id": [1, 1, 1, 2, 3], "user_id": [11, 11, 11, 12, 13],
 19 |         "product_id": [1, 2, 3, 4, 5], "aisle_id": [1, 1, 2, 3, 4],
 20 |         "department_id": [3, 3, 16, 21, 4], "eval_set": ["train"] * 5,
 21 |         "product_name": [None, "b", "c", "d", "e"],
 22 |         "order_dow": pd.array([1, 1, 1, None, 6], dtype="Int8"),
 23 |         "order_hour_of_day": pd.array([6, 6, 6, None, 23], dtype="Int8"),
 24 |         "days_since_prior_order": pd.array([30, 30, 30, None, 0], dtype="Float32")})
 25 | 
 26 | 
 27 | class FoundationTests(unittest.TestCase):
 28 |     def test_split_counts_union_reproducibility(self):
 29 |         users = range(1, 131210)
 30 |         a, b = make_split(users), make_split(reversed(users))
 31 |         self.assertEqual(a.split.value_counts().to_dict(),
 32 |                          {"reference": 39363, "fit": 39363,
 33 |                           "test": 26242, "validation": 26241})
 34 |         self.assertEqual(set(a.user_id), set(users))
 35 |         self.assertFalse(a.user_id.duplicated().any())
 36 |         self.assertEqual(canonical_manifest(a), canonical_manifest(b))
 37 |         self.assertNotEqual(canonical_manifest(a), canonical_manifest(make_split(users, 43)))
 38 | 
 39 |     def test_split_small_rounding(self):
 40 |         for n in range(5, 25):
 41 |             result = make_split(range(n))
 42 |             self.assertEqual(len(result), n)
 43 |             self.assertEqual(result.split.eq("test").sum(), (n + 4) // 5)
 44 |         with self.assertRaisesRegex(ValueError, "Duplicate"):
 45 |             make_split([1, 1, 2, 3, 4])
 46 | 
 47 |     def test_baskets_missing_singleton_and_repeated_department(self):
 48 |         result = build_baskets(fixture(), config())
 49 |         self.assertEqual(result.basket_size.tolist(), [3, 1, 1])
 50 |         self.assertEqual(result.n_departments.tolist(), [2, 1, 1])
 51 |         self.assertEqual(result.n_aisles.tolist(), [2, 1, 1])
 52 |         self.assertEqual(result.hour_band.iloc[0], "06–11")
 53 |         self.assertTrue(pd.isna(result.hour_band.iloc[1]))
 54 |         self.assertEqual(result.hour_band.iloc[2], "18–23")
 55 |         self.assertTrue(pd.isna(result.days_since_prior_order.iloc[1]))
 56 | 
 57 |     def test_hour_boundaries(self):
 58 |         hours = [0, 5, 6, 11, 12, 17, 18, 23]
 59 |         base = pd.concat([fixture().iloc[[3]]] * 8, ignore_index=True)
 60 |         base["order_id"] = range(8)
 61 |         base["user_id"] = range(8)
 62 |         base["order_hour_of_day"] = pd.array(hours, dtype="Int8")
 63 |         self.assertEqual(build_baskets(base, config()).hour_band.tolist(),
 64 |                          ["00–05"] * 2 + ["06–11"] * 2 + ["12–17"] * 2 + ["18–23"] * 2)
 65 | 
 66 |     def test_reject_corrupt_keys_and_multiple_baskets(self):
 67 |         frame = fixture()
 68 |         with self.assertRaisesRegex(ValueError, "Duplicate order"):
 69 |             validate_master(pd.concat([frame, frame.iloc[[0]]]))
 70 |         frame.loc[3, "user_id"] = 11
 71 |         with self.assertRaisesRegex(ValueError, "Multiple baskets"):
 72 |             validate_master(frame)
 73 | 
 74 |     def test_reject_conflicting_na_and_invalid_hour(self):
 75 |         frame = fixture()
 76 |         frame.loc[0, "order_dow"] = pd.NA
 77 |         with self.assertRaisesRegex(ValueError, "Conflicting"):
 78 |             build_baskets(frame, config())
 79 |         frame = fixture()
 80 |         frame.loc[4, "order_hour_of_day"] = 24
 81 |         with self.assertRaisesRegex(ValueError, "Invalid domain"):
 82 |             build_baskets(frame, config())
 83 | 
 84 |     def test_failed_write_preserves_previous(self):
 85 |         with tempfile.TemporaryDirectory() as directory:
 86 |             target = Path(directory) / "result.json"
 87 |             target.write_text("old", encoding="utf-8")
 88 | 
 89 |             def broken(temp):
 90 |                 temp.write_text("incomplete", encoding="utf-8")
 91 |                 raise RuntimeError("failure")
 92 | 
 93 |             with self.assertRaises(RuntimeError):
 94 |                 atomic_write(target, broken)
 95 |             self.assertEqual(target.read_text(), "old")
 96 |             self.assertEqual(len(list(Path(directory).iterdir())), 1)
 97 | 
 98 | 
 99 | if __name__ == "__main__":
100 |     unittest.main(verbosity=2)
```

### 39. `tests/test_m2_summary.py`

> **Vai trò:** Mẫu số và giá trị thiếu của thống kê mô tả.  
> **Mục trong bài:** 3.4 · **Người viết:** —  
> **Đầu vào → đầu ra:** số tính tay  
> **Hàm/lớp chính (dòng):** `SummaryTests` (16)  
> *111 dòng · SHA-256 `d7cd8050c37b…`*

```python
  1 | """Hand-calculated fixtures for member-1 denominators and missing values."""
  2 | 
  3 | import sys
  4 | import unittest
  5 | from pathlib import Path
  6 | 
  7 | import numpy as np
  8 | import pandas as pd
  9 | 
 10 | sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"scripts"))
 11 | from m2_foundation import build_baskets
 12 | from project_io import config
 13 | from m2_eda_summary import department_display, summarize
 14 | 
 15 | 
 16 | class SummaryTests(unittest.TestCase):
 17 |     def setUp(self):
 18 |         self.cfg = config()
 19 |         self.cfg["top_n_grid"] = [1, 2, 10]
 20 |         self.ref = pd.DataFrame({
 21 |             "order_id": [1, 1, 2, 3], "user_id": [11, 11, 12, 13],
 22 |             "product_id": [1, 2, 1, 3], "aisle_id": [1, 2, 1, 3],
 23 |             "department_id": [1, 1, 1, 2], "eval_set": ["train"]*4,
 24 |             "reordered": [1., np.nan, 0., 1.],
 25 |             "order_dow": [0., 0., np.nan, 6.],
 26 |             "order_hour_of_day": [0., 0., np.nan, 23.],
 27 |             "days_since_prior_order": [np.nan, np.nan, 2., 30.],
 28 |         })
 29 |         self.depts = pd.DataFrame({"department_id": [1, 2, 3],
 30 |                                    "department": ["a", "missing", "absent"]})
 31 |         self.aisles = pd.DataFrame({"aisle_id": [1, 2, 3, 4],
 32 |                                     "aisle": ["", "b", "c", "absent"]})
 33 |         self.products = pd.DataFrame({"product_id": [1, 2, 3],
 34 |                                       "product_name": ["", "b", "c"]})
 35 | 
 36 |     def result(self):
 37 |         return summarize(self.ref, build_baskets(self.ref, self.cfg),
 38 |                          self.depts, self.aisles, self.products, self.cfg)
 39 | 
 40 |     def test_union_coverage_not_sum_of_popularities(self):
 41 |         t, _ = self.result()
 42 |         top = t["top_n_coverage"]
 43 |         self.assertEqual(top.basket_count.tolist(), [2, 2, 3])
 44 |         self.assertAlmostEqual(top.iloc[1].row_share, 0.75)
 45 |         self.assertAlmostEqual(top.iloc[1].basket_coverage, 2/3)
 46 | 
 47 |     def test_missing_and_valid_denominators(self):
 48 |         t, _ = self.result()
 49 |         row = t["department_summary"].iloc[0]
 50 |         self.assertEqual(row.reordered_valid, 2)
 51 |         self.assertAlmostEqual(row.observed_reorder_rate, 0.5)
 52 |         self.assertAlmostEqual(row.reordered_missing_pct, 100/3)
 53 |         f = t["categorical_frequencies"]
 54 |         dow = f[f.variable.eq("order_dow")]
 55 |         self.assertEqual(dow["count"].sum(), 3)
 56 |         self.assertEqual(dow.iloc[0].valid_pct, 50)
 57 |         self.assertTrue(pd.isna(dow.iloc[-1].valid_pct))
 58 | 
 59 |     def test_missing_names_and_zero_groups_preserved(self):
 60 |         t, _ = self.result()
 61 |         self.assertEqual(len(t["aisle_summary"]), 4)
 62 |         self.assertEqual(t["aisle_summary"].iloc[0].display_name,
 63 |                          "Chưa có tên (ID=1)")
 64 |         self.assertTrue(pd.isna(
 65 |             t["department_summary"].iloc[-1].observed_reorder_rate))
 66 |         self.assertEqual(t["department_summary"].iloc[1].department, "missing")
 67 | 
 68 |     def test_sample_std_quantiles_and_ranking(self):
 69 |         t, out = self.result()
 70 |         row = t["eda_summary"].iloc[0]
 71 |         self.assertAlmostEqual(row["mean"], 4/3)
 72 |         self.assertAlmostEqual(row["std"], np.sqrt(1/3))
 73 |         self.assertEqual(row.q1, 1)
 74 |         self.assertEqual(row.q3, 1.5)
 75 |         self.assertEqual(out["flagged_baskets"], 0)
 76 |         self.assertEqual(t["product_popularity"].product_id.tolist(), [1, 2, 3])
 77 | 
 78 |     def test_conflicting_order_attribute_rejected(self):
 79 |         self.ref.loc[1, "order_dow"] = np.nan
 80 |         with self.assertRaises(ValueError):
 81 |             self.result()
 82 | 
 83 |     def test_duplicate_product_rejected(self):
 84 |         self.ref = pd.concat([self.ref, self.ref.iloc[[0]]], ignore_index=True)
 85 |         with self.assertRaises(ValueError):
 86 |             self.result()
 87 | 
 88 |     def test_all_missing_frequency_and_numeric(self):
 89 |         self.ref["order_dow"] = np.nan
 90 |         self.ref["days_since_prior_order"] = np.nan
 91 |         t, _ = self.result()
 92 |         d = t["categorical_frequencies"].query("variable == 'order_dow'")
 93 |         self.assertTrue(d.valid_pct.isna().all())
 94 |         self.assertEqual(d.iloc[-1]["count"], 3)
 95 |         self.assertTrue(pd.isna(t["eda_summary"].iloc[-1]["mean"]))
 96 | 
 97 |     def test_remaining_departments_union(self):
 98 |         departments = pd.DataFrame({
 99 |             "department_id": range(1, 13), "row_count": [10]*10+[1, 1],
100 |             "display_name": [str(i) for i in range(1, 13)],
101 |             "row_share": [10/102]*10+[1/102]*2,
102 |             "basket_count": [1]*12, "basket_coverage": [1.]*12,
103 |         })
104 |         ref = pd.DataFrame({"department_id": [11, 12], "order_id": [1, 1]})
105 |         result = department_display(ref, departments, 1)
106 |         self.assertEqual(result.iloc[-1].basket_count, 1)
107 |         self.assertEqual(result.iloc[-1].basket_coverage, 1)
108 | 
109 | 
110 | if __name__ == "__main__":
111 |     unittest.main()
```

### 40. `tests/test_m2_multivariate.py`

> **Vai trò:** Trường hợp biên của bảng đa biến.  
> **Mục trong bài:** 3.5 · **Người viết:** —  
> **Đầu vào → đầu ra:** số tính tay  
> **Hàm/lớp chính (dòng):** `MultivariateTests` (11)  
> *64 dòng · SHA-256 `6e28dd3329d3…`*

```python
 1 | """Hand-computed edge cases for Ban 2 descriptive tables."""
 2 | import sys
 3 | from pathlib import Path
 4 | import unittest
 5 | import numpy as np
 6 | import pandas as pd
 7 | sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
 8 | from m2_eda_multivariate import presence_table, pair_summary, correlations, time_tables, lift_percentile
 9 | 
10 | 
11 | class MultivariateTests(unittest.TestCase):
12 |     def test_hand_calculated_pair_and_direction(self):
13 |         presence=pd.DataFrame({'1':[True,True,True,False,False], '2':[True,True,False,True,False]})
14 |         row=pair_summary(presence).query('department_a==1 and department_b==2').iloc[0]
15 |         self.assertEqual(row.n_AB,2)
16 |         self.assertAlmostEqual(row.support_AB,.4)
17 |         self.assertAlmostEqual(row.lift_AB,10/9)
18 |         self.assertAlmostEqual(row.probability_B_given_A,2/3)
19 | 
20 |     def test_lift_percentile_counts_target_pair(self):
21 |         lifts=pd.Series([0.8,1.0,1.0,1.5])
22 |         self.assertEqual(lift_percentile(lifts,1.5),100)
23 |         self.assertEqual(lift_percentile(lifts,1.0),75)
24 |         self.assertEqual(lift_percentile(lifts,0.8),25)
25 | 
26 |     def test_reject_unknown_department_and_missing_basket(self):
27 |         for reference in [pd.DataFrame({'order_id':[1],'department_id':[3]}),pd.DataFrame({'order_id':[2],'department_id':[1]})]:
28 |             with self.assertRaises(ValueError):
29 |                 presence_table(reference,pd.DataFrame({'order_id':[1]}),pd.DataFrame({'department_id':[1]}))
30 | 
31 |     def test_insufficient_pair_is_na(self):
32 |         tables,n=correlations(pd.DataFrame({'a':[1,np.nan], 'b':[2,3]}),['a','b'])
33 |         self.assertEqual(n.loc['a','b'],1)
34 |         self.assertTrue(np.isnan(tables['spearman'].loc['a','b']))
35 | 
36 |     def test_counts_do_not_overflow_and_absent_department(self):
37 |         baskets=pd.DataFrame({'order_id':range(300)})
38 |         reference=pd.DataFrame({'order_id':list(range(300))*2,'department_id':[1]*300+[1]*300})
39 |         presence=presence_table(reference,baskets,pd.DataFrame({'department_id':[1,2]}))
40 |         summary=pair_summary(presence)
41 |         row=summary.query('department_a==1 and department_b==1').iloc[0]
42 |         self.assertEqual(row.n_AB,300)
43 |         self.assertEqual(row.lift_AB,1)
44 |         self.assertTrue(np.isnan(summary.query('department_a==1 and department_b==2').iloc[0].lift_AB))
45 |         self.assertEqual(presence.shape,(300,2))
46 | 
47 |     def test_pairwise_missing_and_constant(self):
48 |         tables,n=correlations(pd.DataFrame({'a':[1,2,3],'b':[2,np.nan,6],'c':[1,1,1]}),['a','b','c'])
49 |         self.assertEqual(n.loc['a','b'],2)
50 |         self.assertAlmostEqual(tables['spearman'].loc['a','b'],1)
51 |         self.assertTrue(np.isnan(tables['pearson'].loc['a','c']))
52 | 
53 |     def test_empty_time_cells_and_missing_group(self):
54 |         baskets=pd.DataFrame({'order_dow':[0,0,np.nan], 'hour_band':['A','A',None], 'basket_size':[1,3,5]})
55 |         tables,hours=time_tables(baskets,{'hour_labels':['A','B'],'min_group_n':30,'quantile_interpolation':'linear'})
56 |         self.assertEqual(tables['median'].loc[0,'A'],2)
57 |         self.assertEqual(tables['count'].loc[0,'B'],0)
58 |         self.assertTrue(np.isnan(tables['median'].loc[0,'B']))
59 |         self.assertEqual(hours.N.sum(),3)
60 |         self.assertEqual(hours.loc[hours.hour_band=='missing','N'].iloc[0],1)
61 | 
62 | 
63 | if __name__=='__main__':
64 |     unittest.main(verbosity=2)
```

### 41. `tests/test_m2_hypotheses.py`

> **Vai trò:** Chi-square/Fisher và Holm trên bảng mẫu.  
> **Mục trong bài:** 3.6 · **Người viết:** —  
> **Đầu vào → đầu ra:** `tests/fixtures/m2_contingency_cases.json`  
> **Hàm/lớp chính (dòng):** `HypothesisTests` (9)  
> *30 dòng · SHA-256 `a60d79ba7f1b…`*

```python
 1 | import sys,json,unittest
 2 | from pathlib import Path
 3 | import numpy as np
 4 | root=Path(__file__).resolve().parents[1]
 5 | sys.path.insert(0,str(root/'scripts'))
 6 | from m2_hypothesis_tests import test_table,holm
 7 | 
 8 | 
 9 | class HypothesisTests(unittest.TestCase):
10 |     def test_hand_computed_tables(self):
11 |         fixture=json.loads((root/'tests/fixtures/m2_contingency_cases.json').read_text())
12 |         cfg=json.loads((root/'configs/hypotheses_config.json').read_text())
13 |         for case in fixture['cases']:
14 |             with self.subTest(case=case['name']):
15 |                 result,expected=test_table(case['counts'],cfg)
16 |                 self.assertEqual(result['method'],case['method'])
17 |                 for source,target in [('p','p_raw'),('V','cramers_v'),('chi2','chi2_pearson'),('difference_pp','difference_pp')]:
18 |                     if source in case:
19 |                         if case[source] is None:self.assertTrue(np.isnan(result[target]))
20 |                         else:self.assertAlmostEqual(result[target],case[source])
21 |                 if 'expected' in case:np.testing.assert_allclose(expected,case['expected'])
22 |     def test_holm_keeps_family_and_original_order(self):
23 |         np.testing.assert_allclose(holm([.01,.04,.03]),[.03,.06,.06])
24 |         np.testing.assert_allclose(holm([.01,1,.03]),[.03,1,.06])
25 |     def test_invalid_counts(self):
26 |         for table in ([[1,-1],[2,3]],[[.5,1],[1,2]],[[0,0],[0,0]]):
27 |             with self.assertRaises(ValueError):test_table(table,{})
28 | 
29 | 
30 | if __name__=='__main__':unittest.main(verbosity=2)
```

### 42. `tests/fixtures/m2_contingency_cases.json`

> **Vai trò:** Các bảng 2 × 2 mẫu cho kiểm thử kiểm định.  
> **Mục trong bài:** 3.6 · **Người viết:** —  
> **Đầu vào → đầu ra:** —  
> *12 dòng · SHA-256 `9168cb52a745…`*

```json
 1 | {
 2 |   "scope": "Synthetic hand-checkable fixtures only; never thesis results",
 3 |   "axis_order": "rows A=0,1; columns B=0,1",
 4 |   "cases": [
 5 |     {"name": "independent", "counts": [[10, 10], [10, 10]], "N": 40, "method": "chi_square", "expected": [[10, 10], [10, 10]], "chi2": 0, "p": 1, "V": 0},
 6 |     {"name": "association", "counts": [[30, 10], [10, 30]], "N": 80, "method": "chi_square", "expected": [[20, 20], [20, 20]], "chi2": 20, "V": 0.5, "difference_pp": 50},
 7 |     {"name": "sparse", "counts": [[1, 0], [0, 1]], "N": 2, "method": "fisher", "expected": [[0.5, 0.5], [0.5, 0.5]], "p": 1},
 8 |     {"name": "constant", "counts": [[10, 5], [0, 0]], "N": 15, "method": "not_testable", "p": null, "V": null}
 9 |   ],
10 |   "holm": {"p_raw": [0.01, 0.04, 0.03], "p_adjusted": [0.03, 0.06, 0.06]},
11 |   "holm_with_untestable": {"internal_p": [0.01, 1.0, 0.03], "internal_adjusted": [0.03, 1.0, 0.06], "reported_adjusted": [0.03, null, 0.06]}
12 | }
```

### 43. `tests/test_m4_data.py`

> **Vai trò:** Phép che, danh mục C, khai phá luật.  
> **Mục trong bài:** 4.1–4.3 · **Người viết:** —  
> **Đầu vào → đầu ra:** dữ liệu dựng tay  
> **Hàm/lớp chính (dòng):** `MaskTests` (21), `CatalogAndRulesTests` (36), `MaskConfigTests` (63), `FeatureTests` (90)  
> *131 dòng · SHA-256 `b8d1a87ccd77…`*

```python
  1 | """Kiểm thử phần dữ liệu Chương 4: phép che, danh mục C, khai phá luật (dữ liệu dựng tay)."""
  2 | import sys
  3 | import unittest
  4 | from pathlib import Path
  5 | 
  6 | import pandas as pd
  7 | 
  8 | sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
  9 | import numpy as np
 10 | 
 11 | from m4_common import (M, basket_matrix, basket_features, catalog, check_mask, context, evaluate, index_rules,
 12 |                        itemset_signature, make_batches, mask, mask_params, max_support_gap, mine, rules,
 13 |                        sample_negatives, worst_support_gap)
 14 | 
 15 | REFERENCE = pd.DataFrame({  # 4 giỏ; giỏ 4 không chứa sản phẩm nào của Top-2
 16 |     "order_id": [1, 1, 2, 2, 3, 4],
 17 |     "product_id": [10, 20, 10, 20, 10, 30],
 18 |     "department_id": [1, 2, 1, 2, 1, 3]})
 19 | 
 20 | 
 21 | class MaskTests(unittest.TestCase):
 22 |     def test_hidden_count_and_partition(self):
 23 |         for k, h in [(1, 0), (2, 1), (5, 1), (10, 2), (11, 2), (20, 4)]:
 24 |             items = list(range(100, 100 + k))
 25 |             observed, hidden = mask(items, order_id=7)
 26 |             self.assertEqual(len(hidden), h)
 27 |             self.assertFalse(set(observed) & set(hidden))
 28 |             self.assertEqual(sorted(observed + hidden), items)
 29 | 
 30 |     def test_same_seed_and_order_same_mask(self):
 31 |         items = list(range(30))
 32 |         self.assertEqual(mask(items, 5), mask(items, 5))
 33 |         self.assertNotEqual(mask(items, 5), mask(items, 6))
 34 | 
 35 | 
 36 | class CatalogAndRulesTests(unittest.TestCase):
 37 |     def test_catalog_rank_ties_and_denominator(self):
 38 |         c = catalog(REFERENCE)
 39 |         self.assertEqual(c.product_id.tolist(), [10, 20, 30])  # 3 giỏ, 2 giỏ, 1 giỏ
 40 |         self.assertAlmostEqual(c.popularity.iloc[0], 3 / 4)    # mẫu số = 4 giỏ reference
 41 |         ties = catalog(REFERENCE.assign(product_id=[20, 10, 20, 10, 20, 30]))
 42 |         self.assertEqual(ties.product_id.tolist()[:2], [20, 10])
 43 | 
 44 |     def test_empty_rows_kept_and_algorithms_agree(self):
 45 |         m = basket_matrix(REFERENCE, [10, 20])
 46 |         self.assertEqual(m.shape, (4, 2))                      # giỏ 4 là hàng toàn 0
 47 |         a, f = itemset_signature(mine(m, "apriori", 2, 2)), itemset_signature(mine(m, "fpgrowth", 2, 2))
 48 |         self.assertEqual(max_support_gap(a, f), 0.0)
 49 |         self.assertEqual(a[(10, 20)], 0.5)
 50 | 
 51 |     def test_support_gap_detects_small_difference_and_missing_itemset(self):
 52 |         self.assertAlmostEqual(max_support_gap({(1,): 0.5}, {(1,): 0.500001}), 1e-6)
 53 |         self.assertIsNone(max_support_gap({(1,): 0.5}, {(2,): 0.5}))
 54 | 
 55 |     def test_worst_gap_checks_every_run_not_only_the_first(self):
 56 |         same = {(1,): 0.5}
 57 |         self.assertEqual(worst_support_gap([same, same, same]), 0.0)
 58 |         self.assertAlmostEqual(worst_support_gap([same, same, {(1,): 0.500001}]), 1e-6)
 59 |         self.assertIsNone(worst_support_gap([same, same, {(2,): 0.5}]))
 60 |         self.assertIsNone(worst_support_gap([]))
 61 | 
 62 | 
 63 | class MaskConfigTests(unittest.TestCase):
 64 |     def test_stored_mask_must_match_config(self):
 65 |         cfg = {"seeds": {"mask": 42}, "hidden_share": 0.2}
 66 |         check_mask({"mask": mask_params(cfg)}, cfg)
 67 |         for changed in ({"seeds": {"mask": 43}, "hidden_share": 0.2},
 68 |                         {"seeds": {"mask": 42}, "hidden_share": 0.3}):
 69 |             with self.assertRaises(ValueError):
 70 |                 check_mask({"mask": mask_params(cfg)}, changed)
 71 | 
 72 |     def test_rule_metrics_by_hand(self):
 73 |         r = rules(mine(basket_matrix(REFERENCE, [10, 20]), "fpgrowth", 2, 2), 4, 0.5)
 74 |         row = r.loc[r.consequent == 20].iloc[0]                # {10} -> 20
 75 |         self.assertEqual((row.antecedent, row.n_antecedent, row.n_both), ([10], 3, 2))
 76 |         self.assertAlmostEqual(row.confidence, 2 / 3)
 77 |         self.assertAlmostEqual(row.lift, (2 / 4) / ((3 / 4) * (2 / 4)))
 78 | 
 79 | 
 80 | RANKED = pd.DataFrame({"product_id": [1, 2, 3, 4], "popularity": [0.4, 0.3, 0.2, 0.1],
 81 |                        "department_id": [1, 1, 2, 2], "rank": [1, 2, 3, 4]})
 82 | DEPT = np.zeros(M, dtype=int)
 83 | DEPT[[1, 2, 3, 4, 9]] = [1, 1, 2, 2, 1]
 84 | CTX = context(RANKED, 4, DEPT)
 85 | RULES = pd.DataFrame({"antecedent": [[1], [1, 3], [3]], "consequent": [2, 2, 4], "confidence": [0.5, 0.8, 0.3],
 86 |                       "lift": [2.0, 3.0, 1.5]})
 87 | INDEX = index_rules(RULES, CTX)
 88 | 
 89 | 
 90 | class FeatureTests(unittest.TestCase):
 91 |     def test_rule_features_by_hand_and_no_rule_is_zero(self):
 92 |         f = basket_features([1, 3, 9], CTX, INDEX)        # 9 nằm ngoài C; 1 và 3 bị loại khỏi ứng viên
 93 |         self.assertEqual(f["product_id"].tolist(), [2, 4])
 94 |         self.assertEqual(f["matching_rule_count"].tolist(), [2, 1])   # {1}->2 và {1,3}->2; {3}->4
 95 |         self.assertEqual(f["max_rule_confidence"].tolist(), [0.8, 0.3])
 96 |         self.assertEqual(f["max_rule_lift"].tolist(), [3.0, 1.5])
 97 |         self.assertEqual(f["same_department_count"].tolist(), [2, 1])  # ngành 1: {1, 9}; ngành 2: {3}
 98 |         self.assertEqual(f["observed_basket_size"].tolist(), [3, 3])
 99 |         none = basket_features([9], CTX, INDEX)
100 |         for name in ("matching_rule_count", "max_rule_confidence", "max_rule_lift"):
101 |             self.assertEqual(none[name].tolist(), [0] * 4)
102 | 
103 |     def test_hidden_items_do_not_change_features(self):
104 |         a = pd.DataFrame({"order_id": [1], "user_id": [1], "observed": [[1, 3]], "hidden": [[2]]})
105 |         (_, x), (_, y) = (next(make_batches(a.assign(hidden=[h]), CTX, INDEX, 10)) for h in ([2], [4]))
106 |         pd.testing.assert_frame_equal(x.drop(columns="y"), y.drop(columns="y"))
107 |         self.assertEqual((x.y.tolist(), y.y.tolist()), ([True, False], [False, True]))
108 | 
109 |     def test_metrics_by_hand_and_empty_candidates(self):
110 |         part = pd.DataFrame({"order_id": [1, 2], "user_id": [1, 2], "observed": [[3], [1, 2, 3, 4]],
111 |                              "hidden": [[2, 99], [9]]})
112 |         _, X = next(make_batches(part, CTX, INDEX, 10))   # giỏ 2 không còn ứng viên nào
113 |         m = evaluate(part, X, X.candidate_popularity)
114 |         self.assertEqual(m.loc[0, ["hits@5", "P@5", "R@5", "R@10_ceiling"]].tolist(), [1, 0.2, 0.5, 0.5])
115 |         self.assertEqual(m.loc[1, ["hits@10", "R@10", "HR@10"]].tolist(), [0, 0, 0])
116 | 
117 |     def test_ties_break_by_product_id(self):
118 |         part = pd.DataFrame({"order_id": [1], "user_id": [1], "observed": [[9]], "hidden": [[1]]})
119 |         _, X = next(make_batches(part, CTX, INDEX, 10))
120 |         self.assertEqual(evaluate(part, X, np.zeros(len(X)), ks=(1, 2))["hits@1"].tolist(), [1])  # 1 trước 2, 3, 4
121 | 
122 |     def test_negative_sampling_keeps_positives(self):
123 |         part = pd.DataFrame({"order_id": [1], "user_id": [1], "observed": [[9]], "hidden": [[2]]})
124 |         _, X = next(make_batches(part, CTX, INDEX, 10))
125 |         s = sample_negatives(part, X, 2, 43)
126 |         self.assertEqual((s.y.sum(), (~s.y).sum(), s.order_id.unique().tolist()), (1, 2, [1]))
127 |         pd.testing.assert_frame_equal(s, sample_negatives(part, X, 2, 43))
128 | 
129 | 
130 | if __name__ == "__main__":
131 |     unittest.main()
```

### 44. `tests/test_m4_model.py`

> **Vai trò:** Pipeline, chỉ số, bootstrap.  
> **Mục trong bài:** 4.3–4.4 · **Người viết:** Phong  
> **Đầu vào → đầu ra:** số tính tay, dữ liệu tự tạo  
> **Hàm/lớp chính (dòng):** `ModelTests` (14)  
> *102 dòng · SHA-256 `5ab295743319…`*

```python
  1 | """Kiểm thử phần Phong với số tính tay/dữ liệu tự tạo; không đọc dữ liệu nghiên cứu."""
  2 | import sys
  3 | import unittest
  4 | from pathlib import Path
  5 | 
  6 | import numpy as np
  7 | import pandas as pd
  8 | 
  9 | sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
 10 | from m4_classifier import CATEGORY, NUMERIC, build_pipeline, fit_grid, synthetic_data
 11 | from m4_test import best_f1_threshold, classification_metrics, paired_bootstrap
 12 | 
 13 | 
 14 | class ModelTests(unittest.TestCase):
 15 |     def test_preprocessing_fit_only_and_unknown_category(self):
 16 |         x, y = synthetic_data(100)
 17 |         for method in ['LR', 'RF']:
 18 |             model = build_pipeline(method, {'n_estimators': 5} if method == 'RF' else {}).fit(x, y)
 19 |             transform = model['transform']
 20 |             imputer = transform.named_transformers_['numeric']['impute']
 21 |             np.testing.assert_allclose(imputer.statistics_, x[NUMERIC].median())
 22 |             category = transform.named_transformers_['category']
 23 |             self.assertNotIn(99, category['encode'].categories_[0])
 24 |             modified = x.copy()
 25 |             modified[NUMERIC[0]], modified[CATEGORY[0]] = 1000, 99
 26 |             before = imputer.statistics_.copy()
 27 |             self.assertTrue(np.isfinite(model.predict_proba(modified)).all())
 28 |             np.testing.assert_array_equal(before, imputer.statistics_)
 29 |             if method == 'LR':
 30 |                 scale = transform.named_transformers_['numeric']['scale']
 31 |                 np.testing.assert_allclose(scale.mean_, x[NUMERIC].fillna(x[NUMERIC].median()).mean())
 32 |             else:
 33 |                 self.assertNotIn('scale', transform.named_transformers_['numeric'].named_steps)
 34 |             # ID và nhãn thêm vào không thay dự đoán.
 35 |             np.testing.assert_array_equal(model.predict_proba(x),
 36 |                                           model.predict_proba(x.assign(user_id=999, y=1)))
 37 | 
 38 |     def test_ablation_columns(self):
 39 |         x, y = synthetic_data(100)
 40 |         for group, forbidden in [('no_rules', NUMERIC[1:4]),
 41 |                                   ('no_department', [NUMERIC[-1], CATEGORY[0]])]:
 42 |             model = build_pipeline('LR', group=group).fit(x, y)
 43 |             names = model['transform'].get_feature_names_out()
 44 |             self.assertFalse(any(c in name for c in forbidden for name in names))
 45 | 
 46 |     def test_metrics_by_hand(self):
 47 |         result = classification_metrics([0, 0, 1, 1], [0.1, 0.8, 0.4, 0.9], 0.5)
 48 |         for key in ['accuracy', 'precision', 'recall', 'f1']:
 49 |             self.assertEqual(result[key], 0.5)
 50 |         self.assertEqual([result[k] for k in ['tn', 'fp', 'fn', 'tp']], [1, 1, 1, 1])
 51 |         self.assertEqual(result['roc_auc'], 0.75)
 52 |         self.assertAlmostEqual(result['average_precision'], 5 / 6)
 53 |         self.assertIsNone(classification_metrics([0, 0], [0.1, 0.3], 0.5)['roc_auc'])
 54 |         self.assertIsNone(classification_metrics([0, 0], [0.1, 0.3], 0.5)['average_precision'])
 55 |         with self.assertRaises(ValueError):
 56 |             classification_metrics([0, 1], [0.1, np.nan], 0.5)
 57 | 
 58 |     def test_f1_threshold_exhaustive(self):
 59 |         y, scores = [0, 1, 0, 1, 1], [0.1, 0.2, 0.2, 0.6, 0.8]
 60 |         expected = max(scores, key=lambda t: (classification_metrics(y, scores, t)['f1'], t))
 61 |         self.assertEqual(best_f1_threshold(y, scores), expected)
 62 |         with self.assertRaises(ValueError):
 63 |             best_f1_threshold([0, 0], [0.1, 0.2])
 64 | 
 65 |     def test_bootstrap_pairing_and_edges(self):
 66 |         frame = pd.DataFrame({'user_id': [1, 2, 3] * 2, 'order_id': [11, 12, 13] * 2,
 67 |                               'method': ['A'] * 3 + ['B'] * 3,
 68 |                               'R@10': [0.5, 0.75, 1, 0, 0.25, 0.5]})
 69 |         result = paired_bootstrap(frame, 'A', 'B')
 70 |         self.assertEqual((result['difference'], result['ci_low'], result['ci_high']), (0.5, 0.5, 0.5))
 71 |         self.assertEqual(result, paired_bootstrap(frame.sample(frac=1, random_state=9), 'A', 'B'))
 72 |         same = paired_bootstrap(frame, 'A', 'A')
 73 |         self.assertEqual((same['ci_low'], same['ci_high']), (0, 0))
 74 |         reverse = paired_bootstrap(frame, 'B', 'A')
 75 |         self.assertEqual(reverse['difference'], -0.5)
 76 |         for invalid in [frame.iloc[:-1], pd.concat([frame, frame.iloc[:1]]),
 77 |                         frame.assign(**{'R@10': np.nan})]:
 78 |             with self.assertRaises(ValueError):
 79 |                 paired_bootstrap(invalid, 'A', 'B')
 80 | 
 81 |     def test_bootstrap_matches_seeded_reference(self):
 82 |         frame = pd.DataFrame({'user_id': [1, 2, 3] * 2, 'order_id': [11, 12, 13] * 2,
 83 |                               'method': ['A'] * 3 + ['B'] * 3, 'R@10': [1, 0, 0.5, 0, 1, 0]})
 84 |         rng = np.random.default_rng(42)
 85 |         indices = rng.integers(0, 3, (2000, 3))
 86 |         expected = np.quantile(np.array([1, -1, 0.5])[indices].mean(axis=1), [0.025, 0.975])
 87 |         result = paired_bootstrap(frame, 'A', 'B')
 88 |         np.testing.assert_allclose([result['ci_low'], result['ci_high']], expected)
 89 | 
 90 |     def test_grid_selects_fastest_within_tolerance(self):
 91 |         x, y = synthetic_data(100)
 92 |         recalls, seconds = [0.1, 0.2, 0.199, 0.15], [1, 3, 2, 0.1]
 93 |         def evaluate(model):
 94 |             i = [0.01, 0.1, 1, 10].index(model['model'].C)
 95 |             return dict(recall_at_10=recalls[i], inference_seconds=seconds[i])
 96 |         model, table = fit_grid(x, y, 'LR', evaluate)
 97 |         self.assertEqual(model['model'].C, 1)
 98 |         self.assertEqual(table.selected.sum(), 1)
 99 | 
100 | 
101 | if __name__ == '__main__':
102 |     unittest.main()
```

### 45. `tests/test_m4_interpret.py`

> **Vai trò:** Importance và hệ số LR.  
> **Mục trong bài:** 4.5 · **Người viết:** Phong  
> **Đầu vào → đầu ra:** dữ liệu tự tạo  
> **Hàm/lớp chính (dòng):** `InterpretTests` (14)  
> *61 dòng · SHA-256 `ae137248a1da…`*

```python
 1 | """Kiểm diễn giải trên dữ liệu tự tạo, không mở dữ liệu nghiên cứu."""
 2 | import sys
 3 | import unittest
 4 | from pathlib import Path
 5 | 
 6 | import numpy as np
 7 | import pandas as pd
 8 | 
 9 | sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
10 | from m4_classifier import NUMERIC, CATEGORY, build_pipeline, synthetic_data
11 | from m4_interpret import importance_table, lr_coefficients, sample_baskets
12 | 
13 | 
14 | class InterpretTests(unittest.TestCase):
15 |     def test_coefficients_reconstruct_log_odds(self):
16 |         x, y = synthetic_data(100)
17 |         model = build_pipeline('LR').fit(x, y)
18 |         table = lr_coefficients(model)
19 |         self.assertEqual(table.feature.iloc[:-1].tolist(), model['transform'].get_feature_names_out().tolist())
20 |         self.assertEqual(table.kind.eq('numeric_1_sd').sum(), 6)
21 |         reconstructed = model['transform'].transform(x) @ table.coefficient.iloc[:-1].to_numpy() + table.coefficient.iloc[-1]
22 |         np.testing.assert_allclose(reconstructed, model.decision_function(x))
23 | 
24 |     def test_importance_reproducible_and_model_unchanged(self):
25 |         x, y = synthetic_data(100)
26 |         validation, yv = synthetic_data(80, 43)
27 |         validation[NUMERIC[3]] = 2  # cột hằng không thể mất AP khi hoán vị
28 |         for method in ['LR', 'RF']:
29 |             model = build_pipeline(method, {'n_estimators': 5} if method == 'RF' else {}).fit(x, y)
30 |             before = model.predict_proba(validation)
31 |             table, raw, base = importance_table(model, validation, yv, method, repeats=3)
32 |             again, raw_again, _ = importance_table(model, validation, yv, method, repeats=3)
33 |             pd.testing.assert_frame_equal(table, again)
34 |             pd.testing.assert_frame_equal(raw, raw_again)
35 |             self.assertEqual(table.feature.tolist(), NUMERIC + CATEGORY)
36 |             self.assertEqual(len(raw), 21)
37 |             self.assertEqual(table.loc[table.feature.eq(NUMERIC[3]), 'ap_decrease_mean'].iloc[0], 0)
38 |             for row in table.itertuples():
39 |                 values = raw.loc[raw.feature.eq(row.feature), 'ap_decrease']
40 |                 self.assertAlmostEqual(row.ap_decrease_mean, values.mean())
41 |                 self.assertAlmostEqual(row.ap_decrease_std, values.std(ddof=0))
42 |             np.testing.assert_array_equal(before, model.predict_proba(validation))
43 |             self.assertTrue(0 <= base <= 1)
44 | 
45 |     def test_sampling_keeps_whole_baskets(self):
46 |         frame = pd.DataFrame({'order_id': np.repeat(np.arange(20), 3), 'product_id': list(range(3)) * 20})
47 |         sample = sample_baskets(frame, 5)
48 |         self.assertEqual(len(sample), 15)
49 |         self.assertTrue(sample.groupby('order_id').size().eq(3).all())
50 |         self.assertEqual(set(sample.order_id), set(sample_baskets(frame.sample(frac=1), 5).order_id))
51 |         self.assertEqual(len(sample_baskets(frame)), len(frame))
52 | 
53 |     def test_reject_one_class_importance(self):
54 |         x, y = synthetic_data(50)
55 |         model = build_pipeline('LR').fit(x, y)
56 |         with self.assertRaises(ValueError):
57 |             importance_table(model, x, np.zeros(len(x)), 'LR')
58 | 
59 | 
60 | if __name__ == '__main__':
61 |     unittest.main()
```

### 46. `tests/test_m4_environment.py`

> **Vai trò:** Thư viện khai phá, tiền xử lý và hai classifier chạy được trên dữ liệu nhỏ.  
> **Mục trong bài:** 4.3 · **Người viết:** Phong  
> **Đầu vào → đầu ra:** dữ liệu tự tạo  
> **Hàm/lớp chính (dòng):** `M4EnvironmentTests` (17)  
> *63 dòng · SHA-256 `9fadab7ca92c…`*

```python
 1 | """Kiem tra moi truong M4 bang du lieu tu tao; khong doc du lieu nghien cuu."""
 2 | import unittest
 3 | 
 4 | import numpy as np
 5 | import pandas as pd
 6 | import psutil
 7 | from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
 8 | from sklearn.compose import ColumnTransformer
 9 | from sklearn.ensemble import RandomForestClassifier
10 | from sklearn.impute import SimpleImputer
11 | from sklearn.linear_model import LogisticRegression
12 | from sklearn.metrics import average_precision_score, roc_auc_score
13 | from sklearn.pipeline import Pipeline
14 | from sklearn.preprocessing import OneHotEncoder, StandardScaler
15 | 
16 | 
17 | class M4EnvironmentTests(unittest.TestCase):
18 |     def test_synthetic_mining_and_classifier_pipeline(self):
19 |         """Thu vien khai pha, tien xu ly va hai classifier chay tren fixture."""
20 |         baskets = pd.DataFrame({
21 |             'a': [True, True, False, True],
22 |             'b': [True, False, True, True],
23 |             'c': [False, True, True, True],
24 |         }).astype(pd.SparseDtype(bool, False))
25 |         outputs = [fn(baskets, min_support=0.5, use_colnames=True, max_len=2)
26 |                    for fn in (apriori, fpgrowth)]
27 |         normalize = lambda df: {tuple(sorted(r.itemsets)): r.support
28 |                                 for r in df.itertuples()}
29 |         self.assertEqual(normalize(outputs[0]), normalize(outputs[1]))
30 |         rules = association_rules(outputs[1], num_itemsets=len(baskets),
31 |                                   metric='confidence', min_threshold=0.5)
32 |         self.assertGreater(len(rules), 0)
33 |         x = pd.DataFrame({'size': [1., 2., 3., 4., np.nan, 6., 7., 8.],
34 |                           'department': ['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b']})
35 |         y = np.array([0, 0, 0, 1, 0, 1, 1, 1])
36 |         validation = pd.DataFrame({'size': [100., np.nan], 'department': ['new', 'a']})
37 |         for estimator in [LogisticRegression(solver='lbfgs', max_iter=1000),
38 |                           RandomForestClassifier(n_estimators=10, random_state=42, n_jobs=1)]:
39 |             numeric = [('impute', SimpleImputer(strategy='median'))]
40 |             if isinstance(estimator, LogisticRegression):
41 |                 numeric.append(('scale', StandardScaler()))
42 |             transform = ColumnTransformer([
43 |                 ('numeric', Pipeline(numeric), ['size']),
44 |                 ('category', OneHotEncoder(handle_unknown='ignore'), ['department'])])
45 |             model = Pipeline([('transform', transform), ('model', estimator)])
46 |             model.fit(x, y)
47 |             if isinstance(estimator, LogisticRegression):
48 |                 scaler = model['transform'].named_transformers_['numeric']['scale']
49 |                 before = scaler.mean_.copy()
50 |                 np.testing.assert_allclose(before, [x['size'].fillna(x['size'].median()).mean()])
51 |             probabilities = model.predict_proba(validation)[:, 1]
52 |             self.assertTrue(np.isfinite(probabilities).all())
53 |             self.assertTrue(((probabilities >= 0) & (probabilities <= 1)).all())
54 |             if isinstance(estimator, LogisticRegression):
55 |                 np.testing.assert_array_equal(before, scaler.mean_)
56 |             scores = model.predict_proba(x)[:, 1]
57 |             self.assertTrue(np.isfinite(average_precision_score(y, scores)))
58 |             self.assertTrue(np.isfinite(roc_auc_score(y, scores)))
59 |         self.assertGreater(psutil.Process().memory_info().rss, 0)
60 | 
61 | 
62 | if __name__ == '__main__':
63 |     unittest.main()
```

### 47. `tests/test_m4_gate.py`

> **Vai trò:** Cổng khóa từ chối khi tệp lệch hash hoặc test đã bắt đầu.  
> **Mục trong bài:** 4.4 · **Người viết:** Phong  
> **Đầu vào → đầu ra:** thư mục tạm  
> **Hàm/lớp chính (dòng):** `GateTests` (19)  
> *102 dòng · SHA-256 `bd210f7cd17f…`*

```python
  1 | """Cổng khóa dùng thư mục tạm và dữ liệu tự tạo; không đọc test nghiên cứu."""
  2 | import json
  3 | import sys
  4 | import tempfile
  5 | import unittest
  6 | from pathlib import Path
  7 | from unittest.mock import patch
  8 | 
  9 | import numpy as np
 10 | import pandas as pd
 11 | 
 12 | sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
 13 | import m4_test as module
 14 | from m4_classifier import build_pipeline, synthetic_data
 15 | from m4_common import M, context, index_rules
 16 | from project_io import sha256
 17 | 
 18 | 
 19 | class GateTests(unittest.TestCase):
 20 |     def test_lock_rejects_tampering_missing_approval_and_repeat(self):
 21 |         with tempfile.TemporaryDirectory() as folder:
 22 |             root = Path(folder)
 23 |             resolve = lambda p: (root / p).resolve()
 24 |             cfg = {'report_dir': 'report'}
 25 |             report = resolve('report')
 26 |             report.mkdir()
 27 |             names = module.CODE_FILES + ['configs/m4_model.json', 'DATA/Data phai sinh/M4/hashes.json',
 28 |                                         'DATA/Data đã làm sạch/master_train.parquet', 'fixture.bin']
 29 |             for name in names:
 30 |                 target = resolve(name)
 31 |                 target.parent.mkdir(parents=True, exist_ok=True)
 32 |                 target.write_text('fixture', encoding='utf-8')
 33 |             lock = dict(stage_A={'top_n': 3}, main_method='RF', f1_threshold={'LR': .5, 'RF': .5},
 34 |                         files={name: sha256(resolve(name)) for name in names})
 35 |             record = dict(stage_A=lock['stage_A'], files={'fixture.bin': lock['files']['fixture.bin']})
 36 |             def save():
 37 |                 (report / 'lock.json').write_text(json.dumps(lock), encoding='utf-8')
 38 |             save()
 39 |             with patch.object(module, 'path', side_effect=resolve), patch.object(module, 'check_hashes', return_value=record):
 40 |                 with self.assertRaises(ValueError):
 41 |                     module.checked_lock('test', report, cfg)  # chưa duyệt
 42 |                 lock['approvals'] = {'Phong': True, 'Vuong': True}
 43 |                 save()
 44 |                 resolve('fixture.bin').write_text('changed', encoding='utf-8')
 45 |                 with self.assertRaises(ValueError):
 46 |                     module.checked_lock('test', report, cfg)
 47 |                 resolve('fixture.bin').write_text('fixture', encoding='utf-8')
 48 |                 digest = lock['files'].pop('scripts/m4_test.py')
 49 |                 save()
 50 |                 with self.assertRaises(ValueError):
 51 |                     module.checked_lock('test', report, cfg)
 52 |                 lock['files']['scripts/m4_test.py'] = digest
 53 |                 save()
 54 |                 with self.assertRaises(ValueError):
 55 |                     module.checked_lock('test', resolve('other'), cfg)
 56 |                 self.assertFalse((report / 'test_started.json').exists())
 57 |                 module.checked_lock('test', report, cfg)
 58 |                 self.assertTrue((report / 'test_started.json').exists())
 59 |                 with self.assertRaises(FileExistsError):
 60 |                     module.checked_lock('test', report, cfg)
 61 | 
 62 |     def test_synthetic_scoring_outputs_and_primary_self_comparison(self):
 63 |         x, y = synthetic_data(80)
 64 |         models = {m: build_pipeline(m, {'n_estimators': 5} if m == 'RF' else {}).fit(x, y)
 65 |                   for m in ['LR', 'RF']}
 66 |         ranked = pd.DataFrame(dict(product_id=[1, 2, 3], popularity=[.5, .3, .2],
 67 |                                     department_id=[1, 1, 2], rank=[1, 2, 3]))
 68 |         dept = np.zeros(M, int)
 69 |         dept[[1, 2, 3]] = [1, 1, 2]
 70 |         ctx = context(ranked, 3, dept)
 71 |         rules = pd.DataFrame(dict(antecedent=[[1]], consequent=[2], confidence=[.6], lift=[2]))
 72 |         frame = pd.DataFrame(dict(order_id=[1, 2], user_id=[1, 2], eligible=[True, True],
 73 |                                   observed=[[1], [3]], hidden=[[2], [1, 99]]))
 74 |         with tempfile.TemporaryDirectory() as folder:
 75 |             root = Path(folder)
 76 |             cfg = dict(report_dir='report', data_dir='data', batch_size=1, bootstrap_n=20, seeds={'bootstrap': 42})
 77 |             lock = dict(main_method='Popularity', f1_threshold={'LR': .5, 'RF': .5}, locked_at='fixture')
 78 |             (root / 'report').mkdir()
 79 |             (root / 'report/lock.json').write_text(json.dumps(lock))
 80 |             with patch.object(module, 'path', side_effect=lambda p: (root / p).resolve()), \
 81 |                  patch.object(module, 'config', return_value=cfg), \
 82 |                  patch.object(module, 'checked_lock', return_value=lock), \
 83 |                  patch.object(module, 'locked_stage', return_value=(frame, ctx, index_rules(rules, ctx), {})), \
 84 |                  patch.object(module.joblib, 'load', side_effect=lambda p: models['LR' if 'lr' in p.name else 'RF']), \
 85 |                  patch.object(module, 'figure'):
 86 |                 module.run('validation', root / 'validation')
 87 |             self.assertEqual(models['RF'].named_steps['model'].n_jobs, 1)
 88 |             np.testing.assert_array_equal(models['RF'].predict_proba(x), models['RF'].predict_proba(x))
 89 |             boot = pd.read_csv(root / 'validation/paired_bootstrap_validation.csv')
 90 |             self.assertTrue(boot.loc[0, 'primary'])
 91 |             self.assertEqual(boot.loc[0, 'method'], 'Popularity')
 92 |             self.assertEqual((boot.loc[0, 'ci_low'], boot.loc[0, 'ci_high']), (0, 0))
 93 |             recall = pd.read_csv(root / 'validation/recall_at_k_validation.csv')
 94 |             self.assertEqual(len(recall), 5)
 95 |             self.assertTrue(all(f'R@{k}' in recall for k in range(1, 11)))
 96 |             record = json.loads((root / 'validation/results_validation.json').read_text())
 97 |             for name, digest in record['outputs'].items():
 98 |                 self.assertEqual(sha256(root / 'validation' / name), digest)
 99 | 
100 | 
101 | if __name__ == '__main__':
102 |     unittest.main()
```

### 48. `tests/test_no_hard_paths.py`

> **Vai trò:** Code, cấu hình và QMD không chứa đường dẫn tuyệt đối của một máy.  
> **Mục trong bài:** — · **Người viết:** —  
> **Đầu vào → đầu ra:** —  
> **Hàm/lớp chính (dòng):** `NoHardPathTests` (9)  
> *20 dòng · SHA-256 `427bd7653041…`*

```python
 1 | """Code, cấu hình và QMD không được chứa đường dẫn tuyệt đối của một máy cụ thể."""
 2 | from pathlib import Path
 3 | import re
 4 | import unittest
 5 | 
 6 | ROOT = Path(__file__).resolve().parents[1]
 7 | 
 8 | 
 9 | class NoHardPathTests(unittest.TestCase):
10 |     def test_relative_paths_only(self):
11 |         files = [*ROOT.glob('scripts/**/*.py'), *ROOT.glob('scripts/**/*.json'),
12 |                  *ROOT.glob('configs/*.json'), *ROOT.glob('*.qmd')]
13 |         pattern = re.compile(r'[A-Za-z]:\\\\?Users|/Users/|/home/[a-z]')
14 |         bad = [f.relative_to(ROOT).as_posix() for f in files
15 |                if pattern.search(f.read_text(encoding='utf-8', errors='ignore'))]
16 |         self.assertEqual(bad, [])
17 | 
18 | 
19 | if __name__ == '__main__':
20 |     unittest.main()
```
