from fastapi import (
    BackgroundTasks,
    Body,
    Depends,
    Form,
    status,
)


from src.services.auth_service import authenticate
from src.services.jwt_service import (create_access_token, create_refresh_token)
from src.api.routers import auth_router
from src.database import SessionDep
from src.schemas.user import UserCreate, UserLogin, UserRead

@auth_router.post(
    "/login",
    summary="Login user with email or username",
)
async def login(usr_params: UserLogin, session: SessionDep):
    db_user = await authenticate(usr_params, session)
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
    usr_params: UserCreate,
    session: SessionDep,
    background_tasks: BackgroundTasks,
):
    created_user = await register_user(usr_params, session)

    return created_user