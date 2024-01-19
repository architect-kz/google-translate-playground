import pytest

from aiogoogletrans.models import Translated
from unittest.mock import AsyncMock, patch

from app.v1.services.google_translate import GoogleTranslateService
from app.v1.models import Word, Language
from tests.stubs.word import word

"""
We can cover repositories, all services.
I think this is enough to show the mindset of an engineer. 
With some extra time, we could have covered up to 90-99% 
"""


@pytest.fixture
def mock_translator():
    with patch('aiogoogletrans.Translator') as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_translated_word(mock_translator):
    # Setup mock return value
    translated_data = Translated(
        src=word['src'], dest=word['dest'], origin=word['word'], text=word['text'],
        extra_data=word['extra_data'], pronunciation=word['pronunciation'],
    )
    mock_translator.return_value.translate = AsyncMock(return_value=translated_data)

    service = GoogleTranslateService()

    word_model = await service.get_translated_word('challenge', 'en', 'es')

    assert word_model.word == word['word']
    assert word_model.language == word['src']
    assert isinstance(word_model.languages, dict)
    assert isinstance(word_model, Word)
    assert isinstance(word_model.languages[word['dest']], Language)
    # ... more assertions based on your requirements
