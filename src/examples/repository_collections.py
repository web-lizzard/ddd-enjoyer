from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class AggregatorId:
    value: str = field(default_factory=lambda: str(uuid4()))


class Aggregator:
    id: AggregatorId
    name: str

    def __init__(self, name: str, id: AggregatorId | None = None) -> None:
        self.id = id or AggregatorId()
        self.name = name

    def change_name(self, name: str) -> None:
        self.name = name


class AggregatorRepository:
    _aggregates: dict[AggregatorId, Aggregator]

    def __init__(self) -> None:
        self._aggregates = {}

    def find_aggregator(self, id: AggregatorId) -> Aggregator:
        aggregator = self._aggregates.get(id, None)

        if aggregator is None:
            raise Exception

        return aggregator

    def add(self, aggregator: Aggregator) -> None:
        self._aggregates[aggregator.id] = aggregator


if __name__ == "__main__":
    id = AggregatorId()
    aggregator = Aggregator(name="Example Aggregator", id=id)
    repository = AggregatorRepository()
    repository.add(aggregator)

    aggregator_to_rename = repository.find_aggregator(id)

    aggregator_to_rename.change_name("new name")

    changed_aggregator = repository.find_aggregator(id)

    print(
        changed_aggregator.name
    )  ## Wyświetli "new name", ze względu na referencyjność tego podejścia do repozytorium, nie trzeba zapisywać ponownie aggregatu po zmianie jego wartości
