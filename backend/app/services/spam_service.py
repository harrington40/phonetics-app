"""
Anti-Spam Service
Email verification, honeypot detection, and bot prevention
"""
from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
import hashlib
from typing import Optional
import re

from ..db.models import User

# Spam detection configuration
SPAM_PATTERNS = [
    r'viagra', r'casino', r'bitcoin', r'crypto', r'lottery',
    r'winner', r'congratulations', r'claim.*prize', r'click.*here',
    r'\[url\]', r'\[link\]', r'http.*http', r'www\..*www\.'
]

EMAIL_VERIFICATION_EXPIRE_HOURS = 24
MAX_REGISTRATIONS_PER_IP_PER_DAY = 100  # Increased for testing
MIN_TIME_BETWEEN_REGISTRATIONS = 0  # Disabled for testing

# In-memory storage (use Redis in production)
verification_codes = {}
registration_timestamps = {}

def generate_verification_code() -> str:
    """
    Generate a 6-digit verification code
    
    Returns:
        6-digit numeric code
    """
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

def generate_email_token(email: str) -> str:
    """
    Generate secure email verification token
    
    Args:
        email: User email address
        
    Returns:
        URL-safe verification token
    """
    token = secrets.token_urlsafe(32)
    verification_codes[token] = {
        'email': email,
        'code': generate_verification_code(),
        'expires': datetime.utcnow() + timedelta(hours=EMAIL_VERIFICATION_EXPIRE_HOURS)
    }
    return token

def verify_email_token(token: str) -> Optional[str]:
    """
    Verify email token and return email if valid
    
    Args:
        token: Email verification token
        
    Returns:
        Email address if token is valid, None otherwise
    """
    if token not in verification_codes:
        return None
    
    data = verification_codes[token]
    if datetime.utcnow() > data['expires']:
        del verification_codes[token]
        return None
    
    email = data['email']
    del verification_codes[token]
    return email

def check_honeypot(honeypot_field: Optional[str]) -> bool:
    """
    Check if honeypot field was filled (indicates bot)
    
    Args:
        honeypot_field: Value of hidden honeypot field
        
    Returns:
        True if likely spam, False if legitimate
        
    Raises:
        HTTPException: If bot detected
    """
    if honeypot_field:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Spam detected"
        )
    return False

def detect_spam_content(text: str) -> bool:
    """
    Check text for spam patterns
    
    Args:
        text: Text to check for spam
        
    Returns:
        True if spam detected
        
    Raises:
        HTTPException: If spam patterns found
    """
    if not text:
        return False
    
    text_lower = text.lower()
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, text_lower):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Content contains prohibited patterns"
            )
    
    return False

def check_registration_rate(request: Request) -> bool:
    """
    Check if IP address is registering too quickly
    
    Args:
        request: FastAPI request object
        
    Returns:
        True if rate limit passed
        
    Raises:
        HTTPException: If rate limit exceeded
    """
    client_ip = request.client.host
    current_time = datetime.utcnow()
    
    if client_ip not in registration_timestamps:
        registration_timestamps[client_ip] = []
    
    # Clean old timestamps (older than 24 hours)
    registration_timestamps[client_ip] = [
        ts for ts in registration_timestamps[client_ip]
        if current_time - ts < timedelta(days=1)
    ]
    
    # Check daily limit
    if len(registration_timestamps[client_ip]) >= MAX_REGISTRATIONS_PER_IP_PER_DAY:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Maximum {MAX_REGISTRATIONS_PER_IP_PER_DAY} registrations per day exceeded"
        )
    
    # Check minimum time between registrations
    if registration_timestamps[client_ip]:
        last_registration = registration_timestamps[client_ip][-1]
        if (current_time - last_registration).total_seconds() < MIN_TIME_BETWEEN_REGISTRATIONS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Please wait before registering again"
            )
    
    # Record this registration
    registration_timestamps[client_ip].append(current_time)
    return True

def detect_disposable_email(email: str) -> bool:
    """
    Check if email is from a disposable email service
    
    Args:
        email: Email address to check
        
    Returns:
        True if disposable email detected
        
    Raises:
        HTTPException: If disposable email detected
    """
    # Common disposable email domains
    disposable_domains = [
        'tempmail.com', '10minutemail.com', 'guerrillamail.com',
        'mailinator.com', 'throwaway.email', 'temp-mail.org',
        'fakeinbox.com', 'trashmail.com', 'yopmail.com'
    ]
    
    domain = email.split('@')[1].lower()
    if domain in disposable_domains:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Disposable email addresses are not allowed"
        )
    
    return False

def check_duplicate_registrations(email: str, db: Session) -> bool:
    """
    Check if email is already registered or recently attempted
    
    Args:
        email: Email to check
        db: Database session
        
    Returns:
        True if no duplicate found
        
    Raises:
        HTTPException: If duplicate found
    """
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return True

def validate_human_timing(registration_start_time: datetime) -> bool:
    """
    Check if registration was completed too quickly (bot behavior)
    
    Args:
        registration_start_time: When form was loaded
        
    Returns:
        True if timing is human-like
        
    Raises:
        HTTPException: If completed too quickly
    """
    time_taken = (datetime.utcnow() - registration_start_time).total_seconds()
    
    # Human users take at least 3 seconds to fill form
    if time_taken < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Form submitted too quickly"
        )
    
    # Suspiciously slow (form abandoned and submitted later)
    if time_taken > 1800:  # 30 minutes
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Form submission expired, please try again"
        )
    
    return True

def generate_registration_token() -> dict:
    """
    Generate anti-bot registration token
    
    Returns:
        Dictionary with token and timestamp
    """
    token = secrets.token_urlsafe(32)
    timestamp = datetime.utcnow()
    
    return {
        'token': token,
        'timestamp': timestamp.isoformat(),
        'hash': hashlib.sha256(f"{token}{timestamp}".encode()).hexdigest()
    }

def verify_registration_token(token: str, timestamp_str: str, provided_hash: str) -> bool:
    """
    Verify registration token to prevent form replay attacks
    
    Args:
        token: Registration token
        timestamp_str: ISO format timestamp
        provided_hash: Hash to verify
        
    Returns:
        True if token is valid
        
    Raises:
        HTTPException: If token is invalid
    """
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
        expected_hash = hashlib.sha256(f"{token}{timestamp}".encode()).hexdigest()
        
        if expected_hash != provided_hash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid registration token"
            )
        
        # Check if token is expired (30 minutes)
        if (datetime.utcnow() - timestamp).total_seconds() > 1800:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration token expired"
            )
        
        return True
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid registration data"
        )
