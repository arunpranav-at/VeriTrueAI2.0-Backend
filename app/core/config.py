import os
from typing import Optional

# Uncomment this when using Secret Manager (requires billing)
# from google.cloud import secretmanager


# def get_secret(secret_name: str, project_id: str = None) -> Optional[str]:
#     """Get secret from Google Secret Manager."""
#     try:
#         if not project_id:
#             project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "veritrueai")
        
#         client = secretmanager.SecretManagerServiceClient()
#         secret_path = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
#         response = client.access_secret_version(request={"name": secret_path})
#         return response.payload.data.decode("UTF-8")
#     except Exception as e:
#         print(f"Failed to get secret {secret_name}: {e}")
#         return None


class Settings:
    """Application settings and configuration."""
    
    def __init__(self):
        # API Configuration
        self.API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME", "VeriTrueAI2.0")
        self.DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        
        # Google Cloud Configuration
        self.GOOGLE_CLOUD_PROJECT_ID: Optional[str] = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        # Database Configuration
        self.DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
        
        # Redis Configuration
        self.REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        
        # Gemini AI Configuration
        self.GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-pro")
        
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