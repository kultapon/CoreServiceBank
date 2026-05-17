from typing import Generic, TypeVar

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)

    async def save_all(self, objs: list[T]) -> list[T]:
        for obj in objs:
            self.session.add(obj)

        await self.session.flush()
        return objs

    async def perform_custom_query(self, query: Select):
        result = await self.session.scalars(query)
        return result.all()