from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from statistics import mean
from typing import Any, Literal

from app.schemas.trip import (
    AccommodationOption,
    AlternativePlan,
    BudgetBreakdown,
    CandidateActivity,
    DestinationOverview,
    IndoorOutdoorPreference,
    OptimizerMetadata,
    ScheduledActivity,
    ScoreBreakdown,
    TransportOption,
    TripDay,
    TripPlan,
    TripRequest,
    TripStatus,
    ValidationReport,
    WeatherForecast,
)
from app.services.budgeting.money import budget_reconciles, calculate_budget, money
from app.services.geospatial.distance import haversine_km, path_distance_km

_cp_model: Any
try:  # pragma: no cover - exercised when the optional solver is installed.
    from ortools.sat.python import cp_model as _cp_model
except ImportError:  # pragma: no cover - fallback environments still work.
    _cp_model = None

cp_model: Any = _cp_model


OptimizerMode = Literal[
    "proposed_multi_agent",
    "cheapest_first",
    "weighted_ranking",
    "cp_sat_no_weather",
    "cp_sat_no_geospatial",
]


@dataclass(slots=True)
class OptimizationOutcome:
    selected_by_date: dict[date, list[CandidateActivity]]
    selected: list[CandidateActivity]
    method: str
    engine: str
    rejected_candidates: list[str] = field(default_factory=list)
    binding_constraints: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    alternatives_considered: int = 0

    @property
    def feasible(self) -> bool:
        return bool(self.selected)


def trip_dates(request: TripRequest) -> list[date]:
    return [request.start_date + timedelta(days=offset) for offset in range(request.day_count)]


def max_activities_per_day(request: TripRequest) -> int:
    return {"relaxed": 1, "balanced": 2, "active": 3}[request.preferences.pace.value]


def _available_minutes_per_day(request: TripRequest) -> int:
    return {"relaxed": 390, "balanced": 510, "active": 630}[request.preferences.pace.value]


def _weather_aware(mode: OptimizerMode) -> bool:
    return mode != "cp_sat_no_weather"


def _geospatial_aware(mode: OptimizerMode) -> bool:
    return mode != "cp_sat_no_geospatial"


def _is_rain_invalid(activity: CandidateActivity, weather: WeatherForecast | None, weather_aware: bool) -> bool:
    return weather_aware and weather is not None and "rain risk" in weather.suitability_tags and not activity.indoor


def _activity_score(
    request: TripRequest,
    activity: CandidateActivity,
    weather: WeatherForecast | None = None,
    accommodation: AccommodationOption | None = None,
    *,
    weather_aware: bool = True,
    geospatial_aware: bool = True,
) -> float:
    interests = set(request.preferences.interests)
    tags = set(activity.tags + [activity.category])
    preference = 1.0 if not interests else min(1.0, len(interests & tags) / max(1, len(interests)))
    rating = activity.rating / 5
    indoor_fit = 1.0
    if request.preferences.indoor_outdoor == IndoorOutdoorPreference.MOSTLY_INDOOR and not activity.indoor:
        indoor_fit = 0.55
    if request.preferences.indoor_outdoor == IndoorOutdoorPreference.MOSTLY_OUTDOOR and activity.indoor:
        indoor_fit = 0.72
    weather_fit = 0.2 if _is_rain_invalid(activity, weather, weather_aware) else 1.0
    low_cost = 1 / (1 + activity.estimated_cost / 1500)
    source_confidence = activity.source.confidence
    distance_fit = 1.0
    if geospatial_aware and accommodation is not None:
        distance_fit = max(0.0, min(1.0, 1 - haversine_km(accommodation.location, activity.location) / 90))
    return round(
        0.28 * preference
        + 0.18 * rating
        + 0.13 * indoor_fit
        + 0.13 * weather_fit
        + 0.10 * low_cost
        + 0.10 * source_confidence
        + 0.08 * distance_fit,
        4,
    )


def _allowed_activities(request: TripRequest, activities: list[CandidateActivity]) -> tuple[list[CandidateActivity], list[str]]:
    excluded = set(request.preferences.excluded_activities)
    rejected: list[str] = []
    filtered: list[CandidateActivity] = []
    for activity in activities:
        text = " ".join([activity.name, activity.category, *activity.tags]).lower()
        if any(exclusion in text for exclusion in excluded):
            rejected.append(f"{activity.name}: rejected by user exclusion.")
            continue
        if activity.location.latitude == 0 and activity.location.longitude == 0:
            rejected.append(f"{activity.name}: rejected because coordinates are missing.")
            continue
        if request.preferences.accessibility and any("not accessible" in note.lower() for note in activity.accessibility_notes):
            rejected.append(f"{activity.name}: rejected by accessibility constraint.")
            continue
        filtered.append(activity)
    return filtered, rejected


def _daily_activity_cost_cents(request: TripRequest, activity: CandidateActivity) -> int:
    return int(money(activity.estimated_cost * request.traveler_count) * Decimal("100"))


def _base_subtotal_cents(request: TripRequest, transport: TransportOption, accommodation: AccommodationOption) -> int:
    base = calculate_budget(request, transport, accommodation, [])
    subtotal = (
        money(base.transport)
        + money(base.accommodation)
        + money(base.local_transport)
        + money(base.food)
        + money(base.taxes_and_fees)
    )
    return int(subtotal * Decimal("100"))


def _cp_sat_outcome(
    request: TripRequest,
    accommodation: AccommodationOption,
    transport: TransportOption,
    activities: list[CandidateActivity],
    weather: list[WeatherForecast],
    mode: OptimizerMode,
    inherited_rejections: list[str],
) -> OptimizationOutcome | None:
    if cp_model is None or mode in {"cheapest_first", "weighted_ranking"}:
        return None

    dates = trip_dates(request)
    weather_by_date = {item.date: item for item in weather}
    model = cp_model.CpModel()
    variables: dict[tuple[int, int], Any] = {}
    rejected = inherited_rejections[:]
    weather_aware = _weather_aware(mode)
    geospatial_aware = _geospatial_aware(mode)

    for activity_index, activity in enumerate(activities):
        for day_index, target_date in enumerate(dates):
            var = model.NewBoolVar(f"a_{activity_index}_d_{day_index}")
            variables[(activity_index, day_index)] = var
            if _is_rain_invalid(activity, weather_by_date.get(target_date), weather_aware):
                model.Add(var == 0)
                rejected.append(f"{activity.name} on {target_date}: rejected because rain risk conflicts with outdoor activity.")

    for activity_index in range(len(activities)):
        model.Add(sum(variables[(activity_index, day_index)] for day_index in range(len(dates))) <= 1)

    for day_index in range(len(dates)):
        day_vars = [variables[(activity_index, day_index)] for activity_index in range(len(activities))]
        model.Add(sum(day_vars) <= max_activities_per_day(request))
        model.Add(
            sum(
                (activities[activity_index].estimated_duration_minutes + 75) * variables[(activity_index, day_index)]
                for activity_index in range(len(activities))
            )
            <= _available_minutes_per_day(request)
        )

    base_subtotal_cents = _base_subtotal_cents(request, transport, accommodation)
    activity_cost_terms = [
        _daily_activity_cost_cents(request, activity) * variables[(activity_index, day_index)]
        for activity_index, activity in enumerate(activities)
        for day_index in range(len(dates))
    ]
    # Total budget is modeled as (base subtotal + selected activity costs) plus a 5% contingency.
    model.Add(105 * (base_subtotal_cents + sum(activity_cost_terms)) <= int(money(request.total_budget) * Decimal("10000")))

    objective_terms = []
    for activity_index, activity in enumerate(activities):
        for day_index, target_date in enumerate(dates):
            score = _activity_score(
                request,
                activity,
                weather_by_date.get(target_date),
                accommodation,
                weather_aware=weather_aware,
                geospatial_aware=geospatial_aware,
            )
            distance_penalty = haversine_km(accommodation.location, activity.location) / 120 if geospatial_aware else 0
            coefficient = max(1, int(10000 * (score + 0.18 - 0.12 * distance_penalty)))
            objective_terms.append(coefficient * variables[(activity_index, day_index)])
    model.Maximize(sum(objective_terms))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 0.5
    solver.parameters.num_search_workers = 1
    status = solver.Solve(model)
    if status not in {cp_model.OPTIMAL, cp_model.FEASIBLE}:
        return None

    selected_by_date: dict[date, list[CandidateActivity]] = {target_date: [] for target_date in dates}
    selected_ids: set[str] = set()
    for activity_index, activity in enumerate(activities):
        for day_index, target_date in enumerate(dates):
            if solver.Value(variables[(activity_index, day_index)]) == 1:
                selected_by_date[target_date].append(activity)
                selected_ids.add(activity.id)

    selected = [activity for target_date in dates for activity in selected_by_date[target_date]]
    for activity in activities:
        if activity.id not in selected_ids:
            rejected.append(f"{activity.name}: not selected after objective, budget, time, weather, and route tradeoffs.")
    if not selected:
        return None

    return OptimizationOutcome(
        selected_by_date=selected_by_date,
        selected=selected,
        method=mode,
        engine="ortools_cp_sat",
        rejected_candidates=rejected,
        binding_constraints=[
            "total estimated cost <= requested budget",
            "activity assigned to at most one day",
            "daily activity count cap",
            "daily duration with travel and meal buffers",
            "weather-invalid outdoor activities rejected when weather-aware",
        ],
        assumptions=[
            "CP-SAT solves deterministic integer scheduling; no LLM performs arithmetic or constraint enforcement.",
            "Daily travel burden is represented through geospatial objective penalties and validation warnings.",
        ],
        alternatives_considered=len(activities) * len(dates),
    )


def _heuristic_outcome(
    request: TripRequest,
    accommodation: AccommodationOption,
    transport: TransportOption,
    activities: list[CandidateActivity],
    weather: list[WeatherForecast],
    mode: OptimizerMode,
    inherited_rejections: list[str],
) -> OptimizationOutcome:
    dates = trip_dates(request)
    weather_by_date = {item.date: item for item in weather}
    selected_by_date: dict[date, list[CandidateActivity]] = {target_date: [] for target_date in dates}
    selected: list[CandidateActivity] = []
    rejected = inherited_rejections[:]
    remaining = activities[:]
    weather_aware = _weather_aware(mode)
    geospatial_aware = _geospatial_aware(mode)

    for target_date in dates:
        used_minutes = 0
        while len(selected_by_date[target_date]) < max_activities_per_day(request):
            feasible: list[CandidateActivity] = []
            for activity in remaining:
                if used_minutes + activity.estimated_duration_minutes + 75 > _available_minutes_per_day(request):
                    continue
                if _is_rain_invalid(activity, weather_by_date.get(target_date), weather_aware):
                    rejected.append(f"{activity.name} on {target_date}: rejected because rain risk conflicts with outdoor activity.")
                    continue
                candidate_selection = [*selected, activity]
                if calculate_budget(request, transport, accommodation, candidate_selection).total > request.total_budget:
                    rejected.append(f"{activity.name}: rejected because adding it would exceed the requested budget.")
                    continue
                feasible.append(activity)
            if not feasible:
                break
            if mode == "cheapest_first":
                choice = min(feasible, key=lambda item: (item.estimated_cost, -item.rating))
            else:
                choice = max(
                    feasible,
                    key=lambda item: _activity_score(
                        request,
                        item,
                        weather_by_date.get(target_date),
                        accommodation,
                        weather_aware=weather_aware,
                        geospatial_aware=geospatial_aware,
                    ),
                )
            selected.append(choice)
            selected_by_date[target_date].append(choice)
            remaining = [activity for activity in remaining if activity.id != choice.id]
            used_minutes += choice.estimated_duration_minutes + 75

    for activity in remaining:
        rejected.append(f"{activity.name}: not selected by {mode} due to budget, capacity, or lower score.")

    return OptimizationOutcome(
        selected_by_date=selected_by_date,
        selected=selected,
        method=mode,
        engine="deterministic_heuristic",
        rejected_candidates=rejected,
        binding_constraints=[
            "total estimated cost <= requested budget",
            "no duplicate activity selection",
            "daily activity count cap",
            "daily duration with travel and meal buffers",
        ],
        assumptions=["Heuristic fallback is deterministic and uses the same candidate set and budget model as CP-SAT."],
        alternatives_considered=len(activities) * len(dates),
    )


def _optimize_activities(
    request: TripRequest,
    accommodation: AccommodationOption,
    transport: TransportOption,
    activities: list[CandidateActivity],
    weather: list[WeatherForecast],
    mode: OptimizerMode,
) -> OptimizationOutcome:
    allowed, rejected = _allowed_activities(request, activities)
    if not allowed:
        return OptimizationOutcome(
            selected_by_date={target_date: [] for target_date in trip_dates(request)},
            selected=[],
            method=mode,
            engine="none",
            rejected_candidates=rejected or ["No activities remained after hard constraints."],
            binding_constraints=["exclusions and coordinate validity"],
            assumptions=["No activities were scheduled because the candidate set was empty after hard constraints."],
        )
    outcome = _cp_sat_outcome(request, accommodation, transport, allowed, weather, mode, rejected)
    if outcome is not None:
        return outcome
    return _heuristic_outcome(request, accommodation, transport, allowed, weather, mode, rejected)


def _budget_for_selection(
    request: TripRequest,
    transport: TransportOption,
    accommodation: AccommodationOption,
    activities: list[CandidateActivity],
) -> BudgetBreakdown:
    return calculate_budget(request, transport, accommodation, activities)


def _schedule_days(
    request: TripRequest,
    accommodation: AccommodationOption,
    selected_by_date: dict[date, list[CandidateActivity]],
    weather: list[WeatherForecast],
) -> list[TripDay]:
    days: list[TripDay] = []
    for day_index, target in enumerate(trip_dates(request), start=1):
        day_activities = selected_by_date.get(target, [])
        scheduled: list[ScheduledActivity] = []
        start_dt = datetime.combine(target, time(hour=9, minute=30))
        weather_for_day = next(item for item in weather if item.date == target)
        for activity in day_activities:
            end_dt = start_dt + timedelta(minutes=activity.estimated_duration_minutes)
            scheduled.append(
                ScheduledActivity(
                    activity_id=activity.id,
                    title=activity.name,
                    date=target,
                    start_time=start_dt.time(),
                    end_time=end_dt.time(),
                    duration_minutes=activity.estimated_duration_minutes,
                    estimated_cost=round(activity.estimated_cost * request.traveler_count, 2),
                    location=activity.location,
                    category=activity.category,
                    tags=activity.tags,
                    source_label=activity.source.source,
                    data_kind=activity.source.data_kind,
                    rationale=f"Selected for {activity.category} fit, rating {activity.rating:.1f}, source confidence {activity.source.confidence:.2f}, and route/budget balance.",
                    weather_note=weather_for_day.condition,
                )
            )
            start_dt = end_dt + timedelta(minutes=75)
        points = [accommodation.location, *[activity.location for activity in day_activities], accommodation.location]
        days.append(
            TripDay(
                date=target,
                title=f"Day {day_index}: {request.destination} plan",
                weather=weather_for_day,
                activities=scheduled,
                estimated_local_distance_km=round(path_distance_km(points), 2),
                daily_cost=round(sum(item.estimated_cost for item in scheduled), 2),
                notes=["Meal and local-transfer buffers are included between scheduled activities."],
            )
        )
    return days


def _score_breakdown(
    request: TripRequest,
    accommodation: AccommodationOption,
    selected: list[CandidateActivity],
    budget: BudgetBreakdown,
    days: list[TripDay],
) -> ScoreBreakdown:
    weather_by_date = {day.date: day.weather for day in days}
    preference_scores = [_activity_score(request, activity, weather_by_date.get(request.start_date), accommodation) for activity in selected] or [0]
    preference_match = round(mean(preference_scores), 3)
    budget_fit = round(max(0, min(1, 1 - max(0, budget.total - request.total_budget) / request.total_budget)), 3)
    daily_distances = [day.estimated_local_distance_km for day in days]
    distance_efficiency = round(max(0, min(1, 1 - (mean(daily_distances) if daily_distances else 0) / 80)), 3)
    rain_conflicts = sum(
        1
        for day in days
        for activity in day.activities
        if "rain risk" in day.weather.suitability_tags and "indoor" not in activity.tags
    )
    activity_count = sum(len(day.activities) for day in days)
    weather_fit = round(max(0, 1 - rain_conflicts / max(1, activity_count)), 3)
    categories = {activity.category for activity in selected}
    diversity = round(min(1, len(categories) / max(1, len(selected))), 3)
    accommodation_quality = round(accommodation.rating / 5, 3)
    total = round(
        0.24 * preference_match
        + 0.22 * budget_fit
        + 0.16 * distance_efficiency
        + 0.14 * weather_fit
        + 0.12 * diversity
        + 0.12 * accommodation_quality,
        3,
    )
    return ScoreBreakdown(
        total_score=total,
        preference_match=preference_match,
        budget_fit=budget_fit,
        distance_efficiency=distance_efficiency,
        weather_fit=weather_fit,
        diversity=diversity,
        accommodation_quality=accommodation_quality,
        explanation=[
            "Score combines preference match, budget fit, distance efficiency, weather suitability, diversity, and stay quality.",
            "Costs and feasibility are deterministic; narrative generation cannot override them.",
        ],
    )


def _optimizer_metadata(outcome: OptimizationOutcome, score: ScoreBreakdown, budget: BudgetBreakdown, request: TripRequest) -> OptimizerMetadata:
    constraints = outcome.binding_constraints[:]
    if budget.remaining <= max(500, request.total_budget * 0.05):
        constraints.append("budget is binding or nearly binding")
    selected_count = len(outcome.selected)
    if selected_count >= request.day_count * max_activities_per_day(request):
        constraints.append("daily activity capacity is binding")
    return OptimizerMetadata(
        method=outcome.method,
        engine=outcome.engine,
        objective_score=score.total_score,
        normalized_score_breakdown={
            "preference_match": score.preference_match,
            "budget_fit": score.budget_fit,
            "distance_efficiency": score.distance_efficiency,
            "weather_fit": score.weather_fit,
            "diversity": score.diversity,
            "accommodation_quality": score.accommodation_quality,
        },
        binding_constraints=constraints,
        rejected_candidates=outcome.rejected_candidates[:30],
        assumptions=outcome.assumptions,
        feasibility_status="feasible" if outcome.engine == "ortools_cp_sat" else "fallback_feasible",
        alternatives_considered=outcome.alternatives_considered,
    )


def _alternatives(
    request: TripRequest,
    transports: list[TransportOption],
    accommodations: list[AccommodationOption],
    selected: list[CandidateActivity],
) -> list[AlternativePlan]:
    alternatives: list[AlternativePlan] = []
    for transport in transports[:3]:
        for accommodation in accommodations[:3]:
            budget = _budget_for_selection(request, transport, accommodation, selected[: max(1, len(selected) - 1)])
            if budget.total > request.total_budget * 1.2:
                continue
            alternatives.append(
                AlternativePlan(
                    label=f"{transport.mode.title()} + {accommodation.tier.value.replace('_', ' ')}",
                    summary=f"Estimated total {request.currency} {budget.total:,.0f} with {accommodation.name}.",
                    total_cost=budget.total,
                    score=max(0.15, min(0.95, 1 - max(0, budget.total - request.total_budget) / max(1, request.total_budget))),
                    tradeoffs=["Different transport/stay tradeoff", "Activity count may change to preserve budget"],
                )
            )
    unique: dict[str, AlternativePlan] = {}
    for alternative in sorted(alternatives, key=lambda item: item.score, reverse=True):
        unique.setdefault(alternative.label, alternative)
    return list(unique.values())[:2]


def validate_plan(plan: TripPlan) -> ValidationReport:
    errors: list[str] = []
    warnings: list[str] = []
    if plan.budget.total > plan.request.total_budget:
        errors.append("Budget total exceeds the requested maximum budget.")
    if not budget_reconciles(plan.budget):
        errors.append("Budget components do not reconcile to the reported total.")
    if len(plan.days) != plan.request.day_count:
        errors.append("Day count does not match request dates.")
    if plan.budget.nights != plan.request.night_count:
        errors.append("Accommodation nights do not match request dates.")
    if plan.budget.room_count != plan.request.assumed_rooms:
        errors.append("Room count does not match traveler/occupancy assumptions.")
    seen: set[str] = set()
    for day in plan.days:
        if day.date < plan.request.start_date or day.date > plan.request.end_date:
            errors.append(f"{day.date}: scheduled outside trip date range.")
        if len(day.activities) > max_activities_per_day(plan.request):
            errors.append(f"{day.date}: too many activities for requested pace.")
        if day.estimated_local_distance_km > 120:
            warnings.append(f"{day.date}: local travel distance is high; consider a slower day.")
        if not day.activities:
            warnings.append(f"{day.date}: no scheduled activities after constraints were applied.")
        previous_end: time | None = None
        for activity in day.activities:
            if activity.activity_id in seen:
                errors.append(f"Duplicate activity selected: {activity.title}.")
            seen.add(activity.activity_id)
            if activity.location.latitude == 0 and activity.location.longitude == 0:
                errors.append(f"Missing usable coordinates for {activity.title}.")
            if activity.start_time >= activity.end_time:
                errors.append(f"Invalid time window for {activity.title}.")
            if previous_end and activity.start_time < previous_end:
                errors.append(f"Activity time collision on {day.date}: {activity.title}.")
            if "rain risk" in day.weather.suitability_tags and "indoor" not in activity.tags:
                warnings.append(f"{day.date}: {activity.title} is outdoor-friendly but rain risk is present.")
            previous_end = activity.end_time
    return ValidationReport(
        status="failed" if errors else "warning" if warnings else "passed",
        errors=errors,
        warnings=warnings,
    )


def build_plan(
    trip_id: str,
    request: TripRequest,
    destination: DestinationOverview,
    transports: list[TransportOption],
    accommodations: list[AccommodationOption],
    activities: list[CandidateActivity],
    weather: list[WeatherForecast],
    mode: OptimizerMode = "proposed_multi_agent",
) -> TripPlan:
    best_payload = None
    combinations_considered = 0
    for transport in transports:
        for accommodation in accommodations:
            combinations_considered += 1
            outcome = _optimize_activities(request, accommodation, transport, activities, weather, mode)
            budget = _budget_for_selection(request, transport, accommodation, outcome.selected)
            days = _schedule_days(request, accommodation, outcome.selected_by_date, weather)
            score = _score_breakdown(request, accommodation, outcome.selected, budget, days)
            feasible = budget.total <= request.total_budget and bool(outcome.selected)
            if not feasible:
                continue
            candidate = (score.total_score, budget.remaining, transport, accommodation, outcome, budget, days, score)
            if best_payload is None or candidate[:2] > best_payload[:2]:
                best_payload = candidate

    if best_payload is None:
        transport = min(transports, key=lambda item: item.estimated_cost_per_person)
        accommodation = min(accommodations, key=lambda item: item.nightly_price_per_room)
        empty_by_date: dict[date, list[CandidateActivity]] = {target: [] for target in trip_dates(request)}
        budget = _budget_for_selection(request, transport, accommodation, [])
        days = _schedule_days(request, accommodation, empty_by_date, weather)
        score = _score_breakdown(request, accommodation, [], budget, days)
        outcome = OptimizationOutcome(
            selected_by_date=empty_by_date,
            selected=[],
            method=mode,
            engine="ortools_cp_sat" if cp_model is not None and mode not in {"cheapest_first", "weighted_ranking"} else "deterministic_heuristic",
            rejected_candidates=["No candidate set satisfied budget, duration, weather, and preference constraints."],
            binding_constraints=["total estimated cost <= requested budget", "daily activity count cap", "daily duration with buffers"],
            assumptions=["The solver returned no feasible activity schedule under the current budget and fixed trip costs."],
            alternatives_considered=combinations_considered,
        )
        plan = TripPlan(
            trip_id=trip_id,
            status=TripStatus.INFEASIBLE,
            request=request,
            destination=destination,
            transport=transport,
            accommodation=accommodation,
            days=days,
            budget=budget,
            score=score,
            optimizer=_optimizer_metadata(outcome, score, budget, request).model_copy(update={"feasibility_status": "infeasible"}),
            alternatives=_alternatives(request, transports, accommodations, []),
            validation=ValidationReport(
                status="failed",
                errors=["No budget-feasible itinerary found with transport, lodging, food, local transport, and contingency."],
                warnings=["Try increasing budget, reducing duration, changing transport, or choosing a budget stay."],
            ),
            assumptions=[
                "No booking or payment is performed.",
                "Estimated data is used for transport and accommodation.",
            ],
            data_disclaimers=[
                "Transport and accommodation prices are estimates, not live availability.",
                "Weather may be fallback guidance when live forecast is unavailable.",
            ],
            narrative_summary="The request is currently infeasible under the deterministic budget model.",
        )
        return plan

    _, _, transport, accommodation, outcome, budget, days, score = best_payload
    plan = TripPlan(
        trip_id=trip_id,
        status=TripStatus.COMPLETE,
        request=request,
        destination=destination,
        transport=transport,
        accommodation=accommodation,
        days=days,
        budget=budget,
        score=score,
        optimizer=_optimizer_metadata(outcome, score, budget, request),
        alternatives=_alternatives(request, transports, accommodations, outcome.selected),
        validation=ValidationReport(status="passed"),
        assumptions=[
            "No booking or payment is performed.",
            "Transport cost is estimated as outbound plus return per traveler.",
            "Accommodation cost uses room count rather than multiplying room price by travelers.",
            "All coordinates are supplied by the backend from curated/open-data inspired datasets.",
        ],
        data_disclaimers=[
            "Estimated flight/train/bus price",
            "Estimated accommodation price",
            "Public/open-data inspired attraction coordinates",
            "Live weather only when enabled; otherwise fallback guidance is labeled",
        ],
        narrative_summary="",
    )
    plan.validation = validate_plan(plan)
    return plan
