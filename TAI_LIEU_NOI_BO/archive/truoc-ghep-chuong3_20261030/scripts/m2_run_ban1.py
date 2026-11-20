"""Run only member 1; final cross-branch integration remains pending."""

import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render-preview", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    jobs = ["tests/test_m2_summary.py", "scripts/m2_eda_summary.py",
            "scripts/m2_plot_univariate.py", "scripts/m2_write_ban1_drafts.py",
            "scripts/m2_verify_ban1.py"]
    for job in jobs:
        subprocess.run([sys.executable, "-B", str(root/job)], check=True)
    if args.render_preview:
        subprocess.run(["quarto", "render", str(root/"drafts/m2/ban1_preview.qmd"),
                        "--to", "pdf"], cwd=root, check=True)


if __name__ == "__main__":
    main()
