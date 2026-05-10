"""
Voice / speech routes.
"""
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.services.voice_service import VoiceService

router = APIRouter()


@router.post("/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Transcribe uploaded audio to text."""
    svc = VoiceService()
    audio_bytes = await audio.read()
    text = await svc.transcribe(audio_bytes)
    return {"transcript": text}


@router.post("/synthesize")
async def synthesize(
    text: str,
    current_user: User = Depends(get_current_active_user),
):
    """Convert text to speech (returns audio bytes)."""
    svc = VoiceService()
    audio = await svc.synthesize(text)
    return {"audio_base64": audio}