import os
import logging
import aiosqlite

from kasflow.store.base import AsyncBaseStore
from kasflow.models import Expense

logger = logging.getLogger(__name__)


class AioSQLiteStore(AsyncBaseStore):
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def _connect(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS expenses
        (id INTEGER PRIMARY KEY,
        amount FLOAT,
        category VARCHAR,
        description VARCHAR,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        """
        if self.db_path == ":memory:":
            self._conn = await aiosqlite.connect(database=self.db_path)
            await self._conn.execute(create_query)
            logger.info("Created in-memory database")
        else:
            if os.path.exists(self.db_path):
                self._conn = await aiosqlite.connect(database=self.db_path)
                logger.info(
                    "Connected to existing database at %s", self.db_path
                )
            else:
                self._conn = await aiosqlite.connect(database=self.db_path)
                await self._conn.execute(create_query)
                logger.info("Created new database at %s", self.db_path)

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._conn.close()

    async def list_expense(self) -> list[Expense]:
        query = "SELECT * FROM expenses ORDER BY id DESC"
        rows = await self._conn.execute_fetchall(query)
        return [
            Expense(
                id=row[0],
                amount=row[1],
                category=row[2],
                description=row[3],
                created=row[4],
                updated=row[5],
            )
            for row in rows
        ]

    async def create_expense(self, expense: Expense | list[Expense]):
        query = """
        INSERT INTO expenses
        (amount, category, description)
        VALUES ($amount, $category, $description)
        """
        if isinstance(expense, list):
            expenses = [
                e.model_dump(include={"amount", "category", "description"})
                for e in expense
            ]
        else:
            expenses = [
                expense.model_dump(
                    include={"amount", "category", "description"}
                )
            ]
        await self._conn.executemany(query, expenses)
        await self._conn.commit()

    async def get_expense(self, expense_id: int) -> Expense:
        query = "SELECT * FROM expenses WHERE id = ?"
        async with self._conn.execute(query, (expense_id,)) as cursor:
            e = await cursor.fetchone()
            return (
                Expense(
                    id=e[0],
                    amount=e[1],
                    category=e[2],
                    description=e[3],
                    created=e[4],
                    updated=e[5],
                )
                if e
                else None
            )
