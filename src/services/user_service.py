import datetime
from sqlalchemy import asc, desc
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.errors.errors import AppError
from src.models import User
from src.repositories.repositories import UserRepository
from src.schemas.roles import RoleEnum
from src.schemas.user import UserFilter
from src.services.auth_service import pwd_hasher

USER_SORT_FIELDS = {
    "id": User.id,
    "created_at": User.created_at,
    "username": User.username,
}

async def get_user_by_id(
    user_id: int,
    session: AsyncSession,
) -> User:
    usr_rep = UserRepository(session)

    user = await usr_rep.get_active_user_with_role(user_id)

    if not user:
        raise AppError("User not found")

    return user

def build_users_query(
    filter_obj: UserFilter
):
    query = select(User).options(selectinload(User.role))

    if filter_obj.created_from:
        query = query.where(User.created_at >= filter_obj.created_from)

    if filter_obj.created_to:
        query = query.where(User.created_at <= filter_obj.created_to)

    if not filter_obj.include_banned:
        query = query.where(User.banned_at.is_(None))

    sort_col = USER_SORT_FIELDS.get(
        filter_obj.sort_by,
        User.created_at,
    )

    query = query.order_by(
        desc(sort_col)
        if filter_obj.order == "desc"
        else asc(sort_col)
    )

    return query

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