from sqlalchemy import asc, desc, select, literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, with_expression

from src.core.errors.errors import AppError, ForbiddenError, UniqueConstraintError
from src.repositories.repositories import CategoryRepository, ProductRepository
from src.schemas.roles import RoleEnum
from src.models import Product, User
from src.schemas.product import ProductFilter, ProductCreate, ProductUpdate, ProductReadModerator, ProductReadUser

PRODUCT_SORT_FIELDS = {
    "created_at": Product.created_at,
    "price_rub": Product.price_rub,
    "name": Product.name,
}

def build_product_response(
    product: Product,
    current_user: User,
):

    if current_user.role.name == RoleEnum.MODERATOR:
        return ProductReadModerator.model_validate(product)

    return ProductReadUser.model_validate(product)

def build_products_query(
    filters: ProductFilter,
    current_user: User,
):
    query = (
        select(Product)
        .options(
            joinedload(Product.category),
            joinedload(Product.creator),
        )
    )

    if current_user.role.name == RoleEnum.USER:
        query = query.options(
            with_expression(
                Product.special_note,
                literal(None),
            )
        )

    if filters.category_id:
        query = query.where(
            Product.category_id == filters.category_id
        )

    sort_col = PRODUCT_SORT_FIELDS.get(
        filters.sort_by,
        Product.created_at,
    )

    query = query.order_by(
        desc(sort_col)
        if filters.order == "desc"
        else asc(sort_col)
    )

    return query

async def create_product(
    product_data: ProductCreate,
    current_user: User,
    session: AsyncSession
) -> Product:

    product_rep = ProductRepository(session)

    exists = await product_rep.exists(product_data.name)

    if exists:
        raise AppError("Product with this name already exists")

    cat_rep = CategoryRepository(session)
    category = await cat_rep.get_category_by_id(
        product_data.category_id
    )

    if not category:
        raise AppError(
            "Category not found"
        )

    special_note = product_data.special_note


    if current_user.role.name == RoleEnum.USER:
        special_note = None

    product = Product(
        name=product_data.name,
        description=product_data.description,
        price_rub=product_data.price_rub,
        common_note=product_data.common_note,
        special_note=special_note,
        category_id=product_data.category_id,
        creator_id=current_user.id,
    )

    try:

        await product_rep.save(product)

    except UniqueConstraintError as e:
        msg = str(e.__cause__ or e)
        if "unique" in msg.lower():
            raise AppError("Product with this name already exists")
        else:
            raise AppError(msg)


    return product


async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: User,
    session: AsyncSession,
) -> Product:

    product_rep = ProductRepository(session)
    category_rep = CategoryRepository(session)

    product = await product_rep.get_product_by_id(product_id)

    if not product:
        raise AppError("Product not found")

    is_owner = product.creator_id == current_user.id
    is_moderator = current_user.role.name == RoleEnum.MODERATOR

    if not is_owner and not is_moderator:
        raise AppError("You cannot edit this product")

    update_data = product_data.model_dump(
        exclude_unset=True
    )

    if "category_id" in update_data:

        category = await category_rep.get_category_by_id(
            update_data["category_id"]
        )

        if not category:
            raise AppError("Category not found")


    if "name" in update_data:

        exists = await product_rep.exists(update_data["name"])

        if exists:
            raise AppError("Product with this name already exists")

    for field, value in update_data.items():

        if (
            field == "special_note"
            and current_user.role.name != RoleEnum.MODERATOR
        ):
            continue

        setattr(product, field, value)

    await product_rep.save(product)

    return product

async def delete_product(product_id: int, session: AsyncSession):
    product_rep = ProductRepository(session)
    product = await product_rep.get_product_by_id(product_id)

    if not product:
        raise AppError("Product not found")
    name = product.name
    await product_rep.delete(product)
    return name