from datetime import datetime, UTC
from sqlalchemy import String, Integer, Float, DateTime, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    thread_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    __table_args__ = (
        Index(
            "idx_expenses_thread_id_user_id_created_at",
            "thread_id",
            "user_id",
            "created_at",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"Expense(id={self.id}, thread_id={self.thread_id}, "
            f"user_id={self.user_id}, amount={self.amount}, "
            f"category={self.category}, description={self.description}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})",
        )
