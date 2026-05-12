from datetime import datetime
from typing import Literal

from pydantic import ConfigDict, BaseModel, Field


class CategoryBase(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )

class CategoryRead(CategoryBase):
    created_at: datetime
    updated_at: datetime

class CategoryFilter(BaseModel):

    sort_by: Literal["id", "name", "created_at"] = "created_at"

    order: str = Field(
        default="desc",
        pattern="^(asc|desc)$",
    )
