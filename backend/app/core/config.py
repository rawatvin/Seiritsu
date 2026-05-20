from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    app_name: str = "TaskIntelligence"
    app_version: str = "0.1.0"
    debug: bool = True
    secret_key: str

    # Database
    database_url: str
    database_pool_size: int = 20
    database_max_overflow: int = 0

    # Redis
    redis_url: str

    # Microsoft Azure AD
    microsoft_client_id: str
    microsoft_client_secret: str
    microsoft_tenant_id: str = "common"
    microsoft_redirect_uri: str
    microsoft_scopes: str

    @property
    def microsoft_scopes_list(self) -> List[str]:
        return [scope.strip() for scope in self.microsoft_scopes.split(",")]

    # Claude AI
    anthropic_api_key: str

    # Celery
    celery_broker_url: str
    celery_result_backend: str
    celery_task_interval_hours: int = 2

    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 10080  # 1 week

    # Learning System
    learning_enabled: bool = True
    learning_batch_size: int = 10
    learning_update_interval_hours: int = 24

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
