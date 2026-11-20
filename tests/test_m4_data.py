"""Kiểm thử phần dữ liệu Chương 4: phép che, danh mục C, khai phá luật (dữ liệu dựng tay)."""
import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import numpy as np

from m4_common import (M, basket_matrix, basket_features, catalog, check_mask, context, evaluate, index_rules,
                       itemset_signature, make_batches, mask, mask_params, max_support_gap, mine, rules,
                       sample_negatives, worst_support_gap)

REFERENCE = pd.DataFrame({  # 4 giỏ; giỏ 4 không chứa sản phẩm nào của Top-2
    "order_id": [1, 1, 2, 2, 3, 4],
    "product_id": [10, 20, 10, 20, 10, 30],
    "department_id": [1, 2, 1, 2, 1, 3]})


class MaskTests(unittest.TestCase):
    def test_hidden_count_and_partition(self):
        for k, h in [(1, 0), (2, 1), (5, 1), (10, 2), (11, 2), (20, 4)]:
            items = list(range(100, 100 + k))
            observed, hidden = mask(items, order_id=7)
            self.assertEqual(len(hidden), h)
            self.assertFalse(set(observed) & set(hidden))
            self.assertEqual(sorted(observed + hidden), items)

    def test_same_seed_and_order_same_mask(self):
        items = list(range(30))
        self.assertEqual(mask(items, 5), mask(items, 5))
        self.assertNotEqual(mask(items, 5), mask(items, 6))


class CatalogAndRulesTests(unittest.TestCase):
    def test_catalog_rank_ties_and_denominator(self):
        c = catalog(REFERENCE)
        self.assertEqual(c.product_id.tolist(), [10, 20, 30])  # 3 giỏ, 2 giỏ, 1 giỏ
        self.assertAlmostEqual(c.popularity.iloc[0], 3 / 4)    # mẫu số = 4 giỏ reference
        ties = catalog(REFERENCE.assign(product_id=[20, 10, 20, 10, 20, 30]))
        self.assertEqual(ties.product_id.tolist()[:2], [20, 10])

    def test_empty_rows_kept_and_algorithms_agree(self):
        m = basket_matrix(REFERENCE, [10, 20])
        self.assertEqual(m.shape, (4, 2))                      # giỏ 4 là hàng toàn 0
        a, f = itemset_signature(mine(m, "apriori", 2, 2)), itemset_signature(mine(m, "fpgrowth", 2, 2))
        self.assertEqual(max_support_gap(a, f), 0.0)
        self.assertEqual(a[(10, 20)], 0.5)

    def test_support_gap_detects_small_difference_and_missing_itemset(self):
        self.assertAlmostEqual(max_support_gap({(1,): 0.5}, {(1,): 0.500001}), 1e-6)
        self.assertIsNone(max_support_gap({(1,): 0.5}, {(2,): 0.5}))

    def test_worst_gap_checks_every_run_not_only_the_first(self):
        same = {(1,): 0.5}
        self.assertEqual(worst_support_gap([same, same, same]), 0.0)
        self.assertAlmostEqual(worst_support_gap([same, same, {(1,): 0.500001}]), 1e-6)
        self.assertIsNone(worst_support_gap([same, same, {(2,): 0.5}]))
        self.assertIsNone(worst_support_gap([]))


class MaskConfigTests(unittest.TestCase):
    def test_stored_mask_must_match_config(self):
        cfg = {"seeds": {"mask": 42}, "hidden_share": 0.2}
        check_mask({"mask": mask_params(cfg)}, cfg)
        for changed in ({"seeds": {"mask": 43}, "hidden_share": 0.2},
                        {"seeds": {"mask": 42}, "hidden_share": 0.3}):
            with self.assertRaises(ValueError):
                check_mask({"mask": mask_params(cfg)}, changed)

    def test_rule_metrics_by_hand(self):
        r = rules(mine(basket_matrix(REFERENCE, [10, 20]), "fpgrowth", 2, 2), 4, 0.5)
        row = r.loc[r.consequent == 20].iloc[0]                # {10} -> 20
        self.assertEqual((row.antecedent, row.n_antecedent, row.n_both), ([10], 3, 2))
        self.assertAlmostEqual(row.confidence, 2 / 3)
        self.assertAlmostEqual(row.lift, (2 / 4) / ((3 / 4) * (2 / 4)))


RANKED = pd.DataFrame({"product_id": [1, 2, 3, 4], "popularity": [0.4, 0.3, 0.2, 0.1],
                       "department_id": [1, 1, 2, 2], "rank": [1, 2, 3, 4]})
DEPT = np.zeros(M, dtype=int)
DEPT[[1, 2, 3, 4, 9]] = [1, 1, 2, 2, 1]
CTX = context(RANKED, 4, DEPT)
RULES = pd.DataFrame({"antecedent": [[1], [1, 3], [3]], "consequent": [2, 2, 4], "confidence": [0.5, 0.8, 0.3],
                      "lift": [2.0, 3.0, 1.5]})
INDEX = index_rules(RULES, CTX)


class FeatureTests(unittest.TestCase):
    def test_rule_features_by_hand_and_no_rule_is_zero(self):
        f = basket_features([1, 3, 9], CTX, INDEX)        # 9 nằm ngoài C; 1 và 3 bị loại khỏi ứng viên
        self.assertEqual(f["product_id"].tolist(), [2, 4])
        self.assertEqual(f["matching_rule_count"].tolist(), [2, 1])   # {1}->2 và {1,3}->2; {3}->4
        self.assertEqual(f["max_rule_confidence"].tolist(), [0.8, 0.3])
        self.assertEqual(f["max_rule_lift"].tolist(), [3.0, 1.5])
        self.assertEqual(f["same_department_count"].tolist(), [2, 1])  # ngành 1: {1, 9}; ngành 2: {3}
        self.assertEqual(f["observed_basket_size"].tolist(), [3, 3])
        none = basket_features([9], CTX, INDEX)
        for name in ("matching_rule_count", "max_rule_confidence", "max_rule_lift"):
            self.assertEqual(none[name].tolist(), [0] * 4)

    def test_hidden_items_do_not_change_features(self):
        a = pd.DataFrame({"order_id": [1], "user_id": [1], "observed": [[1, 3]], "hidden": [[2]]})
        (_, x), (_, y) = (next(make_batches(a.assign(hidden=[h]), CTX, INDEX, 10)) for h in ([2], [4]))
        pd.testing.assert_frame_equal(x.drop(columns="y"), y.drop(columns="y"))
        self.assertEqual((x.y.tolist(), y.y.tolist()), ([True, False], [False, True]))

    def test_metrics_by_hand_and_empty_candidates(self):
        part = pd.DataFrame({"order_id": [1, 2], "user_id": [1, 2], "observed": [[3], [1, 2, 3, 4]],
                             "hidden": [[2, 99], [9]]})
        _, X = next(make_batches(part, CTX, INDEX, 10))   # giỏ 2 không còn ứng viên nào
        m = evaluate(part, X, X.candidate_popularity)
        self.assertEqual(m.loc[0, ["hits@5", "P@5", "R@5", "R@10_ceiling"]].tolist(), [1, 0.2, 0.5, 0.5])
        self.assertEqual(m.loc[1, ["hits@10", "R@10", "HR@10"]].tolist(), [0, 0, 0])

    def test_ties_break_by_product_id(self):
        part = pd.DataFrame({"order_id": [1], "user_id": [1], "observed": [[9]], "hidden": [[1]]})
        _, X = next(make_batches(part, CTX, INDEX, 10))
        self.assertEqual(evaluate(part, X, np.zeros(len(X)), ks=(1, 2))["hits@1"].tolist(), [1])  # 1 trước 2, 3, 4

    def test_negative_sampling_keeps_positives(self):
        part = pd.DataFrame({"order_id": [1], "user_id": [1], "observed": [[9]], "hidden": [[2]]})
        _, X = next(make_batches(part, CTX, INDEX, 10))
        s = sample_negatives(part, X, 2, 43)
        self.assertEqual((s.y.sum(), (~s.y).sum(), s.order_id.unique().tolist()), (1, 2, [1]))
        pd.testing.assert_frame_equal(s, sample_negatives(part, X, 2, 43))


if __name__ == "__main__":
    unittest.main()
