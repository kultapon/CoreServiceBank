from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.dependencies import get_current_user, require_roles
from src.database import get_session
from src.models import User
from src.api.routers import products_router
from src.schemas.product import ProductFilter, ProductBase
from src.schemas.roles import RoleEnum
from src.services.products_service import build_products_query


SessionDep = Depends(get_session)


@products_router.get(
    "", response_model=Page[ProductBase]
)
async def get_products(
    session: AsyncSession = SessionDep,
    filters: ProductFilter = Depends(),
    params: Params = Depends(),
    current_user: User = Depends(require_roles(RoleEnum.USER,RoleEnum.MODERATOR))
):
    query = build_products_query(
        filters=filters,
        current_user=current_user,
    )
    return await apaginate(
        session,
        query,
        params,
    )