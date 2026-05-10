import structlog
from fastapi import Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from fastapi import status

from src.dependencies import require_roles
from src.database import SessionDep
from src.models import User
from src.api.routers import products_router
from src.schemas.config import DBIntID
from src.schemas.product import ProductFilter, ProductCreate, ProductReadPag, ProductUpdate
from src.schemas.roles import RoleEnum
from src.services.products_service import build_products_query, create_product, update_product, build_product_response

logger = structlog.getLogger(__name__)

@products_router.get(
    "", response_model=Page[ProductReadPag]
)
async def get_products(
    session: SessionDep,
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

@products_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def made_product(
    product_data: ProductCreate,
    session: SessionDep,
    current_user: User = Depends(
    require_roles(
            RoleEnum.USER,
            RoleEnum.MODERATOR,
        )
    ),
):

    product = await create_product(
        product_data,
        current_user,
        session,
    )

    logger.info(
        event="product_created",
        user_id=product.id,
    )

    return build_product_response(
        product,
        current_user,
    )

@products_router.patch(
    "/{product_id}",
)
async def update_product_endpoint(
    product_id: DBIntID,
    product_data: ProductUpdate,
    session: SessionDep,
    current_user: User = Depends(
        require_roles(
            RoleEnum.USER,
            RoleEnum.MODERATOR,
        )
    ),
):

    product = await update_product(
        product_id=product_id,
        product_data=product_data,
        current_user=current_user,
        session=session,
    )
    logger.info(
        event="product_updated",
        user_id=product.id,
    )
    return build_product_response(
        product,
        current_user,
    )


@products_router.delete(
    "/{product_id}",
)
async def delete_product_endpoint(
    product_id: DBIntID,
    product_data: ProductUpdate,
    session: SessionDep,
    current_user: User = Depends(
        require_roles(RoleEnum.MODERATOR,)
    ),
):

    product = await update_product(
        product_id=product_id,
        product_data=product_data,
        current_user=current_user,
        session=session,
    )
    logger.info(
        event="product_updated",
        user_id=product.id,
    )
    return build_product_response(
        product,
        current_user,
    )

