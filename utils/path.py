from pathlib import Path


def get_current_dir(file):
    """
    Returns path to the current directory
    Example:
        >>> current_dir = get_current_dir(__file__)
    """
    return Path(file).resolve().parent
