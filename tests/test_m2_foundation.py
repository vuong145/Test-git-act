"""Small, hand-checkable G0 fixtures. No writes to the production dataset."""

import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from m2_foundation import (build_baskets, canonical_split_sha256 as canonical_manifest,
                           make_split, validate_master)
from project_io import atomic_write, config


def fixture():
    return pd.DataFrame({
        "order_id": [1, 1, 1, 2, 3], "user_id": [11, 11, 11, 12, 13],
        "product_id": [1, 2, 3, 4, 5], "aisle_id": [1, 1, 2, 3, 4],
        "department_id": [3, 3, 16, 21, 4], "eval_set": ["train"] * 5,
        "product_name": [None, "b", "c", "d", "e"],
        "order_dow": pd.array([1, 1, 1, None, 6], dtype="Int8"),
        "order_hour_of_day": pd.array([6, 6, 6, None, 23], dtype="Int8"),
        "days_since_prior_order": pd.array([30, 30, 30, None, 0], dtype="Float32")})


class FoundationTests(unittest.TestCase):
    def test_split_counts_union_reproducibility(self):
        users = range(1, 131210)
        a, b = make_split(users), make_split(reversed(users))
        self.assertEqual(a.split.value_counts().to_dict(),
                         {"reference": 39363, "fit": 39363,
                          "test": 26242, "validation": 26241})
        self.assertEqual(set(a.user_id), set(users))
        self.assertFalse(a.user_id.duplicated().any())
        self.assertEqual(canonical_manifest(a), canonical_manifest(b))
        self.assertNotEqual(canonical_manifest(a), canonical_manifest(make_split(users, 43)))

    def test_split_small_rounding(self):
        for n in range(5, 25):
            result = make_split(range(n))
            self.assertEqual(len(result), n)
            self.assertEqual(result.split.eq("test").sum(), (n + 4) // 5)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            make_split([1, 1, 2, 3, 4])

    def test_baskets_missing_singleton_and_repeated_department(self):
        result = build_baskets(fixture(), config())
        self.assertEqual(result.basket_size.tolist(), [3, 1, 1])
        self.assertEqual(result.n_departments.tolist(), [2, 1, 1])
        self.assertEqual(result.n_aisles.tolist(), [2, 1, 1])
        self.assertEqual(result.hour_band.iloc[0], "06–11")
        self.assertTrue(pd.isna(result.hour_band.iloc[1]))
        self.assertEqual(result.hour_band.iloc[2], "18–23")
        self.assertTrue(pd.isna(result.days_since_prior_order.iloc[1]))

    def test_hour_boundaries(self):
        hours = [0, 5, 6, 11, 12, 17, 18, 23]
        base = pd.concat([fixture().iloc[[3]]] * 8, ignore_index=True)
        base["order_id"] = range(8)
        base["user_id"] = range(8)
        base["order_hour_of_day"] = pd.array(hours, dtype="Int8")
        self.assertEqual(build_baskets(base, config()).hour_band.tolist(),
                         ["00–05"] * 2 + ["06–11"] * 2 + ["12–17"] * 2 + ["18–23"] * 2)

    def test_reject_corrupt_keys_and_multiple_baskets(self):
        frame = fixture()
        with self.assertRaisesRegex(ValueError, "Duplicate order"):
            validate_master(pd.concat([frame, frame.iloc[[0]]]))
        frame.loc[3, "user_id"] = 11
        with self.assertRaisesRegex(ValueError, "Multiple baskets"):
            validate_master(frame)

    def test_reject_conflicting_na_and_invalid_hour(self):
        frame = fixture()
        frame.loc[0, "order_dow"] = pd.NA
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            build_baskets(frame, config())
        frame = fixture()
        frame.loc[4, "order_hour_of_day"] = 24
        with self.assertRaisesRegex(ValueError, "Invalid domain"):
            build_baskets(frame, config())

    def test_failed_write_preserves_previous(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "result.json"
            target.write_text("old", encoding="utf-8")

            def broken(temp):
                temp.write_text("incomplete", encoding="utf-8")
                raise RuntimeError("failure")

            with self.assertRaises(RuntimeError):
                atomic_write(target, broken)
            self.assertEqual(target.read_text(), "old")
            self.assertEqual(len(list(Path(directory).iterdir())), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
