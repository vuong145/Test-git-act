# G1 — Bằng chứng I1–I3, chờ Bạn 2 kiểm tra và viết insight

Không phải bản insight cuối. Foundation SHA-256: `5d42246a800f6c1d30b938783e25b0b512cb2760c99c871297b5fb54cb5780c4`.
Canonical split: `7f8017d16d1ff27e2cfe83c1bd12e1cf33d144bef4fc86953b83e72d28671a13`.
Mẫu số: 39363 giỏ/người, 415053 dòng.

| Insight | Bằng chứng | Nguồn | Giới hạn / việc Bạn 2 xác nhận |
|---|---|---|---|
| I1 | Median=9.0; Q1=5.0; Q3=14.0; IQR=9.0; singleton=2118/39363; vượt rào=1578/39363 | eda_summary.csv; sample_overview.csv; reference_outliers.json | Giữ mọi giỏ; không suy kiểu hộ gia đình. Bạn 2 viết hành động có thể thử. |
| I2 | produce: 122514/415053 dòng; 29108/39363 giỏ | department_summary.csv; department_display.csv | Không suy doanh thu hoặc cộng độ phủ; đọc đủ 21 ngành trong CSV. |
| I3 | Xem toàn bộ năm mốc Top-N bên dưới | top_n_coverage.csv; product_popularity.csv | Không chốt N/support; phủ giỏ không bằng giữ đủ sản phẩm của giỏ. |

| N | Số dòng | Tỷ trọng dòng [0,1] | Số giỏ | Độ phủ giỏ [0,1] |
|---:|---:|---:|---:|---:|
| 10 | 28676 | 0.0690899716421758 | 17933 | 0.4555801133043721 |
| 50 | 67693 | 0.1630948336718443 | 24801 | 0.6300586845514824 |
| 100 | 94565 | 0.2278383724488198 | 28212 | 0.7167136651169881 |
| 500 | 174136 | 0.4195512380346606 | 34089 | 0.8660163097324899 |
| 1000 | 218767 | 0.5270820834929515 | 36041 | 0.9156060259634682 |

Ưu tiên số đầy đủ trong CSV; số trên bản thảo chỉ làm tròn khi trình bày. I4–I5, kiểm định 3.6 và insights.csv thuộc Bạn 2.
