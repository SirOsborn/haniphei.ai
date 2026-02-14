from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    # Application
    app_name: str = "Haniphei.ai API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/haniphei"

    # Session Authentication
    session_secret_key: str = "your-secret-key-min-32-characters-change-in-production"
    session_cookie_name: str = "session"
    session_max_age: int = 1800  # 30 minutes in seconds
    session_cookie_secure: bool = False  # Set to True in production with HTTPS
    session_cookie_httponly: bool = True
    session_cookie_samesite: str = "lax"

    # AI Service
    ai_service_url: str = "http://localhost:8082"

    # S3/R2 Configuration
    s3_endpoint_url: Optional[str] = None  # For Cloudflare R2: https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com
    s3_access_key_id: str = ""
    s3_secret_access_key: str = ""
    s3_bucket_name: str = "haniphei-documents"
    s3_region: str = "auto"  # For R2, use "auto"; for AWS S3, use actual region

    # File Upload Configuration
    max_file_size: int = 10 * 1024 * 1024  # 10MB in bytes
    allowed_file_types: List[str] = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "image/jpeg",
        "image/jpg",
        "image/png"
    ]
    allowed_extensions: List[str] = [".pdf", ".docx", ".jpg", ".jpeg", ".png"]

    # CORS
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]


settings = Settings()
