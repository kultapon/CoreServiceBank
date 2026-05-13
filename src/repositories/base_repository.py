from typing import Generic, TypeVar

from sqlalchemy import Select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.errors.errors import DatabaseError, UniqueConstraintError

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _commit_with_handling(self) -> None:
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            msg = str(e.orig).lower()

            if "duplicate key" in msg or "unique constraint" in msg:
                raise UniqueConstraintError(
                    "Unique constraint violated!"
                ) from e
            else:
                print(e)
                raise DatabaseError(f"Database integrity error") from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseError("Database error") from e

    async def save(self, obj: T) -> T:
        self.session.add(obj)
        await self._commit_with_handling()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)
        await self._commit_with_handling()

    async def save_all(self, objs: list[T]) -> list[T]:
        for obj in objs:
            self.session.add(obj)
        await self._commit_with_handling()
        return objs

    async def perform_custom_query(self, query: Select):
        result = await self.session.scalars(query)
        return result.all()