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