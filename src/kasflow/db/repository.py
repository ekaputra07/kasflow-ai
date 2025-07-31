from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from kasflow.db.models import Expense


class ExpenseRepository:
    """
    Repository for managing expenses in the database.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, expense: Expense | list[Expense]):
        """
        Create a new expense or a list of expenses.
        """
        if isinstance(expense, list):
            self.session.add_all(expense)
        else:
            self.session.add(expense)
        await self.session.commit()

    async def get_by_id(self, id: int) -> Expense | None:
        """
        Get an expense by its ID.
        """
        return await self.session.get(Expense, id)

    async def list_by_thread_id(self, thread_id: int) -> list[Expense]:
        """
        List all expenses by thread ID.
        """
        result = await self.session.execute(
            select(Expense).where(Expense.thread_id == thread_id).order_by(Expense.id.desc())
        )
        return result.scalars().all()

    async def list_by_thread_id_and_date_range(
        self, thread_id: int, from_date: datetime, to_date: datetime
    ) -> list[Expense]:
        """
        List all expenses by thread ID and date range.
        """
        result = await self.session.execute(
            select(Expense)
            .where(Expense.thread_id == thread_id)
            .where(Expense.created_at >= from_date)
            .where(Expense.created_at <= to_date)
            .order_by(Expense.id.desc())
        )
        return result.scalars().all()
