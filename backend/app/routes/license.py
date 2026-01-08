"""
License Management API Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from ..services.license_service import (
    create_license, validate_license, get_license_info,
    upgrade_license, extend_license, check_feature_access,
    LicenseType, get_days_remaining
)

router = APIRouter()

class LicenseCreateRequest(BaseModel):
    email: EmailStr
    license_type: str = "free_trial"
    duration_days: int = 14

class LicenseValidateRequest(BaseModel):
    license_key: str

class LicenseUpgradeRequest(BaseModel):
    license_key: str
    new_type: str
    duration_days: int = 30

class FeatureCheckRequest(BaseModel):
    license_key: str
    feature: str

@router.post("/license/create")
async def create_new_license(request: LicenseCreateRequest):
    """Create a new license (e.g., when user signs up for trial or subscription)"""
    try:
        # Convert string to enum
        license_type = LicenseType(request.license_type)
        
        license = create_license(
            email=request.email,
            license_type=license_type,
            duration_days=request.duration_days
        )
        
        return {
            "success": True,
            "license_key": license.license_key,
            "license_type": license.license_type.value,
            "end_date": license.end_date.isoformat(),
            "message": f"License created successfully. Valid for {request.duration_days} days."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid license type: {request.license_type}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/license/validate")
async def validate_license_key(request: LicenseValidateRequest):
    """Validate a license key and return its status"""
    is_valid, license, message = validate_license(request.license_key)
    
    if not license:
        raise HTTPException(status_code=404, detail="License not found")
    
    return {
        "valid": is_valid,
        "license_type": license.license_type.value,
        "message": message,
        "days_remaining": get_days_remaining(request.license_key) if is_valid else 0,
        "features": {
            "max_students": license.max_students,
            "max_lessons": license.features.max_lessons,
            "teacher_dashboard": license.features.teacher_dashboard,
            "analytics": license.features.analytics
        }
    }

@router.get("/license/info/{license_key}")
async def get_license_details(license_key: str):
    """Get detailed information about a license"""
    info = get_license_info(license_key)
    
    if not info:
        raise HTTPException(status_code=404, detail="License not found")
    
    return info

@router.post("/license/upgrade")
async def upgrade_license_tier(request: LicenseUpgradeRequest):
    """Upgrade a license to a higher tier"""
    try:
        new_type = LicenseType(request.new_type)
        license = upgrade_license(request.license_key, new_type, request.duration_days)
        
        if not license:
            raise HTTPException(status_code=404, detail="License not found")
        
        return {
            "success": True,
            "license_type": license.license_type.value,
            "end_date": license.end_date.isoformat(),
            "message": f"License upgraded to {new_type.value}"
        }
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid license type: {request.new_type}")

@router.post("/license/extend")
async def extend_license_duration(license_key: str, days: int):
    """Extend the duration of an existing license"""
    license = extend_license(license_key, days)
    
    if not license:
        raise HTTPException(status_code=404, detail="License not found")
    
    return {
        "success": True,
        "end_date": license.end_date.isoformat(),
        "message": f"License extended by {days} days"
    }

@router.post("/license/check-feature")
async def check_feature(request: FeatureCheckRequest):
    """Check if a license has access to a specific feature"""
    has_access = check_feature_access(request.license_key, request.feature)
    
    return {
        "feature": request.feature,
        "has_access": has_access
    }

@router.get("/license/trial")
async def start_free_trial(email: EmailStr):
    """Quick endpoint to start a free trial"""
    license = create_license(email=email, license_type=LicenseType.FREE_TRIAL, duration_days=14)
    
    return {
        "success": True,
        "license_key": license.license_key,
        "message": "14-day free trial activated!",
        "instructions": "Save this license key to continue using the app after your session."
    }
