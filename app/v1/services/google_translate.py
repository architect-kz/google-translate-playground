from aiogoogletrans import Translator
from aiogoogletrans.models import Translated

from app.v1.core.exceptions import GoogleTranslateRequestException
from app.v1.models import Definition as DefinitionModel
from app.v1.models import Language as LanguageModel
from app.v1.models import Word as WordModel
from app.v1.models import Translation as TranslationModel


class GoogleTranslateService:
    """
    Responsibility: Get translated word from Google Translate API and format it
    """

    def __init__(self):
        self.translator: Translator = Translator()

    async def get_translated_word(self, word: str, sl: str, tl: str) -> WordModel | None:
        try:
            data = await self.translator.translate(word, src=sl, dest=tl)

            return self.get_model(data)
        except Exception as e:
            raise GoogleTranslateRequestException(
                f'Something went wrong in Google Translate request: {e}. Word "{word}" from {sl} to {tl}')

    def get_model(self, data: Translated) -> WordModel:
        return WordModel(
            word=data.origin,
            language=data.src,
            pronunciation=data.extra_data['translation'][-1][-1],
            languages={data.dest: self._get_language(data)},
        )

    def _get_language(self, data) -> LanguageModel | None:
        return LanguageModel(
            text=data.text,
            confidence=data.extra_data.get('confidence', None),
            pronunciation=data.extra_data['translation'][-1][-2],
            definitions=self._get_definitions(data.extra_data),
            examples=self._get_examples(data.extra_data['examples']),
            translations=self._get_translations(data.extra_data),
        )

    def _get_definitions(self, extra_data: dict) -> dict[str, list[DefinitionModel]] | None:
        """
        Get definitions with synonyms
        """
        if not extra_data['definitions']:
            return

        result = {}
        grouped_synonyms = self._get_synonyms_grouped_by_keys(extra_data)

        for part_of_speech, definitions_list, _, _ in extra_data['definitions']:
            result[part_of_speech] = []

            for definition, key, *context in definitions_list:
                item = DefinitionModel(
                    definition=definition,
                )

                if grouped_synonyms:
                    item.synonyms = grouped_synonyms.get(key, [])

                if context:
                    item.example = context[0]

                    if len(context) > 1:
                        item.context = context[1][0]

                result[part_of_speech].append(item)

        return result

    def _get_synonyms_grouped_by_keys(self, extra_data: dict) -> dict[str, list[str]] | None:
        """
        Group synonyms by keys provided in the translation.
        To link the synonyms to definitions
        """
        if not extra_data['synonyms']:
            return

        result = {}

        for part_of_speech, synonyms_list, *_ in extra_data['synonyms']:
            for group in synonyms_list:
                synonyms = group[0]
                key = group[1]
                result[key] = synonyms

        return result

    def _get_examples(self, examples: list) -> list[str]:
        if not examples:
            return []

        return [example[0] for example in examples[0]]

    def _get_translations(self, extra_data: dict) -> dict[str, list[TranslationModel]] | None:
        if not extra_data['all-translations']:
            return

        result = {}

        for part_of_speech, _, translation, *_ in extra_data['all-translations']:
            result[part_of_speech] = []

            for word in translation:
                confidence = word[-1] if isinstance(word[-1], float) else None

                item = TranslationModel(
                    text=word[0],
                    translations=word[1],
                    confidence=confidence,
                )

                result[part_of_speech].append(item)

        return result
