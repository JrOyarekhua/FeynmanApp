from __future__ import annotations
from uuid import UUID, uuid4
from datetime import datetime
from src.core.models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP, Uuid, Text, JSON


class Session(Base):
    __tablename__ = "sessions"

    session_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
        comment="Unique identifier for learning session"
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        comment="User who owns this session"
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now,
        comment="Timestamp when session was created"
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now,
        onupdate=datetime.now,
        comment="Timestamp when session was last updated"
    )

    # Relationship to owner
    user: Mapped["User"] = relationship(
        back_populates="sessions"
    )

    # Session owns topics
    topics: Mapped[list["Topic"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan"
    )

    # Session owns evaluations
    evaluations: Mapped[list["Evaluation"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan"
    )

    # Session owns attachments
    attachments: Mapped[list["Attachment"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan"
    )

    # session owns transcripts 
    transcript: Mapped["Transcript"] = relationship(
        back_populates='session',
        cascade='all, delete-orphan'
    )