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