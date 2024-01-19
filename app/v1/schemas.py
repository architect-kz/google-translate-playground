from typing import Optional

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, model_validator

from app.v1.core.config import settings


class Word(BaseModel):
    word: str
    language: str


class TranslationListResponse(BaseModel):
    meta: dict
    data: list[Word]


class DeleteWordResponse(BaseModel):
    status: str
    message: str
    word: str


class WordRequest(BaseModel):
    word: str = Field(min_length=2)
    sl: str = Field(min_length=2, pattern='^[a-zA-Z]+$', default='auto')
    tl: str = Field(min_length=2, max_length=2, pattern='^[a-zA-Z]+$', default='en')

    @model_validator(mode='before')
    def check_languages_not_same(cls, data):
        data['sl'] = data['sl'].lower()
        data['tl'] = data['tl'].lower()

        if data['sl'] == data['tl']:
            raise RequestValidationError('Source and target languages cannot be the same', body={
                'sl': data['sl'],
                'tl': data['tl']
            })

        return data


class TranslationListRequest(BaseModel):
    word: Optional[str] = ''
    skip: Optional[int] = Field(ge=0, default=settings.SKIP)
    limit: Optional[int] = Field(ge=1, default=settings.LIMIT)
    sort: Optional[str] = settings.SORTING

    @model_validator(mode='before')
    def check_languages_not_same(cls, data):
        """
        Use "word" filter only it's not empty and length => 2.
        """
        if len(data['word']) < 2:
            data['word'] = ''

        return data
