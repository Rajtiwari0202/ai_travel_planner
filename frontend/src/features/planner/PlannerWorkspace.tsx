import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { AlertTriangle, Download, RefreshCw } from "lucide-react";
import { createTrip, getTrip, providerStatus, reviseTrip, waitForReadiness } from "../../services/api";
import { useTripEvents } from "../../hooks/useTripEvents";
import type { ProviderStatus, TripRecordResponse, TripRequest } from "../../types/api";
import { AgentTimeline } from "../agents/AgentTimeline";
import { BudgetPanel } from "../budget/BudgetPanel";
import { ItineraryResults } from "../itinerary/ItineraryResults";
import { ItineraryMap } from "../map/ItineraryMap";
import { PlannerForm } from "./PlannerForm";
import { ProviderStatusPanel } from "./ProviderStatusPanel";

export function PlannerWorkspace() {
  const [tripId, setTripId] = useState<string | null>(null);
  const [record, setRecord] = useState<TripRecordResponse | null>(null);
  const [providers, setProviders] = useState<ProviderStatus[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [wakeMessage, setWakeMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [revisionText, setRevisionText] = useState("");
  const [revisionBusy, setRevisionBusy] = useState(false);
  const { events, connected, error: eventError, latestProgress, completed } = useTripEvents(tripId);

  useEffect(() => {
    providerStatus()
      .then(setProviders)
      .catch(() => setProviders([]));
  }, []);

  useEffect(() => {
    if (!tripId) {
      return undefined;
    }
    let cancelled = false;
    const load = async () => {
      const next = await getTrip(tripId);
      if (!cancelled) {
        setRecord(next);
      }
    };
    void load();
    const handle = window.setInterval(() => {
      if (!completed) {
        void load();
      }
    }, 1200);
    return () => {
      cancelled = true;
      window.clearInterval(handle);
    };
  }, [tripId, completed]);

  useEffect(() => {
    if (completed && tripId) {
      void getTrip(tripId).then(setRecord);
    }
  }, [completed, tripId]);

  const plan = record?.plan ?? null;
  const statusLabel = useMemo(() => {
    if (!tripId) {
      return "Ready";
    }
    if (plan) {
      return plan.status === "infeasible" ? "Needs adjustment" : "Complete";
    }
    return connected ? "Planning" : "Processing";
  }, [connected, plan, tripId]);

  const handleSubmit = async (payload: TripRequest) => {
    setSubmitting(true);
    setError(null);
    setRecord(null);
    setWakeMessage("Checking planning service readiness.");
    try {
      await waitForReadiness((_attempt, elapsedMs) => {
        if (elapsedMs > 1200) {
          setWakeMessage(
            `The planning service is waking up. Free demo instances can take up to a minute after inactivity. Elapsed ${Math.round(
              elapsedMs / 1000,
            )}s.`,
          );
        }
      });
      setWakeMessage(null);
      const response = await createTrip(payload);
      setTripId(response.trip_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to create trip.");
    } finally {
      setSubmitting(false);
      setWakeMessage(null);
    }
  };

  const handleRevision = async () => {
    if (!tripId || revisionText.trim().length < 3) {
      return;
    }
    setRevisionBusy(true);
    setError(null);
    try {
      const next = await reviseTrip(tripId, revisionText.trim());
      setRecord(next);
      setRevisionText("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to revise trip.");
    } finally {
      setRevisionBusy(false);
    }
  };

  const handleExport = () => {
    if (!record) {
      return;
    }
    const blob = new Blob([JSON.stringify(record, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${record.trip_id}-itinerary.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <main>
      <section className="border-b border-ink/10 bg-[#efe8db]">
        <div className="mx-auto grid max-w-7xl gap-8 px-4 py-10 sm:px-6 lg:grid-cols-[1fr_420px] lg:py-14">
          <div className="flex flex-col justify-end">
            <p className="mb-3 text-sm font-semibold uppercase tracking-[0.18em] text-tide">Local-first decision support</p>
            <h1 className="max-w-4xl text-4xl font-semibold leading-tight text-ink md:text-6xl">
              Explainable agentic travel plans with budget-feasible schedules.
            </h1>
            <p className="mt-5 max-w-2xl text-base leading-7 text-ink/72">
              Create an itinerary with transparent estimated data, backend-supplied coordinates, real agent events,
              weather labels, score explanations, and deterministic fallback planning.
            </p>
          </div>
          <ProviderStatusPanel providers={providers} />
        </div>
      </section>

      <section className="mx-auto grid max-w-7xl gap-5 px-4 py-6 sm:px-6 lg:grid-cols-[390px_minmax(0,1fr)]">
        <div className="space-y-5">
          <PlannerForm onSubmit={handleSubmit} busy={submitting} />
          {wakeMessage && (
            <div className="rounded-lg border border-tide/25 bg-tide/10 p-3 text-sm leading-6 text-ink">
              {wakeMessage}
            </div>
          )}
          <AgentTimeline events={events} connected={connected} progress={latestProgress} statusLabel={statusLabel} />
          {(error || eventError) && (
            <div className="flex gap-3 rounded-lg border border-clay/30 bg-clay/10 p-3 text-sm text-clay">
              <AlertTriangle size={18} aria-hidden="true" />
              <span>{error || eventError}</span>
            </div>
          )}
        </div>

        <div className="space-y-5">
          {plan ? (
            <>
              <div className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_340px]">
                <ItineraryResults plan={plan} />
                <div className="space-y-5">
                  <BudgetPanel budget={plan.budget} score={plan.score} />
                  <div className="rounded-lg border border-ink/10 bg-white p-4 shadow-soft">
                    <label htmlFor="revision" className="text-sm font-semibold text-ink">
                      Revision assistant
                    </label>
                    <textarea
                      id="revision"
                      className="mt-2 min-h-24 w-full rounded-md border border-ink/15 bg-paper px-3 py-2 text-sm"
                      value={revisionText}
                      onChange={(event) => setRevisionText(event.target.value)}
                      placeholder="Reduce the budget to 35000, add more adventure, or avoid outdoor activities on rainy days."
                    />
                    <button
                      type="button"
                      onClick={handleRevision}
                      disabled={revisionBusy || revisionText.trim().length < 3}
                      className="mt-3 inline-flex items-center gap-2 rounded-md bg-ink px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      <RefreshCw size={16} aria-hidden="true" />
                      {revisionBusy ? "Revising" : "Apply revision"}
                    </button>
                  </div>
                  <button
                    type="button"
                    onClick={handleExport}
                    className="inline-flex w-full items-center justify-center gap-2 rounded-md border border-ink/20 bg-white px-4 py-2 text-sm font-semibold text-ink"
                  >
                    <Download size={16} aria-hidden="true" />
                    Export itinerary JSON
                  </button>
                </div>
              </div>
              <ItineraryMap plan={plan} />
            </>
          ) : (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex min-h-[520px] items-center justify-center rounded-lg border border-dashed border-ink/20 bg-white p-8 text-center shadow-soft"
            >
              <div className="max-w-md">
                <p className="text-sm font-semibold uppercase tracking-[0.18em] text-tide">Workspace</p>
                <h2 className="mt-3 text-2xl font-semibold text-ink">Your optimized itinerary appears here</h2>
                <p className="mt-3 text-sm leading-6 text-ink/65">
                  Submit a trip to see streamed agent progress, a saved plan, mapped activities, budget reconciliation,
                  alternatives, warnings, and data-source labels.
                </p>
              </div>
            </motion.div>
          )}
        </div>
      </section>
    </main>
  );
}
