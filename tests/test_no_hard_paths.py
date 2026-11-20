"""Code, cấu hình và QMD không được chứa đường dẫn tuyệt đối của một máy cụ thể."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class NoHardPathTests(unittest.TestCase):
    def test_relative_paths_only(self):
        files = [*ROOT.glob('scripts/**/*.py'), *ROOT.glob('scripts/**/*.json'),
                 *ROOT.glob('configs/*.json'), *ROOT.glob('*.qmd')]
        pattern = re.compile(r'[A-Za-z]:\\\\?Users|/Users/|/home/[a-z]')
        bad = [f.relative_to(ROOT).as_posix() for f in files
               if pattern.search(f.read_text(encoding='utf-8', errors='ignore'))]
        self.assertEqual(bad, [])


if __name__ == '__main__':
    unittest.main()
