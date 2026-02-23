import os
import hashlib
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

# Support both package and module execution
try:
    from .ocr import extract_text
    from .pipeline import analyze_text
    from .trainer import train_model
    from .config import settings
    from .data_collector import collector
    from .data_validator import validator
except ImportError:
    from ocr import extract_text
    from pipeline import analyze_text
    from trainer import train_model
    from config import settings
    from data_collector import collector
    from data_validator import validator

app = FastAPI(
    title="Haniphei.ai - AI Service",
    description="Risk analysis service for legal documents (Khmer & English)",
    version="1.0.0"
)

# Enable CORS for backend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",  # Backend development
        "http://localhost:5173",  # Frontend development  
        "http://localhost:3000",  # Alternative frontend port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    - Automatically collects training data with comprehensive metadata.
    """
    # Extract text from file or use provided text
    extracted = await extract_text(file=file, text=text)
    
    # Compute file hash if file was provided (for deduplication)
    file_hash = None
    filename = None
    if file:
        filename = file.filename
        # Read file content for hashing
        await file.seek(0)  # Reset file pointer
        file_content = await file.read()
        file_hash = hashlib.sha256(file_content).hexdigest()
        await file.seek(0)  # Reset again for potential re-reading
    
    # Analyze text with enhanced metadata
    result = await analyze_text(
        extracted, 
        force_llm=force_llm,
        filename=filename,
        file_hash=file_hash,
    )
    
    return result


@app.get("/data/stats")
async def data_statistics():
    """Get comprehensive statistics about collected training data."""
    stats = collector.get_statistics()
    return stats


@app.get("/data/validate")
async def validate_data():
    """Validate training data quality and get recommendations."""
    results = validator.validate_dataset()
    return results


@app.get("/data/quality-issues")
async def quality_issues():
    """Identify specific low-quality samples in the dataset."""
    issues = validator.identify_low_quality_samples()
    return {
        "total_issues": len(issues),
        "issues": issues[:50],  # Limit to first 50 for performance
    }


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
