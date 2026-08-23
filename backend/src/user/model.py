
from __future__ import annotations
from uuid import UUID, uuid4
from datetime import datetime
from src.core.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, TIMESTAMP, Uuid, Text, JSON

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
        comment="Unique identifier for user"
    )

    auth_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="authentication id used in jwt tokens"
    )

    first_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="User first name"
    )

    last_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="User last name"
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        comment="User email address"
    )


    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now,
        comment="Timestamp when user was created"
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now,
        onupdate=datetime.now,
        comment="Timestamp when user was last updated"
    )

    # One user can have many sessions
    sessions: Mapped[list["Session"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )