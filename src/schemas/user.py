from datetime import datetime
from typing import Annotated, Literal
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    conint,
    conlist,
    field_validator,
    model_validator,
)


class UserLogin(BaseModel):
    username: str | None = Field(
        None,
        pattern="^[a-zA-Z0-9_-]+$",
        title="Username",
        examples=["my_username"],
        min_length=5,
        max_length=50,
    )
    password: str = Field(..., min_length=8, max_length=64)

    @model_validator(mode="after")
    def normalize_and_validate(self):
        if not self.username:
            raise ValueError("Username is required")
        return self


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        pattern="^[a-zA-Z0-9_-]+$",
        title="Username",
        examples=["my_username"],
        min_length=5,
        max_length=50,
    )
    password: str = Field(..., min_length=8, max_length=64, title="Password")


class UserRead(BaseModel):
    id: int = Field(..., title="User ID")
    username: str = Field(..., title="Username")
    created_at: datetime = Field(..., title="Created at")
    role: str = Field(..., title="Role")