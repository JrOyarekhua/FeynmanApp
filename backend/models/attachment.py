from uuid import UUID, uuid4
from datetime import datetime
from models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, TIMESTAMP, Uuid



class Attachment(Base):
    __tablename__ = "attachments"

    attachment_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
        comment="Unique identifier for attachment"
    )

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("sessions.session_id", ondelete="CASCADE"),
        nullable=False,
        comment="Session this attachment belongs to",
    )

    attachment_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Type of attachment (audio, pdf, image, etc.)"
    )

    storage_loc: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="Object storage path/location"
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now,
        comment="Timestamp when attachment was uploaded"
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now,
        onupdate=datetime.now,
        comment="Timestamp when attachment metadata changed"
    )

    session: Mapped["Session"] = relationship(
        back_populates="attachments"
    )

