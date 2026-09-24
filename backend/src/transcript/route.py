from uuid import UUID

from fastapi.routing import APIRouter
from fastapi import HTTPException, Depends, UploadFile
from src.api.dependencies.auth import authorize_user
from src.api.dependencies.services import get_transcript_service
from src.transcript.schema import TranscriptResponse, AllTranscriptsResponse
from src.transcript.service import TranscriptService
from src.transcript.model import Transcript


transcript_router = APIRouter(
    prefix="/api/sessions/{session_id}/transcripts",
    tags=["transcripts"],
    dependencies=[Depends(authorize_user)]
)

@transcript_router.get("/", summary="Get all transcripts for a session", response_model=AllTranscriptsResponse)
def get_all_transcripts(session_id: str, cursor: str = None, limit: int = 10, service: TranscriptService = Depends(get_transcript_service)):
    return service.get_all_transcripts(session_id=session_id, cursor=cursor, limit=limit)

@transcript_router.get("/{transcript_id}", summary="Get transcript by ID", response_model=TranscriptResponse)
def get_transcript(transcript_id: str, service: TranscriptService = Depends(get_transcript_service)):
    return service.get_transcript_by_id(transcript_id=transcript_id)

@transcript_router.post("/", summary="Create transcript for a session")
async def create_transcript(session_id: str, audio:UploadFile, service: TranscriptService = Depends(get_transcript_service)):
    data = await audio.read()
    return {"transcript_id":service.generate_transcript(session_id=session_id, audio=data)}

@transcript_router.patch("/{transcript_id}", summary="Update transcript for a session")
async def update_transcript(transcript_id: str, audio:UploadFile, service: TranscriptService = Depends(get_transcript_service)):
    data = await audio.read()
    return service.update_transcript(transcript_id=transcript_id, audio=data)

@transcript_router.delete("/{transcript_id}", summary="Delete transcript for a session")
def delete_transcript(transcript_id: str, service: TranscriptService = Depends(get_transcript_service)):
    return service.delete_transcript(transcript_id=transcript_id)
