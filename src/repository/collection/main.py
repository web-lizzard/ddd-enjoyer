from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .domain.aggregator import Budget, BudgetId
from .domain.interfaces import BudgetRepository
from .infrastructure.persistence import SQLAlchemyBudgetRepository, map_tables, metadata


def repository_factory(session: AsyncSession) -> BudgetRepository:
    return SQLAlchemyBudgetRepository(session)


# Async SQLite engine (in-memory)
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create async engine and session
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create a session factory
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

_INITIAL_AMOUNT = 10000
_CHANGED_INITIAL_AMOUNT = 200000


async def create_budget(repository: BudgetRepository) -> BudgetId:
    id = await repository.next_identity()
    budget = Budget(_INITIAL_AMOUNT, id)

    await repository.add(budget)
    return id


async def find_budget(repository: BudgetRepository, id: BudgetId) -> Budget:
    return await repository.get_by_id(id)


def change_budget(budget: Budget) -> None:
    budget.change_total_amount(_CHANGED_INITIAL_AMOUNT)


async def init_db() -> None:
    # Create all tables in the in-memory database
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(metadata.create_all)
    print("Database tables created.")


async def main() -> None:
    await init_db()
    async with AsyncSessionLocal() as session:
        map_tables()
        repository = repository_factory(session)
        id = await create_budget(repository)

        await session.commit()  ## Transaction

        budget = await find_budget(repository, id)

        change_budget(budget)

        await session.commit()

        changed_budget = await find_budget(repository, budget.id)

        print(changed_budget.total_amount)

        assert changed_budget.total_amount == _CHANGED_INITIAL_AMOUNT

        await repository.delete_budget(id)

        removed_budget = await repository.get_by_id(id)

        await session.commit()

        print(removed_budget.active)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
