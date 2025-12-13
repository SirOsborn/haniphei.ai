from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "RiskSkanner.ai API"
    ai_service_url: str = "http://localhost:8001" # Example URL for the AI service

    class Config:
        env_file = ".env"

settings = Settings()
