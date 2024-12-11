from motor.motor_asyncio import AsyncIOMotorClient
from settings import settings


async def main() -> None:
    client = AsyncIOMotorClient(settings.mongo.connection_url)

    db = client.get_database(settings.mongo.db_name)

    await db.list_collection_names()
    print(db)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
