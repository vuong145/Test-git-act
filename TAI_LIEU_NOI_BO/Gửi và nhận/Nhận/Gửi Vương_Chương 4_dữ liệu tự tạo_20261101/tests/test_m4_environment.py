"""Kiem tra moi truong M4 bang du lieu tu tao; khong doc du lieu nghien cuu."""
import unittest

import numpy as np
import pandas as pd
import psutil
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class M4EnvironmentTests(unittest.TestCase):
    def test_synthetic_mining_and_classifier_pipeline(self):
        """Thu vien khai pha, tien xu ly va hai classifier chay tren fixture."""
        baskets = pd.DataFrame({
            'a': [True, True, False, True],
            'b': [True, False, True, True],
            'c': [False, True, True, True],
        }).astype(pd.SparseDtype(bool, False))
        outputs = [fn(baskets, min_support=0.5, use_colnames=True, max_len=2)
                   for fn in (apriori, fpgrowth)]
        normalize = lambda df: {tuple(sorted(r.itemsets)): r.support
                                for r in df.itertuples()}
        self.assertEqual(normalize(outputs[0]), normalize(outputs[1]))
        rules = association_rules(outputs[1], num_itemsets=len(baskets),
                                  metric='confidence', min_threshold=0.5)
        self.assertGreater(len(rules), 0)
        x = pd.DataFrame({'size': [1., 2., 3., 4., np.nan, 6., 7., 8.],
                          'department': ['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b']})
        y = np.array([0, 0, 0, 1, 0, 1, 1, 1])
        validation = pd.DataFrame({'size': [100., np.nan], 'department': ['new', 'a']})
        for estimator in [LogisticRegression(solver='lbfgs', max_iter=1000),
                          RandomForestClassifier(n_estimators=10, random_state=42, n_jobs=1)]:
            numeric = [('impute', SimpleImputer(strategy='median'))]
            if isinstance(estimator, LogisticRegression):
                numeric.append(('scale', StandardScaler()))
            transform = ColumnTransformer([
                ('numeric', Pipeline(numeric), ['size']),
                ('category', OneHotEncoder(handle_unknown='ignore'), ['department'])])
            model = Pipeline([('transform', transform), ('model', estimator)])
            model.fit(x, y)
            if isinstance(estimator, LogisticRegression):
                scaler = model['transform'].named_transformers_['numeric']['scale']
                before = scaler.mean_.copy()
                np.testing.assert_allclose(before, [x['size'].fillna(x['size'].median()).mean()])
            probabilities = model.predict_proba(validation)[:, 1]
            self.assertTrue(np.isfinite(probabilities).all())
            self.assertTrue(((probabilities >= 0) & (probabilities <= 1)).all())
            if isinstance(estimator, LogisticRegression):
                np.testing.assert_array_equal(before, scaler.mean_)
            scores = model.predict_proba(x)[:, 1]
            self.assertTrue(np.isfinite(average_precision_score(y, scores)))
            self.assertTrue(np.isfinite(roc_auc_score(y, scores)))
        self.assertGreater(psutil.Process().memory_info().rss, 0)


if __name__ == '__main__':
    unittest.main()
