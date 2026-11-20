"""Hand-computed edge cases for Ban 2 descriptive tables."""
import sys
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from m2_eda_multivariate import presence_table, pair_summary, correlations, time_tables


class MultivariateTests(unittest.TestCase):
    def test_hand_calculated_pair_and_direction(self):
        presence=pd.DataFrame({'1':[True,True,True,False,False], '2':[True,True,False,True,False]})
        row=pair_summary(presence).query('department_a==1 and department_b==2').iloc[0]
        self.assertEqual(row.n_AB,2)
        self.assertAlmostEqual(row.support_AB,.4)
        self.assertAlmostEqual(row.lift_AB,10/9)
        self.assertAlmostEqual(row.probability_B_given_A,2/3)

    def test_reject_unknown_department_and_missing_basket(self):
        for reference in [pd.DataFrame({'order_id':[1],'department_id':[3]}),pd.DataFrame({'order_id':[2],'department_id':[1]})]:
            with self.assertRaises(ValueError):
                presence_table(reference,pd.DataFrame({'order_id':[1]}),pd.DataFrame({'department_id':[1]}))

    def test_insufficient_pair_is_na(self):
        tables,n=correlations(pd.DataFrame({'a':[1,np.nan], 'b':[2,3]}),['a','b'])
        self.assertEqual(n.loc['a','b'],1)
        self.assertTrue(np.isnan(tables['spearman'].loc['a','b']))

    def test_counts_do_not_overflow_and_absent_department(self):
        baskets=pd.DataFrame({'order_id':range(300)})
        reference=pd.DataFrame({'order_id':list(range(300))*2,'department_id':[1]*300+[1]*300})
        presence=presence_table(reference,baskets,pd.DataFrame({'department_id':[1,2]}))
        summary=pair_summary(presence)
        row=summary.query('department_a==1 and department_b==1').iloc[0]
        self.assertEqual(row.n_AB,300)
        self.assertEqual(row.lift_AB,1)
        self.assertTrue(np.isnan(summary.query('department_a==1 and department_b==2').iloc[0].lift_AB))
        self.assertEqual(presence.shape,(300,2))

    def test_pairwise_missing_and_constant(self):
        tables,n=correlations(pd.DataFrame({'a':[1,2,3],'b':[2,np.nan,6],'c':[1,1,1]}),['a','b','c'])
        self.assertEqual(n.loc['a','b'],2)
        self.assertAlmostEqual(tables['spearman'].loc['a','b'],1)
        self.assertTrue(np.isnan(tables['pearson'].loc['a','c']))

    def test_empty_time_cells_and_missing_group(self):
        baskets=pd.DataFrame({'order_dow':[0,0,np.nan], 'hour_band':['A','A',None], 'basket_size':[1,3,5]})
        tables,hours=time_tables(baskets,{'hour_labels':['A','B'],'min_group_n':30,'quantile_interpolation':'linear'})
        self.assertEqual(tables['median'].loc[0,'A'],2)
        self.assertEqual(tables['count'].loc[0,'B'],0)
        self.assertTrue(np.isnan(tables['median'].loc[0,'B']))
        self.assertEqual(hours.N.sum(),3)
        self.assertEqual(hours.loc[hours.hour_band=='missing','N'].iloc[0],1)


if __name__=='__main__':
    unittest.main(verbosity=2)
