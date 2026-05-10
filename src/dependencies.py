from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.repositories import UserRepository
from src.services.jwt_service import decode_token
from src.database import get_session
from src.models import User
from src.schemas.roles import RoleEnum
from src.core.errors.errors import TokenError, AppError, ForbiddenError

SessionDep = Depends(get_session)

def get_payload(expected_type: str):
    def dep(
        authorization: str | None = Header(
            None, alias="Authorization", description="Bearer token"
        )
    ):
        if not authorization:
            raise TokenError("Authorization header was missing")

        scheme, _, token = authorization.partition(" ")

        if scheme.lower() != "bearer" or not token:
            raise TokenError("Authorization scheme must be Bearer")
        return decode_token(token, expected_type)

    return dep


async def get_current_user(
    session: AsyncSession = SessionDep,
    token_payload: dict = Depends(get_payload("access")),
) -> User:
    user_id = token_payload.get("sub")

    if user_id is None:
        raise TokenError("Token Error")

    usr_rep = UserRepository(session)

    user = await usr_rep.get_active_user_with_role(int(user_id))

    if not user:
        raise AppError("User not found")

    return user


def require_roles(*allowed_roles: RoleEnum):
    async def checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role.name not in allowed_roles:
            raise ForbiddenError("Insufficient permissions")

        return current_user

    return checker