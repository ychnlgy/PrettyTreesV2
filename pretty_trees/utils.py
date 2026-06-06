import pathlib


def readFile(path: str | pathlib.Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
