import re
from fastapi import HTTPException, status

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks
    """
    # Remove path separators
    filename = filename.replace('/', '_').replace('\\', '_')
    
    # Remove special characters except dots, dashes, underscores
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    
    # Prevent double extensions (.pdf.exe)
    filename = re.sub(r'\.+', '.', filename)
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:250] + ('.' + ext if ext else '')
    
    # Prevent hidden files
    if filename.startswith('.'):
        filename = 'file' + filename
    
    return filename

def validate_source_parameter(source: str) -> bool:
    """Validate source parameter is one of allowed values"""
    allowed_sources = ['camera', 'file_picker', 'gallery']
    return source in allowed_sources