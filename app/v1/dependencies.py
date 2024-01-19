from fastapi import Depends

from app.v1.core.config import settings
from app.v1.db.mongodb import MongoDB
from app.v1.repositories.translation import TranslationRepository, ITranslation
from app.v1.services.translation import TranslationService

"""
The naming is self-explanatory. Skipped documentation.
"""


def get_mongo_db():
    mongo_db = MongoDB(settings.MONGO_URL)
    return mongo_db.get_database(settings.MONGO_DB)


def get_translation_repository(db=Depends(get_mongo_db)) -> ITranslation:
    return TranslationRepository(db)


def get_translation_service(repo=Depends(get_translation_repository)) -> TranslationService:
    return TranslationService(repo)
