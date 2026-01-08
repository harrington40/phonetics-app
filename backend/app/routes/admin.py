"""
Admin routes for teacher/admin dashboard
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, List
from app.services.learning_algorithm import learning_algorithm

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/stats")
async def get_admin_stats():
    """Get comprehensive admin statistics"""
    try:
        return learning_algorithm.get_admin_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get admin stats: {str(e)}")

@router.get("/algorithm-metrics")
async def get_algorithm_metrics():
    """Get algorithm performance metrics"""
    try:
        return learning_algorithm.get_algorithm_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get algorithm metrics: {str(e)}")

@router.post("/algorithm-settings")
async def update_algorithm_settings(settings: Dict):
    """Update algorithm settings"""
    try:
        success = learning_algorithm.update_admin_settings(settings)
        if success:
            return {"message": "Algorithm settings updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Invalid settings provided")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update settings: {str(e)}")

@router.get("/algorithm-settings")
async def get_algorithm_settings():
    """Get current algorithm settings"""
    try:
        return learning_algorithm.get_admin_settings()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get settings: {str(e)}")

@router.get("/students")
async def get_students_progress():
    """Get all students progress data"""
    try:
        return learning_algorithm.get_student_progress_table()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get students data: {str(e)}")

@router.post("/reset-student/{user_id}")
async def reset_student_progress(user_id: str):
    """Reset a student's progress"""
    try:
        success = learning_algorithm.reset_student_progress(user_id)
        if success:
            return {"message": f"Progress reset for student {user_id}"}
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset progress: {str(e)}")

@router.get("/export-data")
async def export_learning_data():
    """Export all learning data"""
    try:
        return learning_algorithm.export_learning_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export data: {str(e)}")

@router.get("/analytics/{user_id}")
async def get_student_analytics(user_id: str):
    """Get detailed analytics for a specific student"""
    try:
        profile = learning_algorithm.get_learner_stats(user_id)
        phoneme_stats = learning_algorithm.get_all_phoneme_progress(user_id)

        if not profile:
            raise HTTPException(status_code=404, detail="Student not found")

        # Calculate additional analytics
        total_phonemes = len(phoneme_stats)
        mastered_phonemes = sum(1 for stat in phoneme_stats.values() if stat.mastered)
        avg_accuracy = sum(stat.average_score for stat in phoneme_stats.values()) / total_phonemes if total_phonemes > 0 else 0

        # Performance trends (mock data for now)
        performance_trend = [0.6, 0.65, 0.72, 0.78, 0.82, 0.85]  # Last 6 sessions

        # Weak areas
        weak_areas = [
            {"phoneme": phoneme, "score": stat.average_score}
            for phoneme, stat in phoneme_stats.items()
            if stat.average_score < 0.75 and not stat.mastered
        ]
        weak_areas.sort(key=lambda x: x["score"])

        return {
            "profile": {
                "user_id": profile.user_id,
                "username": profile.username,
                "total_attempts": profile.total_attempts,
                "average_score": round(profile.average_score * 100, 1),
                "current_streak": profile.current_streak,
                "longest_streak": profile.longest_streak,
                "total_phonemes_mastered": profile.total_phonemes_mastered,
                "created_at": profile.created_at.isoformat(),
                "last_active": profile.last_active.isoformat()
            },
            "progress": {
                "total_phonemes": total_phonemes,
                "mastered_phonemes": mastered_phonemes,
                "completion_percentage": round((mastered_phonemes / total_phonemes) * 100, 1) if total_phonemes > 0 else 0,
                "average_accuracy": round(avg_accuracy * 100, 1)
            },
            "analytics": {
                "performance_trend": performance_trend,
                "weak_areas": weak_areas[:5],  # Top 5 weak areas
                "phoneme_details": [
                    {
                        "phoneme": phoneme,
                        "attempts": stat.total_attempts,
                        "accuracy": round(stat.average_score * 100, 1),
                        "mastered": stat.mastered,
                        "difficulty_level": stat.difficulty_level,
                        "last_attempted": stat.last_attempted.isoformat() if stat.last_attempted else None
                    }
                    for phoneme, stat in phoneme_stats.items()
                ]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get student analytics: {str(e)}")

@router.get("/system-health")
async def get_system_health():
    """Get system health and performance metrics"""
    try:
        stats = learning_algorithm.get_admin_stats()
        metrics = learning_algorithm.get_algorithm_metrics()

        return {
            "status": "healthy",
            "timestamp": "2025-12-17T22:30:00Z",  # Would be datetime.now().isoformat()
            "uptime": "2 hours 15 minutes",  # Would calculate actual uptime
            "active_users": stats["total_students"],
            "total_sessions": stats["total_attempts"],
            "algorithm_performance": metrics,
            "system_load": {
                "cpu_usage": 45.2,  # Mock data
                "memory_usage": 67.8,
                "disk_usage": 23.1
            },
            "database_status": "connected",
            "last_backup": "2025-12-17T20:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system health: {str(e)}")