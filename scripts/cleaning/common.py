"""Phần dùng chung của clean_vuong.py và clean_phong.py.

Quy tắc theo cột, bộ đếm Audit, tái dựng thứ tự theo dòng CSV, kiểm tra đầu ra và khung
chạy: hash nguồn -> làm sạch vào thư mục tạm -> đọc lại -> so bản trước -> xuất bản.
Không dùng dữ liệu gốc để điền; số kỳ vọng trong config chỉ là kiểm tra hồi quy.

ĐỌC NHANH (vấn đáp):
  Mục đích: làm sạch 6 CSV nhiễu mà KHÔNG xóa dòng, KHÔNG đoán, KHÔNG dùng dữ liệu gốc để điền.
  Bốn nguyên tắc: (1) ô sai/thiếu thì để thiếu; (2) khóa sai thì dừng; (3) mọi thay đổi đều được đếm (Audit);
  (4) chỉ xuất bản khi mọi kiểm tra đạt (làm trong thư mục tạm, xong mới chép sang).
  Bố cục file: Nhóm 1 tiện ích -> Nhóm 2 Audit -> Nhóm 3 quy tắc theo cột -> Nhóm 4 tái dựng thứ tự
  -> Nhóm 5 làm sạch từng loại bảng -> Nhóm 6 kiểm chứng đầu ra và khung chạy (run, cli).
  Hỏi hay gặp: vì sao đọc dạng chữ? (để pandas không tự biến 'null' thành thiếu mà ta không đếm được);
  vì sao SQLite? (nhớ hàng chục triệu khóa mà không tràn RAM); vì sao đọc theo khối 250.000 dòng? (bảng prior 32,4 triệu dòng).
"""
import argparse
from collections import Counter
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import sqlite3
import sys
import time
from types import SimpleNamespace

import numpy as np
import pandas as pd

# Hằng số: tên cột từng bảng (SCHEMA), cột khóa (KEYS), miền hợp lệ và kiểu của từng cột số (DOMAINS).
DETAIL = ['order_id', 'product_id', 'add_to_cart_order', 'reordered']
SCHEMA = {'aisles': ['aisle_id', 'aisle'], 'departments': ['department_id', 'department'],
          'products': ['product_id', 'product_name', 'aisle_id', 'department_id'],
          'orders': ['order_id', 'user_id', 'eval_set', 'order_number', 'order_dow',
                     'order_hour_of_day', 'days_since_prior_order'],
          'order_products__prior': DETAIL, 'order_products__train': DETAIL}
KEYS = {'aisles': ['aisle_id'], 'departments': ['department_id'],
        'products': ['product_id', 'aisle_id', 'department_id'], 'orders': ['order_id', 'user_id'],
        'order_products__prior': ['order_id', 'product_id'],
        'order_products__train': ['order_id', 'product_id']}
DOMAINS = {'order_number': (1, 100, 'Int16'), 'order_dow': (0, 6, 'Int8'),
           'order_hour_of_day': (0, 23, 'Int8'), 'days_since_prior_order': (0, 30, 'Float64'),
           'add_to_cart_order': (1, 2147483647, 'Int32'), 'reordered': (0, 1, 'Int8')}
NUMBER = r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)'
SUFFIX = NUMBER + r'\s*(?:%|[A-Za-z][A-Za-z ]*)'
GOOD = '(known=n AND distinct_n=n AND min_n=1 AND max_n=n)'   # thứ tự 1..n, không trùng/thiếu
TZ = timezone(timedelta(hours=7))


# ===== Nhóm 1: tiện ích nhỏ (hash, ghi JSON, đọc CSV theo khối, ghi nối CSV, đọc cột khóa) =====
def sha256(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def chunks(path, size, schema=None):
    """Đọc theo khối dạng chuỗi, giữ nguyên ký hiệu thiếu cho tới khi quy tắc kiểm tra."""
    with pd.read_csv(path, dtype='string', keep_default_na=False, na_filter=False,
                     encoding='utf-8-sig', chunksize=size, skip_blank_lines=False,
                     on_bad_lines='error') as reader:
        for frame in reader:
            if schema is not None and list(frame.columns) != schema:
                raise ValueError(f'Sai schema {path.name}: {list(frame.columns)}')
            yield frame


def append_csv(frame, path):
    first = not path.exists()
    frame.to_csv(path, mode='w' if first else 'a', header=first, index=False,
                 encoding='utf-8-sig' if first else 'utf-8', na_rep='')


def read_ids(path, column, size, unique=False):
    """Chỉ đọc cột khóa của file nhiễu để kiểm tra khóa ngoại; khóa sai thì dừng."""
    pieces = []
    for frame in pd.read_csv(path, usecols=[column], dtype='string', keep_default_na=False,
                             chunksize=size, encoding='utf-8-sig', skip_blank_lines=False):
        values = frame[column].str.strip()
        if not values.str.fullmatch(r'\d+').all():
            raise ValueError(f'{path.name}.{column}: khóa sai định dạng')
        numbers = pd.to_numeric(values, errors='raise')
        if not numbers.between(1, 2147483647).all():
            raise ValueError(f'{path.name}.{column}: khóa ngoài miền')
        pieces.append(numbers.astype('int64').to_numpy())
    result = pd.Index(np.concatenate(pieces))
    if unique and result.has_duplicates:
        raise ValueError(f'{path.name}: trùng khóa {column}')
    return result if unique else result.unique()


def export_query(db, query, path):
    cursor = db.execute(query)
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow([x[0] for x in cursor.description])
        writer.writerows(cursor.fetchall())


def key_digest(hasher, frame, table):
    """Dấu vân tay của khóa đã chuẩn hóa theo đúng thứ tự dòng."""
    hasher.update(frame[KEYS[table]].to_csv(index=False, header=False,
                                            lineterminator='\n').encode('utf-8'))


def insert(db, table, frame):
    with db:   # khóa chính SQLite từ chối khóa trùng
        db.executemany(f'INSERT INTO {table} VALUES ({",".join("?" * frame.shape[1])})',
                       frame.astype(object).where(frame.notna(), None)
                       .itertuples(index=False, name=None))


# ===== Nhóm 2: Audit = sổ đếm. Mỗi ô được gán một trạng thái (hợp lệ, cắt khoảng trắng, thiếu, ngoài miền...)
# rồi cộng dồn để ra các bảng 'trước và sau' của mục 3.3. Chỉ giữ tối đa 5 ví dụ cho mỗi loại lỗi. =====
class Audit:
    """Đếm trạng thái rời nhau theo ô và giữ tối đa 5 ví dụ mỗi quy tắc."""

    def __init__(self, folder, config):
        self.folder, self.config, self.examples, self.checks = folder, config, [], {}
        self.counts, self.final_counts = Counter(), Counter()
        self.relational_counts, self.example_counts = Counter(), Counter()

    def tokens(self, table, column):
        tokens = self.config.get('missing_tokens_by_column', {}).get(
            f'{table}.{column}', self.config['missing_tokens'])
        return {str(x).strip().casefold() for x in tokens}

    def example(self, table, column, status, index, raw, clean):
        key = (table, column, status)
        if self.example_counts[key] < 5:
            self.examples.append({'table': table, 'column': column, 'status': status,
                                  'record_1based': int(index) + 1, 'raw': raw, 'clean': clean})
            self.example_counts[key] += 1

    def record(self, table, column, raw, clean, status):
        for label, count in status.value_counts().items():
            self.counts[(table, column, str(label))] += int(count)
            for i in [] if label == 'valid_domain' else status[status.eq(label)].index[:5]:
                self.example(table, column, str(label), i, str(raw.loc[i]),
                             '' if pd.isna(clean.loc[i]) else str(clean.loc[i]))

    def record_final(self, table, frame):
        for column in SCHEMA[table]:
            missing = frame[column].isna() | frame[column].eq('').fillna(False)
            self.final_counts[(table, column, 'missing')] += int(missing.sum())
            self.final_counts[(table, column, 'nonmissing')] += int((~missing).sum())

    def save(self):
        def out(rows, columns, name):
            pd.DataFrame(rows, columns=columns).to_csv(self.folder / name, index=False,
                                                       encoding='utf-8-sig')
        cells = ['table', 'column', 'status', 'cells']
        out([(*k, n) for k, n in sorted(self.final_counts.items())], cells, 'final_column_summary.csv')
        out([(*k, n) for k, n in sorted(self.counts.items())], cells, 'cleaning_summary.csv')
        out([(*k, n) for k, n in sorted(self.relational_counts.items())],
            ['table', 'rule', 'affected'], 'relational_summary.csv')
        unusable = ['missing_token', 'invalid_format', 'suffix_unresolved', 'out_of_domain',
                    'invalid_label']
        out([(t, c, self.counts[(t, c, 'missing_token')],
              sum(self.counts[(t, c, s)] for s in unusable),
              self.final_counts[(t, c, 'missing')], self.final_counts[(t, c, 'nonmissing')])
             for t, cols in SCHEMA.items() if t in self.checks for c in cols],
            ['table', 'column', 'missing_tokens_before', 'unusable_after_initial_parse',
             'missing_final', 'nonmissing_final'], 'before_after.csv')
        out(self.examples, ['table', 'column', 'status', 'record_1based', 'raw', 'clean'],
            'examples.csv')


# ===== Nhóm 3: quy tắc làm sạch từng cột. numeric() cho cột số, text_column() cho cột chữ, clean_frame() chọn quy tắc theo tên cột. =====
def numeric(raw, table, column, audit, low, high, dtype, key=False):
    # Bước 1: cắt khoảng trắng; chữ như null/none/? được coi là 'thiếu' (danh sách trong config).
    s = raw.str.strip()
    missing = s.str.casefold().isin(audit.tokens(table, column))
    # Bước 2: chỉ nhận chuỗi đúng dạng số (cột khóa chỉ nhận chữ số).
    syntax = s.str.fullmatch(r'\d+' if key else NUMBER)   # khóa chỉ nhận chữ số
    values = pd.to_numeric(s.where(syntax & ~missing), errors='coerce')
    valid = values.notna() & values.between(low, high)
    if dtype.startswith('Int'):
        valid &= values.mod(1).eq(0)
    # Bước 3: gán nhãn trạng thái cho từng ô để đếm lỗi; nhãn gán sau ghi đè nhãn gán trước. Ví dụ '2 %' = suffix_unresolved (không đoán).
    status = pd.Series('invalid_format', index=raw.index, dtype='string')
    status.loc[~missing & s.str.fullmatch(SUFFIX)] = 'suffix_unresolved'
    status.loc[syntax & ~missing & ~valid] = 'out_of_domain'
    status.loc[missing] = 'missing_token'
    status.loc[valid] = 'valid_domain'
    status.loc[valid & raw.ne(s)] = 'trimmed'
    if not key:
        status.loc[valid & s.str.contains('.', regex=False)] = 'numeric_format_normalized'
    # Bước 4: ô sai miền thì thành thiếu (không sửa bừa); riêng cột khóa sai thì dừng cả chương trình.
    clean = values.where(valid).astype(dtype)
    audit.record(table, column, raw, clean, status)
    if key and clean.isna().any():
        raise ValueError(f'{table}.{column}: khóa không hợp lệ; dừng, không xóa/điền.')
    return clean


# Cột chữ: cắt khoảng trắng; aisle/department/eval_set đổi chữ thường; token thiếu -> thiếu;
# eval_set ngoài {prior, train, test} -> thiếu (sẽ được khôi phục ở clean_phong.py).
def text_column(raw, table, column, audit, lower):
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
    return clean


# Chọn quy tắc theo tên cột: *_id -> khóa số; cột có miền trong DOMAINS -> số; còn lại -> chữ.
def clean_frame(frame, table, audit):
    out = pd.DataFrame(index=frame.index)
    for column in frame.columns:
        if column.endswith('_id'):
            dtype = {'department_id': 'Int8', 'aisle_id': 'Int16'}.get(column, 'Int32')
            high = {'Int8': 127, 'Int16': 32767, 'Int32': 2147483647}[dtype]
            out[column] = numeric(frame[column], table, column, audit, 1, high, dtype, key=True)
        elif column in DOMAINS:
            out[column] = numeric(frame[column], table, column, audit, *DOMAINS[column])
        else:
            out[column] = text_column(frame[column], table, column, audit,
                                      column in {'department', 'aisle', 'eval_set'})
    return out


# ===== Nhóm 4: tái dựng thứ tự (add_to_cart_order, order_number) theo THỨ TỰ DÒNG trong CSV.
# Đây là giả định (thứ tự dòng gốc = thứ tự thật), được nêu rõ trong báo cáo; không sắp lại theo mã. =====
class RowSequence:
    """Đánh số nhóm liên tiếp theo thứ tự dòng CSV, giữ trạng thái qua ranh giới khối.

    Giả định thứ tự dòng gốc là thứ tự mua/thêm giỏ; không sắp lại theo mã.
    Bảng SQLite từ chối nhóm xuất hiện lại ở chỗ khác trong file.
    """

    def __init__(self, db, table, key, column, audit, maximum=None):
        self.db, self.table, self.key, self.column = db, table, key, column
        self.audit, self.maximum, self.last_key, self.last_rank = audit, maximum, None, 0
        db.execute(f'CREATE TABLE groups_{table}(id INTEGER PRIMARY KEY)')

    def apply(self, frame):
        ids = frame[self.key].to_numpy(dtype=np.int64)
        index = np.arange(len(ids))
        # starts = dòng đầu mỗi nhóm (giỏ hoặc khách); rank = vị trí trong nhóm (1, 2, 3...).
        starts = np.r_[True, ids[1:] != ids[:-1]]
        first = np.maximum.accumulate(np.where(starts, index, 0))
        rank = index - first + 1
        # Nhóm bị cắt ngang giữa hai khối: cộng tiếp thứ hạng đã đếm ở khối trước.
        if self.last_key is not None and ids[0] == self.last_key:   # nhóm nối từ khối trước
            rank[first == 0] += self.last_rank
            starts[0] = False
        # SQLite từ chối nhóm xuất hiện lại ở chỗ khác trong file: khi đó giả định thứ tự dòng sai nên dừng.
        try:
            self.db.executemany(f'INSERT INTO groups_{self.table} VALUES(?)',
                                ((int(x),) for x in ids[starts]))
        except sqlite3.IntegrityError as exc:
            raise ValueError(f'{self.table}: nhóm xuất hiện lại; dừng tái dựng thứ tự') from exc
        if self.maximum is not None and (rank > self.maximum).any():
            raise ValueError(f'{self.table}: thứ tự vượt giới hạn {self.maximum}')
        # Phân loại từng ô: thiếu -> điền, lệch -> sửa, đúng -> giữ nguyên; chỉ để đếm cho báo cáo.
        old = frame[self.column].copy()
        rebuilt = pd.Series(rank, index=frame.index, dtype=old.dtype)
        missing = old.isna()
        masks = {'sequence_filled_unusable': missing,
                 'sequence_corrected_observed': (~missing & old.ne(rebuilt)).fillna(False),
                 'sequence_observed_consistent': (~missing & old.eq(rebuilt)).fillna(False)}
        for rule, mask in masks.items():
            self.audit.relational_counts[(self.table, rule)] += int(mask.sum())
            for i in [] if rule.endswith('consistent') else mask[mask].index[:5]:
                self.audit.example(self.table, self.column, rule, i,
                                   '' if pd.isna(old.loc[i]) else str(old.loc[i]), str(rebuilt.loc[i]))
        frame[self.column] = rebuilt
        self.last_key, self.last_rank = int(ids[-1]), int(rank[-1])

    def finish(self):
        self.audit.checks.setdefault(self.table, {}).update(
            sequence_policy='reconstructed_from_preserved_csv_row_order',
            sequence_semantics='assumed original purchase/cart order; not independently proven',
            noncontiguous_groups=0)
        self.db.execute(f'DROP TABLE groups_{self.table}')


# ===== Nhóm 5: làm sạch từng loại bảng. clean_dimension: aisles/departments/products (bảng nhỏ, nạp một lần).
# clean_detail: prior/train (bảng lớn, đọc theo khối). =====
def clean_dimension(table, c):
    """aisles/departments/products: kiểm tra khóa chính và (với products) khóa ngoại."""
    key = KEYS[table][0]
    frame = clean_frame(pd.concat(list(chunks(c.files[table], 100000, c.headers[table])),
                                  ignore_index=True), table, c.audit)
    if frame[key].duplicated().any():
        raise ValueError(f'{table}: trùng khóa chính')
    for parent in ['aisles', 'departments'] if table == 'products' else []:
        if not frame[KEYS[parent][0]].isin(c.references[parent]).all():
            raise ValueError(f'products: khóa ngoại mồ côi {KEYS[parent][0]}')
    digest = hashlib.sha256()
    key_digest(digest, frame, table)
    append_csv(frame, c.work / c.files[table].name)
    c.audit.checks[table] = {'input_rows': len(frame), 'input_columns': c.headers[table],
                             'input_key_sha256': digest.hexdigest(),
                             'primary_key_unique': True, 'foreign_keys_valid': True}


# Bảng chi tiết giỏ hàng (prior, train): kiểm khóa ngoại, khóa trùng, rồi tái dựng add_to_cart_order.
def clean_detail(table, c, order_ids, product_ids):
    """prior/train cùng cấu trúc: kiểm khóa ngoại, khóa trùng, tái dựng add_to_cart_order."""
    audit, db, source = c.audit, c.db, table.rsplit('__', 1)[1]
    db.execute('CREATE TABLE detail (order_id INTEGER, product_id INTEGER, pos INTEGER, '
               'PRIMARY KEY(order_id,product_id)) WITHOUT ROWID')
    count, digest = 0, hashlib.sha256()
    # Vòng 1: mỗi khối -> làm sạch cột -> kiểm khóa ngoại -> tái dựng thứ tự -> ghi vào SQLite và tệp tạm.
    sequence = RowSequence(db, table, 'order_id', 'add_to_cart_order', audit)
    pending = c.work / (table + '.pending')
    for raw in chunks(c.files[table], c.size, c.headers[table]):
        frame = clean_frame(raw, table, audit)
        for column, ids in [('order_id', order_ids), ('product_id', product_ids)]:
            if not frame[column].isin(ids).all():
                raise ValueError(f'{table}: {column} mồ côi')
        sequence.apply(frame)
        insert(db, 'detail', frame[['order_id', 'product_id', 'add_to_cart_order']])
        append_csv(frame, pending)
        key_digest(digest, frame, table)
        count += len(frame)
        print(f'{table}: {count:,}', flush=True)
    # Kiểm tra sau tái dựng: mỗi giỏ phải có thứ tự đúng 1..n, không trùng, không thiếu; nếu không thì dừng.
    db.execute('''CREATE TABLE basket AS SELECT order_id, COUNT(*) AS n, COUNT(pos) AS known,
        COUNT(DISTINCT pos) AS distinct_n, MIN(pos) AS min_n, MAX(pos) AS max_n
        FROM detail GROUP BY order_id''')
    with db:   # khóa chính của sources từ chối đơn vừa thuộc prior vừa thuộc train
        db.execute('INSERT INTO sources SELECT order_id, ? FROM basket', (source,))
    baskets, largest = db.execute('SELECT COUNT(*), MAX(n) FROM basket').fetchone()
    review = db.execute(f'SELECT COUNT(*) FROM basket WHERE NOT {GOOD}').fetchone()[0]
    duplicate = db.execute('SELECT COALESCE(SUM(known-distinct_n),0) FROM basket').fetchone()[0]
    export_query(db, f'''SELECT order_id, n AS basket_size, known AS parsed_positions,
        known-distinct_n AS duplicate_position_extra, min_n AS min_pos, max_n AS max_pos
        FROM basket WHERE NOT {GOOD} ORDER BY order_id LIMIT 20''',
                 audit.folder / f'{source}_basket_issue_examples.csv')
    # Vòng 2: vị trí lớn hơn kích thước giỏ là vô lý -> đặt thiếu (không đoán lại).
    sizes = pd.read_sql_query('SELECT order_id, n FROM basket', db).set_index('order_id')['n']
    rule = (table, 'position_exceeds_basket_size')
    for frame in chunks(pending, c.size, c.headers[table]):
        outside = pd.to_numeric(frame['add_to_cart_order'], errors='coerce').gt(
            frame['order_id'].astype('int64').map(sizes))
        audit.relational_counts[rule] += int(outside.sum())
        frame.loc[outside, 'add_to_cart_order'] = ''
        append_csv(frame, c.work / c.files[table].name)
    audit.checks[table] = {
        'input_rows': count, 'input_columns': c.headers[table], 'input_key_sha256': digest.hexdigest(),
        'baskets': baskets, 'largest_basket': largest, 'primary_key_unique': True,
        'foreign_keys_valid': True, 'baskets_needing_position_review': review,
        'duplicate_position_extra': duplicate,
        'positions_exceeding_basket_size_set_missing': audit.relational_counts[rule]}
    sequence.finish()
    if review:
        raise ValueError(f'{table}: kiểm tra thứ tự sau tái dựng không đạt')
    pending.unlink()
    db.execute('DROP TABLE detail')
    db.execute('DROP TABLE basket')


# ===== Nhóm 6: kiểm chứng đầu ra, so số kỳ vọng và khung chạy chung. =====
def verify_outputs(tables, c):
    """Đọc lại CSV cuối: đúng schema, số dòng, chuỗi khóa và thứ tự tái dựng."""
    for table in tables:
        digest, count, last_group, last_rank = hashlib.sha256(), 0, None, 0
        for frame in chunks(c.work / c.files[table].name, c.size, c.headers[table]):
            if table in {'orders', 'order_products__prior', 'order_products__train'}:
                group, col = (('user_id', 'order_number') if table == 'orders'
                              else ('order_id', 'add_to_cart_order'))
                expected = frame.groupby(group, sort=False).cumcount() + 1
                if frame[group].iloc[0] == last_group:
                    expected.loc[frame[group].eq(last_group)] += last_rank
                if not pd.to_numeric(frame[col], errors='coerce').eq(expected).all():
                    raise ValueError(f'{table}: thứ tự CSV cuối không khớp quy tắc tái dựng')
                last_group, last_rank = frame[group].iloc[-1], int(expected.iloc[-1])
                if table == 'orders' and not frame['eval_set'].isin(['prior', 'train', 'test']).all():
                    raise ValueError('eval_set cuối vẫn thiếu/sai')
            key_digest(digest, frame, table)
            c.audit.record_final(table, frame)
            count += len(frame)
        check = c.audit.checks[table]
        if count != check['input_rows'] or digest.hexdigest() != check['input_key_sha256']:
            raise ValueError(f'{table}: số dòng/chuỗi khóa đầu ra thay đổi')
        check.update(output_rows=count, output_columns=c.headers[table],
                     output_key_sha256=digest.hexdigest(), same_schema=True,
                     same_row_count=True, normalized_key_sequence_preserved=True)


# Kiểm tra hồi quy: số dòng, số giỏ, số lượt sửa phải bằng số đã ghi trong config.
def check_expected(audit):
    """Đối chiếu số dòng, số giỏ, số lượt sửa với config (kiểm tra hồi quy)."""
    config, checks, counts = audit.config, audit.checks, audit.relational_counts
    expected = [(checks[t]['output_rows'], n, t) for t, n in config.get('expected_rows', {}).items()]
    expected += [(checks[t]['baskets'], n, t) for t, n in config.get('expected_baskets', {}).items()]
    expected += [(counts[(t, r)], n, f'{t}.{r}') for t, rules in
                 config.get('expected_sequence_actions', {}).items() for r, n in rules.items()]
    expected += [(counts[('orders', r)], n, f'orders.{r}')
                 for r, n in config.get('expected_eval_recoveries', {}).items()]
    for observed, value, name in expected:
        if observed != value:
            raise ValueError(f'{name}: khác số đối chứng trong config')


# Khung chạy chung của hai người: hash nguồn -> làm sạch vào thư mục tạm -> đọc lại kiểm tra -> so bản trước -> xuất bản.
def run(config, config_dir, member, tables, steps):
    """Chạy `steps(c)` của một thành viên rồi kiểm chứng và xuất bản đúng `tables`."""
    started = time.perf_counter()
    paths = {k: (Path(config_dir) / config[k]).resolve()
             for k in ['input_dir', 'output_dir', 'report_dir']}
    if paths['input_dir'] == paths['output_dir']:
        raise ValueError('Thư mục đầu ra phải khác dữ liệu nguồn')
    if not config.get('reconstruct_sequences_from_preserved_row_order'):
        raise ValueError('Cần xác nhận giả định tái dựng thứ tự trong config')
    files = {t: paths['input_dir'] / f'{t}.csv' for t in SCHEMA}
    headers = {}
    for table, path in files.items():
        with path.open(encoding='utf-8-sig', newline='') as stream:
            headers[table] = next(csv.reader(stream), [])
        if sorted(headers[table]) != sorted(SCHEMA[table]):
            raise ValueError(f'{path.name}: sai tên/số cột: {headers[table]}')
    # Mỗi lượt chạy có thư mục báo cáo riêng theo thời điểm; mọi việc làm trong '_staging' trước.
    stamp = datetime.now(TZ).strftime('%Y%m%d_%H%M%S_%f')
    reports = paths['report_dir'] / stamp
    work = reports / '_staging'
    work.mkdir(parents=True)
    paths['output_dir'].mkdir(parents=True, exist_ok=True)
    audit = Audit(reports, config)
    db = sqlite3.connect(work / 'audit.sqlite')
    try:
        inputs = {t: {'sha256': sha256(p), 'bytes': p.stat().st_size, 'filename': p.name}
                  for t, p in files.items()}
        for table, expected in config.get('expected_source_sha256', {}).items():
            if inputs[table]['sha256'] != expected:
                raise ValueError(f'{table}: SHA-256 nguồn khác cấu hình')
        references = {t: read_ids(files[t], KEYS[t][0], config['chunksize'], unique=True)
                      for t in ['aisles', 'departments', 'products', 'orders']}
        db.execute('CREATE TABLE sources (order_id INTEGER PRIMARY KEY, source TEXT NOT NULL)')
        c = SimpleNamespace(files=files, headers=headers, work=work, db=db, audit=audit,
                            size=config['chunksize'], references=references)
        # Giao cho script của từng người (clean_vuong / clean_phong) làm phần làm sạch riêng.
        steps(c)
        verify_outputs(tables, c)
        check_expected(audit)
        if any(sha256(files[t]) != inputs[t]['sha256'] for t in files):
            raise ValueError('Dữ liệu nguồn thay đổi trong lúc chạy')
        # So hash với bản CSV trước: giống hệt từng byte = tái lập; nếu khác thì lưu bản cũ trước khi thay.
        comparisons = {}
        for table in tables:
            previous = paths['output_dir'] / f'{table}.csv'
            new, old = sha256(work / previous.name), sha256(previous) if previous.exists() else None
            comparisons[table] = {'new_sha256': new, 'previous_sha256': old,
                                  'byte_identical_to_previous': old == new if old else None}
            if old and old != new:   # giữ bản cũ trước khi thay
                (reports / 'previous_csv').mkdir(exist_ok=True)
                shutil.copy2(previous, reports / 'previous_csv' / previous.name)
        # Ghi báo cáo, rồi chỉ khi mọi kiểm tra đã đạt mới chép CSV sang thư mục chính.
        audit.save()
        for table in tables:   # chỉ xuất bản sau khi mọi kiểm tra đã đạt
            os.replace(work / f'{table}.csv', paths['output_dir'] / f'{table}.csv')
        write_json(reports / 'run_report.json', {
            'status': 'completed', 'assigned_to': config['assigned_to'], 'tables_cleaned': tables,
            'created_at_local': datetime.now(TZ).isoformat(),
            'seconds': round(time.perf_counter() - started, 2),
            'python': platform.python_version(), 'platform': platform.platform(),
            'packages': {'pandas': pd.__version__, 'numpy': np.__version__},
            'inputs': inputs, 'checks': audit.checks, 'output_comparison': comparisons,
            'config': config, 'source_hashes_unchanged': True,
            'assumptions': ['CSV rows preserve original purchase/cart encounter order.'],
            'limitations': ['Sequence semantics are assumed, not independently proven.',
                            'Valid-domain values may still be corrupted.',
                            'Unrecoverable attributes remain missing.']})
        write_json(paths['report_dir'] / 'latest.json', {'run_dir': stamp})
        print(f'[{member}] HOÀN TẤT: {reports}', flush=True)
        return reports
    except Exception as exc:
        write_json(reports / 'failure.json', {'status': 'failed', 'error': str(exc)})
        raise
    finally:
        db.close()
        shutil.rmtree(work)


# Dòng lệnh: đọc config (mặc định config_<tên>.json) rồi gọi run().
def cli(member, tables, steps):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    parser = argparse.ArgumentParser(description=f'Làm sạch có kiểm chứng: {member}')
    parser.add_argument('--config', type=Path, default=Path(__file__).with_name(f'config_{member}.json'))
    path = parser.parse_args().config.resolve()
    run(json.loads(path.read_text(encoding='utf-8-sig')), path.parent, member, tables, steps)
