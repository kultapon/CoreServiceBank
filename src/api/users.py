from fastapi import Depends

from src.api.routers import users_router
from src.dependencies import require_roles
from src.models import User
from src.schemas.roles import RoleEnum
from src.schemas.user import UserRead


@users_router.get("/me", response_model=UserRead)
async def get_user(user: User = Depends(require_roles(RoleEnum.MODERATOR, RoleEnum.ADMIN, RoleEnum.USER))):
    return user
