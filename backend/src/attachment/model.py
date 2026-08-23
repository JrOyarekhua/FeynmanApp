from uuid import UUID, uuid4
from datetime import datetime
from src.core.models import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, TIMESTAMP, Uuid, Enum
from src.core.enums import AttachmentType, MimeType


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

    attachment_type: Mapped[AttachmentType] = mapped_column(
        Enum(AttachmentType, 
             values_callable=lambda enum_cols: [c.value for c in enum_cols]),
        nullable=False,
        comment="Type of attachment (audio, pdf, image, etc.)"
    )

    mime_type: Mapped[str] = mapped_column(
        Enum(
            MimeType, 
            values_callable=lambda enum_cols: [c.value for c in enum_cols]
        ),
        nullable=False,
        comment="Label telling other systems the format of a file"
    )

    storage_loc: Mapped[str] = mapped_column(
        String(255),
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

