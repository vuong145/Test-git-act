"""Clean the three tables assigned to vuong; validate before publishing."""
from src.runner import cli


if __name__ == "__main__":
    cli("vuong", __file__)
