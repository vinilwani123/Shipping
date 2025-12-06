from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings"""
    
    # Database Configuration
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/shipping_poc"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:8501",  # Streamlit default port
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Application Settings
    APP_NAME: str = "Shipping POC API"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
