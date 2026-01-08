from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from app.models.schemas import LessonResponse, LessonFeedback, Lesson
from app.services.lesson_service import LessonService, ProgressService, RecordingService
from app.utils.audio_generator import generate_phoneme_audio
import random
import os
import uuid
from pathlib import Path
from urllib.parse import unquote

router = APIRouter(prefix="/api", tags=["lessons"])

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.get("/lesson", response_model=LessonResponse)
async def get_lesson():
    """Get a random lesson"""
    try:
        lesson = await LessonService.get_random_lesson()
        if not lesson:
            raise HTTPException(status_code=404, detail="No lessons available")
        return lesson
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/lessons", response_model=list[LessonResponse])
async def get_all_lessons():
    """Get all available lessons"""
    try:
        lessons = await LessonService.get_all_lessons()
        return lessons
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/lesson/{phoneme}", response_model=LessonResponse)
async def get_lesson_by_phoneme(phoneme: str):
    """Get lesson by specific phoneme"""
    try:
        lesson = await LessonService.get_lesson_by_phoneme(phoneme)
        if not lesson:
            raise HTTPException(status_code=404, detail=f"Lesson for {phoneme} not found")
        return lesson
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback", response_model=LessonFeedback)
async def submit_recording(
    lesson_id: str = Form(...),
    duration_ms: int = Form(...),
    audio: UploadFile = File(...),
    user_id: str = Form(default="demo_user"),
):
    """Submit a recording and get feedback"""
    try:
        # Save audio file
        file_ext = audio.filename.split(".")[-1] if audio.filename else "wav"
        file_name = f"{uuid.uuid4().hex}.{file_ext}"
        file_path = UPLOAD_DIR / file_name
        
        contents = await audio.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        # Save recording metadata
        await RecordingService.save_recording(user_id, lesson_id, duration_ms, str(file_path))

        # Simple scoring logic (in real system, would use ML model)
        score = random.uniform(0.5, 1.0)
        passed = score >= 0.75

        # Update user progress
        lesson = await LessonService.get_lesson_by_phoneme(lesson_id)
        if lesson:
            phoneme = lesson.get("phoneme", lesson_id)
            await ProgressService.update_progress(user_id, phoneme, score, passed)

        # Generate feedback
        if passed:
            messages = [
                "Great job! You nailed it! 🌟",
                "Excellent pronunciation! Keep it up! 🎉",
                "Perfect! You're a phonetics superstar! ⭐",
            ]
            hints = []
        else:
            messages = [
                "Good try! Let's practice more.",
                "Almost there! Try again.",
                "Keep practicing! You'll get it! 💪",
            ]
            hints = [
                "Try pronouncing it a bit slower",
                "Listen to the sample again",
                "Make sure your mouth is in the right shape",
            ]

        return LessonFeedback(
            passed=passed,
            message=random.choice(messages),
            score=score,
            hints=random.sample(hints, k=min(2, len(hints))) if hints else [],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/progression/{user_id}")
async def get_user_progression(user_id: str):
    """Get lesson progression for a user"""
    try:
        progress = await ProgressService.get_user_progress(user_id)
        mastered = await ProgressService.get_mastered_phonemes(user_id)
        
        return {
            "user_id": user_id,
            "progress": progress,
            "mastered_phonemes": mastered,
            "total_attempts": sum(p.get("attempts", 0) for p in progress),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/audio")
async def get_phoneme_audio(phoneme: str):
    """Get audio WAV file for a specific phoneme (query parameter: ?phoneme=/m/)"""
    try:
        # Phoneme comes as query parameter - Flutter compatible
        print(f"[DEBUG] Received phoneme query param: '{phoneme}' (repr: {repr(phoneme)})")
        
        # Ensure phoneme is in correct format
        if not phoneme.startswith('/'):
            phoneme = f"/{phoneme}"
        if not phoneme.endswith('/'):
            phoneme = f"{phoneme}/"
        
        print(f"[DEBUG] Formatted phoneme: '{phoneme}'")
        
        # Generate audio
        audio_data = generate_phoneme_audio(phoneme, duration_ms=800)
        
        return StreamingResponse(
            iter([audio_data]),
            media_type="audio/wav",
            headers={
                "Content-Disposition": f'inline; filename="phoneme_{phoneme.strip("/")}.wav"',
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            }
        )
    except Exception as e:
        print(f"[ERROR] Audio generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/audio/{phoneme}")
async def get_phoneme_audio_path(phoneme: str):
    """Get audio WAV file for a specific phoneme (path parameter: /p)"""
    try:
        # Phoneme comes as path parameter
        print(f"[DEBUG] Received phoneme path param: '{phoneme}' (repr: {repr(phoneme)})")
        
        # Strip leading slashes
        phoneme = phoneme.lstrip('/')
        
        # Ensure phoneme is in correct format
        if not phoneme.startswith('/'):
            phoneme = f"/{phoneme}"
        if not phoneme.endswith('/'):
            phoneme = f"{phoneme}/"
        
        print(f"[DEBUG] Formatted phoneme: '{phoneme}'")
        
        # Generate audio
        audio_data = generate_phoneme_audio(phoneme, duration_ms=800)
        
        return StreamingResponse(
            iter([audio_data]),
            media_type="audio/wav",
            headers={
                "Content-Disposition": f'inline; filename="phoneme_{phoneme.strip("/")}.wav"',
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            }
        )
    except Exception as e:
        print(f"[ERROR] Audio generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "phonetics-orchestrator"}
