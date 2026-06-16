from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Innova Content Agent API"
    app_env: str = "development"
    database_url: str = "sqlite:///./innova.db"
    jwt_secret: str = "development-only-secret-change-me-32"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    frontend_url: str = "http://127.0.0.1:3000"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    openai_image_model: str = "gpt-image-2"
    openai_image_quality: str = "medium"
    openai_image_size: str = "1024x1024"
    llm_provider: str = "mock"
    media_storage_dir: str = "storage/media"

    model_config = SettingsConfigDict(
        env_file=(".env", "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("llm_provider")
    @classmethod
    def validate_provider(cls, value: str) -> str:
        if value not in {"mock", "openai"}:
            raise ValueError("LLM_PROVIDER must be 'mock' or 'openai'")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
