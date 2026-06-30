"""Typed application settings (pydantic-settings, reads ``.env``)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration. Env vars (or ``.env``) override the defaults.

    ``ANTHROPIC_API_KEY`` is optional: when unset, the demo entrypoint falls back
    to a direct tool call so the template still runs with no credentials.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    anthropic_api_key: str | None = None
    agent_model: str = "anthropic:claude-sonnet-4-6"


def load_settings() -> Settings:
    """Load settings from the environment / ``.env``."""
    return Settings()
