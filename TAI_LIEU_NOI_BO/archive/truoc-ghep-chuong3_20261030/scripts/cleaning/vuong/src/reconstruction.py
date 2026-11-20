"""Explicit assumption: original CSV encounter order is purchase/cart order.
No sequence is reconstructed using order_id or product_id sorting.
"""
import sqlite3
import numpy as np
import pandas as pd


class RowSequence:
    """Number contiguous groups, preserving state across arbitrary chunk boundaries.
    A disk registry rejects groups that reappear, including across chunks.
    """
    def __init__(self, db, table, key, column, audit, maximum=None):
        self.db, self.table, self.key, self.column, self.audit = db, table, key, column, audit
        self.maximum = maximum
        self.last_key = None
        self.last_rank = 0
        self.registry = 'sequence_groups_' + table
        db.execute(f'CREATE TABLE {self.registry}(id INTEGER PRIMARY KEY)')

    def apply(self, frame):
        if frame.empty:
            return
        ids = frame[self.key].to_numpy(dtype=np.int64)
        index = np.arange(len(ids), dtype=np.int64)
        starts = np.empty(len(ids), dtype=bool)
        starts[0] = True
        starts[1:] = ids[1:] != ids[:-1]
        last_start = np.maximum.accumulate(np.where(starts, index, 0))
        rank = index - last_start + 1
        continuing = self.last_key is not None and ids[0] == self.last_key
        if continuing:
            rank[last_start == 0] += self.last_rank
        new = starts.copy()
        if continuing:
            new[0] = False
        # Duplicate group identity means the file is not contiguous as audited.
        try:
            self.db.executemany(f'INSERT INTO {self.registry} VALUES(?)',
                                ((int(x),) for x in ids[new]))
        except sqlite3.IntegrityError as exc:
            raise ValueError(f'{self.table}: nhóm xuất hiện lại; dừng tái dựng thứ tự') from exc
        if self.maximum is not None and (rank > self.maximum).any():
            raise ValueError(f'{self.table}: thứ tự vượt giới hạn {self.maximum}')
        old = frame[self.column].copy()
        reconstructed = pd.Series(rank, index=frame.index, dtype=old.dtype)
        missing = old.isna()
        changed = (~missing & old.ne(reconstructed)).fillna(False)
        same = (~missing & old.eq(reconstructed)).fillna(False)
        for rule, mask in [('sequence_filled_unusable', missing),
                           ('sequence_corrected_observed', changed),
                           ('sequence_observed_consistent', same)]:
            self.audit.relational_counts[(self.table, rule)] += int(mask.sum())
        status = pd.Series('consistent', index=frame.index, dtype='string')
        status.loc[missing] = 'sequence_filled_unusable'
        status.loc[changed] = 'sequence_corrected_observed'
        # Bounded examples go into the existing independent examples file.
        for rule in ['sequence_filled_unusable', 'sequence_corrected_observed']:
            k = (self.table, self.column, rule)
            cap = max(0, 5 - self.audit.example_counts[k])
            for i in status[status.eq(rule)].index[:cap]:
                self.audit.examples.append({'table': self.table, 'column': self.column,
                    'status': rule, 'record_1based': int(i) + 1,
                    'raw': '' if pd.isna(old.loc[i]) else str(old.loc[i]),
                    'clean': str(reconstructed.loc[i])})
                self.audit.example_counts[k] += 1
        frame[self.column] = reconstructed
        self.last_key, self.last_rank = int(ids[-1]), int(rank[-1])

    def finish(self):
        self.audit.checks.setdefault(self.table, {}).update(
            sequence_policy='reconstructed_from_preserved_csv_row_order',
            sequence_semantics='assumed original purchase/cart order; not independently proven',
            noncontiguous_groups=0)
        self.db.execute(f'DROP TABLE {self.registry}')
        self.db.commit()
