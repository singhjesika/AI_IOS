"""
AI_IOS - FastAPI Entry Point
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text

from database import init_db, engine
from app.config.settings import settings
from app.api.routes import auth, user, ai, task, finance, health, planner, voice, analytics
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup & shutdown events."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    import os
    logger.info(f"GROQ KEY LOADED: {bool(os.getenv('GROQ_API_KEY'))}")
    await init_db()
    logger.info("Database initialised")
    yield
    logger.info("Shutting down...")
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered personal assistant backend",
    lifespan=lifespan,
)

# ─── CORS ──────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ───────────────────────────────────────────
app.include_router(auth.router,      prefix="/api/auth",      tags=["Auth"])
app.include_router(user.router,      prefix="/api/user",      tags=["User"])
app.include_router(ai.router,        prefix="/api/ai",        tags=["AI"])
app.include_router(task.router,      prefix="/api/tasks",     tags=["Tasks"])
app.include_router(finance.router,   prefix="/api/finance",   tags=["Finance"])
app.include_router(health.router,    prefix="/api/health",    tags=["Health"])
app.include_router(planner.router,   prefix="/api/planner",   tags=["Planner"])
app.include_router(voice.router,     prefix="/api/voice",     tags=["Voice"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])

from fastapi import Request
from fastapi.responses import JSONResponse
import httpx

@app.post("/api/chat", tags=["AI"])
async def chat_proxy(request: Request):
    try:
        body = await request.json()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {body.get('api_key')}"
                },
                json=body.get('payload'),
                timeout=30.0
            )
        return JSONResponse(content=response.json(), status_code=response.status_code)
    except Exception as e:
        return JSONResponse(content={"error":{"message":str(e)}}, status_code=500)

@app.get("/", tags=["Root"])
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}", "version": settings.APP_VERSION}


@app.get("/health", tags=["Root"])
async def health_check():
    db_status = "disconnected"
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "version": "1.0.0",
        "database": db_status,
        "agents": ["finance", "health", "planner"],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)