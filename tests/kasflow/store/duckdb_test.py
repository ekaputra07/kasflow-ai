from kasflow.store.duckdb import DuckDBStore


def test_store_init():
    with DuckDBStore(":memory:") as store:
        # Test table creation
        result = store.list_expenses()
        assert result == []


def test_create_and_list_expenses():
    with DuckDBStore(":memory:") as store:
        # Test table creation
        result = store.list_expenses()
        assert result == []

        # Create an expense
        store.create_expenses(
            [
                (100.0, "food", "Lunch at restaurant"),
                (50.0, "food", "Dinner at restaurant"),
            ]
        )

        # Verify the expense was created
        result = store.list_expenses()
        assert len(result) == 2
        assert result[0][1] == 50.0
        assert result[0][2] == "food"
        assert result[0][3] == "Dinner at restaurant"

        assert result[1][1] == 100.0
        assert result[1][2] == "food"
        assert result[1][3] == "Lunch at restaurant"


def test_get_expense():
    with DuckDBStore(":memory:") as store:
        # Create an expense
        store.create_expenses([(100.0, "food", "Lunch at restaurant")])

        # Get the expense by ID
        expense = store.get_expense(1)
        assert expense is not None
        assert expense[1] == 100.0
        assert expense[2] == "food"
        assert expense[3] == "Lunch at restaurant"

        # Try to get a non-existing expense
        non_existing_expense = store.get_expense(999)
        assert non_existing_expense is None
