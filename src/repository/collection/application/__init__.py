from abc import ABC, abstractmethod
from dataclasses import dataclass

from .interfaces import UnitOfWork


@dataclass
class Command:
    pass


class CommandHandler(ABC):
    _uow: UnitOfWork

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    @abstractmethod
    async def _handle(self, command: Command) -> None:
        pass

    async def handle(self, command: Command) -> None:
        try:
            await self._handle(command=command)
            await self._uow.commit()
        except Exception:
            await self._uow.rollback()
