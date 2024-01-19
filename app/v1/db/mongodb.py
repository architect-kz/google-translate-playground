from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class MongoDB:
    def __init__(self, uri: str):
        self.client = AsyncIOMotorClient(uri)

    def get_database(self, db: str) -> AsyncIOMotorDatabase:
        return self.client.get_database(db)
