"""
Configuration for AI-Interactive Book Backend
"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AI-Interactive Book Backend"
    version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Qdrant configuration
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")

    # OpenAI configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    # Database configuration
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

    class Config:
        env_file = ".env"

settings = Settings()