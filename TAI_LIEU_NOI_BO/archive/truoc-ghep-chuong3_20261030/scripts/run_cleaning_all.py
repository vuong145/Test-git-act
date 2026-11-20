"""Run both member scripts, then verify and summarize their published CSVs."""
from pathlib import Path
import subprocess
import sys

from summarize_cleaning import summarize


def main():
    root = Path(__file__).resolve().parent
    for relative in ['cleaning/vuong/run_cleaning_vuong.py',
                     'cleaning/phong/run_cleaning_phong.py']:
        subprocess.run([sys.executable, '-X', 'utf8', str(root / relative)],
                       cwd=root, check=True)
    summarize()


if __name__ == '__main__':
    main()
