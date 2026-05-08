from datetime import datetime, timedelta, timezone

import jwt

from src.schemas.config import jwt_settings
from src.core.errors.errors import TokenError


def create_token(
    user_id: int |str,
    token_type: str,
    expires_delta: timedelta,
):
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }

    return jwt.encode(
        payload,
        jwt_settings.JWT_SECRET_KEY,
        algorithm=jwt_settings.JWT_ALGORITHM,
    )

def create_access_token(user_id: int):
    return create_token(
        user_id,
        token_type="access",
        expires_delta=timedelta(
            minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )


def create_refresh_token(user_id: int):
    return create_token(
        user_id,
        token_type="refresh",
        expires_delta=timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )



def decode_token(token: str, expected_type:str) -> dict:

    try:
        payload = jwt.decode(
            token, jwt_settings.public_key, algorithms=jwt_settings.ALGORITHM
        )

        if payload["type"] != expected_type:
            raise TokenError("Invalid token type")

        if payload.get("sub") is None:
            raise TokenError("Invalid token")

        return payload

    except jwt.ExpiredSignatureError:
        raise TokenError("Token has expired")
    except (jwt.InvalidSignatureError, jwt.InvalidTokenError, jwt.DecodeError):
        raise TokenError("Invalid token")