from fastapi import FastAPI
from src.core.errors.errors import AppError
from src.schemas.config import api_bank
import httpx
import structlog

app = FastAPI()
logger = structlog.getLogger(__name__)


async def fetch_nbrb_usd_rate() -> dict:

    nbrb_api_url = api_bank.API_BANK_URL

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(nbrb_api_url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            raise AppError("Couldn't connect to NBRB API")


async def get_usd_rate():
    nbrb_data = await fetch_nbrb_usd_rate()
    
    try:
        usd_rate = nbrb_data["Cur_OfficialRate"]
    except Exception:
        raise AppError("Something went wrong with NBRB API")
    return usd_rate