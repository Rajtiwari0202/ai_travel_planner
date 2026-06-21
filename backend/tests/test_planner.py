from __future__ import annotations

import asyncio

from app.core.config import get_settings
from app.schemas.trip import GeoPoint, TripRequest, TripStatus
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
