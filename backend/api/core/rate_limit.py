from fastapi import Request, HTTPException, status
from datetime import datetime, timedelta
from typing import Dict
import time

# In-memory rate limit store (use Redis in production)
rate_limit_store: Dict[str, list] = {}

def rate_limit(max_requests: int = 100, window_seconds: int = 60):
    """
    Rate limiting decorator
    
    Args:
        max_requests: Maximum requests allowed in the time window
        window_seconds: Time window in seconds
    """
    async def limiter(request: Request):
        # Get client identifier (IP + User ID if authenticated)
        client_id = request.client.host
        
        # Add user ID if authenticated
        if hasattr(request.state, 'user'):
            client_id = f"{client_id}:{request.state.user.id}"
        
        current_time = time.time()
        
        # Initialize or get request history
        if client_id not in rate_limit_store:
            rate_limit_store[client_id] = []
        
        # Remove old requests outside the window
        rate_limit_store[client_id] = [
            req_time for req_time in rate_limit_store[client_id]
            if current_time - req_time < window_seconds
        ]
        
        # Check if limit exceeded
        if len(rate_limit_store[client_id]) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {max_requests} requests per {window_seconds} seconds."
            )
        
        # Add current request
        rate_limit_store[client_id].append(current_time)
    
    return limiter

# Specific rate limiters
async def upload_rate_limit(request: Request):
    """Strict limit for file uploads: 10 per minute"""
    return await rate_limit(max_requests=10, window_seconds=60)(request)

async def auth_rate_limit(request: Request):
    """Strict limit for authentication: 5 per minute"""
    return await rate_limit(max_requests=5, window_seconds=60)(request)