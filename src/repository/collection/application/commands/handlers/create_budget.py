from ....domain.aggregator import Budget
from ....domain.interfaces import BudgetRepository
from ...interfaces import UnitOfWork
from ..commands import CreateBudget
from .base import CommandHandler


class CreateBudgetHandler(CommandHandler[CreateBudget]):
    _repository: BudgetRepository

    def __init__(self, uow: UnitOfWork, repository: BudgetRepository) -> None:
        super().__init__(uow)
        self._repository = repository

    async def _handle(self, command: CreateBudget) -> None:
        id = await self._repository.next_identity()
        budget = Budget(total_amount=command.amount, id=id)

        await self._repository.add(budget)
