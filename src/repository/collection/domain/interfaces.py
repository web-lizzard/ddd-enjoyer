from typing import Protocol

from .aggregator import Budget, BudgetId


class BudgetRepository(Protocol):
    async def next_identity(self) -> BudgetId:
        ...

    async def add(self, budget: Budget) -> None:
        ...

    async def get_by_id(self, budget_id: BudgetId) -> Budget:
        ...

    async def delete_budget(self, budget_id: BudgetId) -> None:
        ...
