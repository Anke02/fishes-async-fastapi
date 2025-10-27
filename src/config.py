from typing import Any
from pydantic import PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.constants import Environment


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DATABASE_URL: PostgresDsn
    DATABASE_ASYNC_URL: PostgresDsn
    DATABASE_POOL_SIZE: int = 5
    DATABASE_POOL_TTL: int = 300

    ENVIRONMENT: Environment = Environment.PRODUCTION

    CORS_ORIGINS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]

    SENTRY_DSN: str | None = None
    SHOW_DOCS: bool = True

    @model_validator(mode="after")
    def validate_sentry_non_local(self) -> "Config":
        if self.ENVIRONMENT.is_deployed and not self.SENTRY_DSN:
            raise ValueError("Sentry is not set")
        return self


settings = Config()

app_configs: dict[str, Any] = {"title": "Fishes API"}

if not settings.SHOW_DOCS:
    app_configs["openapi_url"] = None