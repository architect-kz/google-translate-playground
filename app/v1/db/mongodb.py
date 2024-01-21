from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class MongoDB:
    def __init__(self, client: AsyncIOMotorClient, uri: str):
        self.client: AsyncIOMotorClient = client(uri)

    def get_database(self, db: str) -> AsyncIOMotorDatabase:
        return self.client.get_database(db)
