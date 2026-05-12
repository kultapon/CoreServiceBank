import structlog
from fastapi import Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from starlette import status

from src.dependencies import require_roles
from src.database import SessionDep
from src.models import User
from src.api.routers import categories_router
from src.schemas.categories import CategoryFilter, CategoryRead, CategoryCreate
from src.schemas.roles import RoleEnum
from src.services.categories_service import build_categories_query, create_category

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

@categories_router.post(
    "",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
)
async def make_category(
    category_data: CategoryCreate,
    session: SessionDep,
    current_user: User = Depends(
    require_roles(
            RoleEnum.MODERATOR
        )
    ),
):

    category = await create_category(
        category_data,
        session
    )

    logger.info(
        event="category_created",
        category_id=category.id,
    )
    return category