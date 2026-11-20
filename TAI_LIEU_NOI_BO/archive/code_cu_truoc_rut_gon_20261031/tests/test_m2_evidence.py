"""Regression tests for fail-closed acceptance, immutable runs and config."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import m2_common as common
import m2_evidence as evidence


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.cfg = common.config()
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.root_patch = patch.object(common, "ROOT", self.root)
        self.root_patch.start()
        self.token = os.environ.pop("M2_WRITER_TOKEN", None)
        (self.root / "configs").mkdir()
        (self.root / "scripts").mkdir()
        for name in ["m2_verify_foundation.py", "m2_evidence.py"]:
            (self.root / "scripts" / name).write_text("fixture")
        common.write_json(self.root / "configs/m2_eda.json", self.cfg)
        (self.root / "source.bin").write_bytes(b"source")
        self.reports = evidence.common_dir()
        self.reports.mkdir(parents=True)
        common.write_json(self.reports / "foundation_manifest.json", {
            "sources": {"source.bin": common.digest(self.root / "source.bin")},
            "configs": {"configs/m2_eda.json": common.digest(self.root / "configs/m2_eda.json")},
            "outputs": {}, "code": {}, "counts": {"fixture": True}})

    def tearDown(self):
        self.root_patch.stop()
        if self.token is not None:
            os.environ["M2_WRITER_TOKEN"] = self.token
        self.temp.cleanup()

    def commit(self):
        return evidence.verify_and_commit(lambda cfg, manifest, checks: checks.update(fixture=True))

    def test_success_and_second_verify_preserve_old_acceptance(self):
        first = self.commit()
        old = common.path(first["acceptance"]).read_bytes()
        second = self.commit()
        self.assertNotEqual(first["run_id"], second["run_id"])
        self.assertEqual(old, common.path(first["acceptance"]).read_bytes())
        common.load_foundation()

    def test_missing_acceptance_rejected(self):
        record = self.commit()
        common.path(record["acceptance"]).unlink()
        with self.assertRaises(FileNotFoundError):
            common.load_foundation()

    def test_changed_output_rejected(self):
        self.commit()
        (self.root / "source.bin").write_bytes(b"modified")
        with self.assertRaisesRegex(ValueError, "Changed artifact"):
            common.load_foundation()

    def test_old_or_modified_acceptance_rejected(self):
        record = self.commit()
        target = common.path(record["acceptance"])
        data = common.read_json(target)
        data["run_id"] = "old"
        common.write_json(target, data)
        with self.assertRaisesRegex(ValueError, "Acceptance hash"):
            common.load_foundation()

    def test_failed_independent_assertion_invalidates_old_pass(self):
        self.commit()

        def broken(cfg, manifest, checks):
            checks["reached_independent_check"] = True
            raise AssertionError("semantic mismatch with intact hashes")

        with self.assertRaises(AssertionError):
            evidence.verify_and_commit(broken)
        state = common.read_json(self.reports / "foundation_validation.json")
        self.assertEqual(state["status"], "failed")
        self.assertTrue(state["checks"]["reached_independent_check"])
        with self.assertRaisesRegex(ValueError, "not passed"):
            common.load_foundation()

    def test_interruption_invalidates_previous_pass(self):
        self.commit()
        with self.assertRaises(KeyboardInterrupt):
            evidence.verify_and_commit(lambda *args: (_ for _ in ()).throw(KeyboardInterrupt()))
        with self.assertRaisesRegex(ValueError, "not passed"):
            common.load_foundation()

    def test_failed_error_write_still_leaves_verifying(self):
        self.commit()
        original = evidence.write_state

        def unavailable(status, **kwargs):
            if status == "failed":
                raise OSError("disk unavailable")
            return original(status, **kwargs)

        with patch.object(evidence, "write_state", unavailable):
            with self.assertRaises(OSError):
                evidence.verify_and_commit(lambda *args: (_ for _ in ()).throw(ValueError("bad")))
        self.assertEqual(common.read_json(self.reports / "foundation_validation.json")["status"],
                         "verifying")
        with self.assertRaisesRegex(ValueError, "not passed"):
            common.load_foundation()

    def test_split_rule_and_contract_rejected(self):
        for key, value in [("split_rule", "different"), ("contract_version", 99)]:
            altered = {**self.cfg, key: value}
            common.write_json(self.root / "configs/m2_eda.json", altered)
            with self.assertRaisesRegex(ValueError, "Unsupported"):
                common.config()

    def test_changed_config_in_verify_marks_failed(self):
        self.commit()
        altered = {**self.cfg, "top_n_grid": [1]}
        common.write_json(self.root / "configs/m2_eda.json", altered)
        with self.assertRaisesRegex(ValueError, "Changed artifact"):
            self.commit()
        self.assertEqual(common.read_json(self.reports / "foundation_validation.json")["status"],
                         "failed")

    def test_interrupted_state_and_writer_lock(self):
        self.commit()
        evidence.write_state("verifying", run_id="interrupted")
        with self.assertRaisesRegex(ValueError, "not passed"):
            common.load_foundation()
        (self.reports / ".writer.lock").write_text("other-process")
        with self.assertRaises(FileExistsError):
            self.commit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
