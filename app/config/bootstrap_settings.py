from __future__ import annotations

from pydantic_settings import BaseSettings


class BootstrapSettings(BaseSettings):
    ENV: str = "dev"

    # Valkey
    VALKEY_HOST: str
    VALKEY_PORT: int = 6379
    VALKEY_PASSWORD: str

    # Database
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


bootstrap_settings = BootstrapSettings()
