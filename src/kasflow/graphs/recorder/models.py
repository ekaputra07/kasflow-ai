from decimal import Decimal
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, Field, field_validator, ConfigDict


class ExpenseCategory(str, Enum):
    """
    Predefined expense categories for consistency
    """
    FOOD = "food"
    TRANSPORTATION = "transportation"
    ENTERTAINMENT = "entertainment"
    UTILITIES = "utilities"
    HEALTHCARE = "healthcare"
    SHOPPING = "shopping"
    EDUCATION = "education"
    TRAVEL = "travel"
    HOUSING = "housing"
    INSURANCE = "insurance"
    OTHER = "other"


class Expense(BaseModel):
    """
    A single record of expense.
    """
    model_config = ConfigDict(use_enum_values=True)
    amount: Annotated[Decimal, Field(
        description="The monetary amount of the expense",
        gt=0,
        decimal_places=2
    )]
    category: Annotated[ExpenseCategory, Field(
        description="The category this expense belongs to"
    )]
    description: Annotated[str, Field(
        description="A brief description of the expense",
        min_length=1,
        max_length=200
    )]

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Ensure description is not just whitespace"""
        if not v or not v.strip():
            raise ValueError('Description cannot be empty or only whitespace')
        return v.strip()


class ExpenseList(BaseModel):
    """
    Holds a list of expense record.
    """
    expenses: Annotated[list[Expense], Field(
        description="A list of expense records",
        default_factory=list
    )]


class RecorderState(ExpenseList):
    """
    State of the recorder graph.
    """
    message: str = Field(
        description="input message from the user")