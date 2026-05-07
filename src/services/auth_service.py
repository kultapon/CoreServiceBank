from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from src.errors.errors import AppError
from src.schemas.config import db_settings
from src.models import User
from src.repositories.repositories import UserRepository
from src.schemas.user import UserCreate, UserLogin


pwd_hasher = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_hasher.verify(plain_password, hashed_password)


async def authenticate(user: UserLogin, session: AsyncSession) -> User:
    usr_rep = UserRepository(session)

    db_user = await usr_rep.get_user_by_username(user.username)

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise AppError("Invalid username or password")

    if db_user.banned_at is not None:
        raise AppError("User is banned")

    return db_user

