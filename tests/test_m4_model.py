"""Kiểm thử phần Phong với số tính tay/dữ liệu tự tạo; không đọc dữ liệu nghiên cứu."""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from m4_classifier import CATEGORY, NUMERIC, build_pipeline, fit_grid, synthetic_data
from m4_test import best_f1_threshold, classification_metrics, paired_bootstrap


class ModelTests(unittest.TestCase):
    def test_preprocessing_fit_only_and_unknown_category(self):
        x, y = synthetic_data(100)
        for method in ['LR', 'RF']:
            model = build_pipeline(method, {'n_estimators': 5} if method == 'RF' else {}).fit(x, y)
            transform = model['transform']
            imputer = transform.named_transformers_['numeric']['impute']
            np.testing.assert_allclose(imputer.statistics_, x[NUMERIC].median())
            category = transform.named_transformers_['category']
            self.assertNotIn(99, category['encode'].categories_[0])
            modified = x.copy()
            modified[NUMERIC[0]], modified[CATEGORY[0]] = 1000, 99
            before = imputer.statistics_.copy()
            self.assertTrue(np.isfinite(model.predict_proba(modified)).all())
            np.testing.assert_array_equal(before, imputer.statistics_)
            if method == 'LR':
                scale = transform.named_transformers_['numeric']['scale']
                np.testing.assert_allclose(scale.mean_, x[NUMERIC].fillna(x[NUMERIC].median()).mean())
            else:
                self.assertNotIn('scale', transform.named_transformers_['numeric'].named_steps)
            # ID và nhãn thêm vào không thay dự đoán.
            np.testing.assert_array_equal(model.predict_proba(x),
                                          model.predict_proba(x.assign(user_id=999, y=1)))

    def test_ablation_columns(self):
        x, y = synthetic_data(100)
        for group, forbidden in [('no_rules', NUMERIC[1:4]),
                                  ('no_department', [NUMERIC[-1], CATEGORY[0]])]:
            model = build_pipeline('LR', group=group).fit(x, y)
            names = model['transform'].get_feature_names_out()
            self.assertFalse(any(c in name for c in forbidden for name in names))

    def test_metrics_by_hand(self):
        result = classification_metrics([0, 0, 1, 1], [0.1, 0.8, 0.4, 0.9], 0.5)
        for key in ['accuracy', 'precision', 'recall', 'f1']:
            self.assertEqual(result[key], 0.5)
        self.assertEqual([result[k] for k in ['tn', 'fp', 'fn', 'tp']], [1, 1, 1, 1])
        self.assertEqual(result['roc_auc'], 0.75)
        self.assertAlmostEqual(result['average_precision'], 5 / 6)
        self.assertIsNone(classification_metrics([0, 0], [0.1, 0.3], 0.5)['roc_auc'])
        self.assertIsNone(classification_metrics([0, 0], [0.1, 0.3], 0.5)['average_precision'])
        with self.assertRaises(ValueError):
            classification_metrics([0, 1], [0.1, np.nan], 0.5)

    def test_f1_threshold_exhaustive(self):
        y, scores = [0, 1, 0, 1, 1], [0.1, 0.2, 0.2, 0.6, 0.8]
        expected = max(scores, key=lambda t: (classification_metrics(y, scores, t)['f1'], t))
        self.assertEqual(best_f1_threshold(y, scores), expected)
        with self.assertRaises(ValueError):
            best_f1_threshold([0, 0], [0.1, 0.2])

    def test_bootstrap_pairing_and_edges(self):
        frame = pd.DataFrame({'user_id': [1, 2, 3] * 2, 'order_id': [11, 12, 13] * 2,
                              'method': ['A'] * 3 + ['B'] * 3,
                              'R@10': [0.5, 0.75, 1, 0, 0.25, 0.5]})
        result = paired_bootstrap(frame, 'A', 'B')
        self.assertEqual((result['difference'], result['ci_low'], result['ci_high']), (0.5, 0.5, 0.5))
        self.assertEqual(result, paired_bootstrap(frame.sample(frac=1, random_state=9), 'A', 'B'))
        same = paired_bootstrap(frame, 'A', 'A')
        self.assertEqual((same['ci_low'], same['ci_high']), (0, 0))
        reverse = paired_bootstrap(frame, 'B', 'A')
        self.assertEqual(reverse['difference'], -0.5)
        for invalid in [frame.iloc[:-1], pd.concat([frame, frame.iloc[:1]]),
                        frame.assign(**{'R@10': np.nan})]:
            with self.assertRaises(ValueError):
                paired_bootstrap(invalid, 'A', 'B')

    def test_bootstrap_matches_seeded_reference(self):
        frame = pd.DataFrame({'user_id': [1, 2, 3] * 2, 'order_id': [11, 12, 13] * 2,
                              'method': ['A'] * 3 + ['B'] * 3, 'R@10': [1, 0, 0.5, 0, 1, 0]})
        rng = np.random.default_rng(42)
        indices = rng.integers(0, 3, (2000, 3))
        expected = np.quantile(np.array([1, -1, 0.5])[indices].mean(axis=1), [0.025, 0.975])
        result = paired_bootstrap(frame, 'A', 'B')
        np.testing.assert_allclose([result['ci_low'], result['ci_high']], expected)

    def test_grid_selects_fastest_within_tolerance(self):
        x, y = synthetic_data(100)
        recalls, seconds = [0.1, 0.2, 0.199, 0.15], [1, 3, 2, 0.1]
        def evaluate(model):
            i = [0.01, 0.1, 1, 10].index(model['model'].C)
            return dict(recall_at_10=recalls[i], inference_seconds=seconds[i])
        model, table = fit_grid(x, y, 'LR', evaluate)
        self.assertEqual(model['model'].C, 1)
        self.assertEqual(table.selected.sum(), 1)


if __name__ == '__main__':
    unittest.main()
