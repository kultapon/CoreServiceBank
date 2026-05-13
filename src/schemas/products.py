from datetime import datetime
from decimal import Decimal
from typing import Literal

from src.schemas.categories import CategoryBase
from pydantic import (
    BaseModel,
    Field, ConfigDict,

)

class ProductFilter(BaseModel):
    category_id: int | None = Field(None,ge=1,
        le=2147483647)

    sort_by: Literal["id", "username", "price_rub", "created_at"] = "created_at"

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

class ProductBase(BaseModel):
    id: int
    name: str
    description: str | None
    price_rub: Decimal
    common_note: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class ProductReadUser(ProductBase):
    category_id: int
    creator_id: int

class ProductReadModerator(ProductReadUser):
    special_note: str | None = None

class ProductReadPag(ProductBase):
    category: CategoryBase
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

class ProductUpdate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=255,
    )
    description: str | None = None

    price_rub: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    common_note: str | None = None
    special_note: str | None = None
    category_id: int | None = None

    model_config = ConfigDict(
        extra="forbid",
    )