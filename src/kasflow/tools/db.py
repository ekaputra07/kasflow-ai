from datetime import datetime
from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from kasflow.db.session import sessionmaker
from kasflow.db.repository import ExpenseRepository


@tool
async def list_expenses(
    from_datetime: str,
    to_datetime: str,
    thread_id: Annotated[int, InjectedState("thread_id")],
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

    expenses = []
    async with sessionmaker() as session:
        repo = ExpenseRepository(session)
        expenses = await repo.list_by_thread_id_and_date_range(
            thread_id=thread_id, from_date=from_, to_date=to_
        )
        if not expenses:
            return f"No expenses found between {from_datetime} and {to_datetime}"

        items = "\n".join([e.as_list_item() for e in expenses])
        return f"""
        List of expenses between {from_datetime} and {to_datetime}:
        {items}
        """
