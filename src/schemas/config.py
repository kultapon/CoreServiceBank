from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ENV = PROJECT_ROOT / ".env"


class DBSettings(BaseSettings):
    DATABASE_URL: str
    ADMIN_USERNAME: str = "admin_main"
    ADMIN_PASSWORD: str = "change_me123"
    model_config = SettingsConfigDict(
        env_file=ENV,
        extra="ignore",
    )

db_settings = DBSettings()

class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(env_file=ENV, extra="ignore",)


jwt_settings = JWTSettings()