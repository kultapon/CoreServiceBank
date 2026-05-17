import asyncio
import structlog
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import SessionLocal
from src.models import User, Role
from src.schemas.config import db_settings

logger = structlog.getLogger(__name__)

pwd_hasher = PasswordHash.recommended()


async def seed_admin(session: AsyncSession) -> None:
    admin_username = db_settings.ADMIN_USERNAME
    admin_password = db_settings.ADMIN_PASSWORD
    password_hash = pwd_hasher.hash(admin_password)

    existing_admin = await session.scalar(
        select(User).where(User.username == admin_username)
    )

    if existing_admin:
        if pwd_hasher.verify(admin_password, existing_admin.password_hash):
            logger.info(
                event="admin_user_creation_skipped",
                user_id=existing_admin.id,
            )
        else:
            logger.info(
                event="admin_user_set_password",
                user_id=existing_admin.id,
            )
            existing_admin.password_hash = password_hash
            await session.commit()
        return

    admin_role = await session.scalar(
        select(Role).where(Role.name == "admin")
    )

    if not admin_role:
        raise RuntimeError("Required roles are missing. Run roles seed first.")

    admin_user = User(
        username=admin_username,
        password_hash=password_hash,
        role=admin_role,
    )

    session.add(admin_user)
    await session.commit()

    logger.info(f"Admin created: {admin_username}")


async def main():
    async with SessionLocal() as session:
        await seed_admin(session)


if __name__ == "__main__":
    asyncio.run(main())