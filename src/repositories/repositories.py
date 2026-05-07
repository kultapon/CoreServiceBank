
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models import Role, User
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.session.scalars(
            select(User).where(User.username == username)
        )
        return result.one_or_none()

    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.session.scalars(
            select(User).where(User.id == user_id)
        )
        return result.one_or_none()

    async def get_user_with_roles(self, user_id: int) -> User | None:
        result = await self.session.scalars(
            select(User)
            .options(selectinload(User.role))
            .where(User.id == user_id)
        )
        return result.one_or_none()

    async def get_users(self, user_ids: list[int]):
        result = await self.session.scalars(
            select(User)
            .options(selectinload(User.role))
            .where(User.id.in_(user_ids))
        )
        return result.all()
