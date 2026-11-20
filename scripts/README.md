# Mã nguồn PRJ-08 (Chương 3 và Chương 4)

Mọi lệnh chạy từ thư mục bài (thư mục chứa file QMD). Đường dẫn trong code và
config đều tương đối theo thư mục bài, không phụ thuộc thư mục đang đứng.

```powershell
uv venv --python 3.12 .venv-m2
uv pip install --python .venv-m2/Scripts/python.exe -r requirements.txt
```

## Thứ tự chạy

| Bước | Lệnh (`.venv-m2\Scripts\python.exe ...`) | Đầu ra chính | Mục |
|---|---|---|---|
| 1 | `scripts/cleaning/clean_vuong.py` | aisles, departments, order_products__prior | 3.1, 3.3 |
| 2 | `scripts/cleaning/clean_phong.py` | products, orders, order_products__train | 3.1, 3.3 |
| 3 | `scripts/summarize_cleaning.py` | `BAO CAO/Bao cao lam sach/verification.json`, before_after, relational_summary, comparison_previous | 3.3 |
| 4 | `scripts/m1_build_master.py` | `DATA/Data đã làm sạch/master_train.parquet`; join_audit, schema, dictionary, master_verification.json trong `Bảng master TLCK/` | 3.2 |
| 5 | `scripts/m1_quality_summary.py` | missingness_summary.csv, basket_quality_summary.json | 3.2 |
| 5b | `scripts/m1_inspect_artifact.py` | Chỉ đọc Master: so hai chế độ đọc (mặc định, `numpy_nullable`); master_info.txt, master_read_modes.csv/.json trong `Bảng master TLCK/` | 3.2 |
| 6 | `scripts/m1_benchmark.py` | master_benchmark.*, data_benchmark.* trong `Bảng master TLCK/` (code giữ nguyên; chạy lại 04/11 trong `.venv-m2`, chạy một mình để số đo không bị nhiễu) | 3.2 |
| 7 | `scripts/m2_foundation.py` | `DATA/Data phai sinh/M2/` (split, reference, giỏ, lookup) + `BAO CAO/Bao cao EDA/common/hashes.json` | 3.4 |
| 8 | `scripts/m2_profile_inputs.py` | `BAO CAO/Bao cao EDA/common/profile/` | 3.2 |
| 9 | `scripts/m2_eda_summary.py`, `scripts/m2_plot_univariate.py` | 8 CSV + reference_outliers.json; hình ban1 | 3.4 |
| 10 | `scripts/m2_eda_multivariate.py`, `scripts/m2_plot_multivariate.py` | `BAO CAO/Bao cao EDA/ban2/`; hình ban2 | 3.5 |
| 11 | `scripts/m2_hypothesis_tests.py` | hypotheses.csv, hypotheses_details.json | 3.6 |
| 12 | `scripts/render_pdf.py --no-open` | PDF của bài | — |
| C4.1 | `scripts/m4_prepare.py` | `DATA/Data phai sinh/M4/masked_baskets.parquet` (giỏ fit/validation/test đã che) | 4.2 |
| C4.2 | `scripts/m4_mining.py` | `M4/catalog.parquet`, `M4/rules_grid.parquet`, `M4/hashes.json` | 4.3 |
| C4.3 | `scripts/m4_benchmark_mining.py [top_n min_count max_len]` | `BAO CAO/Bao cao mo hinh/mining_benchmark_<cấu hình>.csv`, `itemset_equivalence_<cấu hình>.json` | 4.3 |
| C4.4 | `scripts/m4_validate.py [--pilot]` | `M4/features_fit.parquet`, `pipeline_lr.joblib`, `pipeline_rf.joblib`; `BAO CAO/Bao cao mo hinh/validation_grid_A.csv`, `validation_grid_B.csv`, `validation_methods.csv`, `basket_metrics_validation.csv`, `classifier_validation.csv`, `ablation.csv`, `feature_correlation.csv` (`--pilot`: 2.000 giỏ, ghi vào thư mục con `pilot/`) | 4.1–4.3 |
| C4.5 | `scripts/m4_lock.py [--approve Phong Vuong]` | `BAO CAO/Bao cao mo hinh/lock.json` (phương pháp chính, ngưỡng F1, SHA-256 mã nguồn và dữ liệu; `approvals` chỉ true khi truyền `--approve`; từ chối ghi lại nếu test đã bắt đầu) | 4.3 |
| C4.7 | `scripts/m4_test.py test` (Phong) | Chấm tập test **một lần**: cổng `lock.json` (hash, approvals), `test_started.json`; ghi `*_test.csv`, `results_test.json`, `figures/fig-recall-at-k-test.*` vào `BAO CAO/Bao cao mo hinh/`. Đã chạy 04/11/2026 16:11; chạy lại bị từ chối. Thử trên validation: `m4_test.py validation <thư mục ra>` | 4.4, 4.5 |
| C4.6 | `scripts/m4_report.py` | `BAO CAO/Bao cao mo hinh/dataset_description.csv`, `rule_coverage.json`, `importance.csv`, `importance_repeats.csv`, `importance_baseline.json`, `lr_coefficients.csv`, `examples.csv`, `figures/fig-importance.pdf|png` (validation, hai Pipeline đã khóa, hàm của `m4_interpret.py`) | 4.1, 4.5 |
| — | `scripts/m4_interpret.py --demo`, `scripts/m4_classifier.py --demo` (Phong) | `output/ch4_phong_synthetic_20261101/` (chỉ dữ liệu tự tạo, kiểm chức năng; xóa hoặc chuyển đi sau khi chạy) | 4.4 |

Tiền tố `m4_` là cụm code Chương 4, gồm cả mốc M3, M4 và M5 của roadmap.

Tham số Chương 4 ở `configs/m4_model.json`; thiết kế ở `TAI_LIEU_NOI_BO/Hướng dẫn chung/THIET_KE_CHUONG4_20261101.md`.

Bước 1 và 2 độc lập (chạy song song được); mỗi bước đọc thêm cột khóa từ file nhiễu
của bảng người kia để kiểm tra khóa ngoại. Bước 1 đọc lại 32 triệu dòng prior.

## Cổng kiểm tra

- Làm sạch: hash nguồn nhiễu khớp config; đọc lại CSV cuối; số dòng/giỏ/lượt sửa khớp
  config (`check_expected`); chỉ xuất bản khi đạt.
- M1: 4 phép ghép `validate="many_to_one"`, `indicator=True`; 13 tiêu chí trên tệp tạm.
- M2: `m2_foundation.py` kiểm tra Master và CSV sạch khớp hồ sơ M1/làm sạch rồi ghi
  `hashes.json`; mọi script sau gọi `project_io.check_hashes()` và dừng nếu hash lệch.
  Nhánh Phong dùng thêm `BAO CAO/Bao cao EDA/ban2/hashes.json`.

## Kiểm thử

```powershell
.\.venv-m2\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```
