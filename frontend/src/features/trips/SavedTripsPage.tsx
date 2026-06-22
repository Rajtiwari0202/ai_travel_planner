import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listTrips } from "../../services/api";
import type { TripRecordResponse } from "../../types/api";

export function SavedTripsPage() {
  const [trips, setTrips] = useState<TripRecordResponse[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listTrips()
      .then(setTrips)
      .catch((err: unknown) => setError(err instanceof Error ? err.message : "Unable to load trips."));
  }, []);

  return (
    <main className="mx-auto max-w-5xl px-4 py-10 sm:px-6">
      <h1 className="text-3xl font-semibold text-ink">Saved trips</h1>
      <p className="mt-2 text-ink/65">Trips are persisted in the local SQLite database.</p>
      {error && <p className="mt-4 rounded-md bg-clay/10 p-3 text-sm text-clay">{error}</p>}
      <div className="mt-6 grid gap-3">
        {trips.length ? (
          trips.map((trip) => (
            <article key={trip.trip_id} className="rounded-lg border border-ink/10 bg-white p-4 shadow-soft">
              <p className="text-sm font-semibold uppercase tracking-[0.16em] text-tide">{trip.status}</p>
              <h2 className="mt-1 text-xl font-semibold text-ink">
                {trip.request.origin} to {trip.request.destination}
              </h2>
              <p className="mt-1 text-sm text-ink/65">
                {trip.request.start_date} to {trip.request.end_date} / {trip.request.traveler_count} traveler(s)
              </p>
              <Link className="mt-3 inline-flex rounded-md bg-ink px-3 py-2 text-sm font-semibold text-white" to="/">
                Open planner
              </Link>
            </article>
          ))
        ) : (
          <p className="rounded-lg border border-dashed border-ink/20 bg-white p-6 text-ink/65">No saved trips yet.</p>
        )}
      </div>
    </main>
  );
}
