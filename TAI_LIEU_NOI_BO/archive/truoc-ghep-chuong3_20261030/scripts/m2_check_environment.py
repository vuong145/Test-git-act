"""Verify locked packages and render a clearly synthetic style preview."""

import os
from importlib.metadata import version

from m2_common import (config, environment, path, read_json, require, snapshot,
                       write_json, digest, relative)
from m2_evidence import common_dir, new_run, writer_lock


def main():
    cfg = config()
    run_id, reports = new_run("environment")
    cache = common_dir() / ".mplcache"
    cache.mkdir(exist_ok=True)
    os.environ["MPLCONFIGDIR"] = str(cache)
    for line in path("requirements-m2-lock.txt").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        name, expected = line.split("==")
        require(version(name) == expected, f"Package version mismatch: {name}")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from PIL import Image

    style = read_json(path("configs/m2_plot_style.json"))
    font_manager.findfont(style["font_family"], fallback_to_default=False)
    plt.rcParams.update({"font.family": style["font_family"],
                         "font.size": style["font_size_pt"]})
    figure, axes = plt.subplots(figsize=(style["figure_width_inches"], 3.6),
                                layout="constrained")
    axes.bar(["Giỏ A", "Giỏ B", "Giỏ C"], [3, 1, 1], color=style["colors"][:3])
    axes.set_ylabel("Số sản phẩm (fixture)")
    axes.set_title("KIỂM TRA FONT — DỮ LIỆU GIẢ LẬP\nKhông phải kết quả nghiên cứu")
    png, pdf = reports / "style_fixture.png", reports / "style_fixture.pdf"
    figure.savefig(png, dpi=style["dpi"])
    figure.savefig(pdf)
    plt.close(figure)
    with Image.open(png) as preview:
        require(abs(preview.info["dpi"][0] - 300) < 1, "Incorrect figure DPI")
    write_json(reports / "environment_validation.json", {
        **environment(), "status": "passed", "run_id": run_id, "lock_packages_match": True,
        "font_family": style["font_family"], "font_fallback": False,
        "png_dpi": 300, "plot_is_synthetic": True,
        "artifacts": snapshot([png, pdf, path("requirements-m2-lock.txt"),
                               path("scripts/m2_check_environment.py")])})
    write_json(common_dir() / "environment_latest.json", {
        "run_id": run_id,
        "record": relative(reports / "environment_validation.json"),
        "sha256": digest(reports / "environment_validation.json")})
    print("M2 ENVIRONMENT AND SYNTHETIC STYLE CHECK PASSED")


if __name__ == "__main__":
    with writer_lock():
        main()
