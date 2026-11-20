"""Conservative, column-aware rules; no access to the original dataset."""
from collections import Counter
import csv
import hashlib
import re
from pathlib import Path

import pandas as pd

SCHEMA = {
    'aisles': ['aisle_id', 'aisle'],
    'departments': ['department_id', 'department'],
    'products': ['product_id', 'product_name', 'aisle_id', 'department_id'],
    'orders': ['order_id', 'user_id', 'eval_set', 'order_number',
               'order_dow', 'order_hour_of_day', 'days_since_prior_order'],
    'order_products__prior': ['order_id', 'product_id', 'add_to_cart_order', 'reordered'],
    'order_products__train': ['order_id', 'product_id', 'add_to_cart_order', 'reordered'],
}
SUFFIXES = {'aisles': 1, 'departments': 2, 'order_products__prior': 3,
            'order_products__train': 4, 'orders': 5, 'products': 6}
NUMBER = r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)'
SUFFIX = NUMBER + r'\s*(?:%|[A-Za-z][A-Za-z ]*)'


def resolve_files(folder: Path) -> dict:
    """Accept official names or the user's Vuong1..6 names; reject ambiguity."""
    result = {}
    files = list(folder.glob('*.csv'))
    for table, number in SUFFIXES.items():
        matches = [p for p in files if p.name == table + '.csv'
                   or re.search(rf'Vương{number}\.csv$', p.name, re.I)]
        if len(matches) != 1:
            raise ValueError(f'{table}: cần đúng 1 CSV, tìm thấy {matches}')
        result[table] = matches[0]
    return result


def chunks(path: Path, size: int, schema: list | None = None):
    """Keep literal null markers until our explicit rules inspect them."""
    with pd.read_csv(path, dtype='string', keep_default_na=False,
                     na_filter=False, encoding='utf-8-sig', chunksize=size,
                     skip_blank_lines=False, on_bad_lines='error') as reader:
        for frame in reader:
            if schema is not None and list(frame.columns) != schema:
                raise ValueError(f'Sai schema {path.name}: {list(frame.columns)}')
            yield frame


def append_csv(frame: pd.DataFrame, path: Path) -> None:
    first = not path.exists()
    frame.to_csv(path, mode='w' if first else 'a', header=first, index=False,
                 encoding='utf-8-sig' if first else 'utf-8', na_rep='')


class Audit:
    """Count disjoint statuses and keep bounded raw examples per rule."""

    def __init__(self, folder: Path, config: dict):
        self.folder = folder
        self.config = config
        self.counts = Counter()
        self.examples = []
        self.example_counts = Counter()
        self.checks = {}
        self.final_counts = Counter()
        self.relational_counts = Counter()

    def tokens(self, table: str, column: str) -> set:
        override = self.config.get('missing_tokens_by_column', {})
        tokens = override.get(f'{table}.{column}', self.config['missing_tokens'])
        return {str(x).strip().casefold() for x in tokens}

    def record(self, table: str, column: str, raw: pd.Series,
               clean: pd.Series, status: pd.Series) -> None:
        for label, count in status.value_counts().items():
            self.counts[(table, column, str(label))] += int(count)
            key = (table, column, str(label))
            if label != 'valid_domain':
                limit = 5 - self.example_counts[key]
                for index in status[status.eq(label)].index[:max(0, limit)]:
                    self.examples.append({
                        'table': table, 'column': column, 'status': str(label),
                        'record_1based': int(index) + 1,
                        'raw': str(raw.loc[index]),
                        'clean': '' if pd.isna(clean.loc[index]) else str(clean.loc[index]),
                    })
                    self.example_counts[key] += 1

    def record_final(self, table: str, frame: pd.DataFrame) -> None:
        for column in SCHEMA[table]:
            missing = frame[column].isna() | frame[column].eq('').fillna(False)
            self.final_counts[(table, column, 'missing')] += int(missing.sum())
            self.final_counts[(table, column, 'nonmissing')] += int((~missing).sum())
    def save(self) -> None:
        pd.DataFrame([
            {'table': t, 'column': c, 'status': s, 'cells': n}
            for (t, c, s), n in sorted(self.final_counts.items())
        ], columns=['table', 'column', 'status', 'cells']).to_csv(
            self.folder / 'final_column_summary.csv', index=False, encoding='utf-8-sig')
        pd.DataFrame([
            {'table': t, 'column': c, 'status': s, 'cells': n}
            for (t, c, s), n in sorted(self.counts.items())
        ], columns=['table', 'column', 'status', 'cells']).to_csv(
            self.folder / 'cleaning_summary.csv', index=False, encoding='utf-8-sig')
        pd.DataFrame([
            {'table': t, 'rule': r, 'affected': n}
            for (t, r), n in sorted(self.relational_counts.items())
        ], columns=['table', 'rule', 'affected']).to_csv(
            self.folder / 'relational_summary.csv', index=False, encoding='utf-8-sig')
        missing_statuses = {'missing_token', 'invalid_format', 'suffix_unresolved', 'out_of_domain', 'invalid_label'}
        pd.DataFrame([
            {'table': t, 'column': c,
             'missing_tokens_before': self.counts[(t, c, 'missing_token')],
             'unusable_after_initial_parse': sum(self.counts[(t, c, status)] for status in missing_statuses),
             'missing_final': self.final_counts[(t, c, 'missing')],
             'nonmissing_final': self.final_counts[(t, c, 'nonmissing')]}
            for t, cols in SCHEMA.items() if t in self.checks for c in cols
        ]).to_csv(self.folder / 'before_after.csv', index=False, encoding='utf-8-sig')
        pd.DataFrame(self.examples, columns=[
            'table', 'column', 'status', 'record_1based', 'raw', 'clean'
        ]).to_csv(self.folder / 'examples.csv', index=False, encoding='utf-8-sig')


def numeric(raw: pd.Series, table: str, column: str, audit: Audit,
            low: float, high: float, dtype: str, key: bool = False):
    s = raw.str.strip()
    missing = s.str.casefold().isin(audit.tokens(table, column))
    # IDs accept only digits; attributes may accept exact integer decimals.
    syntax = s.str.fullmatch(r'\d+' if key else NUMBER)
    values = pd.to_numeric(s.where(syntax & ~missing), errors='coerce')
    integer = dtype.lower().startswith('int')
    valid = values.notna() & values.between(low, high)
    if integer:
        valid &= values.mod(1).eq(0)
    status = pd.Series('invalid_format', index=raw.index, dtype='string')
    status.loc[~missing & s.str.fullmatch(SUFFIX)] = 'suffix_unresolved'
    status.loc[syntax & ~missing & ~valid] = 'out_of_domain'
    status.loc[missing] = 'missing_token'
    status.loc[valid] = 'valid_domain'
    status.loc[valid & raw.ne(s)] = 'trimmed'
    if not key:
        status.loc[valid & s.str.contains(r'\.', regex=True)] = 'numeric_format_normalized'
    clean = values.where(valid).astype(dtype)
    audit.record(table, column, raw, clean, status)
    if key and clean.isna().any():
        raise ValueError(f'{table}.{column}: khóa không hợp lệ; dừng, không xóa/điền.')
    return clean, status


def text_column(raw: pd.Series, table: str, column: str,
                audit: Audit, lower: bool = False):
    s = raw.str.strip()
    missing = s.str.casefold().isin(audit.tokens(table, column))
    clean = (s.str.lower() if lower else s).mask(missing)
    status = pd.Series('valid_domain', index=raw.index, dtype='string')
    status.loc[raw.ne(s)] = 'trimmed'
    if lower:
        status.loc[s.ne(s.str.lower())] = 'case_normalized'
    status.loc[missing] = 'missing_token'
    if column == 'eval_set':
        invalid = ~missing & ~clean.isin(['prior', 'train', 'test'])
        status.loc[invalid] = 'invalid_label'
        clean = clean.mask(invalid)
    audit.record(table, column, raw, clean, status)
    return clean, status


def clean_frame(frame: pd.DataFrame, table: str, audit: Audit) -> pd.DataFrame:
    out = pd.DataFrame(index=frame.index)
    domains = {
        'order_number': (1, 100, 'Int16'),
        'order_dow': (0, 6, 'Int8'),
        'order_hour_of_day': (0, 23, 'Int8'),
        'days_since_prior_order': (0, 30, 'Float64'),
        'add_to_cart_order': (1, 2147483647, 'Int32'),
        'reordered': (0, 1, 'Int8'),
    }
    for column in frame.columns:
        if column.endswith('_id'):
            dtype = {'department_id': 'Int8', 'aisle_id': 'Int16'}.get(column, 'Int32')
            high = {'Int8': 127, 'Int16': 32767, 'Int32': 2147483647}[dtype]
            out[column], _ = numeric(frame[column], table, column, audit,
                                     1, high, dtype, key=True)
        elif column in domains:
            out[column], _ = numeric(
                frame[column], table, column, audit, *domains[column])
        else:
            out[column], _ = text_column(
                frame[column], table, column, audit,
                lower=column in {'department', 'aisle', 'eval_set'})
    return out


def export_query(db, query: str, path: Path) -> int:
    cursor = db.execute(query)
    count = 0
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow([x[0] for x in cursor.description])
        while batch := cursor.fetchmany(50000):
            writer.writerows(batch)
            count += len(batch)
    return count


KEYS = {
    'aisles': ['aisle_id'],
    'departments': ['department_id'],
    'products': ['product_id', 'aisle_id', 'department_id'],
    'orders': ['order_id', 'user_id'],
    'order_products__prior': ['order_id', 'product_id'],
    'order_products__train': ['order_id', 'product_id'],
}


def key_digest(hasher, frame: pd.DataFrame, table: str) -> None:
    """Fingerprint normalized identities and row order, not raw text formatting."""
    hasher.update(frame[KEYS[table]].to_csv(
        index=False, header=False, lineterminator='\n'
    ).encode('utf-8'))


def inspect_headers(files: dict) -> dict:
    headers = {}
    for table, path in files.items():
        with path.open(encoding='utf-8-sig', newline='') as stream:
            header = next(csv.reader(stream), [])
        if len(header) != len(SCHEMA[table]) or set(header) != set(SCHEMA[table]):
            raise ValueError(f'{path.name}: sai tên/số cột: {header}')
        headers[table] = header
    return headers


def verify_outputs(files: dict, headers: dict, folder: Path,
                   audit: Audit, size: int) -> None:
    """Read final bytes back; enforce exact schema, row count, and key sequence."""
    for table, original in files.items():
        print(f'Đọc kiểm chứng CSV cuối: {table}', flush=True)
        path = folder / original.name
        digest = hashlib.sha256()
        count = 0
        previous_group, previous_rank = None, 0
        for frame in chunks(path, size, headers[table]):
            if table in {'orders', 'order_products__prior', 'order_products__train'}:
                group = 'user_id' if table == 'orders' else 'order_id'
                col = 'order_number' if table == 'orders' else 'add_to_cart_order'
                expected = frame.groupby(group, sort=False).cumcount() + 1
                first = frame[group].iloc[0]
                if first == previous_group:
                    expected.loc[frame[group].eq(first)] += previous_rank
                actual = pd.to_numeric(frame[col], errors='coerce')
                if not actual.eq(expected).all():
                    raise ValueError(f'{table}: thứ tự CSV cuối không khớp quy tắc tái dựng')
                previous_group, previous_rank = frame[group].iloc[-1], int(expected.iloc[-1])
                if table == 'orders' and not frame['eval_set'].isin(['prior', 'train', 'test']).all():
                    raise ValueError('eval_set cuối vẫn thiếu/sai')
            key_digest(digest, frame, table)
            audit.record_final(table, frame)
            count += len(frame)
        check = audit.checks[table]
        if count != check['input_rows'] or digest.hexdigest() != check['input_key_sha256']:
            raise ValueError(f'{table}: số dòng/chuỗi khóa đầu ra thay đổi')
        check.update(output_rows=count, output_columns=headers[table],
                     output_key_sha256=digest.hexdigest(),
                     same_schema=True, same_row_count=True,
                     normalized_key_sequence_preserved=True)
