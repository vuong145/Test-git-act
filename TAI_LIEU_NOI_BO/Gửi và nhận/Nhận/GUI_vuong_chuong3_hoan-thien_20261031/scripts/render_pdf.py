"""Stage explicit presentation resources; publish only successful PDF builds."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "2521001118_Nhom01_TieuLuan.qmd"


def safe_path(root, relative):
    candidate = (root / relative).resolve()
    if Path(relative).is_absolute() or not candidate.is_relative_to(root.resolve()):
        raise ValueError("Resource escapes project: " + str(relative))
    return candidate


def referenced_files(text):
    links = re.findall(r"!\[[^\]]*\]\(<?([^\n)]+?)>?\)(?:\{[^}]*\})?", text)
    links += re.findall(r"\\(?:includegraphics|VerbatimInput)(?:\[[^\]]*\])?\{([^}]+)\}", text)
    links += re.findall(r"\{\{<\s*include\s+[\"']?([^\"' >]+)[\"']?\s*>\}\}", text)
    return [x.strip() for x in links if not re.match(r"https?://|data:", x)]


def stage_resources(root, stage, source, config):
    records = []
    def copy(relative):
        origin = safe_path(root, relative)
        if not origin.is_file():
            raise FileNotFoundError("Missing render resource: " + str(relative))
        if origin.stat().st_size > config["max_file_bytes"]:
            raise ValueError("Render resource exceeds size limit: " + str(relative))
        destination = stage / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, destination)
        records.append({"path": str(relative), "sha256": hashlib.sha256(origin.read_bytes()).hexdigest()})
    copy(source)
    for name in config["required_files"]:
        copy(name)
    for name in config["optional_directories"]:
        folder = safe_path(root, name)
        if folder.is_dir():
            for origin in sorted(folder.rglob("*")):
                if origin.is_file() and origin.suffix.lower() in config["extensions"]:
                    copy(origin.relative_to(root))
    for name in referenced_files((root / source).read_text(encoding="utf-8")):
        safe_path(root, name)
        if not (stage / name).is_file():
            raise FileNotFoundError("Referenced resource not staged: " + name)
    return records


def find_quarto():
    found = shutil.which("quarto")
    if found:
        return found
    search_dirs = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/bin",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/Quarto/bin"
    ]
    pf = os.environ.get("ProgramFiles")
    if pf:
        search_dirs.append(Path(pf) / "Quarto/bin")
    pf_x86 = os.environ.get("ProgramFiles(x86)")
    if pf_x86:
        search_dirs.append(Path(pf_x86) / "Quarto/bin")
    for folder in search_dirs:
        if (folder / "quarto.exe").is_file():
            return str(folder / "quarto.exe")
    raise FileNotFoundError("Quarto CLI not found")


def render(root=ROOT, source=SOURCE):
    source_path = safe_path(root, source)
    config = json.loads((root / "configs/render_resources.json").read_text(encoding="utf-8-sig"))
    output = source_path.with_suffix(".pdf")
    build = output.with_name(output.stem + ".build.pdf")
    reports = root / "Bao cao bien dich"
    reports.mkdir(exist_ok=True)
    quarto = find_quarto()
    with tempfile.TemporaryDirectory(prefix="tlck-render-", ignore_cleanup_errors=True) as directory:
        stage = Path(directory)
        records = stage_resources(root, stage, source, config)
        result = subprocess.run([quarto, "render", str(stage / source), "--to", "pdf",
                                 "--output", build.name], cwd=stage, capture_output=True,
                                text=True, encoding="utf-8", errors="replace")
        (reports / "render.log").write_text(result.stdout + result.stderr, encoding="utf-8")
        if result.returncode or not (stage / build.name).is_file():
            raise RuntimeError("Render failed; previous PDF preserved; see Bao cao bien dich/render.log")
        shutil.copy2(stage / build.name, build)
    os.replace(build, output)
    metadata = {"status": "passed", "source": source,
                "qmd_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
                "pdf_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                "resources": records}
    (reports / "render_manifest.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PDF:", output)
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args()
    output = render()
    if not args.no_open and hasattr(os, "startfile"):
        os.startfile(output)


if __name__ == "__main__":
    main()
