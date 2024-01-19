from pydantic import BaseModel


class Word(BaseModel):
    word: str
    language: str


class TranslationListResponse(BaseModel):
    meta: dict
    data: list[Word]