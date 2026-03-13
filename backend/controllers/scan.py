from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime, timezone
import logging
import hashlib
import uuid

logger = logging.getLogger(__name__)

from db.tables import User, Document, Analysis
from core.database import get_db
from core.auth import get_current_user
from core.config import settings

# Local AI services
from services.ocr import extract_text
from services.pipeline import analyze_text
from services.data_collector import collector
from services.data_validator import validator
from services.trainer import train_model as local_train_model

# ============================================================================
# SCAN DOCUMENT - Core AI Analysis Logic
# ============================================================================
async def scan_document_logic(
    file: Optional[UploadFile],
    text: Optional[str],
    force_llm: bool,
    db: AsyncSession,
    current_user: User
):
    """
    Analyze document or text for hidden risks locally in the backend logic.
    """
    if not file and not text:
        raise HTTPException(
            status_code=400,
            detail="No file or text provided."
        )
    
    try:
        # 1. Extraction
        file_content = None
        filename = None
        file_hash = None
        
        if file:
            file_content = await file.read()
            filename = file.filename
            file_hash = hashlib.md5(file_content).hexdigest()
            # Reset file pointer for extract_text
            file.file.seek(0)
            extracted_text = await extract_text(file=file)
            logger.info(f"User {current_user.email} scanning file: {filename}")
        else:
            extracted_text = text
            logger.info(f"User {current_user.email} scanning text input")

        if not extracted_text:
             raise HTTPException(status_code=400, detail="Could not extract text for analysis.")

        # 2. Local AI Pipeline Analysis
        result = await analyze_text(
            text=extracted_text,
            force_llm=force_llm,
            filename=filename,
            file_hash=file_hash
        )
        
        risks = result.get("data", [])
        source = result.get("source", "unknown")
        
        # 3. Persistence: Save scan record
        try:
            # Create a virtual document record for the scan
            doc_id = str(uuid.uuid4())
            new_doc = Document(
                id=doc_id,
                user_id=current_user.id,
                filename=filename or "Text Scan",
                original_filename=filename or "direct_text_input",
                file_type="pdf" if (filename and filename.endswith('.pdf')) else "docx" if (filename and filename.endswith('.docx')) else "text",
                file_size=len(file_content) if file_content else (len(text.encode()) if text else 0),
                s3_key=f"scans/{current_user.id}/{doc_id}", # Placeholder key
                source="file_picker" if file else "text_input"
            )
            db.add(new_doc)
            
            # Save Analysis results
            analysis = Analysis(
                id=str(uuid.uuid4()),
                document_id=doc_id,
                data=risks,
                source=source
            )
            db.add(analysis)
            await db.commit()
            scan_id = doc_id
        except Exception as db_err:
            logger.error(f"Failed to save scan results to DB: {db_err}")
            await db.rollback()
            scan_id = None

        # 4. Formulate Response
        return {
            "scan_id": scan_id,
            "user_id": str(current_user.id),
            "timestamp": datetime.utcnow().isoformat(),
            "filename": filename or "Text Scan",
            "source": source,
            "risks": risks,
            "risk_count": len(risks),
            "categories": list(set(r.get("category", "Other") for r in risks))
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during integrated scan logic: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during analysis: {str(e)}"
        )

# ============================================================================
# AI INFRASTRUCTURE & DATA MANAGEMENT
# ============================================================================
async def ai_health_logic():
    """Verify built-in AI capabilities are responsive."""
    return {
        "status": "ok",
        "integrated": True,
        "llm_provider": settings.llm_provider
    }

async def data_statistics_logic():
    """Get training data statistics (Internal)."""
    return collector.get_statistics()

async def validate_data_logic():
    """Validate training data quality."""
    return validator.validate_dataset()

async def train_logic():
    """Train local model using collected data."""
    acc, f1 = local_train_model()
    return {
        "accuracy": acc, 
        "f1_micro": f1, 
        "meets_target": acc >= settings.accuracy_target
    }
