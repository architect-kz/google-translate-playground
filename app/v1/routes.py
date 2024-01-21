from fastapi import APIRouter

from app.v1.endpoints.healthcheck import router as healthcheck_router
from app.v1.endpoints.translation import router as translation_router

router = APIRouter()
router.include_router(translation_router)
router.include_router(healthcheck_router)
