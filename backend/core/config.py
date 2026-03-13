from pydantic import field_validator
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

    @field_validator("database_url", mode="before")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if v and v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    # JWT Authentication
    jwt_secret: str = "4e1de1bc9d9592bf0b54bffc8facd1a9"  # Default for dev
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Session Authentication
    session_secret_key: str
    session_cookie_name: str = "session"
    session_max_age: int = 1800  # 30 minutes in seconds
    session_cookie_secure: bool = False  # Set to True in production with HTTPS
    session_cookie_httponly: bool = True
    session_cookie_samesite: str = "lax"

    # AI Service Settings
    ai_service_url: str = "http://localhost:8082"
    use_llm: bool = True
    llm_provider: str = "gemini" # gemini or ollama
    gemini_api_key: Optional[str] = None
    gemini_model: str = "gemini-1.5-flash"
    groq_api_key: Optional[str] = None
    groq_model: str = "llama-3.3-70b-versatile"
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    accuracy_target: float = 0.85

    # OCR Settings
    tesseract_cmd: Optional[str] = None
    tesseract_lang: str = "eng+khm"

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

    @field_validator("cors_origins", mode="before")
    @classmethod
    def validate_cors_origins(cls, v):
        if isinstance(v, str):
            import json
            try:
                # Try to parse as JSON list: ["url1", "url2"]
                return json.loads(v)
            except json.JSONDecodeError:
                # Fallback to comma-separated: url1,url2
                return [i.strip() for i in v.split(",")]
        return v

    # Data directory for training and metadata
    data_dir: str = "backend/data"
    training_file: str = "backend/data/training.jsonl"
    model_file: str = "backend/models/model.joblib"
    metrics_file: str = "backend/data/metrics.json"


settings = Settings()
