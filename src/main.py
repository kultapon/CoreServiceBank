import uvicorn
from fastapi import FastAPI
from src.api.auth import auth_router
from src.core.errors.handlers import register_exception_handlers
from src.core.logger import setup_logging
from src.core.setnry import setup_sentry

app = FastAPI(title="CoreService")

app.include_router(auth_router)

setup_logging()
setup_sentry()

register_exception_handlers(app)

if __name__ == "__main__":
    uvicorn.run("src.main:app", port=8000, reload=True)