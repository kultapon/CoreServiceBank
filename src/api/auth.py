from fastapi import (
    BackgroundTasks,
    Body,
    Depends,
    Form,
    status,
)
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.api.routers import auth_router
from src.database import SessionDep
from src.schemas.user import UserCreate, UserLogin, UserRead
from src.services.auth_service.service import (
    authenticate,
    change_password,
    check_user_email,
    register_user,
    verify_user,
)
from src.services.jwt_service.service import (
    create_access_token,
    create_email_confirm_token,
    create_refresh_token,
    create_reset_token,
)

templates = Jinja2Templates(directory="src/templates")


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
    email_token = create_email_confirm_token(created_user.id)
    background_tasks.add_task(
        send_email, created_user.email, "Email Confirmation", email_token
    )

    return created_user