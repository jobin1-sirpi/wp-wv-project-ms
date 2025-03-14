import warnings
from typing import List
import importlib.metadata
from pydantic_settings import BaseSettings, SettingsConfigDict


# Get the current version of the project from the package metadata
try:
    current_version = importlib.metadata.version("journal-api")
except Exception:
    current_version = "0.0.0"

# Configure Pydantic settings
warnings.filterwarnings("ignore", category=DeprecationWarning)


class Settings(BaseSettings):
    PROJECT_NAME: str = "WP-WV-PROJECT-MS"
    API_VERSION: str = current_version
    BASE_URL: str = "0.0.0.0"
    INSTANCE: str
    DATABASE_URL: str
    AUTH0_CLIENT_ID: str
    AUTH0_CLIENT_SECRET: str
    AUTH0_DOMAIN: str
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_USERNAME: str
    REDIS_PASSWORD: str
    ACCESS_TOKEN_MAX_AGE: int = 900
    REFRESH_TOKEN_MAX_AGE: int = 86400

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )


settings = Settings()
