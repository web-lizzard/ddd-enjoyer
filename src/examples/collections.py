from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

TCollection = TypeVar("TCollection")


class Collection(ABC, Generic[TCollection]):
    @abstractmethod
    def add(self, item: TCollection) -> None:
        pass

    @abstractmethod
    def remove(self, item: TCollection) -> None:
        pass

    @abstractmethod
    def add_all(self, items: Iterable[TCollection]) -> None:
        pass

    @abstractmethod
    def remove_all(self, items: Iterable[TCollection]) -> None:
        pass


class SomeAggregator:
    pass


class SetCollection(Collection[SomeAggregator]):
    def __init__(self) -> None:
        self.items: set[SomeAggregator] = set()

    def add(self, item: SomeAggregator) -> None:
        self.items.add(item)

    def remove(self, item: SomeAggregator) -> None:
        self.items.remove(item)

    def add_all(self, items: Iterable[SomeAggregator]) -> None:
        self.items.update(items)

    def remove_all(self, items: Iterable[SomeAggregator]) -> None:
        for item in items:
            self.items.discard(
                item
            )  # Używamy discard, aby uniknąć błędu, gdy element nie istnieje


if __name__ == "__main__":
    aggregator = SomeAggregator()
    second_aggregator = SomeAggregator()
    collection = SetCollection()

    collection.add(aggregator)

    print(len(collection.items))  ## 1 - nowo zapisana kolekcja

    collection.add(aggregator)

    print(
        len(collection.items)
    )  ## 1 - set pilnuje aby nie dało się zduplikować obiektu

    collection.add(second_aggregator)

    print(len(collection.items))  ## 2 - dodanowy nowy agregat

    collection.remove_all((aggregator, second_aggregator))

    print(len(collection.items))  ## 0 0 usunięto wszystkie agregaty
