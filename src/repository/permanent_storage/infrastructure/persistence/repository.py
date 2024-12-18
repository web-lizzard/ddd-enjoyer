from bson import ObjectId
from motor.core import AgnosticCollection
from motor.motor_asyncio import AsyncIOMotorClientSession

from ...domain import Product, ProductId, ProductRepository


class MongoProductRepository(ProductRepository):
    _collection: AgnosticCollection  # type: ignore[no-any-unimported]
    _session: AsyncIOMotorClientSession  # type: ignore[no-any-unimported]

    def __init__(  # type: ignore[no-any-unimported]
        self,
        collection: AgnosticCollection,
        session: AsyncIOMotorClientSession,
    ) -> None:
        self._collection = collection
        self._session = session

    async def next_identity(self) -> ProductId:
        return ProductId(value=str(ObjectId()))

    async def save(self, product: Product) -> None:
        await self._collection.update_one(
            {"_id": ObjectId(product.id.value)},
            {"$set": {"name": product.name}},
            upsert=True,
            session=self._session,
        )

    async def get_by_id(self, id: ProductId) -> Product:
        document = await self._collection.find_one({"_id": ObjectId(id.value)})

        if not document:
            raise Exception

        return self._to_product(document)

    def _to_product(self, document: dict) -> Product:
        return Product(id=ProductId(str(document["_id"])), name=document["name"])
