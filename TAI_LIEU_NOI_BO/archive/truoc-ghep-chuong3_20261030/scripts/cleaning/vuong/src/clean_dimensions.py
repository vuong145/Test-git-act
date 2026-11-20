"""Clean dimensions without adding any columns to the data."""
import hashlib
from pathlib import Path

import pandas as pd

from .cleaning_rules import append_csv, chunks, clean_frame, key_digest


def clean_dimensions(files: dict, headers: dict, folder: Path, audit) -> dict:
    dimensions = {}
    for table, key in [('aisles', 'aisle_id'),
                       ('departments', 'department_id'),
                       ('products', 'product_id')]:
        raw = pd.concat(list(chunks(files[table], 100000, headers[table])),
                        ignore_index=True)
        frame = clean_frame(raw, table, audit)
        if frame[key].duplicated().any():
            raise ValueError(f'{table}: trùng khóa {key}; không tự xóa dòng.')
        if table == 'products':
            for parent, fk in [('aisles', 'aisle_id'),
                               ('departments', 'department_id')]:
                if not frame[fk].isin(dimensions[parent][fk]).all():
                    raise ValueError(f'products: khóa ngoại mồ côi {fk}')
        digest = hashlib.sha256()
        key_digest(digest, frame, table)
        dimensions[table] = frame
        append_csv(frame, folder / files[table].name)
        audit.checks[table] = {
            'input_rows': len(raw), 'input_columns': headers[table],
            'input_key_sha256': digest.hexdigest(),
            'primary_key_unique': True, 'foreign_keys_valid': True,
        }
        print(f'{table}: {len(frame):,} dòng, {len(frame.columns)} cột', flush=True)
    return dimensions
