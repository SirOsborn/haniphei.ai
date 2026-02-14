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
    """Extract text from PDF. Supports native text and OCR for scanned PDFs."""
    text = []
    with fitz.open(stream=content, filetype="pdf") as doc:
        for page in doc:
            page_text = page.get_text()
            
            # If page has no text (scanned PDF), perform OCR
            if not page_text.strip():
                try:
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    _ensure_tesseract_config()
                    page_text = pytesseract.image_to_string(img, lang=settings.tesseract_lang)
                except Exception as e:
                    print(f"Warning: OCR failed for PDF page, skipping. Error: {e}")
                    page_text = ""
            
            text.append(page_text)
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
    """Extract text from image using OCR with Khmer + English support."""
    _ensure_tesseract_config()
    import io
    img = Image.open(io.BytesIO(content))
    
    # Use configured language (default: eng+khm for bilingual support)
    try:
        return pytesseract.image_to_string(img, lang=settings.tesseract_lang)
    except pytesseract.TesseractError as e:
        # Fallback to English only if Khmer language data not found
        if 'khm' in settings.tesseract_lang.lower() and 'eng' in settings.tesseract_lang.lower():
            print(f"Warning: Khmer language data not found, falling back to English only. Error: {e}")
            return pytesseract.image_to_string(img, lang='eng')
        raise