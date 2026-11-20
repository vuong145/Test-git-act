"""Cổng khóa dùng thư mục tạm và dữ liệu tự tạo; không đọc test nghiên cứu."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import m4_test as module
from m4_classifier import build_pipeline, synthetic_data
from m4_common import M, context, index_rules
from project_io import sha256


class GateTests(unittest.TestCase):
    def test_lock_rejects_tampering_missing_approval_and_repeat(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            resolve = lambda p: (root / p).resolve()
            cfg = {'report_dir': 'report'}
            report = resolve('report')
            report.mkdir()
            names = module.CODE_FILES + ['configs/m4_model.json', 'DATA/Data phai sinh/M4/hashes.json',
                                        'DATA/Data đã làm sạch/master_train.parquet', 'fixture.bin']
            for name in names:
                target = resolve(name)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('fixture', encoding='utf-8')
            lock = dict(stage_A={'top_n': 3}, main_method='RF', f1_threshold={'LR': .5, 'RF': .5},
                        files={name: sha256(resolve(name)) for name in names})
            record = dict(stage_A=lock['stage_A'], files={'fixture.bin': lock['files']['fixture.bin']})
            def save():
                (report / 'lock.json').write_text(json.dumps(lock), encoding='utf-8')
            save()
            with patch.object(module, 'path', side_effect=resolve), patch.object(module, 'check_hashes', return_value=record):
                with self.assertRaises(ValueError):
                    module.checked_lock('test', report, cfg)  # chưa duyệt
                lock['approvals'] = {'Phong': True, 'Vuong': True}
                save()
                resolve('fixture.bin').write_text('changed', encoding='utf-8')
                with self.assertRaises(ValueError):
                    module.checked_lock('test', report, cfg)
                resolve('fixture.bin').write_text('fixture', encoding='utf-8')
                digest = lock['files'].pop('scripts/m4_test.py')
                save()
                with self.assertRaises(ValueError):
                    module.checked_lock('test', report, cfg)
                lock['files']['scripts/m4_test.py'] = digest
                save()
                with self.assertRaises(ValueError):
                    module.checked_lock('test', resolve('other'), cfg)
                self.assertFalse((report / 'test_started.json').exists())
                module.checked_lock('test', report, cfg)
                self.assertTrue((report / 'test_started.json').exists())
                with self.assertRaises(FileExistsError):
                    module.checked_lock('test', report, cfg)

    def test_synthetic_scoring_outputs_and_primary_self_comparison(self):
        x, y = synthetic_data(80)
        models = {m: build_pipeline(m, {'n_estimators': 5} if m == 'RF' else {}).fit(x, y)
                  for m in ['LR', 'RF']}
        ranked = pd.DataFrame(dict(product_id=[1, 2, 3], popularity=[.5, .3, .2],
                                    department_id=[1, 1, 2], rank=[1, 2, 3]))
        dept = np.zeros(M, int)
        dept[[1, 2, 3]] = [1, 1, 2]
        ctx = context(ranked, 3, dept)
        rules = pd.DataFrame(dict(antecedent=[[1]], consequent=[2], confidence=[.6], lift=[2]))
        frame = pd.DataFrame(dict(order_id=[1, 2], user_id=[1, 2], eligible=[True, True],
                                  observed=[[1], [3]], hidden=[[2], [1, 99]]))
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            cfg = dict(report_dir='report', data_dir='data', batch_size=1, bootstrap_n=20, seeds={'bootstrap': 42})
            lock = dict(main_method='Popularity', f1_threshold={'LR': .5, 'RF': .5}, locked_at='fixture')
            (root / 'report').mkdir()
            (root / 'report/lock.json').write_text(json.dumps(lock))
            with patch.object(module, 'path', side_effect=lambda p: (root / p).resolve()), \
                 patch.object(module, 'config', return_value=cfg), \
                 patch.object(module, 'checked_lock', return_value=lock), \
                 patch.object(module, 'locked_stage', return_value=(frame, ctx, index_rules(rules, ctx), {})), \
                 patch.object(module.joblib, 'load', side_effect=lambda p: models['LR' if 'lr' in p.name else 'RF']), \
                 patch.object(module, 'figure'):
                module.run('validation', root / 'validation')
            boot = pd.read_csv(root / 'validation/paired_bootstrap_validation.csv')
            self.assertTrue(boot.loc[0, 'primary'])
            self.assertEqual(boot.loc[0, 'method'], 'Popularity')
            self.assertEqual((boot.loc[0, 'ci_low'], boot.loc[0, 'ci_high']), (0, 0))
            recall = pd.read_csv(root / 'validation/recall_at_k_validation.csv')
            self.assertEqual(len(recall), 5)
            self.assertTrue(all(f'R@{k}' in recall for k in range(1, 11)))
            record = json.loads((root / 'validation/results_validation.json').read_text())
            for name, digest in record['outputs'].items():
                self.assertEqual(sha256(root / 'validation' / name), digest)


if __name__ == '__main__':
    unittest.main()
