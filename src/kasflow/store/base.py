from abc import ABC, abstractmethod
from datetime import datetime
from kasflow.models import Expense


class AsyncBaseStore(ABC):
    @abstractmethod
    async def list_expenses(self) -> list[Expense]:
        pass

    @abstractmethod
    async def list_expenses_by_date_range(
        self, from_datetime: datetime, to_datetime: datetime
    ) -> list[Expense]:
        pass

    @abstractmethod
    async def list_user_expenses(self, user_id: int) -> list[Expense]:
        pass

    @abstractmethod
    async def list_user_expenses_by_date_range(
        self, user_id: int, from_datetime: datetime, to_datetime: datetime
    ) -> list[Expense]:
        pass

    @abstractmethod
    async def create_expense(self, expense: Expense | list[Expense]):
        pass

    @abstractmethod
    async def get_expense(self, expense_id: int) -> Expense | None:
        pass

    @abstractmethod
    async def get_user_expense(
        self, user_id: int, expense_id: int
    ) -> Expense | None:
        pass
