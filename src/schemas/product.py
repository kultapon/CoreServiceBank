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


class CreatorShortRead(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(
        from_attributes=True
    )

class CategoryShortRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )

class ProductBase(BaseModel):
    id: int
    name: str
    description: str | None
    price_rub: Decimal
    common_note: str | None
    special_note: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class ProductRead(ProductBase):
    category_id: int
    creator_id: int

class ProductReadPag(ProductBase):
    category: CategoryShortRead
    creator: CreatorShortRead

class ProductCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=255,
    )

    description: str | None = None

    price_rub: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    common_note: str | None = None

    special_note: str | None = None

    category_id: int

    model_config = ConfigDict(
        extra="forbid",
    )