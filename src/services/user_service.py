from sqlalchemy.ext.asyncio import AsyncSession

from src.core.errors.errors import AppError
from src.models import User
from src.repositories.repositories import UserRepository


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