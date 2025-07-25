from abc import ABC, abstractmethod
from kasflow.models import Expense


class AsyncBaseStore(ABC):
    @abstractmethod
    async def list_expense(self) -> list[Expense]:
        pass

    @abstractmethod
    async def create_expense(self, expense: Expense | list[Expense]):
        pass

    @abstractmethod
    async def get_expense(self, expense_id: int) -> Expense | None:
        pass
