from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    Field, ConfigDict,

)

class ProductFilter(BaseModel):
    category_id: int | None = None

    sort_by: str = "created_at"

    order: str = Field(
        default="desc",
        pattern="^(asc|desc)$",
    )


class ProductBase(BaseModel):
    id: int
    name: str
    description: str | None
    price_rub: Decimal
    common_note: str | None
    category_id: int
    creator_id: int
    created_at: datetime
    special_note: str | None = None
