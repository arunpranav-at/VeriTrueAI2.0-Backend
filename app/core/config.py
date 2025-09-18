import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "VeriTrueAI2.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Database Configuration
    DATABASE_URL: Optional[str] = None
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = None
    
    # Google Cloud Configuration
    GOOGLE_CLOUD_PROJECT_ID: Optional[str] = None
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None
    
    # File Upload Configuration
    MAX_UPLOAD_SIZE: str = "50MB"
    UPLOAD_DIR: str = "./uploads"
    
    # Web Search Configuration
    SEARCH_API_KEY: Optional[str] = None
    SEARCH_ENGINE_ID: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()