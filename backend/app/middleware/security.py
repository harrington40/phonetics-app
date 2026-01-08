"""
Security Middleware
Rate limiting, input sanitization, and security headers
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import bleach
from typing import Optional
import re

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# HTML sanitization configuration
ALLOWED_TAGS = ['b', 'i', 'u', 'em', 'strong', 'p', 'br']
ALLOWED_ATTRIBUTES = {}

def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent XSS attacks
    
    Args:
        text: User input string
        
    Returns:
        Sanitized string with HTML tags removed
    """
    if not text:
        return text
    
    # Remove all HTML tags except allowed ones
    cleaned = bleach.clean(
        text,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
    
    return cleaned

def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email format
        
    Raises:
        HTTPException: If email format is invalid
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    return True

def sanitize_dict(data: dict) -> dict:
    """
    Recursively sanitize all string values in a dictionary
    
    Args:
        data: Dictionary to sanitize
        
    Returns:
        Sanitized dictionary
    """
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            sanitized[key] = sanitize_input(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value)
        elif isinstance(value, list):
            sanitized[key] = [
                sanitize_input(item) if isinstance(item, str) else item
                for item in value
            ]
        else:
            sanitized[key] = value
    return sanitized

async def validate_request_size(request: Request, max_size: int = 10 * 1024 * 1024):
    """
    Validate request body size to prevent DoS attacks
    
    Args:
        request: FastAPI request object
        max_size: Maximum allowed size in bytes (default 10MB)
        
    Raises:
        HTTPException: If request is too large
    """
    content_length = request.headers.get('content-length')
    if content_length and int(content_length) > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Request body too large. Maximum size is {max_size / 1024 / 1024}MB"
        )

def add_security_headers(response: JSONResponse) -> JSONResponse:
    """
    Add security headers to response
    
    Args:
        response: FastAPI response object
        
    Returns:
        Response with security headers added
    """
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# Rate limit configurations by endpoint type
RATE_LIMITS = {
    "auth": "5/minute",      # Login/register attempts
    "api": "100/minute",     # General API calls
    "payment": "10/minute",  # Payment operations
    "admin": "50/minute"     # Admin operations
}
