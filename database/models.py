
from datetime import datetime, timezone

from sqlalchemy import (
    DateTime, ForeignKey, Integer, String, Text
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    device_uid: Mapped[str] = mapped_column(
        String(100), unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )


class Connection(Base):
    __tablename__ = "connections"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id")
    )
    connected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    disconnected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(20), default="connected"
    )


class MessageRecord(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    message_uid: Mapped[str] = mapped_column(
        String(36), unique=True, index=True
    )
    connection_id: Mapped[int] = mapped_column(
        ForeignKey("connections.id")
    )
    message_type: Mapped[str] = mapped_column(String(30))
    payload: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
