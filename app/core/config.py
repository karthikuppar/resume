import os
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Resume Analyzer"
    OPENAI_API_KEY: Optional[str] = None
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/resume_db"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()