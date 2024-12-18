from typing import Protocol

from .aggregates import Product, ProductId


class ProductRepository(Protocol):
    async def next_identity(self) -> ProductId:
        ...

    async def save(self, product: Product) -> None:
        ...

    async def get_by_id(self, id: ProductId) -> Product:
        ...
