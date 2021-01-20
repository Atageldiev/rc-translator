from pathlib import Path


def get_current_dir(file):
    return Path(file).resolve().parent
