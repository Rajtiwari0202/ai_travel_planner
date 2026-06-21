from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.trip_record import AgentEventRecord, TripRecord
from app.schemas.trip import AgentEvent, TripPlan, TripRecordResponse, TripRequest, TripStatus


def create_trip(db: Session, request: TripRequest, trip_id: str | None = None) -> TripRecord:
    record = TripRecord(
        trip_id=trip_id or str(uuid4()),
        status=TripStatus.PLANNING.value,
        request_json=request.model_dump_json(),
        plan_json=None,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_trip(db: Session, trip_id: str) -> TripRecord | None:
    return db.get(TripRecord, trip_id)


def list_trips(db: Session) -> list[TripRecord]:
    stmt = select(TripRecord).order_by(TripRecord.created_at.desc()).limit(50)
    return list(db.scalars(stmt))


def to_response(record: TripRecord) -> TripRecordResponse:
    return TripRecordResponse(
        trip_id=record.trip_id,
        status=TripStatus(record.status),
        request=TripRequest.model_validate_json(record.request_json),
        plan=TripPlan.model_validate_json(record.plan_json) if record.plan_json else None,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


def update_trip_plan(db: Session, trip_id: str, plan: TripPlan) -> TripRecord:
    record = require_trip(db, trip_id)
    record.plan_json = plan.model_dump_json()
    record.status = plan.status.value
    record.updated_at = datetime.now(UTC)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_trip_status(db: Session, trip_id: str, status: TripStatus) -> TripRecord:
    record = require_trip(db, trip_id)
    record.status = status.value
    record.updated_at = datetime.now(UTC)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def delete_trip(db: Session, trip_id: str) -> bool:
    record = get_trip(db, trip_id)
    if record is None:
        return False
    record.status = TripStatus.DELETED.value
    db.delete(record)
    db.commit()
    return True


def append_event(db: Session, event: AgentEvent) -> AgentEventRecord:
    max_sequence = db.scalar(
        select(func.max(AgentEventRecord.sequence)).where(AgentEventRecord.trip_id == event.trip_id)
    )
    record = AgentEventRecord(
        trip_id=event.trip_id,
        sequence=(max_sequence or 0) + 1,
        event_id=event.event_id,
        event_json=event.model_dump_json(),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_events(db: Session, trip_id: str, after_sequence: int = 0) -> list[AgentEventRecord]:
    stmt = (
        select(AgentEventRecord)
        .where(AgentEventRecord.trip_id == trip_id)
        .where(AgentEventRecord.sequence > after_sequence)
        .order_by(AgentEventRecord.sequence)
    )
    return list(db.scalars(stmt))


def require_trip(db: Session, trip_id: str) -> TripRecord:
    record = get_trip(db, trip_id)
    if record is None:
        raise KeyError(f"Trip not found: {trip_id}")
    return record
