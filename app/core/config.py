import os
from typing import Optional


class Settings:
    """Application settings and configuration."""
    
    def __init__(self):
        # API Configuration
        self.API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME", "VeriTrueAI2.0")
        self.DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        
        # Database Configuration
        self.DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
        
        # Redis Configuration
        self.REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        
        # OpenAI Configuration
        self.OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
        
        # Google Cloud Configuration
        self.GOOGLE_CLOUD_PROJECT_ID: Optional[str] = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        # File Upload Configuration
        self.MAX_UPLOAD_SIZE: str = os.getenv("MAX_UPLOAD_SIZE", "50MB")
        self.UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
        
        # Web Search Configuration
        self.SEARCH_API_KEY: Optional[str] = os.getenv("SEARCH_API_KEY")
        self.SEARCH_ENGINE_ID: Optional[str] = os.getenv("SEARCH_ENGINE_ID")
        
        # Security
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


settings = Settings()