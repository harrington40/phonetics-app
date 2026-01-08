"""
Usage Tracking API Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy import func, desc

from ..db.database import get_db
from ..db.models import ActivityLog, UsageLog, Student, StudentProgress, License

router = APIRouter()

class ActivityCreate(BaseModel):
    student_id: int
    lesson_id: str
    activity_type: str
    score: Optional[float] = None
    duration_seconds: Optional[int] = None
    metadata: Optional[dict] = None

class ProgressUpdate(BaseModel):
    student_id: int
    lesson_id: str
    phoneme: str
    correct: bool

class UsageLogCreate(BaseModel):
    license_key: str
    action: str
    details: Optional[dict] = None

@router.post("/tracking/activity")
async def log_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    """
    Log a student activity
    """
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == activity.student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Create activity log
        log = ActivityLog(
            student_id=activity.student_id,
            lesson_id=activity.lesson_id,
            activity_type=activity.activity_type,
            score=activity.score,
            duration_seconds=activity.duration_seconds,
            metadata=activity.metadata
        )
        db.add(log)
        db.commit()
        
        return {"success": True, "message": "Activity logged"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tracking/progress")
async def update_progress(progress: ProgressUpdate, db: Session = Depends(get_db)):
    """
    Update student progress on a phoneme
    """
    try:
        # Get or create progress record
        student_progress = db.query(StudentProgress).filter(
            StudentProgress.student_id == progress.student_id,
            StudentProgress.phoneme == progress.phoneme
        ).first()
        
        if not student_progress:
            student_progress = StudentProgress(
                student_id=progress.student_id,
                lesson_id=progress.lesson_id,
                phoneme=progress.phoneme,
                mastery_level=0.0,
                attempts=0,
                correct_attempts=0
            )
            db.add(student_progress)
        
        # Update attempts
        student_progress.attempts += 1
        if progress.correct:
            student_progress.correct_attempts += 1
        
        # Calculate mastery level (simple: correct / total)
        if student_progress.attempts > 0:
            student_progress.mastery_level = (
                student_progress.correct_attempts / student_progress.attempts
            ) * 100
        
        student_progress.last_practiced = datetime.utcnow()
        db.commit()
        
        return {
            "success": True,
            "mastery_level": student_progress.mastery_level,
            "attempts": student_progress.attempts
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tracking/usage")
async def log_usage(usage: UsageLogCreate, db: Session = Depends(get_db)):
    """
    Log license usage
    """
    try:
        # Get license
        license = db.query(License).filter(
            License.license_key == usage.license_key
        ).first()
        
        if not license:
            raise HTTPException(status_code=404, detail="License not found")
        
        # Create usage log
        log = UsageLog(
            license_id=license.id,
            action=usage.action,
            details=usage.details
        )
        db.add(log)
        db.commit()
        
        return {"success": True}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tracking/student/{student_id}/summary")
async def get_student_summary(student_id: int, db: Session = Depends(get_db)):
    """
    Get student activity summary
    """
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Get total activities
        total_activities = db.query(func.count(ActivityLog.id)).filter(
            ActivityLog.student_id == student_id
        ).scalar()
        
        # Get lessons completed
        lessons_completed = db.query(func.count(func.distinct(ActivityLog.lesson_id))).filter(
            ActivityLog.student_id == student_id,
            ActivityLog.activity_type == "lesson_complete"
        ).scalar()
        
        # Get average score
        avg_score = db.query(func.avg(ActivityLog.score)).filter(
            ActivityLog.student_id == student_id,
            ActivityLog.score.isnot(None)
        ).scalar() or 0
        
        # Get total time spent (in minutes)
        total_time = db.query(func.sum(ActivityLog.duration_seconds)).filter(
            ActivityLog.student_id == student_id
        ).scalar() or 0
        total_time_minutes = total_time // 60
        
        # Get mastery progress
        mastery_data = db.query(StudentProgress).filter(
            StudentProgress.student_id == student_id
        ).all()
        
        avg_mastery = sum(p.mastery_level for p in mastery_data) / len(mastery_data) if mastery_data else 0
        
        return {
            "student_id": student_id,
            "student_name": student.name,
            "total_activities": total_activities,
            "lessons_completed": lessons_completed,
            "average_score": round(avg_score, 2),
            "total_time_minutes": total_time_minutes,
            "average_mastery": round(avg_mastery, 2),
            "phonemes_practiced": len(mastery_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tracking/student/{student_id}/progress")
async def get_student_progress(student_id: int, limit: int = 20, db: Session = Depends(get_db)):
    """
    Get detailed student progress by phoneme
    """
    try:
        progress_data = db.query(StudentProgress).filter(
            StudentProgress.student_id == student_id
        ).order_by(desc(StudentProgress.last_practiced)).limit(limit).all()
        
        return {
            "student_id": student_id,
            "progress": [
                {
                    "phoneme": p.phoneme,
                    "mastery_level": p.mastery_level,
                    "attempts": p.attempts,
                    "correct_attempts": p.correct_attempts,
                    "last_practiced": p.last_practiced.isoformat()
                }
                for p in progress_data
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tracking/license/{license_key}/usage")
async def get_license_usage(license_key: str, days: int = 30, db: Session = Depends(get_db)):
    """
    Get license usage statistics
    """
    try:
        license = db.query(License).filter(
            License.license_key == license_key
        ).first()
        
        if not license:
            raise HTTPException(status_code=404, detail="License not found")
        
        # Get usage logs from last N days
        since_date = datetime.utcnow() - timedelta(days=days)
        usage_logs = db.query(UsageLog).filter(
            UsageLog.license_id == license.id,
            UsageLog.created_at >= since_date
        ).all()
        
        # Count actions
        action_counts = {}
        for log in usage_logs:
            action_counts[log.action] = action_counts.get(log.action, 0) + 1
        
        return {
            "license_key": license_key,
            "period_days": days,
            "total_actions": len(usage_logs),
            "actions_breakdown": action_counts,
            "first_activity": usage_logs[-1].created_at.isoformat() if usage_logs else None,
            "last_activity": usage_logs[0].created_at.isoformat() if usage_logs else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tracking/analytics/overview")
async def get_analytics_overview(db: Session = Depends(get_db)):
    """
    Get overall platform analytics
    """
    try:
        # Total users
        total_users = db.query(func.count(func.distinct(License.user_id))).scalar()
        
        # Active licenses
        active_licenses = db.query(func.count(License.id)).filter(
            License.is_active == True,
            License.end_date > datetime.utcnow()
        ).scalar()
        
        # Total students
        total_students = db.query(func.count(Student.id)).scalar()
        
        # Total activities (last 30 days)
        since_date = datetime.utcnow() - timedelta(days=30)
        recent_activities = db.query(func.count(ActivityLog.id)).filter(
            ActivityLog.created_at >= since_date
        ).scalar()
        
        # Lessons completed (last 30 days)
        recent_lessons = db.query(func.count(ActivityLog.id)).filter(
            ActivityLog.created_at >= since_date,
            ActivityLog.activity_type == "lesson_complete"
        ).scalar()
        
        return {
            "total_users": total_users,
            "active_licenses": active_licenses,
            "total_students": total_students,
            "recent_activities_30d": recent_activities,
            "lessons_completed_30d": recent_lessons
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
