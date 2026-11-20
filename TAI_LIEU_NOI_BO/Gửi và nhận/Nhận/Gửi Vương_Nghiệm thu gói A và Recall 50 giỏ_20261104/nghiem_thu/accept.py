"""Nghiệm thu gói nhận; giữ bản gốc, chỉ tích hợp tệp thuộc gói sau khi kiểm hash."""
import csv
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from project_io import sha256, check_hashes, write_json

package = ROOT / 'Gửi và Nhận/Nhận/GUI_vuong_ch4_goiA_20261104'
out = Path(__file__).parent
entries = list(csv.DictReader((package / 'DANH_SACH.txt').open(encoding='utf-8-sig'), delimiter='\t'))
for entry in entries:
    source = (package / entry['path']).resolve()
    assert source.is_relative_to(package) and sha256(source) == entry['sha256'].lower(), entry
dependencies = []
for entry in csv.DictReader((package / 'tai_lieu/PHU_THUOC_CO_SAN.txt').open(encoding='utf-8-sig'), delimiter='\t'):
    actual = sha256(ROOT / entry['path'])
    dependencies.append(dict(path=entry['path'], expected=entry['sha256'], actual=actual,
                             match=actual == entry['sha256']))
copied = []
for entry in entries:
    name = entry['path']
    if not name.startswith(('scripts/', 'tests/', 'configs/', 'DATA/', 'BAO CAO/')):
        continue
    source, dest = package / name, ROOT / name
    if dest.exists():
        backup = out / 'before' / name
        backup.parent.mkdir(parents=True, exist_ok=True)
        assert not backup.exists(), 'Không ghi đè bản sao lưu'
        shutil.copy2(dest, backup)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)
    assert sha256(dest) == entry['sha256'].lower()
    copied.append(name)
hashes = {s: len(check_hashes(s)['files']) for s in [
    'BAO CAO/Bao cao EDA/common/hashes.json', 'BAO CAO/Bao cao EDA/ban2/hashes.json',
    'DATA/Data phai sinh/M4/hashes.json', 'BAO CAO/Bao cao mo hinh/lock.json']}
write_json(out / 'acceptance.json', dict(manifest_verified=len(entries), dependencies=dependencies,
                                       copied=copied, hash_checks=hashes,
                                       lock_status='received_draft_not_approved'))
print('Manifest:', len(entries), 'Hash gates:', hashes)
