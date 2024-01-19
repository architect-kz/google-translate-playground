from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.v1.dependencies import get_translation_service
from app.v1.models import Word as WordModel
from app.v1.services.translation import TranslationService
from app.v1.services.google_translate import GoogleTranslateService

router = APIRouter(prefix="/translations", tags=["translations"])
LIMIT = 10


@router.get("/")
async def get_list_of_words(skip: int = 0, limit: int = LIMIT, sort: str = 'asc', word: str = '',
                            translation: TranslationService = Depends(get_translation_service)):
    return await translation.get_list_of_words(skip, limit, sort, word)


@router.delete("/{word}")
async def delete_word(word: str, translation: TranslationService = Depends(get_translation_service)):
    try:
        result = await translation.delete_word(word)

        return {"message": f'The word {word} was deleted successfully.'}
    except Exception as e:
        # # I'd log something here. Didn't have much time
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=f'An error occurred while deleting the word {word}')


@router.get("/{word}", response_model=WordModel)
async def get_word(word: str, sl: str = '', tl: str = '',
                   translation_service: TranslationService = Depends(get_translation_service),
                   google_translate_service: GoogleTranslateService = Depends(GoogleTranslateService)):
    """
    Scenarios:

    1. Word with source language (sl) is in DB, and we have target language (tl) translation. Return it.
    2. Word with sl is in DB, but not tl translation. Google it and append to Word.
    3. Word is DB, but has another sl - letters are the same, but different translation result.
    Google it and add to DB.
    4. Word is not in DB, Google it and add to DB.
    5. sl == tl - Bad request

    Improvements:
    - We could have used Events (Event Driven Design) in case of saving/updating the Word in DB.

    :param word: Word to translate
    :param sl: Source Language (Google named it)
    :param tl: Target Language (Google named it)
    :param translation_service: Injecting Translation Service
    :param google_translate_service: Injecting Google Translate Service

    :return: Returns the Word and it's translation in target language
    """
    if sl == tl:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Source and target languages can not be equal")

    try:
        translated_word = await translation_service.get_word_from_db(word, sl)

        if translated_word:
            is_language_available = tl in translated_word.languages
            print(translated_word.languages)

            if is_language_available:
                return translation_service.get_only_my_language(translated_word, tl)

            google_word = await google_translate_service.get_translated_word(word, sl, tl)

            # Even if raises an exception, we still can return the translation straight from Google Translate
            new_language_result = await translation_service.add_new_language_to_word(translated_word, tl,
                                                                                     google_word.languages[tl])

            return google_word

        google_word = await google_translate_service.get_translated_word(word, sl, tl)

        # We could have used Events (Event Driven Design)
        await translation_service.add_new_word(google_word)

        return google_word
    except Exception as e:
        # I'd log something here. Didn't have much time
        pass
