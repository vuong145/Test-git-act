"""Clean the three tables assigned to phong; validate before publishing."""
from src.runner import cli


if __name__ == "__main__":
    cli("phong", __file__)
