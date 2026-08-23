from src.core.models import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.types import Text, Uuid, TIMESTAMP, Enum
from uuid import UUID, uuid4
from datetime import datetime

class Transcript(Base):
    __tablename__ = "transcripts"

    transcript_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
        comment="Unique identifier for a transcript"
    )

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey('sessions.session_id', ondelete='CASCADE'),
        primary_key=True,
        nullable=False,
        comment='Session which oens this transcript'
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment='content of the transcript'
    )

    # status: Mapped[str] = mapped_column(
    # )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now,
        comment='Timestamp the transcript was created'
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now,
        onupdate=datetime.now,
        comment='Timestamp the transcript was last updated'
    )
    

    session: Mapped["Session"] = relationship(
        back_populates='transcript'
    )