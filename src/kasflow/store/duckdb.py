import os
import logging
import duckdb
from kasflow.models import Expense
from kasflow.store.base import BaseStore

logger = logging.getLogger(__name__)


class DuckDBStore(BaseStore):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self):
        create_query = """
        CREATE SEQUENCE id_seq START 1;
        CREATE TABLE IF NOT EXISTS expenses
        (id INTEGER PRIMARY KEY DEFAULT nextval('id_seq'),
        amount FLOAT,
        category VARCHAR,
        description VARCHAR,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        """
        if self.db_path == ":memory:":
            self._conn = duckdb.connect(database=self.db_path).cursor()
            self._conn.execute(create_query)
            logger.info("Created in-memory database")
        else:
            if os.path.exists(self.db_path):
                self._conn = duckdb.connect(database=self.db_path).cursor()
                logger.info("Connected to existing database at %s", self.db_path)
            else:
                self._conn = duckdb.connect(database=self.db_path).cursor()
                self._conn.execute(create_query)
                logger.info("Created new database at %s", self.db_path)

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._conn.close()

    def execute(self, query: str, params=None):
        if params is None:
            return self._conn.execute(query)
        else:
            return self._conn.execute(query, params)

    def list_expense(self) -> list[Expense]:
        query = "SELECT * FROM expenses ORDER BY created DESC"
        all = self._conn.execute(query).fetchall()
        return [
            Expense(
                id=row[0],
                amount=row[1],
                category=row[2],
                description=row[3],
                created=row[4],
                updated=row[5],
            )
            for row in all
        ]

    def create_expense(self, expense: Expense | list[Expense]):
        query = """
        INSERT INTO expenses
        (amount, category, description)
        VALUES ($amount, $category, $description)
        """
        if isinstance(expense, list):
            expenses = [e.model_dump(include={"amount", "category", "description"}) for e in expense]
        else:
            expenses = [expense.model_dump(include={"amount", "category", "description"})]
        self._conn.executemany(query, expenses)

    def get_expense(self, expense_id: int) -> Expense:
        query = "SELECT * FROM expenses WHERE id = ?"
        e = self.execute(query, (expense_id,)).fetchone()
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
