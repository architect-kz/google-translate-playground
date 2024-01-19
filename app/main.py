from fastapi import FastAPI

from app.v1.core.config import settings
from app.v1.routes import router as v1_router

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
)
app.include_router(v1_router, prefix="/v1")


@app.get("/")
async def root() -> dict:
    """ Welcome endpoint """
    return {
        'title': settings.APP_TITLE,
        'version': settings.APP_VERSION,
        'description': settings.APP_DESCRIPTION
    }
