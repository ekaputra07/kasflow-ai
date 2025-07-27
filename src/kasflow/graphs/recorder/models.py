from pydantic import BaseModel, Field
from kasflow.models import Expense


class ExpensesSchema(BaseModel):
    """
    Holds a list of expense record (structured output from LLM).
    """

    expenses: list[Expense] = Field(
        description="A list of expense records", default_factory=list
    )
