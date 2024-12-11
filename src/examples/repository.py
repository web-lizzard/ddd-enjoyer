from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class AggregatorId:
    value: str = field(default_factory=lambda: str(uuid4()))


class Aggregator:
    id: AggregatorId
    name: str

    def __init__(self, name: str, id: None | AggregatorId = None) -> None:
        self.id = id or AggregatorId()
        self.name = name

    def change_name(self, name: str) -> None:
        self.name = name


class AggregatorRepository:
    pass


if __name__ == "__main__":
    aggregator = Aggregator(name="Aggregator Name")
