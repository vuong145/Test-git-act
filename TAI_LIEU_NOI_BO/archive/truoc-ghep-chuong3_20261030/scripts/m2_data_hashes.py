"""Kiểm tra dữ liệu bằng SHA-256 trước khi đọc; thay cho chuỗi manifest G0 nhiều tầng."""
from m2_common import digest, path, read_json, require, snapshot, write_json

FOUNDATION_HASHES = "BAO CAO/Bao cao EDA/common/hashes.json"


def write_data_hashes(destination, files, **extra):
    """Ghi SHA-256 của các file đầu ra (đường dẫn tương đối theo thư mục bài)."""
    write_json(destination, {"files": snapshot(files), **extra})


def check_data_hashes(source=FOUNDATION_HASHES):
    """Dừng nếu file được ghi trong `source` bị thiếu hoặc đổi nội dung."""
    record = read_json(path(source))
    for name, expected in record["files"].items():
        require(path(name).is_file(), f"Thiếu file: {name}")
        require(digest(path(name)) == expected, f"File đã thay đổi: {name}")
    return record
