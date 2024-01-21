from typing import Optional

from pydantic import BaseModel


class Translation(BaseModel):
    text: str
    translations: list[str]
    confidence: float | None


class Definition(BaseModel):
    definition: Optional[str]
    example: Optional[str] = None
    synonyms: Optional[list[str]] = None
    context: Optional[list[str]] = None


class Language(BaseModel):
    text: str
    confidence: float | None
    pronunciation: Optional[str] = None
    definitions: Optional[dict[str, list[Definition]]] = None
    examples: Optional[list[str]] = None
    translations: dict[str, list[Translation]] | None


class Word(BaseModel):
    word: str | None
    language: str | None
    pronunciation: str | None
    languages: dict[str, Language]
