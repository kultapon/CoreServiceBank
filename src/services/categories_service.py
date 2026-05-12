from sqlalchemy import asc, desc, select, literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, with_expression

from src.core.errors.errors import AppError, ForbiddenError, UniqueConstraintError
from src.repositories.repositories import CategoryRepository, ProductRepository
from src.schemas.categories import CategoryFilter
from src.schemas.roles import RoleEnum
from src.models import Product, User, Category\

CATEGORY_SORT_FIELDS = {
    "id": Category.id,
    "created_at": Category.created_at,
    "name": Category.name,
}


def build_categories_query(
    filters: CategoryFilter
):
    query = select(Category)



    sort_col = CATEGORY_SORT_FIELDS.get(
        filters.sort_by,
        Product.created_at,
    )

    query = query.order_by(
        desc(sort_col)
        if filters.order == "desc"
        else asc(sort_col)
    )

    return query