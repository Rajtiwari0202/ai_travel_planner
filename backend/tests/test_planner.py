from __future__ import annotations

import asyncio

from app.core.config import get_settings
from app.schemas.trip import GeoPoint, TripRequest, TripStatus
from app.services.budgeting.money import budget_reconciles, calculate_budget
from app.services.geospatial.distance import haversine_km
from app.services.optimization.planner import build_plan, trip_dates
from app.services.providers.catalog import (
    get_accommodation_options,
    get_candidate_activities,
    get_destination_overview,
    get_transport_options,
)
from app.services.weather.service import get_weather_forecasts


def test_haversine_distance_is_reasonable() -> None:
    mumbai = GeoPoint(latitude=19.0760, longitude=72.8777)
    goa = GeoPoint(latitude=15.2993, longitude=74.1240)

    assert 430 <= haversine_km(mumbai, goa) <= 470


def test_planner_returns_budget_feasible_plan() -> None:
    request = TripRequest(
        origin="Mumbai",
        destination="Goa",
        start_date="2026-07-10",
        end_date="2026-07-12",
        traveler_count=2,
        total_budget=45000,
        preferences={"interests": ["beach", "food", "culture"], "pace": "balanced"},
    )
    destination = get_destination_overview(request.destination)
    weather = asyncio.run(get_weather_forecasts(get_settings(), destination.center, trip_dates(request)))
    plan = build_plan(
        "test-trip",
        request,
        destination,
        get_transport_options(request, destination),
        get_accommodation_options(request, destination),
        get_candidate_activities(request.destination),
        weather,
    )

    assert plan.status == TripStatus.COMPLETE
    assert plan.budget.total <= request.total_budget
    assert budget_reconciles(plan.budget)
    assert plan.optimizer.engine == "ortools_cp_sat"
    assert plan.optimizer.binding_constraints
    assert plan.optimizer.rejected_candidates
    assert len(plan.days) == 3
    assert all(activity.location.latitude for day in plan.days for activity in day.activities)


def test_planner_reports_infeasible_budget() -> None:
    request = TripRequest(
        origin="Chennai",
        destination="Manali",
        start_date="2026-09-12",
        end_date="2026-09-16",
        traveler_count=2,
        total_budget=12000,
        preferences={"interests": ["adventure"], "pace": "active"},
    )
    destination = get_destination_overview(request.destination)
    weather = asyncio.run(get_weather_forecasts(get_settings(), destination.center, trip_dates(request)))
    plan = build_plan(
        "test-infeasible",
        request,
        destination,
        get_transport_options(request, destination),
        get_accommodation_options(request, destination),
        get_candidate_activities(request.destination),
        weather,
    )

    assert plan.status == TripStatus.INFEASIBLE
    assert plan.validation.errors


def test_budget_model_uses_rooms_not_travelers() -> None:
    request = TripRequest(
        origin="Delhi",
        destination="Jaipur",
        start_date="2026-08-05",
        end_date="2026-08-08",
        traveler_count=4,
        rooms=2,
        total_budget=65000,
        preferences={"interests": ["history"], "pace": "balanced"},
    )
    destination = get_destination_overview(request.destination)
    transport = get_transport_options(request, destination)[0]
    accommodation = get_accommodation_options(request, destination)[0]
    budget = calculate_budget(request, transport, accommodation, [])

    assert budget.room_count == 2
    assert budget.nights == 3
    assert budget.accommodation == accommodation.nightly_price_per_room * 2 * 3
    assert budget.accommodation != accommodation.nightly_price_per_room * request.traveler_count * 3
    assert budget_reconciles(budget)


def test_same_day_trip_is_supported() -> None:
    request = TripRequest(
        origin="Bengaluru",
        destination="Kochi",
        start_date="2026-10-20",
        end_date="2026-10-20",
        traveler_count=1,
        total_budget=22000,
        preferences={"interests": ["culture", "art"], "pace": "relaxed", "transport_preference": "bus"},
    )
    destination = get_destination_overview(request.destination)
    weather = asyncio.run(get_weather_forecasts(get_settings(), destination.center, trip_dates(request)))
    plan = build_plan(
        "same-day",
        request,
        destination,
        get_transport_options(request, destination),
        get_accommodation_options(request, destination),
        get_candidate_activities(request.destination),
        weather,
    )

    assert plan.status == TripStatus.COMPLETE
    assert len(plan.days) == 1
    assert plan.budget.nights == 1
    assert sum(len(day.activities) for day in plan.days) <= 1


def test_weather_aware_optimizer_rejects_outdoor_rain_conflicts() -> None:
    request = TripRequest(
        origin="Mumbai",
        destination="Goa",
        start_date="2026-07-10",
        end_date="2026-07-12",
        traveler_count=2,
        total_budget=45000,
        preferences={"interests": ["beach", "food", "culture"], "pace": "balanced", "indoor_outdoor": "mostly_indoor"},
    )
    destination = get_destination_overview(request.destination)
    weather = asyncio.run(get_weather_forecasts(get_settings(), destination.center, trip_dates(request)))
    plan = build_plan(
        "rain-aware",
        request,
        destination,
        get_transport_options(request, destination),
        get_accommodation_options(request, destination),
        get_candidate_activities(request.destination),
        weather,
    )

    assert all("rain risk" not in day.weather.suitability_tags or all("indoor" in activity.tags for activity in day.activities) for day in plan.days)
    assert any("rain risk conflicts" in reason for reason in plan.optimizer.rejected_candidates)


def test_weather_ablation_allows_outdoor_rain_conflicts() -> None:
    request = TripRequest(
        origin="Mumbai",
        destination="Goa",
        start_date="2026-07-10",
        end_date="2026-07-12",
        traveler_count=2,
        total_budget=45000,
        preferences={"interests": ["beach", "food", "culture"], "pace": "balanced"},
    )
    destination = get_destination_overview(request.destination)
    weather = asyncio.run(get_weather_forecasts(get_settings(), destination.center, trip_dates(request)))
    plan = build_plan(
        "rain-ablation",
        request,
        destination,
        get_transport_options(request, destination),
        get_accommodation_options(request, destination),
        get_candidate_activities(request.destination),
        weather,
        mode="cp_sat_no_weather",
    )

    assert plan.status == TripStatus.COMPLETE
    assert plan.optimizer.method == "cp_sat_no_weather"
    assert any("indoor" not in activity.tags for day in plan.days for activity in day.activities)
