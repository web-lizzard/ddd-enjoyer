from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class ProductId:
    value: str = field(default_factory=lambda: str(uuid4()))


class Product:
    name: str
    id: ProductId

    def __init__(self, id: ProductId, name: str) -> None:
        self.id = id
        self.name = name

    def change_name(self, name: str) -> None:
        self.name = name
