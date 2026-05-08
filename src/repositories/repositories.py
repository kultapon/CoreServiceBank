
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.models import Role, User
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):

    async def exists(self, username: str) -> bool:
        query = select(User.id).where(User.username == username)
        result = await self.session.scalar(query)
        return result is not None

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.session.scalar(
            select(User).where(User.username == username))

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.session.scalar(
            select(User).where(User.id == user_id)
        )

    async def get_active_user_with_role(
        self,
        user_id: int,
    ) -> User | None:

        query = (
            select(User)
            .options(joinedload(User.role))
            .where(User.id == user_id)
            .where(User.banned_at.is_(None))
        )

        return await self.session.scalar(query)

class RoleRepository(BaseRepository[Role]):

    async def get_role_by_id(self, role_id: int) -> Role | None:

        return await self.session.scalar(
            select(Role)
            .where(Role.id == role_id)
        )

    async def get_role_by_name(self, name: str) -> Role | None:

        return await self.session.scalar(
            select(Role).where(Role.name == name)
        )
