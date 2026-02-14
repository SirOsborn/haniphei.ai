import magic
import hashlib
from fastapi import HTTPException, status
from typing import Tuple

def validate_file_content(content: bytes, declared_type: str) -> Tuple[bool, str]:
    """
    Validate file content matches declared MIME type
    Prevents malicious files disguised as safe types
    
    Returns: (is_valid, actual_mime_type)
    """
    try:
        # Use python-magic to detect actual file type
        mime = magic.Magic(mime=True)
        actual_mime_type = mime.from_buffer(content)
        
        # Map of allowed declared types to actual types
        allowed_mappings = {
            'application/pdf': ['application/pdf'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': [
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/zip'  # DOCX is a zip file
            ],
            'image/jpeg': ['image/jpeg'],
            'image/jpg': ['image/jpeg'],
            'image/png': ['image/png']
        }
        
        # Check if actual type matches declared type
        if declared_type in allowed_mappings:
            if actual_mime_type in allowed_mappings[declared_type]:
                return True, actual_mime_type
        
        return False, actual_mime_type
        
    except Exception as e:
        # If validation fails, reject the file
        return False, "unknown"

def calculate_file_hash(content: bytes) -> str:
    """Calculate SHA-256 hash of file content"""
    return hashlib.sha256(content).hexdigest()

def scan_for_malicious_content(content: bytes) -> bool:
    """
    Basic malicious content detection
    Check for common malware signatures
    """
    # List of suspicious patterns (basic example)
    suspicious_patterns = [
        b'<script',  # JavaScript in files
        b'eval(',     # Eval in files
        b'system(',   # System calls
        b'exec(',     # Exec calls
    ]
    
    content_lower = content.lower()
    for pattern in suspicious_patterns:
        if pattern in content_lower:
            return True
    
    return False