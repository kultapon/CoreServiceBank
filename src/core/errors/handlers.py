import structlog
from fastapi import Request, status
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from src.core.errors.errors import AppError

logger = structlog.getLogger(__name__)


def register_exception_handlers(app):

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError):
        logger.warning(f"AppError: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(_: Request, exc: ValueError):
        logger.warning(f"ValueError: {exc}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ResponseValidationError)
    async def validation_exception_handler_response(
        _: Request, exc: ResponseValidationError
    ):
        logger.warning(f"ResponseValError: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": exc.errors()},
        )

    @app.exception_handler(IntegrityError)
    async def sqlalchemy_integrity_error(_: Request, exc: IntegrityError):
        logger.error(f"IntegrityError: {exc}")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Database integrity error"},
        )

    @app.exception_handler(TypeError)
    async def unhandled_exception_handler(_: Request, exc: TypeError):
        logger.exception(f"Unhandled error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception):
        logger.exception(f"Unhandled error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )