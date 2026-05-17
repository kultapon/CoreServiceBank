from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.core.errors.errors import UniqueConstraintError, DatabaseError
from src.schemas.config import db_settings

engine = create_async_engine(db_settings.DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()

        except IntegrityError as e:
            await session.rollback()
            msg = str(e.orig).lower()
            if "duplicate key" in msg or "unique constraint" in msg:

                raise UniqueConstraintError(

                    "Unique constraint violated!"

                ) from e

            else:
                print(e)
                raise DatabaseError(f"Database integrity error") from e

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError("Database error") from e

        finally:
            await session.close()


SessionDep = Annotated[AsyncSession, Depends(get_session)]