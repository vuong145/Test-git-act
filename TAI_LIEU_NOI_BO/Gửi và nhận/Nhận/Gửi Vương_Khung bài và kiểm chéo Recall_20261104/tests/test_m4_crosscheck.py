import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from m4_crosscheck import crosscheck


class CrosscheckTests(unittest.TestCase):
    def test_rule_priority_ties_outside_catalog_and_empty_candidates(self):
        baskets = pd.DataFrame([
            dict(order_id=1, user_id=1, split='validation', eligible=True, observed=[99], hidden=[2, 999]),
            dict(order_id=2, user_id=2, split='validation', eligible=True, observed=[1, 2, 3], hidden=[999])])
        catalog = pd.DataFrame(dict(product_id=[1, 2, 3], rank=[1, 2, 3], popularity=[.9, .5, .5]))
        rules = pd.DataFrame(dict(top_n=[3, 3], min_count=[20, 20], max_len=[2, 2],
                                  confidence=[.8, .8], antecedent=[[99], [99]], consequent=[3, 2]))
        metrics = pd.DataFrame({'order_id': [2, 1], 'method': ['Rules', 'Rules'], 'R@10': [0, .5]})
        result, rankings = crosscheck(baskets, catalog, rules, metrics, top_n=3, count=2)
        self.assertEqual(result.hits.tolist(), [1, 0])
        self.assertEqual(result.difference.tolist(), [0, 0])
        self.assertEqual(rankings.product_id.tolist(), [2, 3, 1])
        with self.assertRaises(ValueError):
            crosscheck(baskets, catalog, rules, metrics.iloc[:1], top_n=3, count=2)


if __name__ == '__main__':
    unittest.main()
