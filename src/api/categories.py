import structlog
from fastapi import Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate

from src.dependencies import require_roles
from src.database import SessionDep
from src.models import User
from src.api.routers import categories_router
from src.schemas.categories import CategoryFilter, CategoryRead
from src.schemas.roles import RoleEnum
from src.services.categories_service import build_categories_query


logger = structlog.getLogger(__name__)

@categories_router.get(
    "", response_model=Page[CategoryRead]
)
async def get_categories(
    session: SessionDep,
    filters: CategoryFilter = Depends(),
    params: Params = Depends(),
    current_user: User = Depends(require_roles(RoleEnum.MODERATOR))
):
    query = build_categories_query(
        filters=filters
    )
    return await apaginate(
        session,
        query,
        params,
    )


