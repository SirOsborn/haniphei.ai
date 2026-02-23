from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
import logging

from api.db.tables import User
from api.core.database import get_db
from api.core.auth import get_current_user
from api.services.ai_service import ai_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/scan")
async def scan_document(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    force_llm: Optional[bool] = Form(False),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze document or text for hidden risks and potential dangers.
    
    Accepts either:
    - file: PDF, DOCX, or image file (scanned Khmer/English contracts)
    - text: Plain text input for analysis
    
    Returns risk analysis with categories: Financial, Schedule, Technical,
    Legal, Operational, Compliance, Other
    
    Supports both Khmer (ភាសាខ្មែរ) and English documents.
    """
    # Validate input
    if not file and not text:
        raise HTTPException(
            status_code=400,
            detail="No file or text provided. Please provide either a file or text for analysis."
        )
    
    try:
        # Prepare data for AI service
        file_content = None
        filename = None
        content_type = None
        
        if file:
            # Read file content
            file_content = await file.read()
            filename = file.filename
            content_type = file.content_type
            
            # Validate file size (basic check)
            if len(file_content) == 0:
                raise HTTPException(status_code=400, detail="Uploaded file is empty")
            
            logger.info(
                f"User {current_user.email} scanning file: {filename} "
                f"({content_type}, {len(file_content)} bytes)"
            )
        else:
            logger.info(f"User {current_user.email} scanning text ({len(text)} chars)")
        
        # Call AI service for risk analysis
        result = await ai_service.scan_document(
            file_content=file_content,
            filename=filename,
            content_type=content_type,
            text=text,
            force_llm=force_llm
        )
        
        # Extract risks and source
        risks = result.get("data", [])
        source = result.get("source", "unknown")
        
        logger.info(
            f"AI service returned {len(risks)} risks from {source} "
            f"for user {current_user.email}"
        )
        
        # Return analysis results
        return {
            "scan_id": None,  # TODO: Save to database and return actual ID
            "user_id": str(current_user.id),
            "timestamp": datetime.utcnow().isoformat(),
            "filename": filename,
            "source": source,
            "risks": risks,
            "risk_count": len(risks),
            "categories": list(set(r.get("category", "Other") for r in risks))
        }
        
    except TimeoutError as e:
        logger.error(f"AI service timeout for user {current_user.email}: {e}")
        raise HTTPException(
            status_code=504,
            detail="Document analysis timed out. Please try with a smaller file or simpler text."
        )
    
    except ConnectionError as e:
        logger.error(f"AI service connection error: {e}")
        raise HTTPException(
            status_code=503,
            detail="AI analysis service is currently unavailable. Please try again later."
        )
    
    except ValueError as e:
        logger.error(f"AI service validation error: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    except Exception as e:
        logger.error(f"Unexpected error during scan: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during document analysis."
        )


@router.get("/health")
async def check_ai_service_health():
    """Check if AI service is running and responsive (no auth required for testing)."""
    is_healthy = await ai_service.health_check()
    
    return {
        "ai_service_healthy": is_healthy,
        "ai_service_url": ai_service.base_url,
        "status": "ok" if is_healthy else "unavailable"
    }
