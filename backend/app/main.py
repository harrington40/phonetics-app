from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
# from slowapi import _rate_limit_exceeded_handler
# from slowapi.errors import RateLimitExceeded
from app.db.connection import db
from app.routes.lessons import router as lessons_router
from app.routes.learning import router as learning_router
from app.routes.admin import router as admin_router
from app.routes.teacher import router as teacher_router
from app.routes.license import router as license_router
from app.routes.payment import router as payment_router
from app.routes.tracking import router as tracking_router
from app.routes.auth import router as auth_router
from app.services.lesson_service import LessonService
from app.db.database import init_db, close_db
# from app.middleware.security import limiter, add_security_headers
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    try:
        await init_db()  # Initialize PostgreSQL tables
        print("✓ Database initialized")
    except Exception as e:
        print(f"⚠️  Database initialization skipped: {e}")
    
    print("✓ Application startup complete")
    
    yield
    
    # Shutdown
    await close_db()
    print("✓ Application shutdown complete")

app = FastAPI(
    title="PhonicsLearn API",
    description="AI-driven phonetics lesson orchestration with licensing, payments & analytics",
    version="2.0.0",
    lifespan=lifespan,
)

# Add rate limiter state (commented out until dependencies installed)
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security: CORS middleware (allow all origins for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Security: Trusted host middleware (prevent host header attacks)
trusted_hosts = os.getenv("TRUSTED_HOSTS", "*").split(",")
if trusted_hosts != ["*"]:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=trusted_hosts)

# Security headers middleware
@app.middleware("http")
async def add_security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# HTTPS redirect (production only)
if os.getenv("FORCE_HTTPS", "false").lower() == "true":
    @app.middleware("http")
    async def https_redirect(request: Request, call_next):
        if request.url.scheme != "https" and request.headers.get("x-forwarded-proto") != "https":
            url = request.url.replace(scheme="https")
            return JSONResponse(
                status_code=301,
                content={"message": "Redirecting to HTTPS"},
                headers={"Location": str(url)}
            )
        return await call_next(request)

# Include routers
app.include_router(auth_router)  # Authentication (login/register)
app.include_router(lessons_router)
app.include_router(learning_router)
app.include_router(admin_router)
app.include_router(teacher_router)
app.include_router(license_router)
app.include_router(payment_router)
app.include_router(tracking_router)

@app.get("/")
async def root():
    return {
        "message": "Phonetics Orchestrator API",
        "docs": "/docs",
        "health": "/api/health",
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
