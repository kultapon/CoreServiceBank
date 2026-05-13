import structlog
from fastapi import Depends, Body, status

from src.api.routers import admin_router
from src.database import SessionDep
from src.dependencies import require_roles
from src.models import User
from src.schemas.config import DBIntID
from src.schemas.roles import RoleEnum
from src.schemas.user import BanReason, UserRead, PasswordChange
from src.services.auth_service import register_user
from src.services.user_service import ban_user_mod, unban_user_mod, change_password, delete_user
from src.schemas.user import UserAuth
logger = structlog.getLogger(__name__)

@admin_router.patch("/ban/{user_id}")
async def ban_user(
    session: SessionDep,
    user_id: DBIntID,
    ban_reason: BanReason,
    current_user: User = Depends(
        require_roles(
        RoleEnum.ADMIN,
        )
    ),
):
    banned_at = await ban_user_mod(user_id, ban_reason.ban_reason, current_user, session)

    return {"banned_at": banned_at}

@admin_router.patch("/unban/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unban_user(
    session: SessionDep,
    user_id: DBIntID,
    current_user: User = Depends(
            require_roles(
                RoleEnum.ADMIN,
            )
        ),
):
    await unban_user_mod(user_id, current_user, session)



@admin_router.post("",response_model=UserRead)
async def create_user_admin(
    session: SessionDep,
    usr_params: UserAuth,
    _: User = Depends(
            require_roles(
                RoleEnum.ADMIN,
            )
        )

):
    created_user = await register_user(usr_params, session)
    logger.info(
        event="admin_user_created",
        user_id=created_user.id,
    )
    return created_user

@admin_router.patch("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(
    user_id: DBIntID,
    session: SessionDep,
    password: PasswordChange,
    current_user: User = Depends(
            require_roles(
                RoleEnum.ADMIN,
            )
        )

):
    user_id = await change_password(user_id, password.password, current_user, session)
    logger.info(
        event="admin_user_password_changed",
        user_id=user_id,
    )

@admin_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_admin(
    user_id: DBIntID,
    session: SessionDep,
    current_user: User = Depends(
            require_roles(
                RoleEnum.ADMIN,
            )
        )

):
    user_id = await delete_user(user_id, current_user, session)
    logger.info(
        event="admin_user_deleted",
        user_id=user_id,
    )
