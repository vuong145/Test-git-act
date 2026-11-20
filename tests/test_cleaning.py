"""Regression checks for partitions, foreign keys and chunk boundaries."""
import contextlib
import io
import json
from pathlib import Path
import sys
import shutil
import sqlite3
import uuid
import unittest

import pandas as pd

TESTS = Path(__file__).resolve().parent
CLEANING = TESTS.parent / 'scripts/cleaning'
sys.path.insert(0, str(CLEANING))
import clean_phong  # noqa: E402
import clean_vuong  # noqa: E402
from common import run  # noqa: E402


class CleaningTests(unittest.TestCase):
    def setUp(self):
        self.root = TESTS / ('tmp_' + uuid.uuid4().hex)
        self.root.mkdir()
        self.addCleanup(self.remove_fixture)
        self.raw = self.root / 'raw'
        self.raw.mkdir()
        tables = {
            'aisles': {'aisle_id': [1], 'aisle': ['unknown']},
            'departments': {'department_id': [1], 'department': [' Food ']},
            'products': {'product_id': [1, 2], 'product_name': ['unknown', 'Milk'],
                         'aisle_id': [1, 1], 'department_id': [1, 1]},
            'orders': {'order_id': [1, 2, 3, 4], 'user_id': [10, 10, 20, 20],
                       'eval_set': ['', 'train', 'prior', ''],
                       'order_number': ['', 8, 1, 2], 'order_dow': [0, 9, 2, 3],
                       'order_hour_of_day': [1, 2, 3, 4],
                       'days_since_prior_order': ['', 7, '', 5]},
            'order_products__prior': {'order_id': [1, 1, 3],
                                      'product_id': [1, 2, 2],
                                      'add_to_cart_order': ['', 9, 1],
                                      'reordered': [0, '?', 0]},
            'order_products__train': {'order_id': [2, 2], 'product_id': [1, 2],
                                      'add_to_cart_order': ['', 8],
                                      'reordered': [1, 1]},
        }
        for table, data in tables.items():
            pd.DataFrame(data).to_csv(self.raw / f'{table}.csv', index=False)

    def remove_fixture(self):
        assert self.root.resolve().parent == TESTS
        shutil.rmtree(self.root)

    def run_clean(self, member, size=2):
        module = clean_vuong if member == 'vuong' else clean_phong
        config = json.loads((CLEANING / f'config_{member}.json').read_text('utf-8'))
        config = {k: v for k, v in config.items() if not k.startswith('expected_')}
        config.update(input_dir=str(self.raw), output_dir=str(self.root / 'clean'),
                      report_dir=str(self.root / 'reports' / member), chunksize=size)
        with contextlib.redirect_stdout(io.StringIO()):
            return run(config, CLEANING, member, module.TABLES, module.steps)

    def test_both_members_independent_of_chunk_size_and_order(self):
        baseline = None
        for size in [1, 2, 3, 100]:
            for member in ['phong', 'vuong']:
                report = self.run_clean(member, size)
                result = json.loads((report / 'run_report.json').read_text('utf-8'))
                self.assertTrue(result['source_hashes_unchanged'])
                before_after = pd.read_csv(report / 'before_after.csv')
                self.assertEqual(len(before_after['table'].unique()), 3)
                self.assertTrue((before_after['nonmissing_final'] > 0).any())
            output = {p.name: p.read_bytes() for p in (self.root / 'clean').glob('*.csv')}
            if baseline is None:
                baseline = output
            self.assertEqual(output, baseline)
        orders = pd.read_csv(self.root / 'clean/orders.csv')
        self.assertEqual(orders.eval_set.tolist(), ['prior', 'train', 'prior', 'test'])
        self.assertEqual(orders.order_number.tolist(), [1, 2, 1, 2])
        self.assertTrue(pd.isna(orders.loc[1, 'order_dow']))
        prior = pd.read_csv(self.root / 'clean/order_products__prior.csv')
        self.assertEqual(prior.add_to_cart_order.tolist(), [1, 2, 1])
        self.assertTrue(pd.isna(prior.loc[1, 'reordered']))
        products = pd.read_csv(self.root / 'clean/products.csv')
        self.assertTrue(pd.isna(products.loc[0, 'product_name']))

    def test_orphan_prior_key_rejected_without_overwriting_output(self):
        self.run_clean('vuong')
        path = self.root / 'clean/order_products__prior.csv'
        previous = path.read_bytes()
        raw = pd.read_csv(self.raw / path.name)
        raw.loc[0, 'product_id'] = 999
        raw.to_csv(self.raw / path.name, index=False)
        with self.assertRaisesRegex(ValueError, 'mồ côi'):
            self.run_clean('vuong')
        self.assertEqual(previous, path.read_bytes())

    def test_partition_overlap_rejected(self):
        path = self.raw / 'order_products__prior.csv'
        frame = pd.read_csv(path)
        frame.loc[0, 'order_id'] = 2
        frame.to_csv(path, index=False)
        with self.assertRaises(sqlite3.IntegrityError):
            self.run_clean('phong')
        self.assertFalse((self.root / 'clean/orders.csv').exists())

    def test_noncontiguous_basket_rejected(self):
        path = self.raw / 'order_products__prior.csv'
        frame = pd.read_csv(path).iloc[[0, 2, 1]]
        frame.to_csv(path, index=False)
        with self.assertRaisesRegex(ValueError, 'nhóm xuất hiện lại'):
            self.run_clean('vuong', 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
