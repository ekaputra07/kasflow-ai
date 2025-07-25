import os
import duckdb
from kasflow.models import Expense


class DuckDBStore:
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
            self._conn = duckdb.connect(database=self.db_path)
            self._conn.execute(create_query)
        else:
            if os.path.exists(self.db_path):
                self._conn = duckdb.connect(database=self.db_path)
            else:
                self._conn = duckdb.connect(database=self.db_path)
                self._conn.execute(create_query)

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

    def list_expenses(self) -> list[Expense]:
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

    def create_expenses(self, expenses: list[Expense]):
        query = """
        INSERT INTO expenses
        (amount, category, description)
        VALUES (?, ?, ?)
        """
        e = [
            (expense.amount, expense.category, expense.description)
            for expense in expenses
        ]
        self._conn.executemany(query, e)

    def get_expense(self, expense_id: int) -> Expense:
        query = "SELECT * FROM expenses WHERE id = ?"
        e = self.execute(query, (expense_id,)).fetchone()
        return Expense(
            id=e[0],
            amount=e[1],
            category=e[2],
            description=e[3],
            created=e[4],
            updated=e[5],
        ) if e else None
