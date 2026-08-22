"""Application settings, read from environment variables or a .env file."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str
    jwt_secret: str
    jwt_issuer: str = "InvoicePortalAPI"
    jwt_expiry_hours: int = 8
    cors_allowed_origins: str = "http://localhost:4200"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached so the .env file is only read once."""
    settings = Settings()  # type: ignore[call-arg]

    if len(settings.jwt_secret) < 32:
        raise RuntimeError("JWT_SECRET must be at least 32 characters long.")

    return settings
