from fastapi import APIRouter, File, UploadFile, Form
from typing import Optional

router = APIRouter()

@router.post("/scan")
async def scan_document(
    file: Optional[UploadFile] = File(None), 
    text: Optional[str] = Form(None)
):
    """
    Accepts a file (.docx, .pdf) or raw text for risk analysis.
    Gives precedence to the file if both are provided.
    """
    if file:
        # Placeholder for file processing logic
        content = await file.read()
        # In a real scenario, you would call the ai-service here
        return {"filename": file.filename, "content_type": file.content_type, "size": len(content)}
    
    if text:
        # Placeholder for text processing logic
        # In a real scenario, you would call the ai-service here
        return {"text_received": text}

    return {"error": "No file or text provided."}
