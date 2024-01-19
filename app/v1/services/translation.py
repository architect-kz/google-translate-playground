from pymongo.results import InsertOneResult, UpdateResult

from app.v1.core.exceptions import WordNotFoundException
from app.v1.models import Word as WordModel
from app.v1.models import Language as LanguageModel
from app.v1.schemas import DeleteWordResponse, TranslationListResponse
from app.v1.repositories.translation import ITranslation


class TranslationService:
    """
    A service layer for managing translations, facilitating interaction
    between the application and the repository layer. It abstracts away
    the details of data access from the application.

    Attributes:
        DOCUMENT_AFFECTED: A constant used to signify a single document affected in CRUD operations.
        DOCUMENT_DELETED_SUCCESS: Message returned when a word is successfully deleted.
        DOCUMENT_UPDATED_SUCCESS: Message returned when a word is successfully updated.
        DOCUMENT_NOT_FOUND: Message returned when a word is not found.
        STATUS_SUCCESS: A constant to represent a successful operation status.
    """
    DOCUMENT_AFFECTED = 1
    DOCUMENT_DELETED_SUCCESS = "Word successfully deleted"
    DOCUMENT_UPDATED_SUCCESS = "Word successfully updated"
    DOCUMENT_NOT_FOUND = "Word not found"
    STATUS_SUCCESS = "success"

    def __init__(self, repository: ITranslation):
        self.repository: ITranslation = repository

    async def get_list_of_words(self, skip: int = 0, limit: int = 10, sort: str = 'asc',
                                word='') -> TranslationListResponse:
        return await self.repository.get_list_of_words(skip, limit, sort, word)

    async def add_new_word(self, word: WordModel) -> InsertOneResult | None:
        try:
            return await self.repository.insert_word(word.model_dump())
        except Exception as e:
            # Log insertion error here
            return None

    async def delete_word(self, word: str) -> DeleteWordResponse:
        result = await self.repository.delete_word(word)

        if result.deleted_count == self.DOCUMENT_AFFECTED:
            return DeleteWordResponse(
                status=self.STATUS_SUCCESS,
                message=self.DOCUMENT_DELETED_SUCCESS,
                word=word
            )

        raise WordNotFoundException(f'{self.DOCUMENT_NOT_FOUND}: {word}')

    async def get_word_from_db(self, word: str, sl: str) -> WordModel | None:
        try:
            word = await self.repository.get_word(word, sl)
            del word['_id']

            return WordModel(**word)
        except Exception as e:
            # Log retrieval error here
            return None

    async def add_new_language_to_word(self, word: WordModel, language: str,
                                       data: LanguageModel) -> UpdateResult | None:
        try:
            word.languages.update({language: data})
            dumped_word = word.model_dump()
            query = {
                'word': word.word,
                'language': word.language
            }

            return await self.repository.update_word(query, {'languages': dumped_word['languages']})
        except Exception as e:
            # Log update error here
            return None

    def get_only_my_language(self, word: WordModel, language: str) -> WordModel:
        word.languages = {language: word.languages[language]}

        return word
