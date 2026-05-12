from sqlalchemy import asc, desc, select, literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, with_expression

from src.core.errors.errors import AppError, ForbiddenError, UniqueConstraintError
from src.repositories.repositories import CategoryRepository, ProductRepository
from src.schemas.categories import CategoryFilter, CategoryCreate
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

async def create_category(
    category_data: CategoryCreate,
    session: AsyncSession
) -> Category:

    cat_rep = CategoryRepository(session)

    exists = await cat_rep.exists(category_data.name)

    if exists:
        raise AppError("Category with this name already exists")


    category = Category(name=category_data.name)

    try:

        await cat_rep.save(category)

    except UniqueConstraintError as e:
        msg = str(e.__cause__ or e)
        if "unique" in msg.lower():
            raise AppError("Category with this name already exists")
        else:
            raise AppError(msg)


    return category


async def update_category(
        category_id: int,
        update_data: CategoryCreate,
        session: AsyncSession,
) -> Category:
    cat_rep = CategoryRepository(session)

    category = await cat_rep.get_category_by_id(category_id)

    if not category:
        raise AppError("Category not found")

    exists_id = await cat_rep.exists(update_data.name)

    if exists_id and exists_id != category.id:
        raise AppError("Category with this name already exists")

    category.name = update_data.name

    try:
        await cat_rep.save(category)

    except UniqueConstraintError as e:
        msg = str(e.__cause__ or e)
        if "unique" in msg.lower():
            raise AppError("Product with this name already exists")
        else:
            raise AppError(msg)

    return category

async def delete_category(category_id: int, session: AsyncSession):
    cat_rep = CategoryRepository(session)
    category = await cat_rep.get_category_by_id(category_id)

    if not category:
        raise AppError("Category not found")

    name = category.name
    await cat_rep.delete(category)
    return name
