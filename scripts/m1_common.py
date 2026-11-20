"""Portable paths and per-file publication shared by the M1 commands."""

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import tempfile


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_NAMES = (
    "order_products__train.csv",
    "orders.csv",
    "products.csv",
    "aisles.csv",
    "departments.csv",
)


def project_path(value):
    """Resolve relative CLI paths against the project, never the shell cwd."""
    path = Path(value).expanduser()
    return (path if path.is_absolute() else PROJECT_ROOT / path).resolve()


def report_path(path):
    """Store relocatable paths; reports declare PROJECT_ROOT as their base."""
    return Path(os.path.relpath(Path(path).resolve(), PROJECT_ROOT)).as_posix()


def parse_args(description, *, benchmark=False):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--clean-dir", default="DATA/Data đã làm sạch",
                        help="Input directory; relative to the thesis directory.")
    parser.add_argument("--output-dir", default=None,
                        help="Report directory; relative to the thesis directory.")
    parser.add_argument("--check-inputs", action="store_true",
                        help="Check paths without importing data libraries or writing files.")
    if benchmark:
        parser.add_argument("--worker", nargs="+", help=argparse.SUPPRESS)
    else:
        parser.add_argument("--chunksize", type=int, default=250000)
    args = parser.parse_args()
    args.clean_dir = project_path(args.clean_dir)
    args.output_dir = (project_path(args.output_dir) if args.output_dir
                       else args.clean_dir / "Bảng master TLCK")
    if not benchmark and args.chunksize <= 0:
        parser.error("--chunksize must be positive")
    if args.check_inputs:
        names = INPUT_NAMES + (("master_train.parquet",) if benchmark else ())
        missing = [str(args.clean_dir / name) for name in names
                   if not (args.clean_dir / name).is_file()]
        if missing:
            parser.error("Missing inputs: " + ", ".join(missing))
        print(f"INPUTS OK: {args.clean_dir}")
        print(f"OUTPUT DIRECTORY: {args.output_dir}")
        raise SystemExit(0)
    if not __debug__:
        parser.error("Do not use python -O: the M1 audit requires assertions.")
    return args


def atomic_publish(source, destination):
    """Copy, verify and replace one destination; not a multi-file transaction.

    A failed copy/hash check/replace leaves the previous destination intact.
    The temporary file lives beside the destination to avoid cross-volume moves.
    This does not promise durability against a power failure.
    """
    source, destination = Path(source), Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent)
    temporary = Path(temporary)
    try:
        with os.fdopen(fd, "wb") as target, source.open("rb") as origin:
            shutil.copyfileobj(origin, target)
            target.flush()
            os.fsync(target.fileno())
        with source.open("rb") as origin, temporary.open("rb") as target:
            if (hashlib.file_digest(origin, "sha256").digest()
                    != hashlib.file_digest(target, "sha256").digest()):
                raise OSError("Publication copy failed SHA-256 verification")
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
