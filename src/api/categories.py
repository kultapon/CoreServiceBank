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
from src.schemas.config import DBIntID
from src.schemas.products import ProductCreate
from src.schemas.roles import RoleEnum
from src.services.categories_service import build_categories_query, create_category, update_category, delete_category

logger = structlog.getLogger(__name__)

@categories_router.get(
    "", response_model=Page[CategoryRead]
)
async def get_categories(
    session: SessionDep,
    filters: CategoryFilter = Depends(),
    params: Params = Depends(),
    _: User = Depends(require_roles(RoleEnum.MODERATOR))
):
    query = build_categories_query(
        filter_obj=filters
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
    _: User = Depends(
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



@categories_router.put(
    "/{category_id}",
    response_model=CategoryRead,)
async def update_product_endpoint(
    category_id: DBIntID,
    category_data: CategoryCreate,
    session: SessionDep,
    _: User = Depends(
        require_roles(
            RoleEnum.MODERATOR,
        )
    ),
):

    category = await update_category(
        category_id=category_id,
        update_data=category_data,
        session=session,
    )
    logger.info(
        event="category_updated",
        product_id=category.id,
    )
    return category

@categories_router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category_endpoint(
    category_id: DBIntID,
    session: SessionDep,
    _: User = Depends(
        require_roles(RoleEnum.MODERATOR)
    ),
):

    category_name = await delete_category(
        category_id=category_id,
        session=session,
    )

    logger.info(
        event="category_deleted",
        category_name=category_name,
    )
