from typing import Optional
import os

from fastapi import UploadFile

from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import docx

# Support both package and module execution
try:
    from .config import settings
except ImportError:
    from config import settings


def _ensure_tesseract_config():
    if settings.tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd


async def extract_text(file: Optional[UploadFile] = None, text: Optional[str] = None) -> str:
    """
    Return text from provided `text` or perform OCR/extraction from `file`.
    Supports: .pdf, .docx, image formats (png/jpg/jpeg), and plain text.
    """
    if text:
        return text

    if not file:
        return ""

    filename = (file.filename or "").lower()
    content = await file.read()

    if filename.endswith(".pdf"):
        return _extract_pdf_bytes(content)
    if filename.endswith(".docx"):
        return _extract_docx_bytes(content)
    if any(filename.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]):
        return _extract_image_bytes(content)

    # Fallback: try decoding as text
    try:
        return content.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def _extract_pdf_bytes(content: bytes) -> str:
    text = []
    with fitz.open(stream=content, filetype="pdf") as doc:
        for page in doc:
            text.append(page.get_text())
    return "\n".join(text)


def _extract_docx_bytes(content: bytes) -> str:
    # Write to a temp file since python-docx expects a path or file-like object
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    try:
        d = docx.Document(tmp_path)
        return "\n".join([p.text for p in d.paragraphs])
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass


def _extract_image_bytes(content: bytes) -> str:
    _ensure_tesseract_config()
    import io
    img = Image.open(io.BytesIO(content))
    return pytesseract.image_to_string(img)