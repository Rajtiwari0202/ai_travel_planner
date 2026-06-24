from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.session import SessionLocal, init_db
from app.repositories.trips import create_trip
from app.schemas.trip import TripRequest


def main() -> None:
    init_db()
    request = TripRequest(
        origin="Mumbai",
        destination="Goa",
        start_date="2026-07-10",
        end_date="2026-07-12",
        traveler_count=2,
        total_budget=45000,
        currency="INR",
    )
    with SessionLocal() as db:
        record = create_trip(db, request, owner_token="demo-seed-token")
        print(f"seeded_trip_id={record.trip_id}")


if __name__ == "__main__":
    main()
