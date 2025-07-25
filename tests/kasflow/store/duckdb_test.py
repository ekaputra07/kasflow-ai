from kasflow.models import Expense
from kasflow.store.duckdb import DuckDBStore


def test_store_init():
    with DuckDBStore(":memory:") as store:
        result = store.list_expense()
        assert result == []


def test_create_and_list_expense():
    with DuckDBStore(":memory:") as store:
        # Create an expense
        store.create_expense(
            [
                Expense(amount=100.0, category="food", description="Lunch at restaurant"),
                Expense(amount=50.0, category="food", description="Dinner at restaurant"),
            ]
        )

        # Verify the expense was created
        result = store.list_expense()
        assert len(result) == 2
        assert result[0].amount == 50.0
        assert result[0].category == "food"
        assert result[0].description == "Dinner at restaurant"

        assert result[1].amount == 100.0
        assert result[1].category == "food"
        assert result[1].description == "Lunch at restaurant"


def test_get_expense():
    with DuckDBStore(":memory:") as store:
        # Create an expense
        store.create_expense(Expense(amount=100.0, category="food", description="Lunch at restaurant"))

        # Get the expense by ID
        expense = store.get_expense(1)
        assert expense is not None
        assert expense.amount == 100.0
        assert expense.category == "food"
        assert expense.description == "Lunch at restaurant"

        # Try to get a non-existing expense
        non_existing_expense = store.get_expense(999)
        assert non_existing_expense is None
