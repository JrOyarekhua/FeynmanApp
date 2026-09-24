from sqlalchemy.orm import Session
from src.transcript.model import Transcript
from datetime import datetime 
from sqlalchemy import select, tuple_
from uuid import UUID
class TranscriptRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_transcript(self, transcript: Transcript) -> UUID:
        self.db.add(transcript)
        self.db.commit()
        self.db.refresh(transcript)
        return transcript.transcript_id

    def get_transcript_by_id(self, transcript_id: str) -> Transcript:
            return self.db.query(Transcript).filter(Transcript.transcript_id == transcript_id).first()

    def get_all_transcripts(self, session_id: str, cursor_created_at: datetime = None, cursor_id: str = None, limit: int = 10) -> list[Transcript]:
        query = select(Transcript).where(Transcript.session_id == session_id)

        if cursor_id and cursor_created_at:
            query = query.where(
                tuple_(Transcript.created_at, Transcript.transcript_id) < 
                tuple_(cursor_created_at, cursor_id)
            )

        query.order_by(Transcript.created_at.desc()).limit(limit)
        return self.db.execute(query).scalars().all()
    
    def update_transcript(self, transcript_id:str, content:str) -> Transcript:
        transcript = self.db.query(Transcript).filter(Transcript.transcript_id == transcript_id).first()
        if transcript:
            transcript.content = content
            self.db.commit()
            self.db.refresh(transcript)
        return transcript
    

    def delete_transcript(self, transcript_id: str) -> str:
        transcript = self.db.query(Transcript).filter(Transcript.transcript_id == transcript_id).first()
        if transcript:
            self.db.delete(transcript)
            self.db.commit()
            return transcript_id
        return None