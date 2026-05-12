import structlog
from fastapi import (
    status, Depends,
)

from src.dependencies import get_payload
from src.services.auth_service import authenticate, register_user
from src.services.jwt_service import (create_access_token, create_refresh_token)
from src.api.routers import auth_router
from src.database import SessionDep
from src.schemas.user import UserAuth, UserRead, TokenResponse
from src.services.user_service import check_user

logger = structlog.getLogger(__name__)

@auth_router.post(
    "/login",
    summary="Login user with email or username",
)
async def login(usr_params: UserAuth, session: SessionDep):
    db_user = await authenticate(usr_params, session)
    logger.info(
        event="user_logged_in",
        user_id=db_user.id,
    )
    return {
        "access_token": create_access_token(db_user.id),
        "refresh_token": create_refresh_token(db_user.id),
        "token_type": "Bearer",
    }


@auth_router.post(
    "/signup",
    summary="User registration",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
)
async def signup(
    usr_params: UserAuth,
    session: SessionDep
):
    created_user = await register_user(usr_params, session)
    logger.info(
        event="user_registered",
        user_id=created_user.id,
    )
    return created_user

@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh_token(session: SessionDep,
        token_payload: dict = Depends(get_payload("refresh")),
):
    user = await check_user(int(token_payload["sub"]), session)
    logger.info(event="user_token_refresh",
                user_id=user.id)
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "Bearer",
    }
