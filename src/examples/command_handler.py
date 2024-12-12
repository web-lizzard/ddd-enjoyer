from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class Command:
    pass


class UnitOfWork(Protocol):
    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...


class InMemoryUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self._committed = False

    async def commit(self) -> None:
        self._committed = True
        print(self._committed)
        print("Changes has been committed")

    async def rollback(self) -> None:
        print("error rollicking changes")
        print(self._committed)


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self.rollback()


class CommandHandler(ABC):
    _uow: UnitOfWork

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    @abstractmethod
    async def _handle(self, *, command: Command) -> None:
        pass

    async def handle(self, command: Command) -> None:
        try:
            await self._handle(command=command)
            await self._uow.commit()
        except Exception:
            await self._uow.rollback()
