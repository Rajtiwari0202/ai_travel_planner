from __future__ import annotations

from datetime import UTC, date, datetime

import httpx

from app.core.config import Settings
from app.schemas.trip import DataKind, GeoPoint, ProviderMetadata, WeatherForecast

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    61: "Rain",
    63: "Moderate rain",
    65: "Heavy rain",
    80: "Rain showers",
    95: "Thunderstorm",
}


def _provider(kind: DataKind, notes: str | None = None) -> ProviderMetadata:
    return ProviderMetadata(
        source="Open-Meteo" if kind == DataKind.LIVE else "Seasonal weather fallback",
        data_kind=kind,
        fetched_at=datetime.now(UTC),
        confidence=0.76 if kind == DataKind.LIVE else 0.45,
        notes=notes,
    )


def _fallback_forecast(target: date) -> WeatherForecast:
    monsoon = target.month in {6, 7, 8, 9}
    condition = "Forecast unavailable; seasonal monsoon guidance" if monsoon else "Forecast unavailable; seasonal fair-weather guidance"
    tags = ["prefer indoor backup", "rain risk"] if monsoon else ["outdoor friendly", "forecast unavailable"]
    return WeatherForecast(
        date=target,
        min_temp_c=None,
        max_temp_c=None,
        precipitation_probability=None,
        condition=condition,
        suitability_tags=tags,
        forecast_available=False,
        source=_provider(DataKind.FALLBACK, "Live forecast was disabled or outside the free forecast horizon."),
    )


async def get_weather_forecasts(settings: Settings, center: GeoPoint, dates: list[date]) -> list[WeatherForecast]:
    if not settings.enable_live_weather:
        return [_fallback_forecast(target) for target in dates]

    try:
        async with httpx.AsyncClient(timeout=settings.provider_timeout_seconds) as client:
            response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": center.latitude,
                    "longitude": center.longitude,
                    "daily": "temperature_2m_min,temperature_2m_max,precipitation_probability_max,weather_code",
                    "timezone": "auto",
                    "forecast_days": 16,
                },
                headers={"User-Agent": "TravelAgenticAI/1.0 local demo"},
            )
            response.raise_for_status()
            payload = response.json()
    except (httpx.HTTPError, ValueError):
        return [_fallback_forecast(target) for target in dates]

    daily = payload.get("daily", {})
    available_dates = {
        datetime.strptime(raw_date, "%Y-%m-%d").date(): index
        for index, raw_date in enumerate(daily.get("time", []))
    }
    forecasts: list[WeatherForecast] = []
    for target in dates:
        index = available_dates.get(target)
        if index is None:
            forecasts.append(_fallback_forecast(target))
            continue
        code = int(daily.get("weather_code", [0])[index])
        precipitation = daily.get("precipitation_probability_max", [None])[index]
        condition = WEATHER_CODES.get(code, f"Weather code {code}")
        rain_risk = precipitation is not None and precipitation >= 50
        forecasts.append(
            WeatherForecast(
                date=target,
                min_temp_c=daily.get("temperature_2m_min", [None])[index],
                max_temp_c=daily.get("temperature_2m_max", [None])[index],
                precipitation_probability=precipitation,
                condition=condition,
                suitability_tags=["prefer indoor backup", "rain risk"] if rain_risk else ["outdoor friendly"],
                forecast_available=True,
                source=_provider(DataKind.LIVE),
            )
        )
    return forecasts
