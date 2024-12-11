from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.aggregator import Budget, BudgetId
from ...domain.interfaces import BudgetRepository


class SQLAlchemyBudgetRepository(BudgetRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, budget: Budget) -> None:
        self._session.add(budget)

    async def next_identity(self) -> BudgetId:
        return BudgetId()

    async def get_by_id(self, budget_id: BudgetId) -> Budget:
        print(budget_id)
        statement = select(Budget).filter_by(id=budget_id)
        result = await self._session.scalar(statement)

        if not result:
            raise Exception

        return result
