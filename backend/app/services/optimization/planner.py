from __future__ import annotations

from datetime import datetime, time, timedelta
from statistics import mean

from app.schemas.trip import (
    AccommodationOption,
    AlternativePlan,
    BudgetBreakdown,
    CandidateActivity,
    DataKind,
    DestinationOverview,
    IndoorOutdoorPreference,
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
from app.services.geospatial.distance import path_distance_km


def trip_dates(request: TripRequest) -> list:
    return [request.start_date + timedelta(days=offset) for offset in range(request.day_count)]


def max_activities_per_day(request: TripRequest) -> int:
    return {"relaxed": 1, "balanced": 2, "active": 3}[request.preferences.pace.value]


def _activity_score(request: TripRequest, activity: CandidateActivity, weather: WeatherForecast | None = None) -> float:
    interests = set(request.preferences.interests)
    tags = set(activity.tags + [activity.category])
    preference = 1.0 if not interests else min(1.0, len(interests & tags) / max(1, len(interests)))
    rating = activity.rating / 5
    indoor_fit = 1.0
    if request.preferences.indoor_outdoor == IndoorOutdoorPreference.MOSTLY_INDOOR and not activity.indoor:
        indoor_fit = 0.65
    if request.preferences.indoor_outdoor == IndoorOutdoorPreference.MOSTLY_OUTDOOR and activity.indoor:
        indoor_fit = 0.75
    weather_fit = 1.0
    if weather and "rain risk" in weather.suitability_tags and not activity.indoor:
        weather_fit = 0.55
    low_cost = 1 / (1 + activity.estimated_cost / 1500)
    return round(0.34 * preference + 0.26 * rating + 0.18 * indoor_fit + 0.12 * weather_fit + 0.10 * low_cost, 4)


def _allowed_activities(request: TripRequest, activities: list[CandidateActivity]) -> list[CandidateActivity]:
    excluded = set(request.preferences.excluded_activities)
    filtered = []
    for activity in activities:
        text = " ".join([activity.name, activity.category, *activity.tags]).lower()
        if any(exclusion in text for exclusion in excluded):
            continue
        filtered.append(activity)
    return filtered


def _budget_for_selection(
    request: TripRequest,
    transport: TransportOption,
    accommodation: AccommodationOption,
    activities: list[CandidateActivity],
) -> BudgetBreakdown:
    transport_total = round(transport.estimated_cost_per_person * request.traveler_count * 2, 2)
    accommodation_total = round(
        accommodation.nightly_price_per_room * request.assumed_rooms * request.night_count,
        2,
    )
    activities_total = round(sum(activity.estimated_cost for activity in activities) * request.traveler_count, 2)
    local_transport = round(350 * request.traveler_count * request.day_count, 2)
    food = round(800 * request.traveler_count * request.day_count, 2)
    taxes_and_fees = round(accommodation_total * 0.08, 2)
    subtotal = transport_total + accommodation_total + activities_total + local_transport + food + taxes_and_fees
    contingency = round(subtotal * 0.05, 2)
    total = round(subtotal + contingency, 2)
    return BudgetBreakdown(
        currency=request.currency,
        transport=transport_total,
        accommodation=accommodation_total,
        activities=activities_total,
        local_transport=local_transport,
        food=food,
        contingency=contingency,
        taxes_and_fees=taxes_and_fees,
        total=total,
        remaining=round(request.total_budget - total, 2),
        room_count=request.assumed_rooms,
        nights=request.night_count,
        assumptions=[
            "Transport estimate is modeled as a round trip per traveler.",
            "Accommodation is calculated per room per night using explicit room-count assumptions.",
            "Food, local transport, taxes, and contingency are deterministic estimates.",
        ],
    )


def _schedule_days(
    request: TripRequest,
    accommodation: AccommodationOption,
    selected: list[CandidateActivity],
    weather: list[WeatherForecast],
) -> list[TripDay]:
    days: list[TripDay] = []
    per_day = max_activities_per_day(request)
    cursor = 0
    for day_index, target in enumerate(trip_dates(request), start=1):
        day_activities = selected[cursor : cursor + per_day]
        cursor += per_day
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
                    rationale=f"Selected for {activity.category} fit, rating {activity.rating:.1f}, and route balance.",
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
    preference_scores = [_activity_score(request, activity) for activity in selected] or [0]
    preference_match = round(mean(preference_scores), 3)
    budget_fit = round(max(0, min(1, 1 - max(0, budget.total - request.total_budget) / request.total_budget)), 3)
    daily_distances = [day.estimated_local_distance_km for day in days]
    distance_efficiency = round(max(0, min(1, 1 - (mean(daily_distances) if daily_distances else 0) / 80)), 3)
    rain_conflicts = sum(
        1
        for day in days
        for activity in day.activities
        if "rain risk" in day.weather.suitability_tags and activity.data_kind != DataKind.FALLBACK and "indoor" not in activity.tags
    )
    weather_fit = round(max(0, 1 - rain_conflicts / max(1, sum(len(day.activities) for day in days))), 3)
    categories = {activity.category for activity in selected}
    diversity = round(min(1, len(categories) / max(1, len(selected))), 3)
    accommodation_quality = round(accommodation.rating / 5, 3)
    total = round(
        0.25 * preference_match
        + 0.25 * budget_fit
        + 0.15 * distance_efficiency
        + 0.13 * weather_fit
        + 0.12 * diversity
        + 0.10 * accommodation_quality,
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


def _alternatives(
    request: TripRequest,
    transports: list[TransportOption],
    accommodations: list[AccommodationOption],
    selected: list[CandidateActivity],
) -> list[AlternativePlan]:
    alternatives: list[AlternativePlan] = []
    for transport in transports[:2]:
        for accommodation in accommodations[:2]:
            budget = _budget_for_selection(request, transport, accommodation, selected[: max(1, len(selected) - 1)])
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
    if len(plan.days) != plan.request.day_count:
        errors.append("Day count does not match request dates.")
    seen: set[str] = set()
    for day in plan.days:
        if not day.activities:
            warnings.append(f"{day.date}: no scheduled activities after constraints were applied.")
        for activity in day.activities:
            if activity.activity_id in seen:
                errors.append(f"Duplicate activity selected: {activity.title}.")
            seen.add(activity.activity_id)
            if activity.location.latitude == 0 and activity.location.longitude == 0:
                errors.append(f"Missing usable coordinates for {activity.title}.")
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
) -> TripPlan:
    allowed = _allowed_activities(request, activities)
    if not allowed:
        allowed = activities[:]
    weather_by_date = {item.date: item for item in weather}
    scored = sorted(
        allowed,
        key=lambda activity: _activity_score(request, activity, weather_by_date.get(request.start_date)),
        reverse=True,
    )
    capacity = request.day_count * max_activities_per_day(request)

    best_payload = None
    for transport in sorted(transports, key=lambda item: item.estimated_cost_per_person):
        for accommodation in sorted(accommodations, key=lambda item: item.nightly_price_per_room):
            for count in range(min(capacity, len(scored)), 0, -1):
                selected = scored[:count]
                budget = _budget_for_selection(request, transport, accommodation, selected)
                days = _schedule_days(request, accommodation, selected, weather)
                score = _score_breakdown(request, accommodation, selected, budget, days)
                feasible = budget.total <= request.total_budget
                candidate = (feasible, score.total_score, budget.remaining, transport, accommodation, selected, budget, days, score)
                if feasible:
                    best_payload = candidate
                    break
            if best_payload:
                break
        if best_payload:
            break

    if best_payload is None:
        transport = min(transports, key=lambda item: item.estimated_cost_per_person)
        accommodation = min(accommodations, key=lambda item: item.nightly_price_per_room)
        selected = scored[: min(1, len(scored))]
        budget = _budget_for_selection(request, transport, accommodation, selected)
        days = _schedule_days(request, accommodation, [], weather)
        score = _score_breakdown(request, accommodation, [], budget, days)
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

    _, _, _, transport, accommodation, selected, budget, days, score = best_payload
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
        alternatives=_alternatives(request, transports, accommodations, selected),
        validation=ValidationReport(status="passed"),
        assumptions=[
            "No booking or payment is performed.",
            "Transport cost is estimated as a round trip per traveler.",
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
