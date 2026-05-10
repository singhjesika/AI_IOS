"""
Application settings loaded from environment variables / .env file.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI_IOS"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Security
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./aiios.db"

    # LLM - Groq (free tier: https://console.groq.com)
    GROQ_API_KEY: str = ""
    DEFAULT_LLM_PROVIDER: str = "groq"
    # Free Groq models: llama3-8b-8192 | llama3-70b-8192 | mixtral-8x7b-32768 | gemma2-9b-it
    DEFAULT_MODEL: str = "llama3-8b-8192"

    # External APIs
    WEATHER_API_KEY: str = ""
    NEWS_API_KEY: str = ""
    FINANCE_API_KEY: str = ""
    GOOGLE_MAPS_API_KEY: str = ""

    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8501"]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()