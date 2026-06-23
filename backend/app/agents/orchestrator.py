from __future__ import annotations

import logging
from time import perf_counter

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.repositories.trips import require_trip, update_trip_plan, update_trip_status
from app.schemas.trip import (
    AgentEvent,
    AgentName,
    EventType,
    IndoorOutdoorPreference,
    RevisionRecord,
    RevisionRequest,
    TripPlan,
    TripRequest,
    TripStatus,
)
from app.services.events import event_broker
from app.services.narrative.providers import TemplateLLMProvider
from app.services.optimization.planner import build_plan, trip_dates
from app.services.providers.catalog import (
    get_accommodation_options,
    get_candidate_activities,
    get_destination_overview,
    get_transport_options,
)
from app.services.weather.service import get_weather_forecasts

logger = logging.getLogger(__name__)


class TripOrchestrator:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.narrative_provider = TemplateLLMProvider()

    async def emit(
        self,
        trip_id: str,
        event_type: EventType,
        stage: str,
        message: str,
        agent: AgentName | None = None,
        progress: int | None = None,
        metadata: dict | None = None,
    ) -> None:
        await event_broker.publish(
            AgentEvent(
                trip_id=trip_id,
                event_type=event_type,
                agent=agent,
                stage=stage,
                message=message,
                progress=progress,
                metadata=metadata or {},
            )
        )

    async def plan_and_persist(self, trip_id: str, request: TripRequest) -> None:
        started = perf_counter()
        try:
            await self.emit(trip_id, EventType.PLAN_STARTED, "planning", "Trip planning started.", progress=0)

            await self.emit(
                trip_id,
                EventType.AGENT_STARTED,
                "intent",
                "Validating dates, travelers, budget, and preferences.",
                AgentName.INTENT,
                5,
            )
            await self.emit(
                trip_id,
                EventType.AGENT_COMPLETED,
                "intent",
                f"Request spans {request.day_count} day(s) and {request.night_count} night(s).",
                AgentName.INTENT,
                10,
                {"days": request.day_count, "rooms": request.assumed_rooms},
            )

            await self.emit(
                trip_id,
                EventType.AGENT_STARTED,
                "destination",
                "Loading destination context and activity candidates.",
                AgentName.DESTINATION,
                18,
            )
            destination = get_destination_overview(request.destination)
            activities = get_candidate_activities(request.destination)
            await self.emit(
                trip_id,
                EventType.AGENT_COMPLETED,
                "destination",
                f"Loaded {len(activities)} candidate activities for {destination.name}.",
                AgentName.DESTINATION,
                28,
            )

            await self.emit(
                trip_id,
                EventType.AGENT_STARTED,
                "transport",
                "Estimating transparent transport options.",
                AgentName.TRANSPORT,
                34,
            )
            transports = get_transport_options(request, destination)
            await self.emit(
                trip_id,
                EventType.AGENT_COMPLETED,
                "transport",
                f"Prepared {len(transports)} estimated transport option(s).",
                AgentName.TRANSPORT,
                42,
            )

            await self.emit(
                trip_id,
                EventType.AGENT_STARTED,
                "accommodation",
                "Estimating accommodation options with room-count assumptions.",
                AgentName.ACCOMMODATION,
                47,
            )
            accommodations = get_accommodation_options(request, destination)
            await self.emit(
                trip_id,
                EventType.AGENT_COMPLETED,
                "accommodation",
                f"Prepared {len(accommodations)} accommodation estimate(s).",
                AgentName.ACCOMMODATION,
                54,
            )

            await self.emit(
                trip_id,
                EventType.AGENT_STARTED,
                "weather",
                "Aligning weather guidance to itinerary dates.",
                AgentName.WEATHER,
                60,
            )
            weather = await get_weather_forecasts(self.settings, destination.center, trip_dates(request))
            await self.emit(
                trip_id,
                EventType.AGENT_COMPLETED,
                "weather",
                "Weather data aligned to trip dates.",
                AgentName.WEATHER,
                68,
                {"live_days": sum(1 for item in weather if item.forecast_available)},
            )

            await self.emit(
                trip_id,
                EventType.AGENT_STARTED,
                "optimization",
                "Optimizing budget-feasible schedule and route balance.",
                AgentName.OPTIMIZATION,
                75,
            )
            plan = build_plan(trip_id, request, destination, transports, accommodations, activities, weather)
            await self.emit(
                trip_id,
                EventType.OPTIMIZATION_COMPLETED,
                "optimization",
                f"Optimization completed with status {plan.status.value}.",
                AgentName.OPTIMIZATION,
                84,
                {"score": plan.score.total_score, "total_cost": plan.budget.total},
            )

            await self.emit(
                trip_id,
                EventType.AGENT_STARTED,
                "writer",
                "Writing grounded itinerary summary.",
                AgentName.WRITER,
                88,
            )
            plan.narrative_summary = await self.narrative_provider.generate_text(plan)
            await self.emit(
                trip_id,
                EventType.AGENT_COMPLETED,
                "writer",
                "Narrative summary generated from structured facts.",
                AgentName.WRITER,
                92,
            )

            await self.emit(
                trip_id,
                EventType.VALIDATION_COMPLETED,
                "critic",
                f"Validation finished with {plan.validation.status} status.",
                AgentName.CRITIC,
                96,
                {"errors": len(plan.validation.errors), "warnings": len(plan.validation.warnings)},
            )
            with SessionLocal() as db:
                update_trip_plan(db, trip_id, plan)

            await self.emit(
                trip_id,
                EventType.PLAN_COMPLETED,
                "complete",
                "Trip plan saved.",
                progress=100,
                metadata={"duration_ms": round((perf_counter() - started) * 1000, 2)},
            )
        except Exception as exc:  # pragma: no cover - defensive safety path
            logger.exception("planning_failed", extra={"trip_id": trip_id})
            with SessionLocal() as db:
                update_trip_status(db, trip_id, TripStatus.FAILED)
            await self.emit(
                trip_id,
                EventType.PLAN_FAILED,
                "failed",
                "Planning failed safely. Check server logs for the sanitized failure category.",
                progress=100,
                metadata={"error_type": type(exc).__name__},
            )

    async def revise_and_persist(self, trip_id: str, revision: RevisionRequest) -> TripPlan:
        with SessionLocal() as db:
            record = require_trip(db, trip_id)
            request = TripRequest.model_validate_json(record.request_json)
            previous = TripPlan.model_validate_json(record.plan_json) if record.plan_json else None

        instruction = revision.instruction.lower()
        changes: list[str] = []
        if "adventure" in instruction:
            interests = sorted({*request.preferences.interests, "adventure", "outdoor"})
            request = request.model_copy(update={"preferences": request.preferences.model_copy(update={"interests": interests})})
            changes.append("Added adventure and outdoor preference signals.")
        if "indoor" in instruction or "rain" in instruction:
            request = request.model_copy(
                update={
                    "preferences": request.preferences.model_copy(
                        update={"indoor_outdoor": IndoorOutdoorPreference.MOSTLY_INDOOR}
                    )
                }
            )
            changes.append("Prioritized indoor-friendly activities.")
        budget_numbers = [
            int(token.replace(",", ""))
            for token in instruction.replace(chr(0x20B9), " ").split()
            if token.replace(",", "").isdigit()
        ]
        if budget_numbers:
            request = request.model_copy(update={"total_budget": float(budget_numbers[0])})
            changes.append(f"Updated max budget to {request.currency} {budget_numbers[0]:,}.")
        if not changes:
            changes.append("Replanned with the existing constraints and recorded the revision request.")

        await self.emit(
            trip_id,
            EventType.AGENT_STARTED,
            "revision",
            "Applying revision to the previous structured itinerary.",
            AgentName.REVISION,
            10,
        )
        destination = get_destination_overview(request.destination)
        activities = get_candidate_activities(request.destination)
        transports = get_transport_options(request, destination)
        accommodations = get_accommodation_options(request, destination)
        weather = await get_weather_forecasts(self.settings, destination.center, trip_dates(request))
        plan = build_plan(trip_id, request, destination, transports, accommodations, activities, weather)
        if previous:
            previous_version_id = (
                previous.revision_history[-1].new_version_id if previous.revision_history else f"{trip_id}:initial"
            )
            previous_day_activity_ids = {
                day.date: [activity.activity_id for activity in day.activities]
                for day in previous.days
            }
            affected_days = [
                day.date
                for day in plan.days
                if previous_day_activity_ids.get(day.date) != [activity.activity_id for activity in day.activities]
            ]
            previous_warnings = set(previous.validation.warnings)
            plan.revision_history = [
                *previous.revision_history,
                RevisionRecord(
                    instruction=revision.instruction,
                    changes=changes,
                    previous_version_id=previous_version_id,
                    requested_change=revision.instruction,
                    actual_changes=changes,
                    cost_difference=round(plan.budget.total - previous.budget.total, 2),
                    score_difference=round(plan.score.total_score - previous.score.total_score, 3),
                    affected_days=affected_days,
                    new_warnings=[warning for warning in plan.validation.warnings if warning not in previous_warnings],
                    unchanged_constraints=plan.optimizer.binding_constraints,
                ),
            ]
        plan.narrative_summary = await self.narrative_provider.generate_text(plan)

        with SessionLocal() as db:
            record = require_trip(db, trip_id)
            record.request_json = request.model_dump_json()
            db.add(record)
            db.commit()
            update_trip_plan(db, trip_id, plan)
        await self.emit(
            trip_id,
            EventType.AGENT_COMPLETED,
            "revision",
            "Revision completed and saved.",
            AgentName.REVISION,
            100,
            {"changes": changes},
        )
        return plan


orchestrator = TripOrchestrator()
