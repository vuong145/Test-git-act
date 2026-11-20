"""Importance LR/RF, hệ số LR và hình mẫu; CLI chỉ chạy dữ liệu tự tạo."""
import argparse

import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.metrics import average_precision_score

from m4_classifier import CATEGORY, NUMERIC, build_pipeline, synthetic_data
from project_io import check_hashes, path, plot_setup, save_figure, write_frame, write_json

LABELS = ['Độ phổ biến', 'Số luật khớp', 'Confidence lớn nhất', 'Lift lớn nhất',
          'Cỡ giỏ quan sát', 'Số món cùng ngành', 'Ngành ứng viên']
FOLDER = 'output/ch4_phong_importance_20261101'


def sample_baskets(frame, n=5000, seed=44):
    """Chọn giỏ, giữ toàn bộ dòng ứng viên; frame chỉ chứa validation do bên gọi bảo đảm."""
    if n < 1 or frame.empty or frame.order_id.isna().any():
        raise ValueError('Cần dữ liệu không rỗng, order_id đầy đủ và n dương.')
    ids = np.sort(frame.order_id.unique())
    chosen = np.random.default_rng(seed).choice(ids, min(n, len(ids)), replace=False)
    return frame.loc[frame.order_id.isin(chosen)].copy()


def importance_table(model, x, y, method, repeats=10, seed=44):
    """Hoán vị cột gốc trước OneHot: ngành là một biến; không fit lại Pipeline."""
    x = x[NUMERIC + CATEGORY]
    if set(np.unique(y)) != {0, 1} or repeats < 1:
        raise ValueError('Importance cần hai lớp và số lần lặp dương.')
    result = permutation_importance(model, x, y, scoring='average_precision',
                                    n_repeats=repeats, random_state=seed, n_jobs=1)
    table = pd.DataFrame({'method': method, 'feature': x.columns,
                          'ap_decrease_mean': result.importances_mean,
                          'ap_decrease_std': result.importances_std})
    raw = pd.DataFrame(result.importances, index=x.columns).rename_axis('feature')
    raw.columns = np.arange(1, repeats + 1)
    raw = raw.stack().rename_axis(['feature', 'repeat']).rename('ap_decrease').reset_index()
    raw.insert(0, 'method', method)
    return table, raw, float(average_precision_score(y, model.predict_proba(x)[:, 1]))


def lr_coefficients(model):
    """Hệ số đúng thứ tự sau biến đổi; sáu biến số theo 1 SD, ngành theo cột OneHot."""
    estimator = model['model']
    if not hasattr(estimator, 'coef_') or estimator.coef_.shape[0] != 1:
        raise ValueError('Cần Pipeline LR nhị phân đã fit.')
    names = model['transform'].get_feature_names_out()
    table = pd.DataFrame({'feature': names, 'coefficient': estimator.coef_[0]})
    table['kind'] = np.where(table.feature.str.startswith('numeric__'), 'numeric_1_sd', 'onehot')
    return pd.concat([table, pd.DataFrame([{'feature': 'intercept',
                     'coefficient': float(estimator.intercept_[0]), 'kind': 'intercept'}])], ignore_index=True)


def figures(importance, coefficients):
    plt, style = plot_setup()
    fig, axes = plt.subplots(2, 1, figsize=(16 / 2.54, 9.0))
    for ax, method, color in zip(axes, ['LR', 'RF'], style['colors']):
        rows = importance.loc[importance.method.eq(method)].set_index('feature').loc[NUMERIC + CATEGORY]
        ax.barh(LABELS, rows.ap_decrease_mean, xerr=rows.ap_decrease_std, color=color, capsize=3)
        ax.invert_yaxis()
        ax.axvline(0, color='gray', linewidth=0.8)
        ax.set_title(method)
        ax.set_xlabel('Mức giảm Average Precision')
    fig.suptitle('Permutation importance LR và RF\nDỮ LIỆU TỰ TẠO', fontsize=12)
    fig.text(0.5, 0.02, 'Thanh sai số: ±1 SD của 10 lần hoán vị; seed 44.', ha='center', fontsize=12)
    fig.subplots_adjust(left=0.36, right=0.96, top=0.88, bottom=0.10, hspace=0.48)
    save_figure(plt, fig, FOLDER + '/figures', 'Hinh_mau_1_Importance_LR_RF', style)
    numeric = coefficients.loc[coefficients.kind.eq('numeric_1_sd')]
    fig, ax = plt.subplots(figsize=(16 / 2.54, 5.2))
    ax.barh(LABELS[:6], numeric.coefficient, color=style['colors'][0])
    ax.invert_yaxis()
    ax.axvline(0, color='gray', linewidth=0.8)
    ax.set_xlabel('Hệ số LR (biến số đã chuẩn hóa)')
    ax.set_title('Hệ số LR của sáu biến số\nDỮ LIỆU TỰ TẠO', fontsize=12)
    fig.text(0.5, 0.03, 'Dấu hệ số không thể hiện quan hệ nhân quả.', ha='center', fontsize=12)
    fig.subplots_adjust(left=0.36, right=0.96, top=0.84, bottom=0.20)
    save_figure(plt, fig, FOLDER + '/figures', 'Hinh_mau_2_He_so_LR', style)


def demo():
    check_hashes()
    x, y = synthetic_data(800, 42)
    validation, yv = synthetic_data(400, 43)
    tables, raw, baselines = [], [], {}
    for method in ['LR', 'RF']:
        model = build_pipeline(method).fit(x, y)
        before = model.predict_proba(validation)
        table, runs, baselines[method] = importance_table(model, validation, yv, method)
        np.testing.assert_array_equal(before, model.predict_proba(validation))
        tables.append(table)
        raw.append(runs)
        if method == 'LR':
            coefficients = lr_coefficients(model)
    importance = pd.concat(tables, ignore_index=True)
    write_frame(path(FOLDER) / 'importance_SYNTHETIC.csv', importance)
    write_frame(path(FOLDER) / 'importance_repeats_SYNTHETIC.csv', pd.concat(raw, ignore_index=True))
    write_frame(path(FOLDER) / 'lr_coefficients_SYNTHETIC.csv', coefficients)
    write_json(path(FOLDER) / 'demo_metadata.json', dict(synthetic_only=True, fit_rows=len(x),
               validation_rows=len(validation), fit_seed=42, validation_seed=43, importance_seed=44,
               repeats=10, scoring='average_precision', std_ddof=0, baseline_ap=baselines,
               note='400 dòng tự tạo, không phải mẫu 5.000 giỏ validation nghiên cứu.'))
    figures(importance, coefficients)
    print('Đã xuất bảng và hai cặp hình mẫu tại ' + FOLDER)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo', action='store_true', required=True)
    parser.parse_args()
    demo()
