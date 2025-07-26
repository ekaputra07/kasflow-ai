import pytest
from kasflow.store import init_store
from kasflow.store.aiosqlite import AioSQLiteStore


@pytest.mark.asyncio
async def test_init_store():
    """
    Test the initialization of the store.
    """
    db_path = ":memory:"
    async with init_store(db_path) as store:
        assert store is not None
        assert isinstance(store, AioSQLiteStore)
        assert store.db_path == db_path
