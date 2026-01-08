"""
CAPTCHA Integration Service
Support for Google reCAPTCHA v3 and hCaptcha
"""
from fastapi import HTTPException, status
import httpx
import os
from typing import Optional

# CAPTCHA Configuration
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY", "")
RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
RECAPTCHA_MIN_SCORE = 0.5  # reCAPTCHA v3 score threshold (0.0-1.0)

HCAPTCHA_SECRET_KEY = os.getenv("HCAPTCHA_SECRET_KEY", "")
HCAPTCHA_VERIFY_URL = "https://hcaptcha.com/siteverify"

async def verify_recaptcha(token: str, action: str = "login") -> bool:
    """
    Verify Google reCAPTCHA v3 token
    
    Args:
        token: reCAPTCHA response token from client
        action: Expected action name (login, register, etc.)
        
    Returns:
        True if verification passed
        
    Raises:
        HTTPException: If verification failed
    """
    if not RECAPTCHA_SECRET_KEY:
        # Skip in development if not configured
        return True
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                RECAPTCHA_VERIFY_URL,
                data={
                    "secret": RECAPTCHA_SECRET_KEY,
                    "response": token
                }
            )
            
            result = response.json()
            
            if not result.get("success"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CAPTCHA verification failed"
                )
            
            # Check score (v3 only)
            score = result.get("score", 0)
            if score < RECAPTCHA_MIN_SCORE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Bot activity detected"
                )
            
            # Verify action matches
            if result.get("action") != action:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid CAPTCHA action"
                )
            
            return True
            
        except httpx.RequestError:
            # Allow requests to pass if CAPTCHA service is down (fail open)
            # In production, consider failing closed for security
            return True

async def verify_hcaptcha(token: str) -> bool:
    """
    Verify hCaptcha token
    
    Args:
        token: hCaptcha response token from client
        
    Returns:
        True if verification passed
        
    Raises:
        HTTPException: If verification failed
    """
    if not HCAPTCHA_SECRET_KEY:
        # Skip in development if not configured
        return True
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                HCAPTCHA_VERIFY_URL,
                data={
                    "secret": HCAPTCHA_SECRET_KEY,
                    "response": token
                }
            )
            
            result = response.json()
            
            if not result.get("success"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CAPTCHA verification failed"
                )
            
            return True
            
        except httpx.RequestError:
            # Fail open if service is down
            return True

def get_captcha_config() -> dict:
    """
    Get CAPTCHA configuration for frontend
    
    Returns:
        Dictionary with CAPTCHA settings
    """
    return {
        "enabled": bool(RECAPTCHA_SECRET_KEY or HCAPTCHA_SECRET_KEY),
        "provider": "recaptcha" if RECAPTCHA_SECRET_KEY else "hcaptcha" if HCAPTCHA_SECRET_KEY else None,
        "site_key": os.getenv("RECAPTCHA_SITE_KEY", "") or os.getenv("HCAPTCHA_SITE_KEY", "")
    }
