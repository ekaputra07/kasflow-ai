from enum import Enum
from typing import Optional
from datetime import datetime
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

    id: Optional[int] = Field(
        description="Unique identifier for the expense", default=None
    )
    amount: float = Field(
        description="The monetary amount of the expense", ge=0.0
    )
    category: ExpenseCategory = Field(
        description="The category this expense belongs to"
    )
    description: str = Field(
        description="A brief description of the expense",
        min_length=1,
        max_length=200,
    )
    created: Optional[datetime] = Field(
        description="The date and time the expense was created", default=None
    )
    updated: Optional[datetime] = Field(
        description="The date and time the expense was updated", default=None
    )

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Ensure description is not just whitespace"""
        if not v or not v.strip():
            raise ValueError("Description cannot be empty or only whitespace")
        return v.strip()
