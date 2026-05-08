import structlog
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.errors.errors import AppError, UniqueConstraintError
from src.schemas.config import db_settings
from src.models import User
from src.repositories.repositories import UserRepository, RoleRepository
from src.schemas.user import UserAuth
logger = structlog.get_logger(__name__)

pwd_hasher = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_hasher.verify(plain_password, hashed_password)


async def authenticate(user: UserAuth, session: AsyncSession) -> User:
    usr_rep = UserRepository(session)

    db_user = await usr_rep.get_user_by_username(user.username)

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise AppError("Invalid username or password")

    if db_user.banned_at is not None:
        raise AppError("User is banned")

    return db_user

async def register_user(user: UserAuth, session: AsyncSession) -> User:
    usr_rep = UserRepository(session)
    role_rep = RoleRepository(session)

    if_exists = await usr_rep.exists(user.username)

    if if_exists:
        raise AppError("User already exists")

    db_user = User(username=user.username)

    db_user.password_hash = pwd_hasher.hash(user.password)

    try:
        role = await role_rep.get_role_by_name(db_settings.DEFAULT_REGISTER_ROLE)
        if role is None:
            raise AppError("Something went wrong while registering user")

        db_user.role = role
        await usr_rep.save(db_user)

    except UniqueConstraintError as e:
        msg = str(e.__cause__ or e)
        if "unique" in msg.lower():
            raise AppError("User already exists")
        else:
            raise AppError(msg)

    return db_user