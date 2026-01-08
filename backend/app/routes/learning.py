"""
Learning System Routes
Endpoints for adaptive learning, progress tracking, and recommendations
"""
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import Optional
from app.models.schemas import LearnerProfile, LearningStats, AdaptiveLesson, VisemeCue
from app.services.learning_algorithm import learning_algorithm
from app.services.lesson_service import LessonService

router = APIRouter(prefix="/api", tags=["learning"])

lesson_service = LessonService()

@router.post("/learner/init")
async def initialize_learner(user_id: str, username: str):
    """Initialize a new learner profile"""
    try:
        profile = learning_algorithm.initialize_learner(user_id, username)
        return {
            "success": True,
            "message": f"Learner {username} initialized",
            "profile": profile
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/attempt/record")
async def record_attempt(
    user_id: str,
    phoneme: str,
    score: float = Query(..., ge=0.0, le=1.0),
    duration_ms: int = Query(default=0, ge=0),
    feedback: str = Query(default="")
):
    """Record a learning attempt"""
    try:
        if not (0.0 <= score <= 1.0):
            raise ValueError("Score must be between 0.0 and 1.0")
        
        stats = learning_algorithm.record_attempt(
            user_id=user_id,
            phoneme=phoneme,
            score=score,
            duration_ms=duration_ms,
            feedback=feedback
        )
        
        return {
            "success": True,
            "message": "Attempt recorded",
            "stats": stats,
            "next_review": stats.next_review_date.isoformat() if stats.next_review_date else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/learner/stats")
async def get_learner_stats(user_id: str):
    """Get comprehensive learner statistics"""
    try:
        profile = learning_algorithm.get_learner_stats(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Learner profile not found")
        
        return {
            "user_id": profile.user_id,
            "username": profile.username,
            "total_attempts": profile.total_attempts,
            "total_phonemes_mastered": profile.total_phonemes_mastered,
            "average_score": round(profile.average_score, 2),
            "current_streak": profile.current_streak,
            "longest_streak": profile.longest_streak,
            "created_at": profile.created_at.isoformat(),
            "last_active": profile.last_active.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/phoneme/progress/{phoneme}")
async def get_phoneme_progress(phoneme: str, user_id: str):
    """Get progress for a specific phoneme"""
    try:
        stats = learning_algorithm.get_phoneme_progress(user_id, phoneme)
        if not stats:
            raise HTTPException(status_code=404, detail="Phoneme progress not found")
        
        return {
            "phoneme": stats.phoneme,
            "total_attempts": stats.total_attempts,
            "correct_attempts": stats.correct_attempts,
            "average_score": round(stats.average_score, 2),
            "success_rate": round(stats.success_rate, 2),
            "last_attempted": stats.last_attempted.isoformat() if stats.last_attempted else None,
            "next_review_date": stats.next_review_date.isoformat() if stats.next_review_date else None,
            "difficulty_level": stats.difficulty_level,
            "mastered": stats.mastered
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/phoneme/all-progress")
async def get_all_phoneme_progress(user_id: str):
    """Get progress for all phonemes"""
    try:
        stats_dict = learning_algorithm.get_all_phoneme_progress(user_id)
        
        results = {}
        for phoneme, stats in stats_dict.items():
            results[phoneme] = {
                "total_attempts": stats.total_attempts,
                "correct_attempts": stats.correct_attempts,
                "average_score": round(stats.average_score, 2),
                "success_rate": round(stats.success_rate, 2),
                "difficulty_level": stats.difficulty_level,
                "mastered": stats.mastered,
                "last_attempted": stats.last_attempted.isoformat() if stats.last_attempted else None
            }
        
        return {
            "user_id": user_id,
            "phoneme_progress": results,
            "total_phonemes": len(results),
            "mastered_count": sum(1 for s in stats_dict.values() if s.mastered)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/lesson/next")
async def get_next_lesson(user_id: str):
    """Get the next recommended lesson based on spaced repetition"""
    try:
        next_phoneme_info = learning_algorithm.get_next_lesson(user_id)
        
        if not next_phoneme_info:
            # Return a random lesson if no progress data
            lesson = await lesson_service.get_random_lesson()
            phoneme = lesson.get("phoneme") if lesson else None
            difficulty = 1
            priority = 0.5
        else:
            phoneme, difficulty, priority = next_phoneme_info
            lesson = await lesson_service.get_lesson_by_phoneme(phoneme)
        
        if not lesson:
            raise HTTPException(status_code=404, detail="No lesson found")
        
        # Get stats if available
        stats = learning_algorithm.get_phoneme_progress(user_id, phoneme)
        
        return {
            "lesson_id": lesson.get("id"),
            "phoneme": lesson.get("phoneme"),
            "prompt": lesson.get("prompt"),
            "audio_url": lesson.get("audio_url"),
            "visemes": [{"viseme": v.get("viseme"), "start_ms": v.get("start_ms"), "end_ms": v.get("end_ms")} for v in lesson.get("visemes", [])],
            "difficulty": difficulty,
            "priority_score": round(priority, 2),
            "attempts_so_far": stats.total_attempts if stats else 0,
            "current_score": round(stats.average_score, 2) if stats else 0.0,
            "mastered": stats.mastered if stats else False
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations")
async def get_learning_recommendations(user_id: str):
    """Get personalized learning recommendations"""
    try:
        recommendations = learning_algorithm.get_learning_recommendations(user_id)
        
        return {
            "user_id": user_id,
            "focus_areas": [
                {"phoneme": p[0], "score": round(p[1], 2)}
                for p in recommendations.get('focus_areas', [])
            ],
            "strong_areas": [
                {"phoneme": p[0], "score": round(p[1], 2)}
                for p in recommendations.get('strong_areas', [])
            ],
            "suggested_daily_practice_items": recommendations.get('suggested_daily_practice', 0),
            "estimated_days_to_mastery": recommendations.get('estimated_time_to_mastery_days', 0),
            "next_milestone": recommendations.get('next_milestone', 'Keep practicing!'),
            "tip": "Focus on your weak areas first, then maintain your strong areas"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard")
async def get_dashboard(user_id: str):
    """Get complete dashboard with all relevant learning data"""
    try:
        profile = learning_algorithm.get_learner_stats(user_id)
        if not profile:
            profile = learning_algorithm.initialize_learner(user_id, f"User_{user_id}")
        
        stats = learning_algorithm.get_all_phoneme_progress(user_id)
        recommendations = learning_algorithm.get_learning_recommendations(user_id)
        
        mastered = [p for p, s in stats.items() if s.mastered]
        in_progress = [p for p, s in stats.items() if not s.mastered]
        
        return {
            "user": {
                "id": profile.user_id,
                "username": profile.username,
                "total_attempts": profile.total_attempts,
                "average_score": round(profile.average_score, 2),
                "current_streak": profile.current_streak,
                "longest_streak": profile.longest_streak
            },
            "progress": {
                "total_phonemes_mastered": profile.total_phonemes_mastered,
                "mastered_phonemes": mastered,
                "in_progress_phonemes": in_progress,
                "mastery_percentage": round((len(mastered) / max(len(mastered) + len(in_progress), 1)) * 100, 1)
            },
            "recommendations": recommendations,
            "next_milestone": recommendations.get('next_milestone', 'Keep practicing!')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset-progress")
async def reset_progress(user_id: str):
    """Reset all progress for a user (for testing/starting over)"""
    try:
        learning_algorithm.learner_profiles.pop(user_id, None)
        learning_algorithm.phoneme_stats.pop(user_id, None)
        return {"success": True, "message": f"Progress reset for user {user_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
