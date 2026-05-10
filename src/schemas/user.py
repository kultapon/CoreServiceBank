from datetime import datetime
from pydantic import (
    BaseModel,
    Field, ConfigDict,

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
    password: str = Field(..., min_length=8, max_length=64)


class UserRead(BaseModel):
    id: int = Field(..., title="User ID")
    username: str = Field(..., title="Username")
    created_at: datetime = Field(..., title="Created at")
    model_config = ConfigDict(from_attributes=True)


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