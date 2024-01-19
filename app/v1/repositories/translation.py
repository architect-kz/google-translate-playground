from abc import ABC, abstractmethod

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pymongo.results import DeleteResult


class ITranslation(ABC):
    """
    Responsibility: Manage translations in DB
    """

    @abstractmethod
    async def get_word(self, word: str, sl: str) -> dict:
        pass

    @abstractmethod
    async def insert_word(self, word: dict) -> bool:
        pass

    @abstractmethod
    async def delete_word(self, word: str) -> DeleteResult:
        pass

    @abstractmethod
    async def get_list_of_words(self, skip: int, limit: int, sort: str, word: str) -> list:
        pass

    @abstractmethod
    async def update_word(self, query: dict, data: dict) -> bool:
        pass


class TranslationRepository(ITranslation):
    """
    Responsibility: Manage translations in MongoDB
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection: AsyncIOMotorCollection = db['translations']

    async def get_word(self, word: str, sl: str) -> dict:
        return await self.collection.find_one({"word": word, 'language': sl})

    async def insert_word(self, word: dict) -> bool:
        try:
            result = await self.collection.insert_one(word)
            return result.acknowledged
        except Exception as e:
            # Log something here
            return False

    async def update_word(self, query: dict, data: dict) -> bool:
        try:
            result = await self.collection.update_one(query, {"$set": data})
            return result.acknowledged
        except Exception as e:
            # Log something here
            return False

    async def delete_word(self, word: str) -> DeleteResult:
        return await self.collection.delete_one({"word": word})

    async def get_list_of_words(self, skip: int = 0, limit: int = 10, sort: str = 'asc', word: str = '') -> list:
        """
        Return list of all words in DB.
        Play with "projection" to get desired fields.

        Filters:
        - Partial by word match
        - Sorting by word
        - Limit and skip
        """
        sort_order = -1 if sort == 'desc' else 1
        projection = {
            '_id': 0,
            'word': 1,
            'language': 1
        }

        if filter:
            regex_pattern = f".*{word}.*"
            query = {
                'word': {'$regex': regex_pattern, '$options': 'i'}
            }
            cursor = self.collection.find(query, projection=projection).skip(skip).limit(limit).sort('word', sort_order)
        else:
            cursor = self.collection.find(projection=projection).skip(skip).limit(limit).sort('word', sort_order)

        words = await cursor.to_list(length=None)

        return words
