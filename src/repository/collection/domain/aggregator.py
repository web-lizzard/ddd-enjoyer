from dataclasses import dataclass, field
from uuid import uuid4


## Value Object
@dataclass
class BudgetId:
    value: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class ExpenseId:
    value: str = field(default_factory=lambda: str(uuid4()))


## Aggregates


class Expense:
    id: ExpenseId
    budget_id: BudgetId
    value: int

    def __init__(self, id: ExpenseId, value: int, budget_id: BudgetId) -> None:
        self.id = id
        self.value = value
        self.budget_id = budget_id


class Budget:
    id: BudgetId
    total_amount: int
    active: bool

    def __init__(self, total_amount: int, id: BudgetId) -> None:
        self.id = id
        self.total_amount = total_amount
        self.active = True

    def change_total_amount(self, value: int) -> None:
        self.total_amount = value

    def deactivate(self) -> None:
        self.active = False

    def add_expense(self, expense_id: ExpenseId, value: int) -> Expense:
        return Expense(id=expense_id, value=value, budget_id=self.id)
