import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env file
load_dotenv()


@dataclass
class Settings:
    # LLM provider: 'ollama' (local) or 'gemini' (cloud)
    llm_provider: str = os.getenv("LLM_PROVIDER", "gemini")

    # Google Gemini (cloud, free tier)
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    # Ollama (local, completely free)
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434")

    # Hybrid controls
    use_llm: bool = os.getenv("USE_LLM", "true").lower() == "true"
    accuracy_target: float = float(os.getenv("ACCURACY_TARGET", "0.85"))

    # Paths (use absolute paths based on script location)
    base_dir: str = os.path.dirname(os.path.abspath(__file__))
    data_dir: str = os.getenv("AI_DATA_DIR", os.path.join(base_dir, "data"))
    models_dir: str = os.getenv("AI_MODELS_DIR", os.path.join(base_dir, "models"))
    training_file: str = os.path.join(data_dir, "training.jsonl")
    metrics_file: str = os.path.join(models_dir, "metrics.json")
    model_file: str = os.path.join(models_dir, "risk_model.joblib")

    # OCR
    tesseract_cmd: str = os.getenv("TESSERACT_CMD", "")
    # OCR Language support: 'eng' for English only, 'eng+khm' for English + Khmer
    tesseract_lang: str = os.getenv("TESSERACT_LANG", "eng+khm")


settings = Settings()

# Ensure folders exist
os.makedirs(settings.data_dir, exist_ok=True)
os.makedirs(settings.models_dir, exist_ok=True)