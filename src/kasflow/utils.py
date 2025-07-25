from pathlib import Path
from kasflow.conf import BASE_DIR


def read_text_file(path: str, base_dir: Path = BASE_DIR) -> str:
    """
    Read a text file from the given path relative to kasflow package.
    Args:
        path (str): The relative path to the text file.
    Returns:
        str: The content of the text file.
    """
    filename = base_dir / path
    with open(filename) as file:
        return file.read()


def db_path(id: str | int) -> str:
    """
    Return the path to the database file for the given user ID.
    Args:
        id (str | int): The user/group ID.
    Returns:
        str: The path to the database file.
    """
    return f"{BASE_DIR}/data/db/{id}.db"


def format_currency(amount: float) -> str:
    """Format currency with optional decimal places."""
    if amount % 1 == 0:
        return f"{amount:,.0f}"
    else:
        return f"{amount:,.2f}"
