from sqlalchemy import asc, desc, select
from sqlalchemy.orm import joinedload

from src.schemas.roles import RoleEnum
from src.models import Product, User
from src.schemas.product import ProductFilter

PRODUCT_SORT_FIELDS = {
    "created_at": Product.created_at,
    "price_rub": Product.price_rub,
    "name": Product.name,
}

def build_products_query(
    filters: ProductFilter,
    current_user: User,
):
    user_role = current_user.role.name


    if user_role == RoleEnum.USER:

        query = (
            select(
                Product.id,
                Product.name,
                Product.description,
                Product.price_rub,
                Product.common_note,
                Product.category_id,
                Product.creator_id,
                Product.created_at,
                Product.updated_at,
            )
            .select_from(Product)
        )

    else:
        query = (
            select(Product)
            .options(
                joinedload(Product.category),
                joinedload(Product.creator),
            )
        )

    if filters.category_id:
        query = query.where(
            Product.category_id == filters.category_id
        )


    sort_col = PRODUCT_SORT_FIELDS.get(filters.sort_by)

    if not sort_col:
        sort_col = Product.created_at

    query = query.order_by(
        desc(sort_col)
        if filters.order == "desc"
        else asc(sort_col)
    )

    return query