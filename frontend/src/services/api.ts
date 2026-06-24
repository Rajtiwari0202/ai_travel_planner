import { z } from "zod";
import type {
  AgentEvent,
  DestinationSearchResult,
  ProviderStatus,
  TripCreateResponse,
  TripRecordResponse,
  TripRequest,
} from "../types/api";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";
const SESSION_KEY = "travelagenticai.anonymousSession";

function getAnonymousSession(): string {
  const existing = window.localStorage.getItem(SESSION_KEY);
  if (existing) {
    return existing;
  }
  const bytes = new Uint8Array(32);
  window.crypto.getRandomValues(bytes);
  const token = Array.from(bytes, (byte) => byte.toString(16).padStart(2, "0")).join("");
  window.localStorage.setItem(SESSION_KEY, token);
  return token;
}

function authHeaders(): Record<string, string> {
  return { "X-Anonymous-Session": getAnonymousSession() };
}

const tripCreateSchema = z.object({
  trip_id: z.string(),
  status: z.string(),
  events_url: z.string(),
  message: z.string(),
  plan: z.unknown().nullable().optional(),
});

const tripRecordSchema = z.object({
  trip_id: z.string(),
  status: z.string(),
  request: z.unknown(),
  plan: z.unknown().nullable().optional(),
  created_at: z.string(),
  updated_at: z.string(),
});

async function requestJson<T>(path: string, init?: RequestInit, schema?: z.ZodType): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
      ...(init?.headers ?? {}),
    },
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with ${response.status}`);
  }
  const json = await response.json();
  if (schema) {
    schema.parse(json);
  }
  return json as T;
}

export function createTrip(payload: TripRequest): Promise<TripCreateResponse> {
  return requestJson<TripCreateResponse>(
    "/trips",
    { method: "POST", body: JSON.stringify(payload) },
    tripCreateSchema,
  );
}

export async function waitForReadiness(
  onAttempt?: (attempt: number, elapsedMs: number) => void,
  maxAttempts = 6,
): Promise<void> {
  const started = Date.now();
  let delay = 1000;
  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    onAttempt?.(attempt, Date.now() - started);
    try {
      const response = await fetch(`${API_BASE}/health/ready`, { headers: authHeaders() });
      if (response.ok) {
        return;
      }
    } catch {
      // The public demo backend may be waking up; retry below.
    }
    await new Promise((resolve) => window.setTimeout(resolve, delay));
    delay = Math.min(delay * 1.8, 8000);
  }
  throw new Error("The planning service did not become ready in time. Please try again shortly.");
}

export function getTrip(tripId: string): Promise<TripRecordResponse> {
  return requestJson<TripRecordResponse>(`/trips/${tripId}`, undefined, tripRecordSchema);
}

export function listTrips(): Promise<TripRecordResponse[]> {
  return requestJson<TripRecordResponse[]>("/trips");
}

export function reviseTrip(tripId: string, instruction: string): Promise<TripRecordResponse> {
  return requestJson<TripRecordResponse>(
    `/trips/${tripId}/revise`,
    { method: "POST", body: JSON.stringify({ instruction }) },
    tripRecordSchema,
  );
}

export function providerStatus(): Promise<ProviderStatus[]> {
  return requestJson<ProviderStatus[]>("/providers/status");
}

export function searchDestinations(query = ""): Promise<DestinationSearchResult[]> {
  const suffix = query ? `?q=${encodeURIComponent(query)}` : "";
  return requestJson<DestinationSearchResult[]>(`/destinations/search${suffix}`);
}

export function eventSourceUrl(tripId: string): string {
  const separator = API_BASE.includes("?") ? "&" : "?";
  return `${API_BASE}/trips/${tripId}/events${separator}session=${encodeURIComponent(getAnonymousSession())}`;
}

export function parseAgentEvent(raw: MessageEvent<string>): AgentEvent {
  return JSON.parse(raw.data) as AgentEvent;
}
