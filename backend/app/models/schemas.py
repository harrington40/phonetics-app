from pydantic import BaseModel
from typing import List, Literal, Optional, Dict, Any
from datetime import datetime
import json

Viseme = Literal["rest", "smile", "open", "round"]

class VisemeCue(BaseModel):
    viseme: Viseme
    start_ms: int
    end_ms: int

class LessonResponse(BaseModel):
    id: str
    phoneme: str
    prompt: str
    audio_url: str
    visemes: List[VisemeCue]

class LessonFeedback(BaseModel):
    passed: bool
    message: str
    score: float
    hints: List[str]

class UserProgress(BaseModel):
    user_id: str
    phoneme: str
    attempts: int
    best_score: float
    last_attempted: Optional[datetime] = None
    mastered: bool = False

class RecordingRequest(BaseModel):
    lesson_id: str
    duration_ms: int

class Lesson(BaseModel):
    id: str
    phoneme: str
    prompt: str
    audio_url: str
    visemes: List[VisemeCue]
    difficulty: int = 1
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "lesson_001",
                "phoneme": "/p/",
                "prompt": "Let's pop like a puppy! Say: p p p",
                "audio_url": "https://example.com/audio/p.mp3",
                "visemes": [
                    {"viseme": "rest", "start_ms": 0, "end_ms": 120},
                    {"viseme": "round", "start_ms": 120, "end_ms": 220},
                ],
                "difficulty": 1,
            }
        }

# Learning Algorithm Models
class AttemptRecord(BaseModel):
    """Record of a single learning attempt"""
    timestamp: datetime
    score: float  # 0.0 to 1.0
    duration_ms: int
    feedback: str

class LearnerProfile(BaseModel):
    """Comprehensive user learning profile"""
    user_id: str
    username: str
    total_attempts: int = 0
    total_phonemes_mastered: int = 0
    average_score: float = 0.0
    current_streak: int = 0
    longest_streak: int = 0
    phoneme_progress: Dict[str, Dict[str, Any]] = {}  # phoneme -> progress data
    created_at: datetime
    last_active: datetime

class LearningStats(BaseModel):
    """Statistics for adaptive learning"""
    phoneme: str
    total_attempts: int
    correct_attempts: int
    average_score: float
    success_rate: float
    last_attempted: Optional[datetime]
    next_review_date: Optional[datetime]
    difficulty_level: int
    mastered: bool

class AdaptiveLesson(BaseModel):
    """Lesson adapted to learner's level"""
    lesson_id: str
    phoneme: str
    prompt: str
    audio_url: str
    visemes: List[VisemeCue]
    difficulty: int
    suggested_attempts: int
    time_until_next_review: Optional[int]  # in seconds
    priority_score: float  # 0.0 to 1.0, higher = more important

# Teacher Dashboard Models
class StudentSession(BaseModel):
    """Real-time student session in teacher class"""
    student_id: str
    student_name: str
    status: Literal["active", "practicing", "idle"] = "idle"
    mastery_level: float = 0.0  # 0.0 to 1.0
    accuracy: float = 0.0  # 0 to 100
    practice_time: int = 0  # minutes
    current_phoneme: str = ""
    current_activity: str = ""
    streak: int = 0
    mastered_phonemes: List[str] = []
    error_patterns: Dict[str, int] = {}  # phoneme -> error count
    joined_at: datetime = None
    last_active: Optional[datetime] = None


class ClassStats(BaseModel):
    """Aggregated classroom statistics"""
    total_students: int
    active_students: int
    average_mastery: float
    average_accuracy: float
    total_practice_time: int  # minutes


class TeacherClass(BaseModel):
    """Teacher's classroom"""
    teacher_id: str
    class_code: str
    class_name: str
    students: Dict[str, StudentSession] = {}
    created_at: datetime