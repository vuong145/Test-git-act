"""Build and verify G0; pipeline records are immutable, not live pointers."""
import subprocess
import sys

from m2_common import digest, environment, path, read_json, relative, require, write_json
from m2_evidence import common_dir, new_run, writer_lock, write_state


def main():
    with writer_lock():
        run_id, directory = new_run("pipeline")
        write_state("building", run_id=run_id)
        jobs = ["tests/test_m2_foundation.py", "tests/test_m2_evidence.py",
                "scripts/m2_split_data.py", "scripts/m2_prepare_reference.py",
                "scripts/m2_verify_foundation.py", "scripts/m2_check_environment.py"]
        checks = []
        try:
            for job in jobs:
                print(f"Running {job}", flush=True)
                result = subprocess.run([sys.executable, str(path(job))],
                                        cwd=path("tests"), capture_output=True,
                                        text=True, encoding="utf-8", errors="replace")
                log = directory / (path(job).stem + ".log")
                log.write_text(result.stdout + result.stderr, encoding="utf-8")
                checks.append({"job": job, "returncode": result.returncode,
                               "log": relative(log), "log_sha256": digest(log)})
                require(result.returncode == 0, f"Failed: {job}; see {relative(log)}")
            latest = read_json(common_dir() / "latest.json")
            record = read_json(path(latest["record"]))
            write_json(directory / "pipeline.json", {
                **environment(), "status": "passed", "run_id": run_id,
                "jobs": checks, "verification": latest,
                "acceptance": record["acceptance"],
                "acceptance_sha256": record["acceptance_sha256"],
                "environment": read_json(common_dir() / "environment_latest.json"),
                "scope": "Historical full run; current consumer gate uses latest.json"})
            write_json(common_dir() / "pipeline_latest.json", {
                "record": relative(directory / "pipeline.json"),
                "sha256": digest(directory / "pipeline.json")})
        except BaseException as exc:
            write_state("failed", run_id=run_id, error=str(exc))
            write_json(directory / "failure.json", {"status": "failed", "jobs": checks,
                                                    "error": str(exc)})
            raise
    print("G0 COMPLETE: common/pipeline_latest.json; EDA gate: common/latest.json")


if __name__ == "__main__":
    main()
