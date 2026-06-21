from __future__ import annotations

from datetime import UTC, date, datetime, time
from enum import Enum
from math import ceil
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, model_validator


class DataKind(str, Enum):
    ESTIMATE = "estimate"
    LIVE = "live"
    CACHED = "cached"
    SYNTHETIC = "synthetic"
    OPEN_DATA = "open_data"
    FALLBACK = "fallback"


class Pace(str, Enum):
    RELAXED = "relaxed"
    BALANCED = "balanced"
    ACTIVE = "active"


class TransportPreference(str, Enum):
    ANY = "any"
    FLIGHT = "flight"
    TRAIN = "train"
    BUS = "bus"


class AccommodationTier(str, Enum):
    BUDGET = "budget"
    MID_RANGE = "mid_range"
    PREMIUM = "premium"


class IndoorOutdoorPreference(str, Enum):
    ANY = "any"
    MOSTLY_INDOOR = "mostly_indoor"
    MOSTLY_OUTDOOR = "mostly_outdoor"


class TripStatus(str, Enum):
    PLANNING = "planning"
    COMPLETE = "complete"
    INFEASIBLE = "infeasible"
    FAILED = "failed"
    DELETED = "deleted"


class AgentName(str, Enum):
    INTENT = "intent_agent"
    DESTINATION = "destination_research_agent"
    TRANSPORT = "transport_research_agent"
    ACCOMMODATION = "accommodation_research_agent"
    WEATHER = "weather_agent"
    GEOSPATIAL = "geospatial_agent"
    OPTIMIZATION = "optimization_agent"
    BUDGET = "budget_agent"
    WRITER = "itinerary_writer_agent"
    CRITIC = "critic_validation_agent"
    REVISION = "revision_agent"


class EventType(str, Enum):
    PLAN_STARTED = "plan.started"
    AGENT_STARTED = "agent.started"
    AGENT_PROGRESS = "agent.progress"
    AGENT_COMPLETED = "agent.completed"
    AGENT_FAILED = "agent.failed"
    OPTIMIZATION_COMPLETED = "optimization.completed"
    VALIDATION_COMPLETED = "validation.completed"
    PLAN_COMPLETED = "plan.completed"
    PLAN_FAILED = "plan.failed"


class GeoPoint(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class ProviderMetadata(BaseModel):
    source: str
    data_kind: DataKind
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    confidence: float = Field(default=0.8, ge=0, le=1)
    notes: str | None = None


class TripPreferences(BaseModel):
    interests: list[str] = Field(default_factory=list)
    pace: Pace = Pace.BALANCED
    transport_preference: TransportPreference = TransportPreference.ANY
    accommodation_tier: AccommodationTier = AccommodationTier.MID_RANGE
    food_preferences: list[str] = Field(default_factory=list)
    accessibility: list[str] = Field(default_factory=list)
    indoor_outdoor: IndoorOutdoorPreference = IndoorOutdoorPreference.ANY
    excluded_activities: list[str] = Field(default_factory=list)

    @field_validator("interests", "food_preferences", "accessibility", "excluded_activities")
    @classmethod
    def normalize_list(cls, values: list[str]) -> list[str]:
        return sorted({item.strip().lower() for item in values if item.strip()})


class TripRequest(BaseModel):
    origin: str = Field(..., min_length=2, max_length=80)
    destination: str = Field(..., min_length=2, max_length=80)
    start_date: date
    end_date: date
    traveler_count: int = Field(..., ge=1, le=20)
    rooms: int | None = Field(default=None, ge=1, le=10)
    total_budget: float = Field(..., gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    natural_language: str | None = Field(default=None, max_length=2000)
    preferences: TripPreferences = Field(default_factory=TripPreferences)

    @field_validator("origin", "destination", "currency")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()

    @model_validator(mode="after")
    def validate_dates(self) -> TripRequest:
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self

    @property
    def day_count(self) -> int:
        return (self.end_date - self.start_date).days + 1

    @property
    def night_count(self) -> int:
        return max(1, (self.end_date - self.start_date).days)

    @property
    def assumed_rooms(self) -> int:
        return self.rooms or ceil(self.traveler_count / 2)


class DestinationOverview(BaseModel):
    name: str
    country: str
    center: GeoPoint
    summary: str
    best_for: list[str]
    provider: ProviderMetadata


class CandidateActivity(BaseModel):
    id: str
    name: str
    category: str
    tags: list[str]
    location: GeoPoint
    estimated_duration_minutes: int = Field(..., ge=30, le=720)
    estimated_cost: float = Field(..., ge=0)
    rating: float = Field(..., ge=0, le=5)
    indoor: bool = False
    accessibility_notes: list[str] = Field(default_factory=list)
    opening_hours: str | None = None
    source: ProviderMetadata
    description: str


class TransportOption(BaseModel):
    id: str
    mode: str
    provider_name: str
    origin: str
    destination: str
    estimated_cost_per_person: float = Field(..., ge=0)
    duration_minutes: int = Field(..., ge=15)
    is_estimate: bool = True
    source: ProviderMetadata


class AccommodationOption(BaseModel):
    id: str
    name: str
    tier: AccommodationTier
    location: GeoPoint
    nightly_price_per_room: float = Field(..., ge=0)
    occupancy_per_room: int = Field(default=2, ge=1)
    rating: float = Field(..., ge=0, le=5)
    amenities: list[str]
    area: str
    is_estimate: bool = True
    source: ProviderMetadata


class WeatherForecast(BaseModel):
    date: date
    min_temp_c: float | None = None
    max_temp_c: float | None = None
    precipitation_probability: float | None = Field(default=None, ge=0, le=100)
    condition: str
    suitability_tags: list[str]
    forecast_available: bool
    source: ProviderMetadata


class ScheduledActivity(BaseModel):
    activity_id: str
    title: str
    date: date
    start_time: time
    end_time: time
    duration_minutes: int
    estimated_cost: float
    location: GeoPoint
    category: str
    tags: list[str]
    source_label: str
    data_kind: DataKind
    rationale: str
    weather_note: str | None = None


class TripDay(BaseModel):
    date: date
    title: str
    weather: WeatherForecast
    activities: list[ScheduledActivity]
    estimated_local_distance_km: float = Field(..., ge=0)
    daily_cost: float = Field(..., ge=0)
    notes: list[str] = Field(default_factory=list)


class BudgetBreakdown(BaseModel):
    currency: str
    transport: float = Field(..., ge=0)
    accommodation: float = Field(..., ge=0)
    activities: float = Field(..., ge=0)
    local_transport: float = Field(..., ge=0)
    food: float = Field(..., ge=0)
    contingency: float = Field(..., ge=0)
    taxes_and_fees: float = Field(..., ge=0)
    total: float = Field(..., ge=0)
    remaining: float
    room_count: int = Field(..., ge=1)
    nights: int = Field(..., ge=1)
    assumptions: list[str]


class ScoreBreakdown(BaseModel):
    total_score: float = Field(..., ge=0, le=1)
    preference_match: float = Field(..., ge=0, le=1)
    budget_fit: float = Field(..., ge=0, le=1)
    distance_efficiency: float = Field(..., ge=0, le=1)
    weather_fit: float = Field(..., ge=0, le=1)
    diversity: float = Field(..., ge=0, le=1)
    accommodation_quality: float = Field(..., ge=0, le=1)
    explanation: list[str]


class ValidationReport(BaseModel):
    status: Literal["passed", "warning", "failed"]
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    checked_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class RevisionRecord(BaseModel):
    revision_id: str = Field(default_factory=lambda: str(uuid4()))
    requested_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    instruction: str
    changes: list[str]


class AlternativePlan(BaseModel):
    label: str
    summary: str
    total_cost: float
    score: float = Field(..., ge=0, le=1)
    tradeoffs: list[str]


class TripPlan(BaseModel):
    trip_id: str
    status: TripStatus
    request: TripRequest
    destination: DestinationOverview
    transport: TransportOption
    accommodation: AccommodationOption
    days: list[TripDay]
    budget: BudgetBreakdown
    score: ScoreBreakdown
    alternatives: list[AlternativePlan]
    validation: ValidationReport
    assumptions: list[str]
    data_disclaimers: list[str]
    narrative_summary: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    revision_history: list[RevisionRecord] = Field(default_factory=list)


class RevisionRequest(BaseModel):
    instruction: str = Field(..., min_length=3, max_length=1000)


class AgentEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    trip_id: str
    event_type: EventType
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    agent: AgentName | None = None
    stage: str
    message: str
    progress: int | None = Field(default=None, ge=0, le=100)
    metadata: dict[str, Any] = Field(default_factory=dict)


class TripCreateResponse(BaseModel):
    trip_id: str
    status: TripStatus
    events_url: str
    message: str
    plan: TripPlan | None = None


class TripRecordResponse(BaseModel):
    trip_id: str
    status: TripStatus
    request: TripRequest
    plan: TripPlan | None = None
    created_at: datetime
    updated_at: datetime


class DestinationSearchResult(BaseModel):
    name: str
    country: str
    center: GeoPoint
    tags: list[str]


class ProviderStatus(BaseModel):
    name: str
    status: Literal["available", "degraded", "disabled"]
    data_kind: DataKind
    message: str
