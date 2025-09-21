import os
from typing import Optional

try:
    from google.cloud import secretmanager
    SECRET_MANAGER_AVAILABLE = True
except ImportError:
    SECRET_MANAGER_AVAILABLE = False


def get_secret(secret_name: str, project_id: str = None) -> Optional[str]:
    """Get secret from Google Secret Manager."""
    try:
        if not SECRET_MANAGER_AVAILABLE:
            print("Google Secret Manager SDK not available. Install google-cloud-secret-manager")
            return None
            
        if not project_id:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "veritrueai")
        
        client = secretmanager.SecretManagerServiceClient()
        secret_path = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": secret_path})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Failed to get secret {secret_name}: {e}")
        return None


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
        
        # Gemini AI Configuration - Secure secrets from Secret Manager
        self.GEMINI_API_KEY: Optional[str] = self._get_secret_or_env("GEMINI_API_KEY")
        self.GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-pro")
        
        # File Upload Configuration
        self.MAX_UPLOAD_SIZE: str = os.getenv("MAX_UPLOAD_SIZE", "50MB")
        self.UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
        
        # Web Search Configuration - Secure secrets from Secret Manager
        self.SEARCH_API_KEY: Optional[str] = self._get_secret_or_env("SEARCH_API_KEY")
        self.SEARCH_ENGINE_ID: Optional[str] = self._get_secret_or_env("SEARCH_ENGINE_ID")
        
        # Security - Secure secret from Secret Manager
        self.SECRET_KEY: str = self._get_secret_or_env("SECRET_KEY") or "your-secret-key-change-this-in-production"
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    def _get_secret_or_env(self, key: str) -> Optional[str]:
        """Try to get value from Secret Manager first, fallback to environment variable."""
        # First try environment variable (for local development)
        env_value = os.getenv(key)
        if env_value:
            return env_value
            
        # Try Secret Manager (for production)
        return get_secret(key, self.GOOGLE_CLOUD_PROJECT_ID)


settings = Settings()