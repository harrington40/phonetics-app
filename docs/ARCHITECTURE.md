# Architecture & Design

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Flutter)                       │
├──────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Lesson       │  │ Cartoon      │  │ Audio Player &   │  │
│  │ Screen       │  │ Animal       │  │ Recording UI     │  │
│  │ (UI)         │  │ (Canvas)     │  │                  │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│         │                 │                    │            │
│         └─────────────────┼────────────────────┘            │
│                           │                                 │
│                  ┌────────▼────────┐                        │
│                  │ ApiService      │                        │
│                  │ (HTTP Client)   │                        │
│                  └────────┬────────┘                        │
└───────────────────────────┼──────────────────────────────────┘
                            │ HTTP/REST
                            │
┌───────────────────────────▼──────────────────────────────────┐
│                 Backend (FastAPI/Python)                     │
├──────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ /lesson      │  │ /feedback    │  │ /progression     │  │
│  │ /lessons     │  │ (Recording   │  │ (User Progress)  │  │
│  │ (Lesson      │  │  Upload)     │  │                  │  │
│  │  Retrieval)  │  │              │  │                  │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│         │                 │                    │            │
│         └─────────────────┼────────────────────┘            │
│                           │                                 │
│     ┌─────────────────────┼────────────────────┐            │
│     │                     │                    │            │
│  ┌──▼──────────┐  ┌───────▼────────┐  ┌──────▼─────────┐ │
│  │ Lesson      │  │ Progress       │  │ Recording      │ │
│  │ Service     │  │ Service        │  │ Service        │ │
│  │             │  │                │  │                │ │
│  │ - Random    │  │ - Track        │  │ - Save files   │ │
│  │   lesson    │  │   attempts     │  │ - Score audio  │ │
│  │ - By        │  │ - Mastery      │  │                │ │
│  │   phoneme   │  │   tracking     │  │                │ │
│  └──────┬──────┘  └────────┬───────┘  └───────┬────────┘ │
│         │                  │                   │          │
│         └──────────────────┼───────────────────┘          │
│                            │                             │
│                  ┌─────────▼────────┐                   │
│                  │ RethinkDB        │                   │
│                  │ Connection       │                   │
│                  └─────────┬────────┘                   │
└──────────────────────────────┼──────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                  RethinkDB (Database)                       │
├──────────────────────────────────────────────────────────────┤
│  ┌────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ lessons    │  │ user_progress│  │ recordings        │  │
│  │            │  │              │  │                   │  │
│  │ - id       │  │ - id         │  │ - id              │  │
│  │ - phoneme  │  │ - user_id    │  │ - user_id         │  │
│  │ - prompt   │  │ - phoneme    │  │ - lesson_id       │  │
│  │ - audio_url│  │ - attempts   │  │ - duration_ms     │  │
│  │ - visemes  │  │ - best_score │  │ - file_path       │  │
│  │ - difficulty  │ - mastered   │  │ - created_at      │  │
│  └────────────┘  └──────────────┘  └───────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Lesson Request Flow

```
User Presses "Get Lesson"
         ↓
Flutter: loadLesson()
         ↓
HTTP GET /api/lesson
         ↓
Backend: get_random_lesson()
         ↓
Query RethinkDB table "lessons"
         ↓
Return LessonResponse (phoneme, audio_url, visemes)
         ↓
Flutter: Parse & Display lesson
         ↓
Render Phoneme text + Prompt + Buttons
```

### 2. Audio Playback + Animation Flow

```
User Presses "Play + Animate"
         ↓
Flutter: playLesson()
         ↓
Start Viseme Scheduler (Timer)
         ↓
Play Audio (UrlSource)
         ↓
┌─────────────────────────────┐
│ Timer ticks every 16ms      │
│ Check current_ms            │
│ Find matching viseme        │
│ Trigger setState()          │
│ Redraw mouth shape          │
└─────────────────────────────┘
         ↓
Audio Complete
         ↓
Stop Timer + Reset mouth
```

### 3. Recording & Feedback Flow

```
User Records Audio
         ↓
Flutter: submitRecording(audioPath, duration_ms)
         ↓
HTTP POST /api/feedback (multipart form-data)
         ↓
Backend: submit_recording()
         ↓
Save file to /uploads/
Save metadata to recordings table
         ↓
Calculate Score (random 0.5-1.0 for PoC)
         ↓
Update user_progress table
         ↓
Return LessonFeedback (passed, message, score, hints)
         ↓
Flutter: Display feedback UI
```

## Module Responsibilities

### Frontend (Flutter)

| Module | Responsibility |
|--------|-----------------|
| `main.dart` | App entry point, screen routing |
| `models/lesson.dart` | Data structures (Lesson, Viseme, VisemeCue) |
| `services/api_service.dart` | HTTP client, API communication |
| `screens/lesson_screen.dart` | Main UI, state management |
| `widgets/cartoon_animal.dart` | CustomPainter for mouth animation |

### Backend (Python)

| Module | Responsibility |
|--------|-----------------|
| `main.py` | FastAPI setup, middleware, startup/shutdown |
| `models/schemas.py` | Pydantic models for validation |
| `routes/lessons.py` | API endpoints (lesson, feedback, progression) |
| `services/lesson_service.py` | Business logic (lesson selection, scoring, progress) |
| `db/connection.py` | RethinkDB connection & query helpers |

## Database Schema Design

### lessons Table

```javascript
{
  id: String,          // Primary key
  phoneme: String,     // /p/, /m/, /s/, etc.
  prompt: String,      // Kid-friendly instruction
  audio_url: String,   // URL to audio file
  visemes: Array<{
    viseme: String,    // "rest" | "smile" | "open" | "round"
    start_ms: Number,
    end_ms: Number
  }>,
  difficulty: Number,  // 1-5 progression
  created_at: String,  // ISO timestamp
  updated_at: String   // ISO timestamp
}

// Indexes
CREATE INDEX ON lessons(phoneme)
```

### user_progress Table

```javascript
{
  id: String,              // Primary key
  user_id: String,         // Foreign key to users (future)
  phoneme: String,         // Which phoneme being tracked
  attempts: Number,        // Total attempts
  best_score: Number,      // 0.0-1.0
  last_attempted: String,  // ISO timestamp
  mastered: Boolean        // best_score >= 0.8
}

// Indexes
CREATE INDEX ON user_progress(user_id)
```

### recordings Table

```javascript
{
  id: String,       // Primary key
  user_id: String,  // Foreign key
  lesson_id: String,// Reference to lesson
  duration_ms: Number,
  file_path: String, // Local storage path
  created_at: String // ISO timestamp
}

// Indexes
CREATE INDEX ON recordings(user_id)
```

## API Contract

### GET /api/lesson

**Response**: LessonResponse
```json
{
  "id": "lesson_p",
  "phoneme": "/p/",
  "prompt": "Let's pop like a puppy!",
  "audio_url": "https://example.com/audio/p.mp3",
  "visemes": [
    {"viseme": "rest", "start_ms": 0, "end_ms": 120},
    {"viseme": "round", "start_ms": 120, "end_ms": 220}
  ]
}
```

### POST /api/feedback

**Request**: multipart/form-data
```
lesson_id: string
user_id: string (default: "demo_user")
duration_ms: number
audio: file
```

**Response**: LessonFeedback
```json
{
  "passed": true,
  "message": "Great job!",
  "score": 0.92,
  "hints": []
}
```

### GET /api/progression/{user_id}

**Response**:
```json
{
  "user_id": "demo_user",
  "progress": [...],
  "mastered_phonemes": ["/p/", "/m/"],
  "total_attempts": 15
}
```

## Error Handling

### Frontend

```dart
try {
  final lesson = await apiService.getLesson();
  // Process lesson
} catch (e) {
  setState(() => errorMessage = 'Error: $e');
  // Show error UI
}
```

### Backend

```python
@router.get("/lesson")
async def get_lesson():
    try:
        lesson = await LessonService.get_random_lesson()
        if not lesson:
            raise HTTPException(status_code=404, detail="No lessons available")
        return lesson
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Security Considerations

1. **CORS**: Configured to accept all origins (change in production)
2. **Input Validation**: Pydantic models validate all inputs
3. **File Upload**: Save to designated directory, sanitize filenames
4. **Database**: No SQL injection (ORM used)
5. **Authentication**: Currently none (add JWT for production)

### To Add Authentication (Future)

```python
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()

@router.get("/lesson")
async def get_lesson(credentials: HTTPAuthCredentials = Depends(security)):
    token = credentials.credentials
    user = await verify_jwt(token)
    # ...
```

## Performance Metrics

| Operation | Typical Time |
|-----------|--------------|
| Get random lesson | 10-50ms |
| Save recording | 100-500ms |
| Update progress | 20-50ms |
| Viseme update (frontend) | <1ms |
| Animation frame rate | 60fps (16ms/frame) |

## Scaling Considerations

### Current Limitations

- Single RethinkDB instance
- No caching layer
- Files stored locally
- No user authentication

### To Scale

1. **Database**: Use RethinkDB cluster
2. **Cache**: Add Redis for frequently accessed lessons
3. **Storage**: Move uploads to S3/GCS
4. **Auth**: Implement JWT + user service
5. **CDN**: Host audio files on CDN
6. **Microservices**: Split services if needed
7. **Load Balancer**: Add reverse proxy (Nginx/Caddy)

---

Last Updated: December 2024
