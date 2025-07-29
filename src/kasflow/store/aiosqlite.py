import os
import logging
import aiosqlite
from datetime import datetime

from kasflow.store.base import AsyncBaseStore
from kasflow.models import Expense

logger = logging.getLogger(__name__)


class AioSQLiteStore(AsyncBaseStore):
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def _connect(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS expenses
        (id INTEGER PRIMARY KEY,
        user_id INTEGER,
        amount FLOAT,
        category VARCHAR,
        description VARCHAR,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        """
        add_index_user_id_query = """
        CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses(user_id);
        """
        add_index_created_query = """
        CREATE INDEX IF NOT EXISTS idx_expenses_created ON expenses(created);
        """
        if self.db_path == ":memory:":
            self._conn = await aiosqlite.connect(database=self.db_path)
            await self._conn.execute(create_table_query)
            await self._conn.execute(add_index_user_id_query)
            await self._conn.execute(add_index_created_query)
            logger.info("Created in-memory database")
        else:
            if os.path.exists(self.db_path):
                self._conn = await aiosqlite.connect(database=self.db_path)
                logger.info(
                    "Connected to existing database at %s", self.db_path
                )
            else:
                self._conn = await aiosqlite.connect(database=self.db_path)
                await self._conn.execute(create_table_query)
                await self._conn.execute(add_index_user_id_query)
                await self._conn.execute(add_index_created_query)
                logger.info("Created new database at %s", self.db_path)

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._conn.close()

    def _row_to_expense(self, row):
        return Expense(
            id=row[0],
            user_id=row[1],
            amount=row[2],
            category=row[3],
            description=row[4],
            created=row[5],
            updated=row[6],
        )

    async def list_expenses(self) -> list[Expense]:
        query = "SELECT * FROM expenses ORDER BY id DESC"
        rows = await self._conn.execute_fetchall(query)
        return [self._row_to_expense(row) for row in rows]

    async def list_expenses_by_date_range(
        self, from_datetime: datetime, to_datetime: datetime
    ) -> list[Expense]:
        query = "SELECT * FROM expenses WHERE created BETWEEN ? AND ? ORDER BY id DESC"
        rows = await self._conn.execute_fetchall(
            query, (from_datetime, to_datetime)
        )
        return [self._row_to_expense(row) for row in rows]

    async def list_user_expenses(self, user_id: int) -> list[Expense]:
        query = "SELECT * FROM expenses WHERE user_id = ? ORDER BY id DESC"
        rows = await self._conn.execute_fetchall(query, (user_id,))
        return [self._row_to_expense(row) for row in rows]

    async def list_user_expenses_by_date_range(
        self, user_id: int, from_datetime: datetime, to_datetime: datetime
    ) -> list[Expense]:
        query = "SELECT * FROM expenses WHERE user_id = ? AND created BETWEEN ? AND ? ORDER BY id DESC"
        rows = await self._conn.execute_fetchall(
            query, (user_id, from_datetime, to_datetime)
        )
        return [self._row_to_expense(row) for row in rows]

    async def create_expense(self, expense: Expense | list[Expense]):
        query = """
        INSERT INTO expenses
        (user_id, amount, category, description)
        VALUES ($user_id, $amount, $category, $description)
        """
        fields = ["user_id", "amount", "category", "description"]

        if isinstance(expense, list):
            expenses = [e.model_dump(include=fields) for e in expense]
        else:
            expenses = [expense.model_dump(include=fields)]
        await self._conn.executemany(query, expenses)
        await self._conn.commit()

    async def get_expense(self, expense_id: int) -> Expense:
        query = "SELECT * FROM expenses WHERE id = ?"
        async with self._conn.execute(query, (expense_id,)) as cursor:
            e = await cursor.fetchone()
            return self._row_to_expense(e) if e else None

    async def get_user_expense(self, user_id: int, expense_id: int) -> Expense:
        query = "SELECT * FROM expenses WHERE user_id = ? AND id = ?"
        async with self._conn.execute(
            query,
            (user_id, expense_id),
        ) as cursor:
            e = await cursor.fetchone()
            return self._row_to_expense(e) if e else None
