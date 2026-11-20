"""Run read-only audits on the dirty dataset plus an original-data comparison."""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--clean-dir', required=True, type=Path)
    parser.add_argument('--dirty-dir', required=True, type=Path)
    parser.add_argument('--out-dir', type=Path, default=Path(__file__).resolve().parent / 'dirty_audit_results')
    parser.add_argument('--temp-dir', type=Path)
    args = parser.parse_args()
    if not args.clean_dir.is_dir() or not args.dirty_dir.is_dir():
        parser.error('Both data directories must exist.')
    if args.clean_dir.resolve() == args.dirty_dir.resolve():
        parser.error('Use different directories for original and dirty data.')
    args.out_dir.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parent
    statuses = []
    # Run reference comparison first. Continue other audits if one fails.
    names = ['06_compare_original', '01_inventory', '02_primary_keys',
             '03_foreign_keys', '04_order_history', '05_basket_structure']
    for name in names:
        command = [sys.executable, str(root / (name + '.py')), '--out-dir', str(args.out_dir)]
        if name.startswith('06'):
            command += ['--clean-dir', str(args.clean_dir), '--dirty-dir', str(args.dirty_dir)]
        else:
            command += ['--data-dir', str(args.dirty_dir)]
            if args.temp_dir:
                command += ['--temp-dir', str(args.temp_dir)]
        print('\nRUNNING ' + name, flush=True)
        # Reports are written by each script; keep console progress short.
        completed = subprocess.run(command, stdout=subprocess.DEVNULL)
        statuses.append({'script': name, 'return_code': completed.returncode})
    (args.out_dir / '00_run_summary.txt').write_text(json.dumps(statuses, indent=2), encoding='utf-8')
    print('\nFINISHED. Send the TXT files in: ' + str(args.out_dir.resolve()))
    if any(s['return_code'] for s in statuses):
        print('Some checks failed/incomplete. Send those reports too; do not interpret as PASS.')
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
