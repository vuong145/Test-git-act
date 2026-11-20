"""Tiện ích chung cho các script M2: đường dẫn theo thư mục bài, ghi file, cổng hash."""
import hashlib
import json
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOUNDATION_HASHES = "BAO CAO/Bao cao EDA/common/hashes.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def path(value):
    return (ROOT / value).resolve()


def relative(value):
    return Path(value).resolve().relative_to(ROOT).as_posix()


def sha256(value):
    with Path(value).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read_json(value):
    return json.loads(Path(value).read_text(encoding="utf-8"))


def config():
    """configs/m2_eda.json với các tham số đã chốt cho phép chia tập."""
    cfg = read_json(path("configs/m2_eda.json"))
    require(cfg["seed"] == 42 and cfg["rng"] == "PCG64", "Phép chia cần PCG64 seed 42")
    require(cfg["slice_order"] == ["test", "reference", "fit", "validation"], "Sai thứ tự tập")
    require(cfg["min_group_n"] == 30, "Ngưỡng báo cáo nhóm nhỏ phải là 30")
    return cfg


def atomic_write(destination, writer):
    """Ghi vào tệp tạm cạnh đích rồi os.replace; lỗi giữa chừng không làm hỏng bản cũ."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=destination.parent, suffix=".tmp")
    os.close(fd)
    try:
        writer(Path(name))
        os.replace(name, destination)
    finally:
        Path(name).unlink(missing_ok=True)


def write_json(destination, obj):
    atomic_write(destination, lambda p: p.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8"))


def write_frame(destination, frame):
    if str(destination).endswith(".parquet"):
        atomic_write(destination, lambda p: frame.to_parquet(p, index=False))
    else:
        atomic_write(destination, lambda p: frame.to_csv(
            p, index=False, encoding="utf-8", lineterminator="\n"))


def write_hashes(destination, files, **extra):
    write_json(path(destination), {"files": {relative(p): sha256(p) for p in files}, **extra})


def check_hashes(source=FOUNDATION_HASHES):
    """Dừng nếu file ghi trong `source` bị thiếu hoặc đổi nội dung; trả về bản ghi."""
    record = read_json(path(source))
    for name, expected in record["files"].items():
        require(path(name).is_file(), f"Thiếu file: {name}")
        require(sha256(path(name)) == expected, f"File đã thay đổi: {name}")
    return record


def plot_setup():
    """Matplotlib Agg, font và cỡ chữ theo configs/m2_plot_style.json."""
    os.environ.setdefault("MPLCONFIGDIR", str(path("BAO CAO/Bao cao EDA/common/.mplcache")))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    style = read_json(path("configs/m2_plot_style.json"))
    font_manager.findfont(style["font_family"], fallback_to_default=False)
    size = style["font_size_pt"]
    plt.rcParams.update({"font.family": style["font_family"], "font.size": size,
                         "axes.titlesize": size, "axes.labelsize": size,
                         "xtick.labelsize": size, "ytick.labelsize": size,
                         "legend.fontsize": size, "pdf.fonttype": 42})
    return plt, style


def save_figure(plt, fig, folder, stem, style):
    """Lưu PNG 300 DPI và PDF vector cùng tên; trả về danh sách file."""
    from PIL import Image
    files = []
    for extension in style["formats"]:
        target = path(folder) / f"{stem}.{extension}"
        atomic_write(target, lambda p: fig.savefig(
            p, format=extension, dpi=style["dpi"],
            metadata={"CreationDate": None} if extension == "pdf" else None))
        files.append(target)
    with Image.open(path(folder) / f"{stem}.png") as image:
        require(abs(image.info["dpi"][0] - style["dpi"]) < 1, "Sai DPI của PNG")
    plt.close(fig)
    return files
