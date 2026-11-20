# Bàn giao đầy đủ phần độc lập Bạn 2 — gồm 3.6

Phong (Bạn 2) gửi Vương (Bạn 1): phân tích đa biến, hình 3–5, insight mô tả I4–I5 và kiểm định/bản thảo 3.6. Nền: G0 hợp nhất version 2, reference 39.363 giỏ / 415.053 dòng. Gói này thay gói mô tả không 3.6 cho lần gửi hiện tại; gói cũ là lịch sử.

## Mục 3.6 được bổ sung

- scripts/m2_hypothesis_tests.py: ba cặp ngành đã khóa; crosstab đầy đủ mọi giỏ; kiểm tra tên/ID, kỳ vọng và nhánh Chi-square/Fisher; Holm họ ba cặp; V, xác suất có điều kiện và chênh lệch điểm phần trăm.
- Bao cao EDA/ban2/runs/20261030T073707_dfdcac30/hypotheses/: hypotheses.csv, hypotheses_details.json (bảng đếm/kỳ vọng), validation.json.
- drafts/m2/ban2/ban2_3_6.qmd: thiết kế, hai bảng có caption/nhãn, kết quả và giới hạn.
- output/bo_sung_3_6/: tests.log và audit_3_6.json. Ba fixture tests đạt; đối soát độc lập counts/chi-square/V và Holm trong miền log đạt. H1 có p nhỏ hơn độ chính xác thông thường, bảng trình bày theo ngưỡng; audit lưu log10(p) để truy vết.

Cả ba cặp đủ kỳ vọng cho Chi-square không Yates, bác bỏ H0 sau Holm; V lần lượt khoảng 0,201; 0,152; 0,152. Liên hệ chưa điều chỉnh kích thước giỏ, không chứng minh nhân quả hoặc hiệu quả gợi ý. Không khẳng định đăng ký trước độc lập. Các insight mô tả vẫn chạy độc lập với script kiểm định; kết quả 3.6 nằm riêng để tránh phụ thuộc vòng.

## Chạy và tích hợp

Dùng môi trường M2/G0 đã nghiệm thu tại máy nhận. Lần lượt chạy scripts/m2_eda_multivariate.py, scripts/m2_plot_multivariate.py và scripts/m2_hypothesis_tests.py; tests/test_m2_multivariate.py và tests/test_m2_hypotheses.py kiểm tra hai phần. Nếu chỉ nhận kết quả, đối chiếu PACKAGE_MANIFEST.json và hash nền trước tích hợp.

Vương ghép bản thảo hình và insight vào 3.5, bản thảo 3.6 vào mục tương ứng, giữ đường dẫn từ gốc project; review rồi render toàn QMD để kiểm tra bố cục. Chưa chèn vào QMD/PDF chính trong lượt này. I1–I3 cần G1 của Vương khi tổng hợp năm insight. Hồ sơ rà soát mô tả trong output/ra_soat_ban2_mo_ta ghi phạm vi của đợt trước; thông tin bàn giao hiện hành là file này.
