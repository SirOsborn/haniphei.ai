"""
AI Service Client for Backend Integration

Handles communication with the separate AI service running on port 8082.
Provides risk analysis by forwarding documents/text to the AI service.
"""

import httpx
from typing import Dict, List, Optional
import logging

from api.core.config import settings

logger = logging.getLogger(__name__)


class AIServiceClient:
    """Client for communicating with the AI service"""
    
    def __init__(self):
        self.base_url = settings.ai_service_url
        self.timeout = 60.0  # AI processing can take time
    
    async def scan_document(
        self,
        file_content: Optional[bytes] = None,
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
        text: Optional[str] = None,
        force_llm: bool = False
    ) -> Dict:
        """
        Send document or text to AI service for risk analysis.
        
        Args:
            file_content: Binary content of uploaded file
            filename: Original filename
            content_type: MIME type of file
            text: Plain text input (if no file)
            force_llm: Force use of LLM instead of local model
            
        Returns:
            Dict with structure:
            {
                "data": [
                    {
                        "risk": "...",
                        "category": "Financial|Schedule|...",
                        "context": "..."
                    }
                ],
                "source": "llm" | "model"
            }
            
        Raises:
            httpx.HTTPError: If AI service is unreachable or returns error
            httpx.TimeoutException: If processing takes longer than timeout
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Prepare multipart form data
                files = {}
                data = {}
                
                if file_content and filename:
                    # Upload file to AI service
                    files["file"] = (filename, file_content, content_type or "application/octet-stream")
                
                if text:
                    data["text"] = text
                
                if force_llm:
                    data["force_llm"] = "true"
                
                # Make request to AI service
                response = await client.post(
                    f"{self.base_url}/scan",
                    files=files if files else None,
                    data=data if data else None
                )
                
                response.raise_for_status()
                return response.json()
                
        except httpx.TimeoutException as e:
            logger.error(f"AI service timeout: {e}")
            raise TimeoutError(
                "AI service took too long to process the document. Please try with a smaller file."
            )
        except httpx.ConnectError as e:
            logger.error(f"AI service connection failed: {e}")
            raise ConnectionError(
                f"Could not connect to AI service at {self.base_url}. "
                "Please ensure the AI service is running."
            )
        except httpx.HTTPStatusError as e:
            logger.error(f"AI service returned error: {e.response.status_code} - {e.response.text}")
            raise ValueError(
                f"AI service error: {e.response.text}"
            )
        except Exception as e:
            logger.error(f"Unexpected error calling AI service: {e}")
            raise RuntimeError(
                f"Failed to analyze document: {str(e)}"
            )
    
    async def health_check(self) -> bool:
        """
        Check if AI service is running and responsive.
        
        Returns:
            bool: True if service is healthy, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"AI service health check failed: {e}")
            return False
    
    async def get_data_stats(self) -> Dict:
        """
        Get training data collection statistics from AI service.
        
        Returns:
            Dict with statistics about collected training data
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/data/stats")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to get AI service stats: {e}")
            return {}
    
    async def validate_data_quality(self) -> Dict:
        """
        Get data quality validation from AI service.
        
        Returns:
            Dict with validation results and recommendations
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/data/validate")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to validate AI service data: {e}")
            return {}
    
    async def train_model(self) -> Dict:
        """
        Trigger model training on AI service.
        
        Returns:
            Dict with training results (accuracy, f1_micro, meets_target)
        """
        try:
            async with httpx.AsyncClient(timeout=300.0) as client:  # Training can take time
                response = await client.post(f"{self.base_url}/train")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to train AI model: {e}")
            raise RuntimeError(f"Model training failed: {str(e)}")


# Global instance
ai_service = AIServiceClient()
