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
