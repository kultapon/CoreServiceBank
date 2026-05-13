import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.errors.errors import AppError
from src.models import User
from src.repositories.repositories import UserRepository
from src.schemas.roles import RoleEnum


async def get_user_by_id(
    user_id: int,
    session: AsyncSession,
) -> User:
    usr_rep = UserRepository(session)

    user = await usr_rep.get_active_user_with_role(user_id)

    if not user:
        raise AppError("User not found")

    return user


async def check_user(user_id:int, session:AsyncSession):
    return await get_user_by_id(user_id, session)

async def ban_user_mod(
    user_id: int, ban_reason: str, current_user: User, session: AsyncSession
):
    user = await get_user_by_id(user_id, session)

    if user.id == current_user.id:
        raise AppError("You can't ban yourself")

    if current_user.role.name == user.role.name and current_user.role.name == RoleEnum.ADMIN:
        raise AppError("Cannot ban other admins")

    if user.banned_at:
        raise AppError("User is already banned")

    user.banned_at = datetime.datetime.now(datetime.timezone.utc)
    user.ban_reason = ban_reason

    usr_rep = UserRepository(session)
    await usr_rep.save(user)

    return user.banned_at


async def unban_user_mod(
    user_id: int, current_user: User, session: AsyncSession
):
    usr_rep = UserRepository(session)

    user = await usr_rep.get_user_by_id(user_id)

    if not user:
        raise AppError("User not found")

    if user.id == current_user.id:
        raise AppError("Something went wrong")

    if user.banned_at is None:
        raise AppError("User is already unbanned")

    if current_user.role.name == user.role.name and current_user.role.name == RoleEnum.ADMIN:
        raise AppError("Cannot unban other admins")

    user.banned_at = None
    user.ban_reason = None

    usr_rep = UserRepository(session)
    await usr_rep.save(user)
