from abc import ABC, abstractmethod

from kasflow.models import Expense


class BaseStore(ABC):
    @abstractmethod
    def list_expense(self) -> list[Expense]:
        pass

    @abstractmethod
    def create_expense(self, expense: Expense | list[Expense]):
        pass

    @abstractmethod
    def get_expense(self, expense_id: int) -> Expense | None:
        pass
