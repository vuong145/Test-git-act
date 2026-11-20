"""Hand-calculated fixtures for member-1 denominators and missing values."""

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"scripts"))
from m2_common import build_baskets, config
from m2_eda_summary import department_display, summarize


class SummaryTests(unittest.TestCase):
    def setUp(self):
        self.cfg = config()
        self.cfg["top_n_grid"] = [1, 2, 10]
        self.ref = pd.DataFrame({
            "order_id": [1, 1, 2, 3], "user_id": [11, 11, 12, 13],
            "product_id": [1, 2, 1, 3], "aisle_id": [1, 2, 1, 3],
            "department_id": [1, 1, 1, 2], "eval_set": ["train"]*4,
            "reordered": [1., np.nan, 0., 1.],
            "order_dow": [0., 0., np.nan, 6.],
            "order_hour_of_day": [0., 0., np.nan, 23.],
            "days_since_prior_order": [np.nan, np.nan, 2., 30.],
        })
        self.depts = pd.DataFrame({"department_id": [1, 2, 3],
                                   "department": ["a", "missing", "absent"]})
        self.aisles = pd.DataFrame({"aisle_id": [1, 2, 3, 4],
                                    "aisle": ["", "b", "c", "absent"]})
        self.products = pd.DataFrame({"product_id": [1, 2, 3],
                                      "product_name": ["", "b", "c"]})

    def result(self):
        return summarize(self.ref, build_baskets(self.ref, self.cfg),
                         self.depts, self.aisles, self.products, self.cfg)

    def test_union_coverage_not_sum_of_popularities(self):
        t, _ = self.result()
        top = t["top_n_coverage"]
        self.assertEqual(top.basket_count.tolist(), [2, 2, 3])
        self.assertAlmostEqual(top.iloc[1].row_share, 0.75)
        self.assertAlmostEqual(top.iloc[1].basket_coverage, 2/3)

    def test_missing_and_valid_denominators(self):
        t, _ = self.result()
        row = t["department_summary"].iloc[0]
        self.assertEqual(row.reordered_valid, 2)
        self.assertAlmostEqual(row.observed_reorder_rate, 0.5)
        self.assertAlmostEqual(row.reordered_missing_pct, 100/3)
        f = t["categorical_frequencies"]
        dow = f[f.variable.eq("order_dow")]
        self.assertEqual(dow["count"].sum(), 3)
        self.assertEqual(dow.iloc[0].valid_pct, 50)
        self.assertTrue(pd.isna(dow.iloc[-1].valid_pct))

    def test_missing_names_and_zero_groups_preserved(self):
        t, _ = self.result()
        self.assertEqual(len(t["aisle_summary"]), 4)
        self.assertEqual(t["aisle_summary"].iloc[0].display_name,
                         "Chưa có tên (ID=1)")
        self.assertTrue(pd.isna(
            t["department_summary"].iloc[-1].observed_reorder_rate))
        self.assertEqual(t["department_summary"].iloc[1].department, "missing")

    def test_sample_std_quantiles_and_ranking(self):
        t, out = self.result()
        row = t["eda_summary"].iloc[0]
        self.assertAlmostEqual(row["mean"], 4/3)
        self.assertAlmostEqual(row["std"], np.sqrt(1/3))
        self.assertEqual(row.q1, 1)
        self.assertEqual(row.q3, 1.5)
        self.assertEqual(out["flagged_baskets"], 0)
        self.assertEqual(t["product_popularity"].product_id.tolist(), [1, 2, 3])

    def test_conflicting_order_attribute_rejected(self):
        self.ref.loc[1, "order_dow"] = np.nan
        with self.assertRaises(ValueError):
            self.result()

    def test_duplicate_product_rejected(self):
        self.ref = pd.concat([self.ref, self.ref.iloc[[0]]], ignore_index=True)
        with self.assertRaises(ValueError):
            self.result()

    def test_all_missing_frequency_and_numeric(self):
        self.ref["order_dow"] = np.nan
        self.ref["days_since_prior_order"] = np.nan
        t, _ = self.result()
        d = t["categorical_frequencies"].query("variable == 'order_dow'")
        self.assertTrue(d.valid_pct.isna().all())
        self.assertEqual(d.iloc[-1]["count"], 3)
        self.assertTrue(pd.isna(t["eda_summary"].iloc[-1]["mean"]))

    def test_remaining_departments_union(self):
        departments = pd.DataFrame({
            "department_id": range(1, 13), "row_count": [10]*10+[1, 1],
            "display_name": [str(i) for i in range(1, 13)],
            "row_share": [10/102]*10+[1/102]*2,
            "basket_count": [1]*12, "basket_coverage": [1.]*12,
        })
        ref = pd.DataFrame({"department_id": [11, 12], "order_id": [1, 1]})
        result = department_display(ref, departments, 1)
        self.assertEqual(result.iloc[-1].basket_count, 1)
        self.assertEqual(result.iloc[-1].basket_coverage, 1)


if __name__ == "__main__":
    unittest.main()
