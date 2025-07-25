import pytest
from pydantic import ValidationError
from kasflow.models import Expense, ExpenseCategory


def test_expense_model():
    expense = Expense(
        amount=100.0, category="food", description="Lunch at restaurant"
    )
    assert expense.id is None
    assert expense.amount == 100.0
    assert expense.category == "food"
    assert expense.description == "Lunch at restaurant"


@pytest.mark.xfail(raises=ValidationError)
def test_expense_category_validation():
    Expense(amount=100.0, category="eat", description="Lunch at restaurant")


@pytest.mark.xfail(raises=ValidationError)
def test_expense_description_validation():
    Expense(amount=100.0, category=ExpenseCategory.FOOD, description="")
