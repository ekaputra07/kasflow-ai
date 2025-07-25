import pytest
from kasflow.models import Expense
from kasflow.store.aiosqlite import AioSQLiteStore


@pytest.mark.asyncio
async def test_store_init():
    async with AioSQLiteStore(":memory:") as store:
        result = await store.list_expense()
        assert result == []


@pytest.mark.asyncio
async def test_create_and_list_expense():
    async with AioSQLiteStore(":memory:") as store:
        # Create an expense
        await store.create_expense(
            [
                Expense(
                    amount=100.0,
                    category="food",
                    description="Lunch at restaurant",
                ),
                Expense(
                    amount=50.0,
                    category="food",
                    description="Dinner at restaurant",
                ),
            ]
        )

        # Verify the expense was created
        result = await store.list_expense()
        assert len(result) == 2
        assert result[0].amount == 50.0
        assert result[0].category == "food"
        assert result[0].description == "Dinner at restaurant"

        assert result[1].amount == 100.0
        assert result[1].category == "food"
        assert result[1].description == "Lunch at restaurant"


@pytest.mark.asyncio
async def test_get_expense():
    async with AioSQLiteStore(":memory:") as store:
        # Create an expense
        await store.create_expense(
            Expense(
                amount=100.0,
                category="food",
                description="Lunch at restaurant",
            )
        )

        # Get the expense by ID
        expense = await store.get_expense(1)
        assert expense is not None
        assert expense.amount == 100.0
        assert expense.category == "food"
        assert expense.description == "Lunch at restaurant"

        # Try to get a non-existing expense
        non_existing_expense = await store.get_expense(999)
        assert non_existing_expense is None
