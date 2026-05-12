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

class CategoryCreate(BaseModel):
    name:str = Field(
        min_length=2,
        max_length=255,
    )
    model_config = ConfigDict(
        extra="forbid",
    )