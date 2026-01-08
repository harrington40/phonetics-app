"""
License Management System for PhonicsLearn
"""
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Dict
from pydantic import BaseModel

class LicenseType(str, Enum):
    FREE_TRIAL = "free_trial"
    PARENT = "parent"
    TEACHER = "teacher"
    SCHOOL = "school"
    EXPIRED = "expired"

class LicenseFeatures(BaseModel):
    max_students: int
    max_lessons: int
    progress_tracking: bool
    teacher_dashboard: bool
    custom_lessons: bool
    analytics: bool
    priority_support: bool
    api_access: bool

class License(BaseModel):
    license_key: str
    license_type: LicenseType
    user_email: str
    start_date: datetime
    end_date: datetime
    is_active: bool
    max_students: int
    features: LicenseFeatures

# License tier definitions
LICENSE_TIERS = {
    LicenseType.FREE_TRIAL: LicenseFeatures(
        max_students=3,
        max_lessons=10,
        progress_tracking=True,
        teacher_dashboard=False,
        custom_lessons=False,
        analytics=False,
        priority_support=False,
        api_access=False
    ),
    LicenseType.PARENT: LicenseFeatures(
        max_students=3,
        max_lessons=81,
        progress_tracking=True,
        teacher_dashboard=False,
        custom_lessons=False,
        analytics=True,
        priority_support=False,
        api_access=False
    ),
    LicenseType.TEACHER: LicenseFeatures(
        max_students=30,
        max_lessons=81,
        progress_tracking=True,
        teacher_dashboard=True,
        custom_lessons=True,
        analytics=True,
        priority_support=True,
        api_access=False
    ),
    LicenseType.SCHOOL: LicenseFeatures(
        max_students=999999,
        max_lessons=81,
        progress_tracking=True,
        teacher_dashboard=True,
        custom_lessons=True,
        analytics=True,
        priority_support=True,
        api_access=True
    )
}

# In-memory license storage (replace with database in production)
licenses_db: Dict[str, License] = {}

def generate_license_key(email: str, license_type: LicenseType) -> str:
    """Generate a unique license key"""
    import hashlib
    import secrets
    timestamp = datetime.now().isoformat()
    raw = f"{email}{license_type.value}{timestamp}{secrets.token_hex(8)}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32].upper()

def create_license(email: str, license_type: LicenseType, duration_days: int = 14) -> License:
    """Create a new license"""
    license_key = generate_license_key(email, license_type)
    start_date = datetime.now()
    end_date = start_date + timedelta(days=duration_days)
    
    license = License(
        license_key=license_key,
        license_type=license_type,
        user_email=email,
        start_date=start_date,
        end_date=end_date,
        is_active=True,
        max_students=LICENSE_TIERS[license_type].max_students,
        features=LICENSE_TIERS[license_type]
    )
    
    licenses_db[license_key] = license
    return license

def validate_license(license_key: str) -> tuple[bool, Optional[License], str]:
    """Validate a license key and return status"""
    if license_key not in licenses_db:
        return False, None, "Invalid license key"
    
    license = licenses_db[license_key]
    
    if not license.is_active:
        return False, license, "License has been deactivated"
    
    if datetime.now() > license.end_date:
        license.is_active = False
        license.license_type = LicenseType.EXPIRED
        return False, license, "License has expired"
    
    return True, license, "License is valid"

def check_feature_access(license_key: str, feature: str) -> bool:
    """Check if a license has access to a specific feature"""
    is_valid, license, _ = validate_license(license_key)
    
    if not is_valid or not license:
        return False
    
    return getattr(license.features, feature, False)

def get_days_remaining(license_key: str) -> int:
    """Get days remaining on license"""
    if license_key not in licenses_db:
        return 0
    
    license = licenses_db[license_key]
    remaining = (license.end_date - datetime.now()).days
    return max(0, remaining)

def upgrade_license(license_key: str, new_type: LicenseType, duration_days: int = 30) -> Optional[License]:
    """Upgrade an existing license"""
    if license_key not in licenses_db:
        return None
    
    license = licenses_db[license_key]
    license.license_type = new_type
    license.end_date = datetime.now() + timedelta(days=duration_days)
    license.is_active = True
    license.features = LICENSE_TIERS[new_type]
    license.max_students = LICENSE_TIERS[new_type].max_students
    
    return license

def extend_license(license_key: str, days: int) -> Optional[License]:
    """Extend license duration"""
    if license_key not in licenses_db:
        return None
    
    license = licenses_db[license_key]
    license.end_date += timedelta(days=days)
    
    return license

def get_license_info(license_key: str) -> Optional[Dict]:
    """Get detailed license information"""
    is_valid, license, message = validate_license(license_key)
    
    if not license:
        return None
    
    return {
        "license_key": license.license_key,
        "license_type": license.license_type.value,
        "user_email": license.user_email,
        "is_valid": is_valid,
        "is_active": license.is_active,
        "start_date": license.start_date.isoformat(),
        "end_date": license.end_date.isoformat(),
        "days_remaining": get_days_remaining(license_key),
        "max_students": license.max_students,
        "features": {
            "max_lessons": license.features.max_lessons,
            "progress_tracking": license.features.progress_tracking,
            "teacher_dashboard": license.features.teacher_dashboard,
            "custom_lessons": license.features.custom_lessons,
            "analytics": license.features.analytics,
            "priority_support": license.features.priority_support,
            "api_access": license.features.api_access
        },
        "message": message
    }
