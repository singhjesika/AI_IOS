from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from app.config import settings
from app.database import init_db
from app.api.routes import user, task, ai


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🧠 AI-IOS starting up...")
    await init_db()
    logger.info("✅ Database initialized")
    yield
    logger.info("🛑 AI-IOS shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI Life Optimization System — Backend API",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Middleware ────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(user.router,  prefix="/api/v1/users",  tags=["users"])
app.include_router(task.router,  prefix="/api/v1/tasks",  tags=["tasks"])
app.include_router(ai.router,    prefix="/api/v1/ai",     tags=["ai"])


@app.get("/")
async def root():
    return {"message": "🧠 AI-IOS is running", "version": settings.VERSION}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}






