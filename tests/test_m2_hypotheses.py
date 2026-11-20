import sys,json,unittest
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'scripts'))
from m2_hypothesis_tests import test_table,holm


class HypothesisTests(unittest.TestCase):
    def test_hand_computed_tables(self):
        fixture=json.loads((root/'tests/fixtures/m2_contingency_cases.json').read_text())
        cfg=json.loads((root/'configs/hypotheses_config.json').read_text())
        for case in fixture['cases']:
            with self.subTest(case=case['name']):
                result,expected=test_table(case['counts'],cfg)
                self.assertEqual(result['method'],case['method'])
                for source,target in [('p','p_raw'),('V','cramers_v'),('chi2','chi2_pearson'),('difference_pp','difference_pp')]:
                    if source in case:
                        if case[source] is None:self.assertTrue(np.isnan(result[target]))
                        else:self.assertAlmostEqual(result[target],case[source])
                if 'expected' in case:np.testing.assert_allclose(expected,case['expected'])
    def test_holm_keeps_family_and_original_order(self):
        np.testing.assert_allclose(holm([.01,.04,.03]),[.03,.06,.06])
        np.testing.assert_allclose(holm([.01,1,.03]),[.03,1,.06])
    def test_invalid_counts(self):
        for table in ([[1,-1],[2,3]],[[.5,1],[1,2]],[[0,0],[0,0]]):
            with self.assertRaises(ValueError):test_table(table,{})


if __name__=='__main__':unittest.main(verbosity=2)
