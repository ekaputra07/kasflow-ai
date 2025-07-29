import logging
import aiofiles
from datetime import datetime, UTC
from pathlib import Path
from telegram import Update
from kasflow.conf import BASE_DIR

logger = logging.getLogger(__name__)


def now() -> datetime:
    """
    Returns the current date and time in the UTC timezone.
    """
    return datetime.now(UTC)


async def read_text_file(path: str, base_dir: Path = BASE_DIR) -> str:
    """
    Read a text file from the given path relative to kasflow package.
    Args:
        path (str): The relative path to the text file.
    Returns:
        str: The content of the text file.
    """
    filename = base_dir / path
    async with aiofiles.open(filename) as file:
        return await file.read()


def database_path(id: str | int, ext: str = ".db") -> str:
    """
    Return the path to the database file for the given user ID.
    Args:
        id (str | int): The user/group ID.
    Returns:
        str: The path to the database file.
    """
    return f"{BASE_DIR}/data/db/{id}{ext}"


def format_currency(amount: float) -> str:
    """Format currency with optional decimal places."""
    if amount % 1 == 0:
        return f"{amount:,.0f}"
    else:
        return f"{amount:,.2f}"


def is_group_update(update: Update) -> bool:
    """
    Check if the update is from a group chat.
    Args:
        update (Update): The Telegram update object.
    Returns:
        bool: True if the update is from a group chat, False otherwise.
    """
    return update.message.chat.type in ["group", "supergroup"]
