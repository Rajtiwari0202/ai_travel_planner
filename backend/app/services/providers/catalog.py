from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.schemas.trip import (
    AccommodationOption,
    AccommodationTier,
    CandidateActivity,
    DataKind,
    DestinationOverview,
    DestinationSearchResult,
    GeoPoint,
    ProviderMetadata,
    ProviderStatus,
    TransportOption,
    TransportPreference,
    TripRequest,
)
from app.services.geospatial.distance import haversine_km

KNOWN_ORIGINS: dict[str, GeoPoint] = {
    "mumbai": GeoPoint(latitude=19.0760, longitude=72.8777),
    "delhi": GeoPoint(latitude=28.6139, longitude=77.2090),
    "bengaluru": GeoPoint(latitude=12.9716, longitude=77.5946),
    "bangalore": GeoPoint(latitude=12.9716, longitude=77.5946),
    "pune": GeoPoint(latitude=18.5204, longitude=73.8567),
    "chennai": GeoPoint(latitude=13.0827, longitude=80.2707),
    "kolkata": GeoPoint(latitude=22.5726, longitude=88.3639),
}


DESTINATIONS: dict[str, dict[str, Any]] = {
    "goa": {
        "name": "Goa",
        "country": "India",
        "center": GeoPoint(latitude=15.2993, longitude=74.1240),
        "summary": "A coastal destination known for beaches, Portuguese-era streets, spice farms, markets, and relaxed food culture.",
        "best_for": ["beaches", "food", "relaxation", "nightlife", "water sports"],
        "activities": [
            ("goa-fort-aguada", "Fort Aguada", "history", ["history", "views", "heritage"], 120, 150, 4.4, False, 15.4920, 73.7732, "Open-air Portuguese-era fort with sea-facing views."),
            ("goa-fontainhas", "Fontainhas Heritage Walk", "culture", ["culture", "food", "walking"], 150, 600, 4.6, False, 15.4989, 73.8278, "Colorful Latin Quarter lanes and local cafes."),
            ("goa-spice-farm", "Ponda Spice Farm Visit", "nature", ["nature", "food", "family"], 180, 900, 4.3, False, 15.4032, 74.0156, "Guided spice plantation visit with lunch options."),
            ("goa-museum", "Museum of Goa", "art", ["art", "indoor", "culture"], 120, 300, 4.2, True, 15.5607, 73.8012, "Indoor contemporary art and cultural exhibits."),
            ("goa-kayak", "Mandovi Kayaking", "adventure", ["adventure", "water", "outdoor"], 120, 1600, 4.5, False, 15.5007, 73.8347, "Guided backwater kayaking for active travelers."),
            ("goa-beach", "Miramar Beach Sunset", "relaxation", ["beach", "relaxation", "outdoor"], 90, 0, 4.1, False, 15.4811, 73.8078, "Low-cost sunset pause near Panaji."),
        ],
    },
    "jaipur": {
        "name": "Jaipur",
        "country": "India",
        "center": GeoPoint(latitude=26.9124, longitude=75.7873),
        "summary": "A heritage-rich city with forts, markets, museums, textile crafts, and Rajasthani cuisine.",
        "best_for": ["history", "culture", "shopping", "food", "architecture"],
        "activities": [
            ("jaipur-amber", "Amber Fort", "history", ["history", "architecture", "views"], 180, 500, 4.7, False, 26.9855, 75.8513, "Large hilltop fort complex with courtyards and city views."),
            ("jaipur-city-palace", "City Palace Museum", "culture", ["culture", "indoor", "history"], 120, 700, 4.5, True, 26.9258, 75.8237, "Museum and palace complex in the old city."),
            ("jaipur-jantar", "Jantar Mantar", "science", ["history", "science", "outdoor"], 90, 200, 4.4, False, 26.9248, 75.8246, "UNESCO-listed astronomical instruments."),
            ("jaipur-bazaar", "Johari Bazaar Walk", "shopping", ["shopping", "food", "walking"], 120, 300, 4.2, False, 26.9217, 75.8267, "Jewelry, textiles, snacks, and old-city street scenes."),
            ("jaipur-craft", "Block Printing Workshop", "craft", ["art", "culture", "indoor"], 150, 1200, 4.6, True, 26.8897, 75.8086, "Hands-on textile printing session."),
            ("jaipur-nahargarh", "Nahargarh Sunset Point", "views", ["views", "outdoor", "relaxation"], 120, 100, 4.5, False, 26.9373, 75.8153, "Ridge-top city viewpoint."),
        ],
    },
    "kochi": {
        "name": "Kochi",
        "country": "India",
        "center": GeoPoint(latitude=9.9312, longitude=76.2673),
        "summary": "A port city blending historic Fort Kochi, backwaters, art spaces, seafood, and ferry-linked neighborhoods.",
        "best_for": ["culture", "food", "water", "history", "art"],
        "activities": [
            ("kochi-fort-walk", "Fort Kochi Heritage Walk", "culture", ["culture", "history", "walking"], 150, 400, 4.6, False, 9.9656, 76.2422, "Historic streets, churches, and colonial-era buildings."),
            ("kochi-biennale", "Kochi Art Venues", "art", ["art", "indoor", "culture"], 120, 300, 4.4, True, 9.9667, 76.2429, "Independent galleries and contemporary art spaces."),
            ("kochi-ferry", "Local Ferry Circuit", "water", ["water", "local", "relaxation"], 120, 80, 4.2, False, 9.9679, 76.2526, "Low-cost public ferry ride through harbor channels."),
            ("kochi-spice-market", "Mattancherry Spice Market", "food", ["food", "shopping", "culture"], 120, 250, 4.1, True, 9.9576, 76.2596, "Spice shops and old trading lanes."),
            ("kochi-kathakali", "Kathakali Performance", "performance", ["culture", "indoor", "family"], 120, 500, 4.5, True, 9.9650, 76.2420, "Classical performance with make-up demonstration."),
            ("kochi-backwater", "Backwater Canoe Trip", "nature", ["nature", "water", "outdoor"], 180, 1500, 4.6, False, 9.8490, 76.3180, "Guided village-waterway canoe loop."),
        ],
    },
    "manali": {
        "name": "Manali",
        "country": "India",
        "center": GeoPoint(latitude=32.2432, longitude=77.1892),
        "summary": "A Himalayan base for valleys, temples, cafes, short treks, mountain views, and adventure activities.",
        "best_for": ["adventure", "nature", "mountains", "cafes", "relaxation"],
        "activities": [
            ("manali-hadimba", "Hadimba Devi Temple", "culture", ["culture", "nature", "walking"], 90, 50, 4.5, False, 32.2484, 77.1806, "Cedar forest temple close to Old Manali."),
            ("manali-old-town", "Old Manali Cafe Walk", "food", ["food", "walking", "relaxation"], 120, 600, 4.2, False, 32.2527, 77.1782, "Cafes, lanes, and river views."),
            ("manali-vashisht", "Vashisht Hot Springs", "relaxation", ["relaxation", "culture", "wellness"], 120, 100, 4.1, True, 32.2621, 77.1881, "Hot spring area and temple lanes."),
            ("manali-solang", "Solang Valley Adventure", "adventure", ["adventure", "outdoor", "views"], 180, 1800, 4.4, False, 32.3160, 77.1570, "Adventure operators and valley views."),
            ("manali-jogini", "Jogini Falls Trek", "nature", ["nature", "adventure", "outdoor"], 180, 200, 4.6, False, 32.2716, 77.1868, "Moderate short trek to waterfall views."),
            ("manali-museum", "Himachal Culture Museum", "history", ["history", "indoor", "culture"], 90, 100, 4.0, True, 32.2473, 77.1814, "Small indoor folk-culture exhibit."),
        ],
    },
}


def _provider(source: str, data_kind: DataKind, confidence: float = 0.8, notes: str | None = None) -> ProviderMetadata:
    return ProviderMetadata(
        source=source,
        data_kind=data_kind,
        fetched_at=datetime.now(UTC),
        confidence=confidence,
        notes=notes,
    )


def normalize_destination_name(name: str) -> str:
    return name.strip().lower()


def get_destination_overview(destination: str) -> DestinationOverview:
    data = DESTINATIONS.get(normalize_destination_name(destination), DESTINATIONS["goa"])
    fallback = normalize_destination_name(destination) not in DESTINATIONS
    return DestinationOverview(
        name=data["name"] if not fallback else destination.strip().title(),
        country=data["country"],
        center=data["center"],
        summary=data["summary"] if not fallback else "Fallback destination profile based on curated Indian city defaults.",
        best_for=data["best_for"],
        provider=_provider(
            "Curated local demonstration dataset",
            DataKind.SYNTHETIC if fallback else DataKind.OPEN_DATA,
            confidence=0.55 if fallback else 0.82,
            notes="Synthetic fallback used because the destination is not in the bundled dataset." if fallback else None,
        ),
    )


def get_candidate_activities(destination: str) -> list[CandidateActivity]:
    data = DESTINATIONS.get(normalize_destination_name(destination), DESTINATIONS["goa"])
    activities: list[CandidateActivity] = []
    for raw in data["activities"]:
        (
            activity_id,
            name,
            category,
            tags,
            duration,
            cost,
            rating,
            indoor,
            lat,
            lon,
            description,
        ) = raw
        activities.append(
            CandidateActivity(
                id=activity_id,
                name=name,
                category=category,
                tags=tags,
                location=GeoPoint(latitude=lat, longitude=lon),
                estimated_duration_minutes=duration,
                estimated_cost=cost,
                rating=rating,
                indoor=indoor,
                accessibility_notes=["step-free details unavailable"],
                opening_hours="Typical daytime opening; verify before travel",
                source=_provider("Curated POI dataset with open-map inspired coordinates", DataKind.OPEN_DATA),
                description=description,
            )
        )
    return activities


def get_transport_options(request: TripRequest, destination: DestinationOverview) -> list[TransportOption]:
    origin_point = KNOWN_ORIGINS.get(request.origin.strip().lower())
    distance = haversine_km(origin_point, destination.center) if origin_point else 750.0
    modes = [
        ("flight", "Estimated domestic flight", max(3500, distance * 7.2), int(max(75, distance * 0.12))),
        ("train", "Estimated rail route", max(650, distance * 1.3), int(max(180, distance * 0.9))),
        ("bus", "Estimated intercity bus", max(900, distance * 1.6), int(max(240, distance * 1.05))),
    ]
    if request.preferences.transport_preference != TransportPreference.ANY:
        modes = [mode for mode in modes if mode[0] == request.preferences.transport_preference.value] or modes
    return [
        TransportOption(
            id=f"{mode}-{destination.name.lower()}",
            mode=mode,
            provider_name=label,
            origin=request.origin,
            destination=destination.name,
            estimated_cost_per_person=round(cost, 2),
            duration_minutes=duration,
            is_estimate=True,
            source=_provider(
                "Distance-based estimated transport model",
                DataKind.ESTIMATE,
                confidence=0.62,
                notes="Not live availability or booking data.",
            ),
        )
        for mode, label, cost, duration in modes
    ]


def get_accommodation_options(request: TripRequest, destination: DestinationOverview) -> list[AccommodationOption]:
    base = destination.center
    tiers = [
        (AccommodationTier.BUDGET, "Value Stay Hub", 1800, 3.8, ["wifi", "private room"], "central budget area", 0.015, -0.011),
        (AccommodationTier.MID_RANGE, "Neighbourhood Boutique Stay", 3600, 4.3, ["wifi", "breakfast", "air conditioning"], "walkable core", -0.012, 0.013),
        (AccommodationTier.PREMIUM, "Heritage Comfort Hotel", 6200, 4.6, ["wifi", "breakfast", "pool", "concierge"], "quiet premium zone", 0.018, 0.016),
    ]
    preferred = request.preferences.accommodation_tier
    ordered = sorted(tiers, key=lambda item: 0 if item[0] == preferred else 1)
    return [
        AccommodationOption(
            id=f"{destination.name.lower()}-{tier.value}",
            name=f"{destination.name} {name}",
            tier=tier,
            location=GeoPoint(latitude=base.latitude + lat_delta, longitude=base.longitude + lon_delta),
            nightly_price_per_room=float(price),
            occupancy_per_room=2,
            rating=rating,
            amenities=amenities,
            area=area,
            is_estimate=True,
            source=_provider(
                "Curated accommodation estimate dataset",
                DataKind.ESTIMATE,
                confidence=0.68,
                notes="Price is an estimate per room per night, not live availability.",
            ),
        )
        for tier, name, price, rating, amenities, area, lat_delta, lon_delta in ordered
    ]


def search_destinations(query: str | None = None) -> list[DestinationSearchResult]:
    results: list[DestinationSearchResult] = []
    needle = (query or "").strip().lower()
    for data in DESTINATIONS.values():
        if needle and needle not in data["name"].lower() and not any(needle in tag for tag in data["best_for"]):
            continue
        results.append(
            DestinationSearchResult(
                name=data["name"],
                country=data["country"],
                center=data["center"],
                tags=data["best_for"],
            )
        )
    return results


def provider_statuses(enable_live_weather: bool) -> list[ProviderStatus]:
    return [
        ProviderStatus(
            name="Curated destination and POI dataset",
            status="available",
            data_kind=DataKind.OPEN_DATA,
            message="Bundled local dataset is available for deterministic demos.",
        ),
        ProviderStatus(
            name="Distance-based transport estimator",
            status="available",
            data_kind=DataKind.ESTIMATE,
            message="Returns transparent estimated costs and durations, not live availability.",
        ),
        ProviderStatus(
            name="Open-Meteo weather adapter",
            status="available" if enable_live_weather else "disabled",
            data_kind=DataKind.LIVE if enable_live_weather else DataKind.FALLBACK,
            message="Live forecast is optional and disabled by default; fallback labels are used otherwise.",
        ),
        ProviderStatus(
            name="Template LLM provider",
            status="available",
            data_kind=DataKind.FALLBACK,
            message="Deterministic narrative fallback works without paid LLM services.",
        ),
    ]
