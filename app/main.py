import uvicorn

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.v1.core.config import settings
from app.v1.routes import router as v1_router

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
)
app.include_router(v1_router, prefix="/v1")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom exception handler. jsonapi.org conventions error responses.
    Example:
    {
        "error": {
            "message": "Error message",
            "detail": "Error detail"
        }
    }
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({'error': exc.detail})
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom validation exception handler.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.get("/")
async def root() -> dict:
    """ Welcome endpoint """
    return {
        'title': settings.APP_TITLE,
        'version': settings.APP_VERSION,
        'description': settings.APP_DESCRIPTION
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
