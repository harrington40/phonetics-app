"""
Teacher Dashboard Routes
Handles real-time student monitoring, class management, and progress tracking
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import List, Dict, Optional
import json
from datetime import datetime
from ..models.schemas import (
    StudentSession,
    ClassStats,
    UserProgress,
    TeacherClass
)

router = APIRouter(prefix="/api/teacher", tags=["teacher"])

# In-memory storage for classes and connections
classes_db: Dict[str, TeacherClass] = {}
active_connections: Dict[str, List[WebSocket]] = {}

class TeacherClass:
    """Represents a teacher's classroom"""
    def __init__(self, teacher_id: str, class_name: str = "My Class"):
        self.teacher_id = teacher_id
        self.class_code = f"TEACHER{teacher_id[-6:].upper()}"
        self.class_name = class_name
        self.students: Dict[str, StudentSession] = {}
        self.created_at = datetime.now()
        
    def add_student(self, student_id: str, student_name: str):
        """Add a student to the class"""
        self.students[student_id] = StudentSession(
            student_id=student_id,
            student_name=student_name,
            status="active",
            joined_at=datetime.now()
        )
        
    def remove_student(self, student_id: str):
        """Remove a student from the class"""
        if student_id in self.students:
            del self.students[student_id]
            
    def get_stats(self) -> ClassStats:
        """Calculate class statistics"""
        if not self.students:
            return ClassStats(
                total_students=0,
                active_students=0,
                average_mastery=0,
                average_accuracy=0,
                total_practice_time=0
            )
            
        active = sum(1 for s in self.students.values() if s.status == "active")
        avg_mastery = sum(s.mastery_level for s in self.students.values()) / len(self.students)
        avg_accuracy = sum(s.accuracy for s in self.students.values()) / len(self.students)
        total_time = sum(s.practice_time for s in self.students.values())
        
        return ClassStats(
            total_students=len(self.students),
            active_students=active,
            average_mastery=avg_mastery,
            average_accuracy=avg_accuracy,
            total_practice_time=total_time
        )


@router.post("/class/create")
async def create_class(teacher_id: str, class_name: str = "My Class"):
    """
    Create a new teacher classroom
    
    Args:
        teacher_id: Unique teacher identifier
        class_name: Name of the classroom
        
    Returns:
        Class code and information
    """
    if teacher_id in classes_db:
        raise HTTPException(status_code=400, detail="Teacher already has an active class")
    
    teacher_class = TeacherClass(teacher_id, class_name)
    classes_db[teacher_id] = teacher_class
    
    return {
        "success": True,
        "class_code": teacher_class.class_code,
        "class_name": class_name,
        "teacher_id": teacher_id,
        "message": "Class created successfully"
    }


@router.post("/class/{teacher_id}/add-student")
async def add_student_to_class(
    teacher_id: str,
    student_id: str,
    student_name: str
):
    """
    Add a student to a teacher's class
    
    Args:
        teacher_id: Teacher's ID
        student_id: Student's ID
        student_name: Student's name
        
    Returns:
        Confirmation of student added
    """
    if teacher_id not in classes_db:
        # Auto-create class if doesn't exist
        classes_db[teacher_id] = TeacherClass(teacher_id)
    
    teacher_class = classes_db[teacher_id]
    teacher_class.add_student(student_id, student_name)
    
    return {
        "success": True,
        "message": f"{student_name} added to class",
        "class_code": teacher_class.class_code
    }


@router.get("/class/{teacher_id}/students")
async def get_class_students(teacher_id: str):
    """
    Get all students in a teacher's class with real-time stats
    
    Args:
        teacher_id: Teacher's ID
        
    Returns:
        List of students and their current status
    """
    if teacher_id not in classes_db:
        raise HTTPException(status_code=404, detail="Class not found")
    
    teacher_class = classes_db[teacher_id]
    
    students = []
    for student_id, session in teacher_class.students.items():
        students.append({
            "student_id": student_id,
            "student_name": session.student_name,
            "status": session.status,
            "mastery_level": session.mastery_level,
            "accuracy": session.accuracy,
            "practice_time": session.practice_time,
            "current_phoneme": session.current_phoneme,
            "current_activity": session.current_activity,
            "streak": session.streak,
            "joined_at": session.joined_at.isoformat()
        })
    
    return {
        "class_code": teacher_class.class_code,
        "total_students": len(students),
        "students": students
    }


@router.get("/class/{teacher_id}/stats")
async def get_class_stats(teacher_id: str):
    """
    Get aggregated class statistics
    
    Args:
        teacher_id: Teacher's ID
        
    Returns:
        Class statistics including averages and trends
    """
    if teacher_id not in classes_db:
        raise HTTPException(status_code=404, detail="Class not found")
    
    teacher_class = classes_db[teacher_id]
    stats = teacher_class.get_stats()
    
    return {
        "total_students": stats.total_students,
        "active_students": stats.active_students,
        "average_mastery": round(stats.average_mastery, 2),
        "average_accuracy": round(stats.average_accuracy, 2),
        "total_practice_time": stats.total_practice_time,
        "phoneme_completion": calculate_class_phoneme_progress(teacher_class)
    }


@router.get("/class/{teacher_id}/student/{student_id}")
async def get_student_details(teacher_id: str, student_id: str):
    """
    Get detailed progress for a specific student
    
    Args:
        teacher_id: Teacher's ID
        student_id: Student's ID
        
    Returns:
        Detailed student progress and performance metrics
    """
    if teacher_id not in classes_db:
        raise HTTPException(status_code=404, detail="Class not found")
    
    teacher_class = classes_db[teacher_id]
    if student_id not in teacher_class.students:
        raise HTTPException(status_code=404, detail="Student not found in class")
    
    student = teacher_class.students[student_id]
    
    return {
        "student_id": student_id,
        "student_name": student.student_name,
        "status": student.status,
        "mastery_level": student.mastery_level,
        "accuracy": student.accuracy,
        "practice_time": student.practice_time,
        "streak": student.streak,
        "mastered_phonemes": student.mastered_phonemes,
        "current_phoneme": student.current_phoneme,
        "current_activity": student.current_activity,
        "error_patterns": student.error_patterns,
        "last_active": student.last_active.isoformat() if student.last_active else None,
        "joined_at": student.joined_at.isoformat()
    }


@router.post("/student/{student_id}/update-progress")
async def update_student_progress(
    student_id: str,
    teacher_id: str,
    phoneme: str,
    activity: str,
    quality: int,
    accuracy: float
):
    """
    Update student progress in real-time
    Called from student app to sync with teacher dashboard
    
    Args:
        student_id: Student's ID
        teacher_id: Associated teacher
        phoneme: Current phoneme
        activity: Current activity type
        quality: Quality score (0-5)
        accuracy: Accuracy percentage
    """
    if teacher_id not in classes_db:
        return {"error": "Teacher class not found"}
    
    teacher_class = classes_db[teacher_id]
    if student_id not in teacher_class.students:
        return {"error": "Student not in this class"}
    
    student = teacher_class.students[student_id]
    student.current_phoneme = phoneme
    student.current_activity = activity
    student.accuracy = accuracy
    student.last_active = datetime.now()
    
    # Update mastery based on quality
    if quality >= 4:
        if phoneme not in student.mastered_phonemes:
            student.mastered_phonemes.append(phoneme)
            student.mastery_level = len(student.mastered_phonemes) / 15
    
    # Broadcast update to teacher
    await broadcast_class_update(teacher_id, {
        "type": "student_progress",
        "student_id": student_id,
        "phoneme": phoneme,
        "accuracy": accuracy,
        "quality": quality
    })
    
    return {"success": True, "message": "Progress updated"}


@router.websocket("/ws/teacher/{teacher_id}")
async def websocket_teacher_endpoint(websocket: WebSocket, teacher_id: str):
    """
    WebSocket endpoint for real-time teacher dashboard
    Sends real-time student updates to teacher
    """
    await websocket.accept()
    
    if teacher_id not in active_connections:
        active_connections[teacher_id] = []
    
    active_connections[teacher_id].append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            elif message.get("type") == "get_class_stats":
                if teacher_id in classes_db:
                    stats = classes_db[teacher_id].get_stats()
                    await websocket.send_json({
                        "type": "class_stats",
                        "stats": {
                            "total_students": stats.total_students,
                            "active_students": stats.active_students,
                            "average_mastery": stats.average_mastery
                        }
                    })
    
    except WebSocketDisconnect:
        active_connections[teacher_id].remove(websocket)


@router.websocket("/ws/student/{student_id}")
async def websocket_student_endpoint(websocket: WebSocket, student_id: str):
    """
    WebSocket endpoint for student to teacher connection
    Allows students to send real-time updates to teacher dashboard
    """
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            update = json.loads(data)
            
            # Broadcast to teacher
            teacher_id = update.get("teacher_id")
            if teacher_id and teacher_id in active_connections:
                for teacher_ws in active_connections[teacher_id]:
                    await teacher_ws.send_json({
                        "type": "student_update",
                        "student_id": student_id,
                        "data": update
                    })
    
    except WebSocketDisconnect:
        pass


async def broadcast_class_update(teacher_id: str, message: dict):
    """
    Broadcast an update to all connected teachers in a class
    """
    if teacher_id in active_connections:
        for websocket in active_connections[teacher_id]:
            try:
                await websocket.send_json(message)
            except:
                pass


@router.post("/class/{teacher_id}/send-message")
async def send_message_to_class(
    teacher_id: str,
    student_id: Optional[str] = None,
    message: str = ""
):
    """
    Send a message from teacher to student(s)
    
    Args:
        teacher_id: Teacher's ID
        student_id: Specific student (or None for whole class)
        message: Message content
    """
    if teacher_id not in classes_db:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Broadcast message via WebSocket
    await broadcast_class_update(teacher_id, {
        "type": "teacher_message",
        "target_student": student_id,
        "message": message,
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "success": True,
        "message": "Message sent",
        "target": "specific student" if student_id else "entire class"
    }


def calculate_class_phoneme_progress(teacher_class: TeacherClass) -> dict:
    """Calculate overall phoneme mastery across the class"""
    all_phonemes = ['a', 'e', 'i', 'o', 'u', 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm']
    
    if not teacher_class.students:
        return {p: {"mastered": 0, "practicing": 0, "learning": 0} for p in all_phonemes}
    
    phoneme_stats = {p: {"mastered": 0, "practicing": 0, "learning": 0} for p in all_phonemes}
    
    for student in teacher_class.students.values():
        for phoneme in all_phonemes:
            if phoneme in student.mastered_phonemes:
                phoneme_stats[phoneme]["mastered"] += 1
            elif phoneme == student.current_phoneme:
                phoneme_stats[phoneme]["practicing"] += 1
            else:
                phoneme_stats[phoneme]["learning"] += 1
    
    return phoneme_stats
