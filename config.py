import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    ENVIRONMENT: str = "production"
    PROJECT_NAME: str = "VINCER Research Assistant"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()