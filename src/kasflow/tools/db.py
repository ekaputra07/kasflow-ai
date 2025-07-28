from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from kasflow.store import init_store
from kasflow.utils import format_currency


@tool
async def list_expenses(
    db_path: Annotated[str, InjectedState("db_path")],
) -> str:
    """
    Get a list of all expenses
    """
    async with init_store(db_path) as store:
        expenses = await store.list_expenses()
        if not expenses:
            return "No expenses found"

        return "\n".join(
            [
                f"{e.created.strftime('%b %d %H:%M')} - {format_currency(e.amount)} - {e.description}"
                for e in expenses
            ]
        )
