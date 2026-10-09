"""Settings read from environment variables (prefix SAILPREP_)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SAILPREP_", env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://sailprep:sailprep@localhost:5432/sailprep"
    environment: str = "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
