from datetime import datetime
from typing import Literal

from pydantic import (
    BaseModel,
    Field, ConfigDict, model_validator, field_validator,

)

class BanReason (BaseModel):
    ban_reason: str = Field(..., min_length=5, max_length=100, title="Ban Reason")

class PasswordChange(BaseModel):
    password: str = Field(..., min_length=8, max_length=64,
                          pattern="^[A-Za-z0-9]+$")

class UserFilter(BaseModel):

    sort_by: Literal["id", "username", "created_at"] = "created_at"
    created_from: datetime | None = None
    created_to: datetime | None = None
    include_banned: bool = False
    order: str = Field(
        default="desc",
        pattern="^(asc|desc)$",
    )


class UserAuth(BaseModel):
    username: str = Field(
        ...,
        pattern="^[a-zA-Z0-9_-]+$",
        title="Username",
        examples=["my_username"],
        min_length=5,
        max_length=50,
    )
    password: str = Field(..., min_length=8, max_length=64,
        pattern="^[A-Za-z0-9]+$")


class UserRead(BaseModel):
    id: int
    username: str
    created_at: datetime
    role: str

    @field_validator("role", mode="before")
    @classmethod
    def serialize_roles(cls, role):
        if not role:
            return None
        return role.name if hasattr(role, "name") else str(role)

    model_config = ConfigDict(from_attributes=True)

class UserReadPag(UserRead):
    banned_at: datetime | None = None
    ban_reason: str | None = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenResponseLogin(TokenResponse):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIs...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
                "token_type": "Bearer",
            }
        }
    )