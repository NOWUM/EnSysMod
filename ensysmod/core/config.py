import secrets

from pydantic import PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from utils.utils import get_project_root


class Settings(BaseSettings):
    """
    Settings for this application.

    You can override the variables with a .env file.
    You can override the variables (and .env file) by environment variables.
    """

    SERVER_NAME: str = "EnSysMod"

    # Secret key for hashing passwords
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # Expire duration for access tokens
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # Database access
    POSTGRES_SERVER: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    SQLALCHEMY_DATABASE_URI: str | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None, values: ValidationInfo) -> str:
        if v is None:
            return f"sqlite:///{get_project_root()}/ensysmod/local.db"
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            path=f"{values.data.get('POSTGRES_DB') or ''}",
        ).unicode_string()

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
