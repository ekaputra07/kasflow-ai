from .base import AsyncBaseStore
from .aiosqlite import AioSQLiteStore


def init_store(db_path: str) -> AsyncBaseStore:
    """
    Initialize the store with the given database path.

    Args:
        db_path (str): The path to the database file.

    Returns:
        AsyncBaseStore: An instance of the store.
    """
    return AioSQLiteStore(db_path)
