# air_quality_app/app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    # Model configuration for loading settings
    # This tells PydanticSettings to look for a .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # FastAPI application settings
    APP_NAME: str = "Air Quality Monitoring & Prediction API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False # Set to True for development, False for production

    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str | None = None # Will be constructed later

    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # External API Keys (from .env)
    OPENAQ_API_KEY: str | None = None # OpenAQ typically doesn't require an API key for basic usage, but include for consistency
    OPENWEATHER_API_KEY: str
    MAPBOX_ACCESS_TOKEN: str

    # Firebase Admin SDK path (for authentication)
    FIREBASE_SERVICE_ACCOUNT_PATH: str = os.path.join(os.getcwd(), "firebase_service_account.json") # Default path

    # JWT settings (if not using Firebase Auth's session tokens directly)
    # SECRET_KEY: str = "super-secret-key" # Generate a strong one for production
    # ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


# Create a single instance of settings to be imported throughout your app
settings = Settings()

# Dynamically construct DATABASE_URL if not provided
if settings.DATABASE_URL is None:
    settings.DATABASE_URL = (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
        f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )