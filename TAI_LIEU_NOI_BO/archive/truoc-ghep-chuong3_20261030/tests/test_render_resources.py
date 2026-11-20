"""Resource staging regression: EDA images, light tables, and missing files."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from render_pdf import stage_resources


class StagingTests(unittest.TestCase):
    def test_eda_image_and_derived_light_table(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stage = root / 'staging'
            stage.mkdir()
            image = root / 'Bao cao EDA/figures/ban2/example.png'
            table = root / 'Data phai sinh/light/summary.csv'
            for p in (image, table):
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(b'fixture')
            qmd = root / 'fixture.qmd'
            qmd.write_text('![Fixture](Bao cao EDA/figures/ban2/example.png)\n'
                           'pd.read_csv("Data phai sinh/light/summary.csv")', encoding='utf-8')
            stage_resources(root, qmd, stage)
            self.assertEqual((stage / image.relative_to(root)).read_bytes(), b'fixture')
            self.assertEqual((stage / table.relative_to(root)).read_bytes(), b'fixture')
            image.unlink()
            with self.assertRaises(FileNotFoundError):
                stage_resources(root, qmd, stage)

    def test_forbid_escape_and_large_resource(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'configs').mkdir()
            qmd = root / 'a.qmd'
            qmd.write_text('![x](../outside.png)')
            with self.assertRaises(ValueError):
                stage_resources(root, qmd, root / 'stage')
            qmd.write_text('![x](large.png)')
            (root / 'large.png').write_bytes(b'12345')
            (root / 'configs/render_resources.json').write_text(json.dumps({'max_file_bytes': 4}))
            with self.assertRaises(ValueError):
                stage_resources(root, qmd, root / 'stage')


if __name__ == '__main__':
    unittest.main(verbosity=2)
