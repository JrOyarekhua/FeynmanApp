from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, TIMESTAMP, Uuid, Text
from models.base import Base



class Topic(Base):
    __tablename__ = "topics"

    topic_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
        comment="Unique identifier for topic"
    )

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("sessions.session_id", ondelete="CASCADE"),
        nullable=False,
        comment="Session this topic belongs to"
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="AI generated Topic name"
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        comment="AI generated topic summary"
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now,
        comment="Timestamp when topic was created"
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now,
        onupdate=datetime.now,
        comment="Timestamp when topic was last updated"
    )

    session: Mapped["Session"] = relationship(
        back_populates="topics"
    )
