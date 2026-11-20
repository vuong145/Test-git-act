"""Kiểm diễn giải trên dữ liệu tự tạo, không mở dữ liệu nghiên cứu."""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from m4_classifier import NUMERIC, CATEGORY, build_pipeline, synthetic_data
from m4_interpret import importance_table, lr_coefficients, sample_baskets


class InterpretTests(unittest.TestCase):
    def test_coefficients_reconstruct_log_odds(self):
        x, y = synthetic_data(100)
        model = build_pipeline('LR').fit(x, y)
        table = lr_coefficients(model)
        self.assertEqual(table.feature.iloc[:-1].tolist(), model['transform'].get_feature_names_out().tolist())
        self.assertEqual(table.kind.eq('numeric_1_sd').sum(), 6)
        reconstructed = model['transform'].transform(x) @ table.coefficient.iloc[:-1].to_numpy() + table.coefficient.iloc[-1]
        np.testing.assert_allclose(reconstructed, model.decision_function(x))

    def test_importance_reproducible_and_model_unchanged(self):
        x, y = synthetic_data(100)
        validation, yv = synthetic_data(80, 43)
        validation[NUMERIC[3]] = 2  # cột hằng không thể mất AP khi hoán vị
        for method in ['LR', 'RF']:
            model = build_pipeline(method, {'n_estimators': 5} if method == 'RF' else {}).fit(x, y)
            before = model.predict_proba(validation)
            table, raw, base = importance_table(model, validation, yv, method, repeats=3)
            again, raw_again, _ = importance_table(model, validation, yv, method, repeats=3)
            pd.testing.assert_frame_equal(table, again)
            pd.testing.assert_frame_equal(raw, raw_again)
            self.assertEqual(table.feature.tolist(), NUMERIC + CATEGORY)
            self.assertEqual(len(raw), 21)
            self.assertEqual(table.loc[table.feature.eq(NUMERIC[3]), 'ap_decrease_mean'].iloc[0], 0)
            for row in table.itertuples():
                values = raw.loc[raw.feature.eq(row.feature), 'ap_decrease']
                self.assertAlmostEqual(row.ap_decrease_mean, values.mean())
                self.assertAlmostEqual(row.ap_decrease_std, values.std(ddof=0))
            np.testing.assert_array_equal(before, model.predict_proba(validation))
            self.assertTrue(0 <= base <= 1)

    def test_sampling_keeps_whole_baskets(self):
        frame = pd.DataFrame({'order_id': np.repeat(np.arange(20), 3), 'product_id': list(range(3)) * 20})
        sample = sample_baskets(frame, 5)
        self.assertEqual(len(sample), 15)
        self.assertTrue(sample.groupby('order_id').size().eq(3).all())
        self.assertEqual(set(sample.order_id), set(sample_baskets(frame.sample(frac=1), 5).order_id))
        self.assertEqual(len(sample_baskets(frame)), len(frame))

    def test_reject_one_class_importance(self):
        x, y = synthetic_data(50)
        model = build_pipeline('LR').fit(x, y)
        with self.assertRaises(ValueError):
            importance_table(model, x, np.zeros(len(x)), 'LR')


if __name__ == '__main__':
    unittest.main()
