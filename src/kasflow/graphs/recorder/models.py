from pydantic import BaseModel, Field
from kasflow.models import Expense


class ExpenseList(BaseModel):
    """
    Holds a list of expense record (structured output from LLM).
    """

    expenses: list[Expense] = Field(
        description="A list of expense records", default_factory=list
    )


class RecorderState(ExpenseList):
    """
    State of the recorder graph.
    """

    message: str = Field(description="input message from the user")
    stored: bool = Field(
        description="whether the message has been stored", default=False
    )
    store_exception: str = Field(
        description="exception message raised during storing the message",
        default="",
    )
