import pytest
from kasflow.models import Expense
from kasflow.store.aiosqlite import AioSQLiteStore


@pytest.mark.asyncio
async def test_store_init():
    async with AioSQLiteStore(":memory:") as store:
        result = await store.list_expenses()
        assert result == []


@pytest.mark.asyncio
async def test_create_and_list_expenses():
    async with AioSQLiteStore(":memory:") as store:
        # Create an expense
        await store.create_expense(
            [
                Expense(
                    user_id=1,
                    amount=100.0,
                    category="food",
                    description="Lunch at restaurant",
                ),
                Expense(
                    user_id=2,
                    amount=50.0,
                    category="food",
                    description="Dinner at restaurant",
                ),
            ]
        )

        # Verify the expense was created
        result = await store.list_expenses()
        assert len(result) == 2
        assert result[0].user_id == 2
        assert result[0].amount == 50.0
        assert result[0].category == "food"
        assert result[0].description == "Dinner at restaurant"

        assert result[1].user_id == 1
        assert result[1].amount == 100.0
        assert result[1].category == "food"
        assert result[1].description == "Lunch at restaurant"

        # List user expenses
        user_expenses = await store.list_user_expenses(1)
        assert len(user_expenses) == 1
        assert user_expenses[0].user_id == 1


@pytest.mark.asyncio
async def test_get_expense():
    async with AioSQLiteStore(":memory:") as store:
        # Create an expense
        await store.create_expense(
            Expense(
                user_id=1,
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


@pytest.mark.asyncio
async def test_get_user_expense():
    async with AioSQLiteStore(":memory:") as store:
        # Create a list of expenses
        await store.create_expense(
            [
                Expense(
                    user_id=1,
                    amount=100.0,
                    category="food",
                    description="Lunch at restaurant",
                ),
                Expense(
                    user_id=2,
                    amount=50.0,
                    category="food",
                    description="Dinner at restaurant",
                ),
            ]
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

        # Get user-specific expense
        user_expense = await store.get_user_expense(1, 1)
        assert user_expense is not None
        assert user_expense.user_id == 1

        # Try to get a user-specific expense that doesn't exist
        non_existing_user_expense = await store.get_user_expense(1, 999)
        assert non_existing_user_expense is None
