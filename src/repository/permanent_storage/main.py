from motor.motor_asyncio import AsyncIOMotorClient

from src.settings import settings

from .domain import Product
from .infrastructure.persistence import MongoProductRepository


async def main() -> None:
    client = AsyncIOMotorClient(settings.mongo.connection_url)

    db = client.get_database(settings.mongo.db_name)

    collection = db.get_collection("products")

    if collection is None:
        await db.create_collection("products")

    async with await client.start_session() as session:
        async with session.start_transaction():
            repository = MongoProductRepository(collection, session)

            id = await repository.next_identity()

            product = Product(id=id, name="Some product")

            await repository.save(product)

    found_product = await repository.get_by_id(id)

    found_product.change_name("new name")

    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                repository = MongoProductRepository(collection, session)

                await repository.save(found_product)
                raise Exception

            except Exception:
                await session.abort_transaction()

    updated_product = await repository.get_by_id(found_product.id)
    print(updated_product.name)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
