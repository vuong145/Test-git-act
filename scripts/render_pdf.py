"""Xuất PDF bằng Quarto trong thư mục tạm; chỉ thay PDF cũ khi render thành công."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / '2521001118_Nhom01_TieuLuan.qmd'
LOG = ROOT / 'BAO CAO/Bao cao lam sach/logs/render_pdf.log'


def resources(text):
    """File khai báo trong configs/render_resources.json và file QMD trỏ tới (hình, bảng)."""
    spec = json.loads((ROOT / 'configs/render_resources.json').read_text(encoding='utf-8'))
    files = set(spec.get('files', []))
    for pattern in spec.get('globs', []):
        files.update(p.relative_to(ROOT).as_posix() for p in ROOT.glob(pattern) if p.is_file())
    found = re.findall(r'!\[[^\]]*\]\(([^\n)]+)\)', text)
    found += re.findall(r'\\(?:includegraphics|VerbatimInput|input)(?:\[[^\]]*\])?\{([^}]+)\}', text)
    found += re.findall(r'''(?:read_csv|read_json|read_parquet|open)\(\s*["']([^"']+)["']''', text)
    files.update(v.strip().strip('<>') for v in found if not v.startswith(('http', 'data:')))
    for name in sorted(files):
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise FileNotFoundError(f'Thiếu tài nguyên hoặc nằm ngoài thư mục bài: {name}')
        if path.stat().st_size > spec.get('max_file_bytes', 10 * 1024 * 1024):
            raise ValueError(f'Tài nguyên quá lớn, cần xuất bảng nhẹ: {name}')
        yield path


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    args = argparse.ArgumentParser(description='Xuất PDF bằng Quarto/XeLaTeX')
    args.add_argument('--no-open', action='store_true')
    args = args.parse_args()
    candidates = [Path(os.environ.get('ProgramFiles', 'C:/Program Files')),
                  Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs']
    quarto = shutil.which('quarto') or next(
        (str(p) for p in (b / 'Quarto/bin/quarto.exe' for b in candidates) if p.exists()), None)
    if not quarto:
        raise RuntimeError('Không tìm thấy Quarto CLI')
    target, build = SOURCE.with_suffix('.pdf'), ROOT / (SOURCE.stem + '.build.pdf')
    started = time.perf_counter()
    # Quarto có thể xóa PDF cùng tên nguồn, nên render bản sao trong thư mục tạm.
    with tempfile.TemporaryDirectory(prefix='quarto-build-', dir=ROOT,
                                     ignore_cleanup_errors=True) as directory:
        staging = Path(directory)
        for name in [SOURCE.name, 'references.bib']:
            shutil.copy2(ROOT / name, staging / name)
        for name in ['styles', 'assets']:
            shutil.copytree(ROOT / name, staging / name)
        for path in resources(SOURCE.read_text(encoding='utf-8')):
            (staging / path.relative_to(ROOT)).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, staging / path.relative_to(ROOT))
        process = subprocess.run([quarto, 'render', SOURCE.name, '--to', 'pdf', '--output', build.name],
                                 cwd=staging, capture_output=True, text=True, encoding='utf-8',
                                 errors='replace')
        if process.returncode == 0 and (staging / build.name).exists():
            os.replace(staging / build.name, build)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text((process.stdout or '') + (process.stderr or ''), encoding='utf-8')
    if process.returncode or not build.exists():
        raise RuntimeError(f'Render thất bại; xem {LOG.relative_to(ROOT)}; PDF cũ được giữ')
    try:
        os.replace(build, target)
    except PermissionError as exc:
        raise PermissionError(f'PDF đang mở ở chương trình khác; bản mới lưu tại {build}') from exc
    print(f'THÀNH CÔNG: {target}; {time.perf_counter() - started:.2f} giây')
    if not args.no_open and hasattr(os, 'startfile'):
        os.startfile(target)


if __name__ == '__main__':
    main()
