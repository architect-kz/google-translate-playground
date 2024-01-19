from pymongo.results import DeleteResult

from app.v1.models import Word as WordModel
from app.v1.models import Language as LanguageModel
from app.v1.repositories.translation import ITranslation


class TranslationService:
    """
    A layer above the repository to manage translations in any preferred storage.
    Just change the repository to implement your own.
    """

    def __init__(self, repository: ITranslation):
        self.repository = repository

    async def get_list_of_words(self, skip: int = 0, limit: int = 10, sort: str = 'asc', word='') -> list:
        return await self.repository.get_list_of_words(skip, limit, sort, word)

    async def add_new_word(self, word: WordModel) -> int:
        return await self.repository.insert_word(word.model_dump())

    async def delete_word(self, word: str) -> DeleteResult:
        return await self.repository.delete_word(word)

    async def get_word_from_db(self, word: str, sl: str) -> WordModel | None:
        try:
            word = await self.repository.get_word(word, sl)
            del word['_id']

            return WordModel(**word)
        except Exception as e:
            return None

    async def add_new_language_to_word(self, word: WordModel, language: str, data: LanguageModel) -> bool:
        word.languages.update({language: data})
        query = {
            'word': word.word,
            'language': word.language
        }
        dumped_word = word.model_dump()

        return await self.repository.update_word(query, {'languages': dumped_word['languages']})

    def get_only_my_language(self, word: WordModel, language: str) -> WordModel:
        word.languages = {language: word.languages[language]}

        return word
