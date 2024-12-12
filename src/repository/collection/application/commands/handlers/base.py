from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ...interfaces import UnitOfWork
from ..commands import Command

TCommand = TypeVar("TCommand", bound=Command)


class CommandHandler(ABC, Generic[TCommand]):
    _uow: UnitOfWork

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    @abstractmethod
    async def _handle(self, command: TCommand) -> None:
        pass

    async def handle(self, command: TCommand) -> None:
        try:
            await self._handle(command=command)
            await self._uow.commit()

        except Exception as e:
            await self._uow.rollback()
            raise e
