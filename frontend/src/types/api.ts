export type DataKind = "estimate" | "live" | "cached" | "synthetic" | "open_data" | "fallback";
export type TripStatus = "planning" | "complete" | "infeasible" | "failed" | "deleted";
export type EventType =
  | "plan.started"
  | "agent.started"
  | "agent.progress"
  | "agent.completed"
  | "agent.failed"
  | "optimization.completed"
  | "validation.completed"
  | "plan.completed"
  | "plan.failed";

export interface GeoPoint {
  latitude: number;
  longitude: number;
}

export interface TripPreferences {
  interests: string[];
  pace: "relaxed" | "balanced" | "active";
  transport_preference: "any" | "flight" | "train" | "bus";
  accommodation_tier: "budget" | "mid_range" | "premium";
  food_preferences: string[];
  accessibility: string[];
  indoor_outdoor: "any" | "mostly_indoor" | "mostly_outdoor";
  excluded_activities: string[];
}

export interface TripRequest {
  origin: string;
  destination: string;
  start_date: string;
  end_date: string;
  traveler_count: number;
  rooms?: number | null;
  total_budget: number;
  currency: string;
  natural_language?: string | null;
  preferences: TripPreferences;
}

export interface ProviderMetadata {
  source: string;
  data_kind: DataKind;
  fetched_at: string;
  confidence: number;
  notes?: string | null;
}

export interface DestinationOverview {
  name: string;
  country: string;
  center: GeoPoint;
  summary: string;
  best_for: string[];
  provider: ProviderMetadata;
}

export interface TransportOption {
  id: string;
  mode: string;
  provider_name: string;
  origin: string;
  destination: string;
  estimated_cost_per_person: number;
  duration_minutes: number;
  is_estimate: boolean;
  source: ProviderMetadata;
}

export interface AccommodationOption {
  id: string;
  name: string;
  tier: "budget" | "mid_range" | "premium";
  location: GeoPoint;
  nightly_price_per_room: number;
  occupancy_per_room: number;
  rating: number;
  amenities: string[];
  area: string;
  is_estimate: boolean;
  source: ProviderMetadata;
}

export interface WeatherForecast {
  date: string;
  min_temp_c?: number | null;
  max_temp_c?: number | null;
  precipitation_probability?: number | null;
  condition: string;
  suitability_tags: string[];
  forecast_available: boolean;
  source: ProviderMetadata;
}

export interface ScheduledActivity {
  activity_id: string;
  title: string;
  date: string;
  start_time: string;
  end_time: string;
  duration_minutes: number;
  estimated_cost: number;
  location: GeoPoint;
  category: string;
  tags: string[];
  source_label: string;
  data_kind: DataKind;
  rationale: string;
  weather_note?: string | null;
}

export interface TripDay {
  date: string;
  title: string;
  weather: WeatherForecast;
  activities: ScheduledActivity[];
  estimated_local_distance_km: number;
  daily_cost: number;
  notes: string[];
}

export interface BudgetBreakdown {
  currency: string;
  transport: number;
  accommodation: number;
  activities: number;
  local_transport: number;
  food: number;
  contingency: number;
  taxes_and_fees: number;
  total: number;
  remaining: number;
  room_count: number;
  nights: number;
  assumptions: string[];
}

export interface ScoreBreakdown {
  total_score: number;
  preference_match: number;
  budget_fit: number;
  distance_efficiency: number;
  weather_fit: number;
  diversity: number;
  accommodation_quality: number;
  explanation: string[];
}

export interface ValidationReport {
  status: "passed" | "warning" | "failed";
  errors: string[];
  warnings: string[];
  checked_at: string;
}

export interface RevisionRecord {
  revision_id: string;
  requested_at: string;
  instruction: string;
  changes: string[];
}

export interface AlternativePlan {
  label: string;
  summary: string;
  total_cost: number;
  score: number;
  tradeoffs: string[];
}

export interface TripPlan {
  trip_id: string;
  status: TripStatus;
  request: TripRequest;
  destination: DestinationOverview;
  transport: TransportOption;
  accommodation: AccommodationOption;
  days: TripDay[];
  budget: BudgetBreakdown;
  score: ScoreBreakdown;
  alternatives: AlternativePlan[];
  validation: ValidationReport;
  assumptions: string[];
  data_disclaimers: string[];
  narrative_summary: string;
  created_at: string;
  updated_at: string;
  revision_history: RevisionRecord[];
}

export interface TripCreateResponse {
  trip_id: string;
  status: TripStatus;
  events_url: string;
  message: string;
  plan?: TripPlan | null;
}

export interface TripRecordResponse {
  trip_id: string;
  status: TripStatus;
  request: TripRequest;
  plan?: TripPlan | null;
  created_at: string;
  updated_at: string;
}

export interface AgentEvent {
  event_id: string;
  trip_id: string;
  event_type: EventType;
  timestamp: string;
  agent?: string | null;
  stage: string;
  message: string;
  progress?: number | null;
  metadata: Record<string, unknown>;
  sequence?: number;
}

export interface ProviderStatus {
  name: string;
  status: "available" | "degraded" | "disabled";
  data_kind: DataKind;
  message: string;
}

export interface DestinationSearchResult {
  name: string;
  country: string;
  center: GeoPoint;
  tags: string[];
}
