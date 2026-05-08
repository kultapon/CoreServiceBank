import uvicorn
from fastapi import FastAPI
from src.api.auth import auth_router
from src.core.errors.handlers import register_exception_handlers

app = FastAPI(title="CoreService")

app.include_router(auth_router)

register_exception_handlers(app)

if __name__ == "__main__":
    uvicorn.run("src.main:app", port=8000, reload=True)