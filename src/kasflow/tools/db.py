from datetime import datetime
from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from kasflow.store import init_store
from kasflow.utils import format_currency


@tool
async def list_expenses(
    from_datetime: str,
    to_datetime: str,
    db_path: Annotated[str, InjectedState("db_path")],
) -> str:
    """
    Get a list of all expenses between two dates.
    Args:
        from_datetime (str): The start date and time in the format of YYYY-MM-DD HH:MM:SS
        to_datetime (str): The end date and time in the format of YYYY-MM-DD HH:MM:SS
    Returns:
        str: A list of expenses between the two dates
    """
    from_ = datetime.strptime(from_datetime, "%Y-%m-%d %H:%M:%S")
    to_ = datetime.strptime(to_datetime, "%Y-%m-%d %H:%M:%S")

    async with init_store(db_path) as store:
        expenses = await store.list_expenses_by_date_range(
            from_datetime=from_, to_datetime=to_
        )
        if not expenses:
            return (
                f"No expenses found between {from_datetime} and {to_datetime}"
            )

        items = "\n".join(
            [
                f"{e.created.strftime('%b %d %H:%M')} - {format_currency(e.amount)} - {e.description}"
                for e in expenses
            ]
        )
        return f"""
        List of expenses between {from_datetime} and {to_datetime}:
        {items}
        """
