from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class TripRecord(Base):
    __tablename__ = "trip_records"

    trip_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    request_json: Mapped[str] = mapped_column(Text)
    plan_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
    )

    events: Mapped[list[AgentEventRecord]] = relationship(
        back_populates="trip",
        cascade="all, delete-orphan",
        order_by="AgentEventRecord.sequence",
    )


class AgentEventRecord(Base):
    __tablename__ = "agent_event_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trip_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("trip_records.trip_id", ondelete="CASCADE"),
        index=True,
    )
    sequence: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    event_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    trip: Mapped[TripRecord] = relationship(back_populates="events")


Index("ix_agent_event_trip_sequence", AgentEventRecord.trip_id, AgentEventRecord.sequence)
