import uvicorn
from fastapi import FastAPI
from src.api.auth import auth_router
app = FastAPI(title="CoreService")

app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", port=8000, reload=True)