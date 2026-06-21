from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.schemas.trip import TripRequest


def test_trip_request_calculates_days_nights_and_rooms() -> None:
    request = TripRequest(
        origin="Mumbai",
        destination="Goa",
        start_date="2026-07-10",
        end_date="2026-07-12",
        traveler_count=3,
        total_budget=50000,
    )

    assert request.day_count == 3
    assert request.night_count == 2
    assert request.assumed_rooms == 2


def test_trip_request_rejects_reversed_dates() -> None:
    with pytest.raises(ValidationError):
        TripRequest(
            origin="Mumbai",
            destination="Goa",
            start_date="2026-07-12",
            end_date="2026-07-10",
            traveler_count=2,
            total_budget=50000,
        )
