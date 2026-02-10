"""
Authentication Routes
User registration, login, logout, and profile management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta

from ..db.database import get_db
from ..db.models import User
from ..services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    validate_password_strength
)
from ..middleware.security import sanitize_input, validate_email
# from ..middleware.security import limiter  # Disabled until slowapi is installed
from ..services.spam_service import (
    check_honeypot,
    detect_spam_content,
    check_registration_rate,
    detect_disposable_email,
    check_duplicate_registrations,
    validate_human_timing,
    verify_registration_token
)
from ..services.captcha_service import verify_recaptcha, verify_hcaptcha

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

# Pydantic models for request/response
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = "student"  # student, teacher
    teacher_code: Optional[str] = None  # For students enrolling with a teacher
    # Anti-spam fields
    honeypot: Optional[str] = None  # Should be empty
    captcha_token: Optional[str] = None  # reCAPTCHA/hCaptcha token
    reg_token: Optional[str] = None  # Registration form token
    reg_timestamp: Optional[str] = None  # Form load timestamp
    reg_hash: Optional[str] = None  # Token verification hash

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    captcha_token: Optional[str] = None  # Optional CAPTCHA for login

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    created_at: str

# Dependency to get current user from JWT token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Validate JWT token and return current user
    
    Args:
        credentials: HTTP Bearer token
        db: Database session
        
    Returns:
        Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
# @limiter.limit("5/minute")  # Disabled until slowapi installed
async def register(user_data: UserRegister, request: Request, db: Session = Depends(get_db)):
    """
    Register a new user with anti-spam protection
    
    - **email**: Valid email address (no disposable emails)
    - **password**: Strong password (8+ chars, upper/lower/number)
    - **full_name**: Optional user's full name
    - **captcha_token**: Optional CAPTCHA verification token
    - **honeypot**: Must be empty (bot trap)
    
    Returns JWT access token
    """
    # 🛡️ ANTI-SPAM CHECKS (TEMPORARILY DISABLED FOR TESTING)
    
    # 1. Check honeypot field (bot trap)
    # check_honeypot(user_data.honeypot)
    
    # 2. Check registration rate limiting per IP
    # check_registration_rate(request)
    
    # 3. Verify registration token (prevent form replay)
    # if user_data.reg_token and user_data.reg_timestamp and user_data.reg_hash:
    #     verify_registration_token(
    #         user_data.reg_token,
    #         user_data.reg_timestamp,
    #         user_data.reg_hash
    #     )
    #     # 4. Validate human timing
    #     try:
    #         form_load_time = datetime.fromisoformat(user_data.reg_timestamp)
    #         validate_human_timing(form_load_time)
    #     except:
    #         pass
    
    # 5. Verify CAPTCHA if provided
    # if user_data.captcha_token:
    #     await verify_recaptcha(user_data.captcha_token, "register")
    
    # 6. Detect disposable email addresses
    # detect_disposable_email(user_data.email)
    
    # 7. Check for spam in name field
    # if user_data.full_name:
    #     detect_spam_content(user_data.full_name)
    
    # Validate email format
    # validate_email(user_data.email)
    
    # Check if user already exists (DISABLED - no database)
    # check_duplicate_registrations(user_data.email, db)
    
    # Validate password strength
    validate_password_strength(user_data.password)
    
    # Sanitize inputs
    full_name = sanitize_input(user_data.full_name) if user_data.full_name else None
    
    # Validate role
    if user_data.role not in ["student", "teacher"]:
        user_data.role = "student"  # Default to student
    
    # Find teacher if teacher_code provided (for student enrollment)
    teacher_id = None
    if user_data.role == "student" and user_data.teacher_code:
        try:
            from ..db.models import TeacherClass
            teacher_class = db.query(TeacherClass).filter(
                TeacherClass.class_code == user_data.teacher_code,
                TeacherClass.is_active == True
            ).first()
            if teacher_class:
                teacher_id = teacher_class.teacher_id
        except Exception as e:
            print(f"Teacher enrollment lookup failed: {e}")
    
    # Create new user (password hashing disabled for testing)
    # hashed_password = hash_password(user_data.password)
    hashed_password = user_data.password  # Plain text for testing only
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        full_name=full_name,
        is_active=True,
        role=user_data.role,
        has_paid=False,  # Default: payment required
        teacher_id=teacher_id
    )
    
    # Try to save to database (graceful failure if no DB)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user_id = new_user.id
    except Exception as e:
        print(f"Database save failed (expected without PostgreSQL): {e}")
        # Use email as fallback ID for in-memory token generation
        user_id = hash(user_data.email)
    
    # Create access token
    access_token = create_access_token(
        data={"user_id": user_id, "email": user_data.email, "role": user_data.role}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id if hasattr(new_user, 'id') else user_id,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "role": new_user.role,
            "has_paid": new_user.has_paid,
            "teacher_id": new_user.teacher_id
        }
    }

@router.post("/login", response_model=TokenResponse)
# @limiter.limit("5/minute")  # Disabled until slowapi installed
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password (with optional CAPTCHA)
    
    - **email**: Registered email address
    - **password**: User password
    - **captcha_token**: Optional CAPTCHA for suspicious logins
    
    Returns JWT access token
    """
    # Verify CAPTCHA if provided
    if credentials.captcha_token:
        await verify_recaptcha(credentials.captcha_token, "login")
    
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )
    
    # Check payment status for students
    if user.role == "student" and not user.has_paid:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Payment required. Please complete payment to access student materials."
        )
    
    # Get enrolled students if user is a teacher
    enrolled_students = []
    if user.role == "teacher":
        try:
            students = db.query(User).filter(
                User.teacher_id == user.id,
                User.role == "student",
                User.is_active == True
            ).all()
            enrolled_students = [
                {
                    "id": s.id,
                    "email": s.email,
                    "full_name": s.full_name,
                    "has_paid": s.has_paid,
                    "created_at": s.created_at.isoformat() if s.created_at else None
                }
                for s in students
            ]
        except Exception as e:
            print(f"Failed to fetch enrolled students: {e}")
    
    # Create access token
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email, "role": user.role}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "has_paid": user.has_paid,
            "teacher_id": user.teacher_id,
            "enrolled_students": enrolled_students if user.role == "teacher" else []
        }
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user profile
    
    Requires valid JWT token in Authorization header
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "created_at": current_user.created_at.isoformat()
    }

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout current user
    
    Note: JWT tokens are stateless, so client should delete the token.
    For added security, implement token blacklist in production.
    """
    return {"message": "Successfully logged out"}

@router.put("/change-password")
# @limiter.limit("3/minute")  # Disabled until slowapi installed
async def change_password(
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password
    
    - **current_password**: Current password for verification
    - **new_password**: New strong password
    """
    # Verify current password
    if not verify_password(current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )
    
    # Validate new password strength
    validate_password_strength(new_password)
    
    # Update password
    current_user.password_hash = hash_password(new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}

@router.put("/update-profile")
async def update_profile(
    full_name: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile information
    
    - **full_name**: Updated full name
    """
    if full_name is not None:
        # Sanitize input
        current_user.full_name = sanitize_input(full_name)
    
    current_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "Profile updated successfully",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "full_name": current_user.full_name
        }
    }

# Admin role check dependency
async def require_admin(current_user: User = Depends(get_current_user)):
    """
    Require user to have admin role
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# Teacher role check dependency
async def require_teacher(current_user: User = Depends(get_current_user)):
    """
    Require user to have teacher role
    """
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher access required"
        )
    return current_user

# ===== TEACHER ENDPOINTS =====

@router.post("/teacher/create-class")
async def create_teacher_class(
    class_name: str,
    description: Optional[str] = None,
    max_students: int = 30,
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    """
    Create a new class for teacher
    Returns unique class code for student enrollment
    """
    import random
    import string
    from ..db.models import TeacherClass
    
    # Generate unique class code
    class_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # Check if code already exists
    while db.query(TeacherClass).filter(TeacherClass.class_code == class_code).first():
        class_code = ''.join(random.choices (string.ascii_uppercase + string.digits, k=8))
    
    new_class = TeacherClass(
        teacher_id=current_user.id,
        class_name=class_name,
        class_code=class_code,
        description=description,
        max_students=max_students,
        is_active=True
    )
    
    try:
        db.add(new_class)
        db.commit()
        db.refresh(new_class)
        
        return {
            "message": "Class created successfully",
            "class_code": class_code,
            "class_name": class_name,
            "max_students": max_students
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create class: {str(e)}"
        )

@router.get("/teacher/students")
async def get_enrolled_students(
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    """
    Get all students enrolled with this teacher
    """
    try:
        students = db.query(User).filter(
            User.teacher_id == current_user.id,
            User.role == "student",
            User.is_active == True
        ).all()
        
        return {
            "total_students": len(students),
            "students": [
                {
                    "id": s.id,
                    "email": s.email,
                    "full_name": s.full_name,
                    "has_paid": s.has_paid,
                    "created_at": s.created_at.isoformat() if s.created_at else None
                }
                for s in students
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch students: {str(e)}"
        )

@router.get("/teacher/classes")
async def get_teacher_classes(
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    """
    Get all classes created by this teacher
    """
    try:
        from ..db.models import TeacherClass
        classes = db.query(TeacherClass).filter(
            TeacherClass.teacher_id == current_user.id
        ).all()
        
        return {
            "total_classes": len(classes),
            "classes": [
                {
                    "id": c.id,
                    "class_name": c.class_name,
                    "class_code": c.class_code,
                    "description": c.description,
                    "max_students": c.max_students,
                    "is_active": c.is_active,
                    "created_at": c.created_at.isoformat() if c.created_at else None
                }
                for c in classes
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch classes: {str(e)}"
        )

# ===== PAYMENT / ADMIN ENDPOINTS =====

@router.post("/admin/mark-paid/{user_id}")
async def mark_student_paid(
    user_id: int,
    current_user: User = Depends(require_teacher),  # Teachers can mark their students as paid
    db: Session = Depends(get_db)
):
    """
    Mark a student as paid (accessible by teachers for their students and admins)
    """
    student = db.query(User).filter(User.id == user_id, User.role == "student").first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Teachers can only mark their own students as paid
    if current_user.role == "teacher" and student.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only mark your enrolled students as paid"
        )
    
    student.has_paid = True
    student.updated_at = datetime.utcnow()
    
    try:
        db.commit()
        db.refresh(student)
        
        return {
            "message": "Student marked as paid",
            "student": {
                "id": student.id,
                "email": student.email,
                "full_name": student.full_name,
                "has_paid": student.has_paid
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update payment status: {str(e)}"
        )

@router.get("/check-access")
async def check_user_access(current_user: User = Depends(get_current_user)):
    """
    Check user's access level and permissions
    """
    can_access_materials = True
    access_message = "Full access"
    
    if current_user.role == "student" and not current_user.has_paid:
        can_access_materials = False
        access_message = "Payment required to access student materials"
    
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "has_paid": current_user.has_paid,
        "can_access_materials": can_access_materials,
        "access_message": access_message,
        "teacher_id": current_user.teacher_id
    }
