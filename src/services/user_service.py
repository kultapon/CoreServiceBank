import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.errors.errors import AppError
from src.models import User
from src.repositories.repositories import UserRepository
from src.schemas.roles import RoleEnum
from src.services.auth_service import pwd_hasher

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
        raise AppError("You cannot ban yourself")

    if user.role.name == RoleEnum.ADMIN:
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

    if user.role.name == RoleEnum.ADMIN:
        raise AppError("Cannot unban other admins")

    user.banned_at = None
    user.ban_reason = None

    usr_rep = UserRepository(session)
    await usr_rep.save(user)

async def change_password(user_id: int, new_password: str, current_user: User, session: AsyncSession):

    user = await get_user_by_id(user_id, session)

    if user.role.name == RoleEnum.ADMIN and user.id != current_user.id:
        raise AppError("Cannot change other admins passwords")

    hashed = pwd_hasher.hash(new_password)

    user.password_hash = hashed

    usr_rep = UserRepository(session)
    await usr_rep.save(user)
    return user.id

async def delete_user(user_id: int, current_user: User, session: AsyncSession):

    usr_rep = UserRepository(session)

    user = await usr_rep.get_user_by_id(user_id)

    if not user:
        raise AppError("User not found")

    if user.id == current_user.id:
        raise AppError("Cannot delete yourself")

    if user.role.name == RoleEnum.ADMIN:
        raise AppError("Cannot delete other Admins")

    usr_rep = UserRepository(session)

    user_id = user.id
    await usr_rep.delete(user)

    return user_id