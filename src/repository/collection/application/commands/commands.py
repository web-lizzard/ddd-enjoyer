from dataclasses import dataclass


@dataclass
class Command:
    pass


@dataclass
class CreateBudget(Command):
    amount: int
