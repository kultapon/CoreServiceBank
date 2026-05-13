from fastapi import Depends, Body, status

from src.api.routers import admin_router
from src.database import SessionDep
from src.dependencies import require_roles
from src.models import User
from src.schemas.config import DBIntID
from src.schemas.roles import RoleEnum
from src.schemas.user import BanReason
from src.services.user_service import ban_user_mod, unban_user_mod


@admin_router.patch("/ban/{user_id}")
async def ban_user(
    session: SessionDep,
    user_id: DBIntID,
    ban_reason: BanReason = Body(..., embed=True),
    current_user: User = Depends(
        require_roles(
        RoleEnum.ADMIN,
        )
    ),
):
    banned_at = await ban_user_mod(user_id, ban_reason, current_user, session)

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
