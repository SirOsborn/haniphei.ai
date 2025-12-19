import os
from fastapi import FastAPI, File, UploadFile, Form
from typing import Optional

# Support both package and module execution
try:
    from .ocr import extract_text
    from .pipeline import analyze_text
    from .trainer import train_model
    from .config import settings
except ImportError:
    from ocr import extract_text
    from pipeline import analyze_text
    from trainer import train_model
    from config import settings

app = FastAPI()

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

@app.post("/scan")
async def scan(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    force_llm: Optional[bool] = Form(None),
):
    """
    Hybrid risk analysis:
    - If a file is provided, perform OCR/text extraction.
    - If `force_llm` is true, use the LLM regardless of local model status.
    - Otherwise, use the local model when available and LLM is disabled.
    """
    extracted = await extract_text(file=file, text=text)
    result = await analyze_text(extracted, force_llm=force_llm)
    return result

@app.get("/")
async def read_root():
    return {
        "service": "ai-service",
        "llm_provider": settings.llm_provider,
        "use_llm": settings.use_llm,
    }


@app.post("/train")
async def train():
    """Train the local model from accumulated LLM-labeled data."""
    acc, f1 = train_model()
    ready = acc >= settings.accuracy_target
    return {"accuracy": acc, "f1_micro": f1, "meets_target": ready}
