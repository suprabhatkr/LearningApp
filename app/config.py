import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "Ascend - Senior SDE Learn Hub"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "127.0.0.1"

    # JWT Authentication
    SECRET_KEY: str = "SUPER_SECRET_KEY_FOR_JWT_SIGNING_SENIOR_SDE_PREP_12345!"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # PostgreSQL Configuration
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5433)
    POSTGRES_DB: str = Field(default="ascend_learning")
    
    # SQLite fallback
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./ascend_learning.db")

    # Redis Configuration
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_PASSWORD: str | None = Field(default=None)

    # Elasticsearch Configuration
    ELASTICSEARCH_HOST: str = Field(default="http://localhost:9200")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def get_postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
