import { FormEvent, useState } from "react";
import type { ReactNode } from "react";
import { CalendarDays, Loader2, SlidersHorizontal } from "lucide-react";
import type { TripRequest } from "../../types/api";

interface PlannerFormProps {
  busy: boolean;
  onSubmit: (payload: TripRequest) => Promise<void>;
}

const today = new Date();
const defaultStart = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 21)
  .toISOString()
  .slice(0, 10);
const defaultEnd = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 23)
  .toISOString()
  .slice(0, 10);

export function PlannerForm({ busy, onSubmit }: PlannerFormProps) {
  const [origin, setOrigin] = useState("Mumbai");
  const [destination, setDestination] = useState("Goa");
  const [startDate, setStartDate] = useState(defaultStart);
  const [endDate, setEndDate] = useState(defaultEnd);
  const [travelerCount, setTravelerCount] = useState(2);
  const [rooms, setRooms] = useState<number | "">("");
  const [budget, setBudget] = useState(45000);
  const [interests, setInterests] = useState("beach, food, culture");
  const [naturalLanguage, setNaturalLanguage] = useState("");
  const [pace, setPace] = useState<TripRequest["preferences"]["pace"]>("balanced");
  const [transport, setTransport] = useState<TripRequest["preferences"]["transport_preference"]>("any");
  const [tier, setTier] = useState<TripRequest["preferences"]["accommodation_tier"]>("mid_range");
  const [indoorOutdoor, setIndoorOutdoor] = useState<TripRequest["preferences"]["indoor_outdoor"]>("any");
  const [exclusions, setExclusions] = useState("");
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await onSubmit({
      origin,
      destination,
      start_date: startDate,
      end_date: endDate,
      traveler_count: travelerCount,
      rooms: rooms === "" ? null : rooms,
      total_budget: budget,
      currency: "INR",
      natural_language: naturalLanguage || null,
      preferences: {
        interests: splitList(interests),
        pace,
        transport_preference: transport,
        accommodation_tier: tier,
        food_preferences: [],
        accessibility: [],
        indoor_outdoor: indoorOutdoor,
        excluded_activities: splitList(exclusions),
      },
    });
  };

  return (
    <form onSubmit={handleSubmit} className="rounded-lg border border-ink/10 bg-white p-4 shadow-soft">
      <div className="mb-4 flex items-center gap-2">
        <CalendarDays className="text-tide" size={20} aria-hidden="true" />
        <h2 className="text-lg font-semibold text-ink">Plan a trip</h2>
      </div>

      <div className="grid gap-3">
        <Field label="From">
          <input required value={origin} onChange={(event) => setOrigin(event.target.value)} className={inputClass} />
        </Field>
        <Field label="To">
          <input
            required
            value={destination}
            onChange={(event) => setDestination(event.target.value)}
            className={inputClass}
          />
        </Field>
        <div className="grid grid-cols-2 gap-3">
          <Field label="Start">
            <input
              required
              type="date"
              value={startDate}
              onChange={(event) => setStartDate(event.target.value)}
              className={inputClass}
            />
          </Field>
          <Field label="End">
            <input
              required
              type="date"
              value={endDate}
              onChange={(event) => setEndDate(event.target.value)}
              className={inputClass}
            />
          </Field>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <Field label="Travelers">
            <input
              required
              type="number"
              min={1}
              max={20}
              value={travelerCount}
              onChange={(event) => setTravelerCount(Number(event.target.value))}
              className={inputClass}
            />
          </Field>
          <Field label="Budget INR">
            <input
              required
              type="number"
              min={1}
              value={budget}
              onChange={(event) => setBudget(Number(event.target.value))}
              className={inputClass}
            />
          </Field>
        </div>
        <Field label="Interests">
          <input value={interests} onChange={(event) => setInterests(event.target.value)} className={inputClass} />
        </Field>
        <Field label="Natural-language notes">
          <textarea
            value={naturalLanguage}
            onChange={(event) => setNaturalLanguage(event.target.value)}
            className={`${inputClass} min-h-20 resize-y`}
            placeholder="Prefer cafes, avoid late nights, keep one slow afternoon..."
          />
        </Field>
      </div>

      <button
        type="button"
        onClick={() => setShowAdvanced((value) => !value)}
        className="mt-4 inline-flex items-center gap-2 rounded-md border border-ink/15 px-3 py-2 text-sm font-semibold text-ink"
      >
        <SlidersHorizontal size={16} aria-hidden="true" />
        Advanced preferences
      </button>

      {showAdvanced && (
        <div className="mt-3 grid gap-3 border-t border-ink/10 pt-3">
          <div className="grid grid-cols-2 gap-3">
            <Field label="Pace">
              <select value={pace} onChange={(event) => setPace(event.target.value as typeof pace)} className={inputClass}>
                <option value="relaxed">Relaxed</option>
                <option value="balanced">Balanced</option>
                <option value="active">Active</option>
              </select>
            </Field>
            <Field label="Transport">
              <select
                value={transport}
                onChange={(event) => setTransport(event.target.value as typeof transport)}
                className={inputClass}
              >
                <option value="any">Any</option>
                <option value="flight">Flight</option>
                <option value="train">Train</option>
                <option value="bus">Bus</option>
              </select>
            </Field>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <Field label="Stay tier">
              <select value={tier} onChange={(event) => setTier(event.target.value as typeof tier)} className={inputClass}>
                <option value="budget">Budget</option>
                <option value="mid_range">Mid range</option>
                <option value="premium">Premium</option>
              </select>
            </Field>
            <Field label="Rooms">
              <input
                type="number"
                min={1}
                max={10}
                value={rooms}
                onChange={(event) => setRooms(event.target.value ? Number(event.target.value) : "")}
                className={inputClass}
                placeholder="Auto"
              />
            </Field>
          </div>
          <Field label="Indoor/outdoor">
            <select
              value={indoorOutdoor}
              onChange={(event) => setIndoorOutdoor(event.target.value as typeof indoorOutdoor)}
              className={inputClass}
            >
              <option value="any">Any</option>
              <option value="mostly_indoor">Mostly indoor</option>
              <option value="mostly_outdoor">Mostly outdoor</option>
            </select>
          </Field>
          <Field label="Excluded activities">
            <input value={exclusions} onChange={(event) => setExclusions(event.target.value)} className={inputClass} />
          </Field>
        </div>
      )}

      <button
        type="submit"
        disabled={busy}
        className="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-md bg-leaf px-4 py-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
      >
        {busy && <Loader2 className="animate-spin" size={16} aria-hidden="true" />}
        {busy ? "Starting agents" : "Create optimized itinerary"}
      </button>
    </form>
  );
}

const inputClass = "w-full rounded-md border border-ink/15 bg-paper px-3 py-2 text-sm text-ink";

function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="grid gap-1 text-sm font-medium text-ink/75">
      <span>{label}</span>
      {children}
    </label>
  );
}

function splitList(value: string): string[] {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}
