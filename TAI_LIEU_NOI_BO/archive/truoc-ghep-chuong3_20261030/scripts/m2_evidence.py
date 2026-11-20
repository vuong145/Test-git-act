"""Immutable verification runs, fail-closed state and single-writer lock."""

import os
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone

from m2_common import (digest, environment, load_foundation_inputs, path,
                       read_json, relative, require, write_json)


def common_dir():
    # State location cannot be redirected by a malformed config.
    return path("BAO CAO/Bao cao EDA/common")


def new_run(kind):
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "_" + uuid.uuid4().hex[:8]
    directory = common_dir() / "runs" / kind / run_id
    directory.mkdir(parents=True, exist_ok=False)
    return run_id, directory


@contextmanager
def writer_lock():
    root = common_dir()
    root.mkdir(parents=True, exist_ok=True)
    lock = root / ".writer.lock"
    inherited = os.environ.get("M2_WRITER_TOKEN")
    if inherited and lock.exists() and lock.read_text() == inherited:
        yield
        return
    token = uuid.uuid4().hex
    # Existing lock is never silently removed, even after a crash.
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    with os.fdopen(descriptor, "w") as stream:
        stream.write(token)
    old = os.environ.get("M2_WRITER_TOKEN")
    os.environ["M2_WRITER_TOKEN"] = token
    try:
        yield
    finally:
        if old is None:
            os.environ.pop("M2_WRITER_TOKEN", None)
        else:
            os.environ["M2_WRITER_TOKEN"] = old
        lock.unlink()


def write_state(status, **fields):
    write_json(common_dir() / "foundation_validation.json",
               {"status": status, **fields})


def verify_and_commit(checker):
    """State invalidated before any read/check; interruption cannot leave passed."""
    with writer_lock():
        run_id, directory = new_run("verification")
        checks = {}
        write_state("verifying", run_id=run_id)
        try:
            cfg, manifest = load_foundation_inputs()
            manifest_sha = digest(common_dir() / "foundation_manifest.json")
            checks["input_hashes"] = True
            checker(cfg, manifest, checks)
            load_foundation_inputs()
            require(digest(common_dir() / "foundation_manifest.json") == manifest_sha,
                    "Manifest changed during verification")
            checks["hashes_after_checks"] = True
            acceptance = {**environment(), "status": "passed", "run_id": run_id,
                          "foundation_manifest_sha256": manifest_sha,
                          "checks": checks, "counts": manifest["counts"],
                          "verifier_sha256": digest(path("scripts/m2_verify_foundation.py")),
                          "evidence_code_sha256": digest(path("scripts/m2_evidence.py"))}
            write_json(directory / "acceptance.json", acceptance)
            record = {"status": "passed", "run_id": run_id,
                      "foundation_manifest_sha256": manifest_sha,
                      "acceptance": relative(directory / "acceptance.json"),
                      "acceptance_sha256": digest(directory / "acceptance.json")}
            write_json(directory / "run.json", record)
            latest = {"run_id": run_id, "record": relative(directory / "run.json"),
                      "record_sha256": digest(directory / "run.json")}
            write_json(common_dir() / "latest.json", latest)
            # Commit is last. A failed write here leaves verifying/failed.
            write_state("passed", run_id=run_id,
                        manifest_sha256=manifest_sha,
                        latest_sha256=digest(common_dir() / "latest.json"))
            return record
        except BaseException as exc:
            failure = {"status": "failed", "run_id": run_id, "checks": checks,
                       "error_type": type(exc).__name__, "error": str(exc)}
            try:
                write_json(directory / "failure.json", failure)
            finally:
                write_state("failed", run_id=run_id, checks=checks,
                            error_type=type(exc).__name__, error=str(exc))
            raise


def accepted_foundation():
    root = common_dir()
    state = read_json(root / "foundation_validation.json")
    require(state["status"] == "passed", "G0 state is not passed")
    latest = read_json(root / "latest.json")
    require(digest(root / "latest.json") == state["latest_sha256"], "Latest pointer mismatch")
    require(latest["run_id"] == state["run_id"], "State/run mismatch")
    record_file = path(latest["record"])
    require(record_file.is_relative_to(root / "runs"), "Run path outside evidence tree")
    require(digest(record_file) == latest["record_sha256"], "Run record hash mismatch")
    record = read_json(record_file)
    acceptance_file = path(record["acceptance"])
    require(acceptance_file.parent == record_file.parent, "Acceptance from another run")
    require(digest(acceptance_file) == record["acceptance_sha256"], "Acceptance hash mismatch")
    acceptance = read_json(acceptance_file)
    for obj in (record, acceptance):
        require(obj["status"] == "passed" and obj["run_id"] == state["run_id"],
                "Acceptance not passed/current")
        require(obj["foundation_manifest_sha256"] == state["manifest_sha256"],
                "Acceptance belongs to another foundation")
    require(digest(root / "foundation_manifest.json") == state["manifest_sha256"],
            "Foundation manifest changed")
    require(acceptance["verifier_sha256"] == digest(path("scripts/m2_verify_foundation.py")),
            "Verifier changed after acceptance")
    require(acceptance["evidence_code_sha256"] == digest(path("scripts/m2_evidence.py")),
            "Evidence code changed after acceptance")
    result = load_foundation_inputs()
    require(read_json(root / "foundation_validation.json") == state,
            "State changed while loading foundation")
    return result
