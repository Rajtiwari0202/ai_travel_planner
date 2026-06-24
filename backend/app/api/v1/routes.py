from __future__ import annotations

import json

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.agents.orchestrator import orchestrator
from app.core.config import get_settings
from app.db.session import SessionLocal, check_database, get_db
from app.models.trip_record import AgentEventRecord
from app.repositories.trips import create_trip, delete_trip, get_trip, list_events, list_trips, owns_trip, to_response
from app.schemas.trip import (
    AgentEvent,
    DestinationSearchResult,
    ProviderStatus,
    RevisionRequest,
    TripCreateResponse,
    TripRecordResponse,
    TripRequest,
    TripStatus,
)
from app.services.events import event_broker
from app.services.providers.catalog import provider_statuses, search_destinations

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "TravelAgenticAI"}


@router.get("/health/live")
async def health_live() -> dict[str, str]:
    return {"status": "ok", "service": "TravelAgenticAI"}


@router.get("/health/ready")
async def health_ready() -> dict[str, str]:
    try:
        check_database()
    except Exception as exc:  # pragma: no cover - defensive readiness guard
        raise HTTPException(status_code=503, detail="Database is not ready") from exc
    return {"status": "ready", "database": "ok"}


@router.get("/version")
async def version() -> dict[str, str]:
    settings = get_settings()
    return {"service": settings.app_name, "version": "1.1.0-dev", "environment": settings.environment}


@router.post("/trips", response_model=TripCreateResponse, status_code=202)
async def create_trip_endpoint(
    request: TripRequest,
    background_tasks: BackgroundTasks,
    anonymous_session: str | None = Header(default=None, alias="X-Anonymous-Session"),
    db: Session = Depends(get_db),
) -> TripCreateResponse:
    record = create_trip(db, request, owner_token=anonymous_session)
    background_tasks.add_task(orchestrator.plan_and_persist, record.trip_id, request)
    return TripCreateResponse(
        trip_id=record.trip_id,
        status=TripStatus.PLANNING,
        events_url=f"{get_settings().api_prefix}/trips/{record.trip_id}/events",
        message="Planning started. Subscribe to the events URL for progress.",
    )


@router.get("/trips", response_model=list[TripRecordResponse])
async def list_trip_records(
    anonymous_session: str | None = Header(default=None, alias="X-Anonymous-Session"),
    db: Session = Depends(get_db),
) -> list[TripRecordResponse]:
    return [to_response(record) for record in list_trips(db, anonymous_session)]


@router.get("/trips/{trip_id}", response_model=TripRecordResponse)
async def get_trip_record(
    trip_id: str,
    anonymous_session: str | None = Header(default=None, alias="X-Anonymous-Session"),
    db: Session = Depends(get_db),
) -> TripRecordResponse:
    record = get_trip(db, trip_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    if not owns_trip(record, anonymous_session):
        raise HTTPException(status_code=404, detail="Trip not found")
    return to_response(record)


@router.post("/trips/{trip_id}/revise", response_model=TripRecordResponse)
async def revise_trip(
    trip_id: str,
    revision: RevisionRequest,
    anonymous_session: str | None = Header(default=None, alias="X-Anonymous-Session"),
    db: Session = Depends(get_db),
) -> TripRecordResponse:
    record = get_trip(db, trip_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    if not owns_trip(record, anonymous_session):
        raise HTTPException(status_code=404, detail="Trip not found")
    await orchestrator.revise_and_persist(trip_id, revision)
    db.expire_all()
    refreshed = get_trip(db, trip_id)
    if refreshed is None:
        raise HTTPException(status_code=404, detail="Trip not found after revision")
    return to_response(refreshed)


@router.delete("/trips/{trip_id}", status_code=204, response_class=Response)
async def delete_trip_record(
    trip_id: str,
    anonymous_session: str | None = Header(default=None, alias="X-Anonymous-Session"),
    db: Session = Depends(get_db),
) -> Response:
    record = get_trip(db, trip_id)
    if record is None or not owns_trip(record, anonymous_session):
        raise HTTPException(status_code=404, detail="Trip not found")
    if not delete_trip(db, trip_id):
        raise HTTPException(status_code=404, detail="Trip not found")
    return Response(status_code=204)


def _sse_payload(event: AgentEvent, sequence: int | None = None) -> str:
    data = event.model_dump(mode="json")
    if sequence is not None:
        data["sequence"] = sequence
    return f"id: {event.event_id}\nevent: {event.event_type.value}\ndata: {json.dumps(data)}\n\n"


def _event_from_record(record: AgentEventRecord) -> AgentEvent:
    return AgentEvent.model_validate_json(record.event_json)


@router.get("/trips/{trip_id}/events")
async def stream_trip_events(
    trip_id: str,
    after: int = Query(default=0, ge=0),
    session: str | None = Query(default=None, min_length=16, max_length=256),
    anonymous_session: str | None = Header(default=None, alias="X-Anonymous-Session"),
    db: Session = Depends(get_db),
) -> StreamingResponse:
    record = get_trip(db, trip_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    owner_token = anonymous_session or session
    if not owns_trip(record, owner_token):
        raise HTTPException(status_code=404, detail="Trip not found")

    async def generator():
        last_sequence = after
        with SessionLocal() as event_db:
            for event_record in list_events(event_db, trip_id, after_sequence=last_sequence):
                last_sequence = event_record.sequence
                yield _sse_payload(_event_from_record(event_record), sequence=event_record.sequence)
            trip = get_trip(event_db, trip_id)
            if trip and trip.status in {TripStatus.COMPLETE.value, TripStatus.INFEASIBLE.value, TripStatus.FAILED.value}:
                return

        async for event in event_broker.subscribe(trip_id):
            if event is None:
                with SessionLocal() as poll_db:
                    trip = get_trip(poll_db, trip_id)
                    for event_record in list_events(poll_db, trip_id, after_sequence=last_sequence):
                        last_sequence = event_record.sequence
                        yield _sse_payload(_event_from_record(event_record), sequence=event_record.sequence)
                    if trip and trip.status in {TripStatus.COMPLETE.value, TripStatus.INFEASIBLE.value, TripStatus.FAILED.value}:
                        break
                yield ": keep-alive\n\n"
                continue
            yield _sse_payload(event)

    return StreamingResponse(generator(), media_type="text/event-stream")


@router.get("/providers/status", response_model=list[ProviderStatus])
async def providers_status() -> list[ProviderStatus]:
    return provider_statuses(get_settings().enable_live_weather)


@router.get("/destinations/search", response_model=list[DestinationSearchResult])
async def destinations_search(q: str | None = None) -> list[DestinationSearchResult]:
    return search_destinations(q)
