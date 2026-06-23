from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def _payload() -> dict:
    return {
        "origin": "Mumbai",
        "destination": "Goa",
        "start_date": "2026-07-10",
        "end_date": "2026-07-12",
        "traveler_count": 2,
        "total_budget": 45000,
        "currency": "INR",
        "preferences": {
            "interests": ["beach", "food", "culture"],
            "pace": "balanced",
            "transport_preference": "any",
            "accommodation_tier": "mid_range",
            "indoor_outdoor": "any",
        },
    }


def test_create_get_events_and_revise_trip() -> None:
    with TestClient(app) as client:
        created = client.post("/api/v1/trips", json=_payload())
        assert created.status_code == 202
        trip_id = created.json()["trip_id"]

        fetched = client.get(f"/api/v1/trips/{trip_id}")
        assert fetched.status_code == 200
        body = fetched.json()
        assert body["status"] == "complete"
        assert body["plan"]["budget"]["total"] <= _payload()["total_budget"]

        with client.stream("GET", f"/api/v1/trips/{trip_id}/events") as response:
            text = "".join(response.iter_text())
        assert response.status_code == 200
        assert "plan.completed" in text
        assert text.count("event:") >= 5

        revised = client.post(f"/api/v1/trips/{trip_id}/revise", json={"instruction": "add more adventure"})
        assert revised.status_code == 200
        revised_body = revised.json()
        assert revised_body["plan"]["revision_history"]


def test_provider_and_destination_endpoints() -> None:
    with TestClient(app) as client:
        providers = client.get("/api/v1/providers/status")
        assert providers.status_code == 200
        assert providers.json()

        destinations = client.get("/api/v1/destinations/search?q=goa")
        assert destinations.status_code == 200
        assert destinations.json()[0]["name"] == "Goa"


def test_anonymous_trip_ownership_is_scoped() -> None:
    owner_headers = {"X-Anonymous-Session": "owner-session-token-1234567890"}
    other_headers = {"X-Anonymous-Session": "other-session-token-1234567890"}

    with TestClient(app) as client:
        created = client.post("/api/v1/trips", json=_payload(), headers=owner_headers)
        assert created.status_code == 202
        trip_id = created.json()["trip_id"]

        owner_list = client.get("/api/v1/trips", headers=owner_headers)
        assert owner_list.status_code == 200
        assert any(item["trip_id"] == trip_id for item in owner_list.json())

        other_list = client.get("/api/v1/trips", headers=other_headers)
        assert other_list.status_code == 200
        assert all(item["trip_id"] != trip_id for item in other_list.json())

        forbidden_get = client.get(f"/api/v1/trips/{trip_id}", headers=other_headers)
        assert forbidden_get.status_code == 404

        forbidden_revision = client.post(
            f"/api/v1/trips/{trip_id}/revise",
            json={"instruction": "add more adventure"},
            headers=other_headers,
        )
        assert forbidden_revision.status_code == 404

        allowed_get = client.get(f"/api/v1/trips/{trip_id}", headers=owner_headers)
        assert allowed_get.status_code == 200
