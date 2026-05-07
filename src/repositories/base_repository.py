from typing import Generic, TypeVar

from sqlalchemy import Select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.errors.errors import DatabaseError, UniqueConstraintError

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
                raise DatabaseError(f"Database integrity error: {msg}") from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseError("Database integrity error") from e

    async def save(self, obj: T) -> T:
        self.session.add(obj)
        await self._commit_with_handling()
        return obj

    async def save_all(self, objs: list[T]) -> list[T]:
        for obj in objs:
            self.session.add(obj)
        await self._commit_with_handling()
        return objs

    async def perform_custom_query(self, query: Select):
        result = await self.session.scalars(query)
        return result.all()