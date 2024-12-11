from sqlalchemy import Boolean, Column, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import Composite, composite, registry, relationship

from ...domain.aggregator import Budget, BudgetId, Expense, ExpenseId

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


budgets_table = Table(
    "budgets",
    metadata,
    Column("budget_id", String, primary_key=True),
    Column("total_amount", Integer),
    Column("active", Boolean),
)


expenses_table = Table(
    "expenses",
    metadata,
    Column("expense_id", String, primary_key=True),
    Column("value", Integer),
    Column("b_id", String, ForeignKey("budgets.budget_id")),
)


def budget_id_mapper(column: Column) -> Composite:
    return composite(BudgetId, column)


def expense_id_mapper(column: Column) -> Composite:
    return composite(ExpenseId, column)


def map_tables() -> None:
    mapper_registry.map_imperatively(
        Expense,
        expenses_table,
        properties={
            "id": expense_id_mapper(expenses_table.c.expense_id),
            "budget_id": budget_id_mapper(expenses_table.c.b_id),
            "budget": relationship("Budget", back_populates="expenses"),
        },
    )

    mapper_registry.map_imperatively(
        Budget,
        budgets_table,
        properties={
            "id": budget_id_mapper(budgets_table.c.budget_id),
            "expenses": relationship(
                Expense, back_populates="budget", cascade="all, delete-orphan"
            ),
        },
    )
