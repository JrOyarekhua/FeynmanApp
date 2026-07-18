from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import String, TIMESTAMP, Uuid, Text, JSON


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
        comment="Unique identifier for user"
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


class Session(Base):
    __tablename__ = "sessions"

    session_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
        comment="Unique identifier for learning session"
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
        comment="User who owns this session"
    )

    transcript: Mapped[str | None] = mapped_column(
        Text,
        comment="Generated transcript from uploaded recording"
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


class Topic(Base):
    __tablename__ = "topics"

    topic_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
        comment="Unique identifier for topic"
    )

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("sessions.session_id"),
        nullable=False,
        comment="Session this topic belongs to"
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Topic name"
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


class Evaluation(Base):
    __tablename__ = "evaluations"

    evaluation_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
        comment="Unique identifier for evaluation"
    )

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("sessions.session_id"),
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


class Attachment(Base):
    __tablename__ = "attachments"

    attachment_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
        comment="Unique identifier for attachment"
    )

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("sessions.session_id"),
        nullable=False,
        comment="Session this attachment belongs to"
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

