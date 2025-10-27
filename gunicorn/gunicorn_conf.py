from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    host: str = "0.0.0.0"
    port: int = 8000
    bind: str | None = None

    workers: int = 2
    graceful_timeout: int = 30
    timeout: int = 60
    keepalive: int = 5
    log_level: str = "INFO"
    log_config: str = "/src/logging_prod.ini"

    @property
    def computed_bind(self) -> str:
        return self.bind or f"{self.host}:{self.port}"


settings = Settings()

# Gunicorn config
loglevel = settings.log_level
workers = settings.workers
bind = settings.computed_bind
graceful_timeout = settings.graceful_timeout
timeout = settings.timeout
keepalive = settings.keepalive
logconfig = settings.log_config