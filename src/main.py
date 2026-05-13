import uvicorn
from fastapi import FastAPI
from src.api.auth import auth_router
from src.api.products import products_router
from src.api.categories import categories_router
from src.api.admin import admin_router
from src.core.errors.handlers import register_exception_handlers
from src.core.logger import setup_logging
from src.core.middleware import logging_middleware
from src.core.sentry import setup_sentry

app = FastAPI(title="CoreService")

app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(categories_router)

setup_logging()
setup_sentry()


register_exception_handlers(app)
app.middleware("http")(logging_middleware)

if __name__ == "__main__":
    uvicorn.run("src.main:app", port=8000, reload=True)