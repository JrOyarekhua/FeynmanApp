from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP, Uuid, JSON
from src.core.models.base import Base




class Evaluation(Base):
    __tablename__ = "evaluations"

    evaluation_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
        comment="Unique identifier for evaluation"
    )

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("sessions.session_id", ondelete="CASCADE"),
        nullable=False,
        comment="Session being evaluated"
    )

    evaluation_details: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        comment="AI evaluation output stored as JSON"
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now,
        comment="Timestamp when evaluation was generated"
    )

    session: Mapped["Session"] = relationship(
        back_populates="evaluations"
    )
