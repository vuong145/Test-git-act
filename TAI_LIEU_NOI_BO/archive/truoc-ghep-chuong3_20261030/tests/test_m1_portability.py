"""Regression checks for portable M1 entry points and safe file publication."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import m1_common


class M1PortabilityTests(unittest.TestCase):
    def test_commands_resolve_inputs_outside_project(self):
        with tempfile.TemporaryDirectory() as cwd:
            for script in ("m1_build_master.py", "m1_benchmark.py"):
                result = subprocess.run(
                    [sys.executable, str(SCRIPTS / script), "--check-inputs"],
                    cwd=cwd, capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("INPUTS OK:", result.stdout)

    def test_explicit_relative_paths_are_project_relative(self):
        with tempfile.TemporaryDirectory() as cwd:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "m1_build_master.py"),
                 "--clean-dir", "DATA/Data đã làm sạch",
                 "--output-dir", "DATA/Data đã làm sạch/Bảng master TLCK",
                 "--check-inputs"],
                cwd=cwd, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(m1_common.PROJECT_ROOT), result.stdout)

    def test_missing_inputs_fail_before_processing(self):
        with tempfile.TemporaryDirectory() as empty:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "m1_build_master.py"),
                 "--clean-dir", empty, "--check-inputs"],
                cwd=empty, capture_output=True, text=True, encoding="utf-8")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Missing inputs:", result.stderr)
            self.assertEqual(list(Path(empty).iterdir()), [])

    def test_successful_publication_preserves_source_and_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            source, target = Path(folder) / "source", Path(folder) / "target"
            source.write_bytes(b"verified master")
            target.write_bytes(b"previous master")
            m1_common.atomic_publish(source, target)
            self.assertEqual(target.read_bytes(), source.read_bytes())
            self.assertEqual(len(list(Path(folder).iterdir())), 2)

    def test_failed_replace_preserves_previous_target(self):
        with tempfile.TemporaryDirectory() as folder:
            source, target = Path(folder) / "source", Path(folder) / "target"
            source.write_bytes(b"new")
            target.write_bytes(b"previous")
            with patch.object(m1_common.os, "replace", side_effect=PermissionError):
                with self.assertRaises(PermissionError):
                    m1_common.atomic_publish(source, target)
            self.assertEqual(target.read_bytes(), b"previous")
            self.assertEqual(len(list(Path(folder).iterdir())), 2)

    def test_partial_copy_never_replaces_target(self):
        def broken_copy(origin, destination):
            destination.write(b"partial")
            raise OSError("interrupted")

        with tempfile.TemporaryDirectory() as folder:
            source, target = Path(folder) / "source", Path(folder) / "target"
            source.write_bytes(b"new")
            target.write_bytes(b"previous")
            with patch.object(m1_common.shutil, "copyfileobj", broken_copy):
                with self.assertRaises(OSError):
                    m1_common.atomic_publish(source, target)
            self.assertEqual(target.read_bytes(), b"previous")
            self.assertEqual(len(list(Path(folder).iterdir())), 2)

    def test_corrupt_copy_never_replaces_target(self):
        def corrupt_copy(origin, destination):
            destination.write(b"wrong content")

        with tempfile.TemporaryDirectory() as folder:
            source, target = Path(folder) / "source", Path(folder) / "target"
            source.write_bytes(b"new")
            target.write_bytes(b"previous")
            with patch.object(m1_common.shutil, "copyfileobj", corrupt_copy):
                with self.assertRaises(OSError):
                    m1_common.atomic_publish(source, target)
            self.assertEqual(target.read_bytes(), b"previous")


if __name__ == "__main__":
    unittest.main()
