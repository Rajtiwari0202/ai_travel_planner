from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str = "TravelAgenticAI"
    environment: str = os.getenv("APP_ENV", "development")
    api_prefix: str = "/api/v1"
    database_url: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'travelagenticai.sqlite3'}",
    )
    cors_origins: tuple[str, ...] = tuple(
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000",
        ).split(",")
        if origin.strip()
    )
    enable_live_weather: bool = os.getenv("ENABLE_LIVE_WEATHER", "false").lower() == "true"
    provider_timeout_seconds: float = float(os.getenv("PROVIDER_TIMEOUT_SECONDS", "4"))
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "90"))


@lru_cache
def get_settings() -> Settings:
    return Settings()

