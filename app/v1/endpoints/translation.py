from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from app.v1.core.exceptions import WordNotFoundException
from app.v1.schemas import WordRequest, TranslationListRequest
from app.v1.dependencies import get_translation_service
from app.v1.models import Word as WordModel
from app.v1.schemas import TranslationListResponse, DeleteWordResponse
from app.v1.services.translation import TranslationService
from app.v1.services.google_translate import GoogleTranslateService

router = APIRouter(prefix="/translations", tags=["translations"])


@router.get("/{word}", response_model=WordModel)
async def get_word(request: WordRequest = Depends(),
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

    :param request: WordRequest
        word: Word to translate
        sl: Source Language (Google named it)
        tl: Target Language (Google named it)
    :param translation_service: Injecting Translation Service
    :param google_translate_service: Injecting Google Translate Service

    :return: Returns the Word and it's translation in target language
    """
    word, sl, tl = request.word, request.sl, request.tl

    try:
        translated_word = await translation_service.get_word_from_db(word, sl)

        if translated_word:
            is_language_available = tl in translated_word.languages

            if is_language_available:
                return translation_service.get_only_my_language(translated_word, tl)

            google_word = await google_translate_service.get_translated_word(word, sl, tl)

            # Even if raises an exception, we still can return the translation straight from Google Translate
            await translation_service.add_new_language_to_word(translated_word, tl, google_word.languages[tl])

            return google_word

        google_word = await google_translate_service.get_translated_word(word, sl, tl)

        # We could have used Events (Event Driven Design)
        await translation_service.add_new_word(google_word)

        return google_word
    except ValidationError as e:
        # Log the details <here>
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail={'message': str(e)})
    except Exception as e:
        # Log the details <here>
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail={'message': 'An error occurred while processing the request'})


@router.get("/", response_model=TranslationListResponse)
async def get_list_of_words(request: TranslationListRequest = Depends(),
                            translation: TranslationService = Depends(get_translation_service)):
    """
    Get list of all words in DB. See TranslationsList

    Filters:
    - Partial by word match
    - Sorting by word
    - Limit and skip
    """
    return await translation.get_list_of_words(request.skip, request.limit, request.sort, request.word)


@router.delete("/{word}", response_model=DeleteWordResponse)
async def delete_word(word: str, translation: TranslationService = Depends(get_translation_service)):
    try:
        return await translation.delete_word(word)
    except WordNotFoundException as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail={'message': str(e)}
        )
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail={'message': f'An error occurred while deleting the word {word}'}
        )
