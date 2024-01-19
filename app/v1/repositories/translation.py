from abc import ABC, abstractmethod

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from app.v1.schemas import TranslationListResponse


class ITranslation(ABC):
    """
    Responsibility: Manage translations in DB
    """

    @abstractmethod
    async def get_word(self, word: str, sl: str) -> dict:
        pass

    @abstractmethod
    async def insert_word(self, word: dict) -> InsertOneResult:
        pass

    @abstractmethod
    async def delete_word(self, word: str) -> DeleteResult:
        pass

    @abstractmethod
    async def update_word(self, query: dict, data: dict) -> UpdateResult:
        pass

    @abstractmethod
    async def get_list_of_words(self, skip: int, limit: int, sort: str, word: str) -> TranslationListResponse:
        pass


class TranslationRepository(ITranslation):
    """
    Responsibility: Manage translations in MongoDB
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection: AsyncIOMotorCollection = db['translations']

    async def get_word(self, word: str, sl: str) -> dict:
        return await self.collection.find_one({"word": word, 'language': sl})

    async def insert_word(self, word: dict) -> InsertOneResult:
        return await self.collection.insert_one(word)

    async def delete_word(self, word: str) -> DeleteResult:
        return await self.collection.delete_one({"word": word})

    async def update_word(self, query: dict, data: dict) -> UpdateResult:
        return await self.collection.update_one(query, {"$set": data})

    async def get_list_of_words(self, skip: int = 0, limit: int = 10, sort: str = 'asc',
                                word: str = '') -> TranslationListResponse:
        """
        Return list of all words in DB with totalPages. See TranslationListResponse
        Play with "projection" to get desired fields.

        Filters:
        - Partial by word match
        - Sorting by word
        - Limit and skip
        """
        sort_order: int = -1 if sort == 'desc' else 1
        projection: dict = {
            '_id': 0,
            'word': 1,
            'language': 1
        }
        query: dict = {}

        if word:
            regex_pattern = f".*{word}.*"
            query = {
                'word': {'$regex': regex_pattern, '$options': 'i'}
            }

        pipeline: list[dict] = [
            {"$match": query},
            {"$facet": {
                "totalCount": [{"$count": "count"}],
                "results": [
                    {"$sort": {"word": sort_order}},
                    {"$skip": skip},
                    {"$limit": limit},
                    {"$project": projection}
                ]
            }}
        ]
        result = await self.collection.aggregate(pipeline).to_list(length=None)

        if result and result[0]:
            total_count: int = result[0]["totalCount"][0]["count"] if result[0]["totalCount"] else 0
            words: list = result[0]["results"]
        else:
            total_count: int = 0
            words: list = []

        return TranslationListResponse(
            meta={
                'totalPages': total_count,
                'limit': limit,
                'skip': skip,
            },
            data=words
        )
