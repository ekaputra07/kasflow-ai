from typing import Annotated
from pydantic import BaseModel, Field
from kasflow.models import Expense


class ExpenseList(BaseModel):
    """
    Holds a list of expense record (structured output from LLM).
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