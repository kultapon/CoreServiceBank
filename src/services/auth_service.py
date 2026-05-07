from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.config import db_settings
from src.models import User
from src.repositories.repositories import RoleRepository, UserRepository
from src.schemas.user import UserCreate, UserLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate(user: UserLogin, session: AsyncSession) -> User:
    usr_rep = UserRepository(session)
    db_user: User | None

    if user.username:
        db_user = await usr_rep.get_user_by_username(user.username)
    else:
        db_user = await usr_rep.get_user_by_email(user.email)

    if not db_user or not verify_password(user.password, db_user.password):
        raise AppError("Invalid username or password")

    if db_user.deleted_at is not None:
        raise AppError("User is deleted")

    if db_user.banned_at is not None:
        raise AppError("User is banned")

    return db_user


async def register_user(user: UserCreate, session: AsyncSession) -> User:
    usr_rep = UserRepository(session)
    db_user = User(**user.model_dump())
    role_rep = RoleRepository(session)
    db_user.password = pwd_context.hash(user.password)

    try:
        role = await role_rep.get_role_by_name(
            db_settings.DEFAULT_REGISTER_ROLE
        )
        db_user.roles.append(role)
        await usr_rep.save(db_user)
    except UniqueConstraintError as e:
        msg = str(e.__cause__ or e)
        if "unique" in msg.lower():
            raise AppError("User already exists")
        else:
            raise AppError(msg)

    return db_user