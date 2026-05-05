import uvicorn
from fastapi import FastAPI

app = FastAPI(title="CoreService")

if __name__ == "__main__":
    uvicorn.run("src.main:app", port=8000, reload=True)