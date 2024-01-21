import os

from functools import lru_cache

from pydantic_settings import BaseSettings


class CommonSettings(BaseSettings):
    """
    Common settings for all environments.
    """
    APP_TITLE: str
    APP_VERSION: str
    APP_DESCRIPTION: str
    DEBUG: bool
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_URL: str
    MONGO_DB: str
    LIMIT: int = 10
    SKIP: int = 0
    SORTING: str = 'asc'


class DevelopmentSettings(CommonSettings):
    class Config:
        env_file: str = ".env.development"
        extra: str = 'allow'


class ProductionSettings(CommonSettings):
    class Config:
        env_file: str = ".env.production"
        extra: str = 'allow'


@lru_cache()
def get_settings() -> BaseSettings:
    """
    Returns cached settings object based on the current environment.
    """
    environment = os.getenv("ENVIRONMENT", "development")

    if environment == "production":
        return ProductionSettings()

    return DevelopmentSettings()


settings = get_settings()
