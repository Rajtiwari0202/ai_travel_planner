from __future__ import annotations

from math import asin, cos, radians, sin, sqrt

from app.schemas.trip import GeoPoint

EARTH_RADIUS_KM = 6371.0088


def haversine_km(origin: GeoPoint, destination: GeoPoint) -> float:
    lat1 = radians(origin.latitude)
    lon1 = radians(origin.longitude)
    lat2 = radians(destination.latitude)
    lon2 = radians(destination.longitude)

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(a))


def path_distance_km(points: list[GeoPoint]) -> float:
    if len(points) < 2:
        return 0.0
    return sum(haversine_km(points[index], points[index + 1]) for index in range(len(points) - 1))
