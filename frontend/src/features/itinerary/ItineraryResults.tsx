import { AlertTriangle, BedDouble, CloudSun, IndianRupee, Route, TrainFront } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import type { TripPlan } from "../../types/api";

export function ItineraryResults({ plan }: { plan: TripPlan }) {
  return (
    <section className="rounded-lg border border-ink/10 bg-white p-5 shadow-soft" aria-label="Itinerary results">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-tide">{plan.status}</p>
          <h2 className="mt-1 text-3xl font-semibold text-ink">{plan.destination.name} itinerary</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-ink/70">{plan.narrative_summary}</p>
        </div>
        <span className="rounded-full bg-leaf/10 px-3 py-1 text-sm font-semibold text-leaf">
          Score {(plan.score.total_score * 100).toFixed(0)}%
        </span>
      </div>

      <div className="mt-5 grid gap-3 md:grid-cols-3">
        <Fact icon={TrainFront} label="Transport" value={`${plan.transport.mode} estimate`} />
        <Fact icon={BedDouble} label="Stay" value={`${plan.accommodation.name} · ${plan.budget.room_count} room(s)`} />
        <Fact icon={IndianRupee} label="Total" value={`${plan.budget.currency} ${plan.budget.total.toLocaleString()}`} />
      </div>

      {(plan.validation.errors.length > 0 || plan.validation.warnings.length > 0) && (
        <div className="mt-5 rounded-lg border border-clay/25 bg-clay/10 p-3">
          <div className="flex items-center gap-2 font-semibold text-clay">
            <AlertTriangle size={17} aria-hidden="true" />
            Validation {plan.validation.status}
          </div>
          {[...plan.validation.errors, ...plan.validation.warnings].map((item) => (
            <p key={item} className="mt-1 text-sm text-clay">
              {item}
            </p>
          ))}
        </div>
      )}

      <div className="mt-6 space-y-4">
        {plan.days.map((day) => (
          <article key={day.date} className="rounded-lg border border-ink/10 bg-paper p-4">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <h3 className="text-lg font-semibold text-ink">{day.title}</h3>
                <p className="mt-1 flex items-center gap-2 text-sm text-ink/65">
                  <CloudSun size={16} aria-hidden="true" />
                  {day.weather.condition}
                </p>
              </div>
              <span className="rounded-full bg-white px-3 py-1 text-xs font-semibold text-ink/70">
                {day.estimated_local_distance_km.toFixed(1)} km local route
              </span>
            </div>
            <div className="mt-4 grid gap-3">
              {day.activities.length ? (
                day.activities.map((activity, index) => (
                  <div key={activity.activity_id} className="rounded-md bg-white p-3">
                    <div className="flex flex-wrap items-start justify-between gap-3">
                      <div>
                        <p className="text-sm font-semibold text-ink">
                          {index + 1}. {activity.title}
                        </p>
                        <p className="mt-1 text-xs text-ink/60">
                          {activity.start_time.slice(0, 5)}-{activity.end_time.slice(0, 5)} · {activity.duration_minutes} min ·{" "}
                          {plan.budget.currency} {activity.estimated_cost.toLocaleString()}
                        </p>
                      </div>
                      <span className="rounded-full bg-tide/10 px-2 py-1 text-xs font-semibold text-tide">
                        {activity.data_kind.replace("_", " ")}
                      </span>
                    </div>
                    <p className="mt-2 text-sm leading-6 text-ink/70">{activity.rationale}</p>
                    <p className="mt-2 text-xs text-ink/55">
                      Source: {activity.source_label} · {activity.location.latitude.toFixed(4)},{" "}
                      {activity.location.longitude.toFixed(4)}
                    </p>
                  </div>
                ))
              ) : (
                <p className="rounded-md bg-white p-3 text-sm text-ink/65">
                  No activities scheduled because the optimizer could not keep the trip feasible under the budget.
                </p>
              )}
            </div>
          </article>
        ))}
      </div>

      <div className="mt-5 grid gap-3 md:grid-cols-2">
        <InfoList title="Data disclaimers" items={plan.data_disclaimers} />
        <InfoList title="Assumptions" items={plan.assumptions} />
      </div>

      <div className="mt-5 rounded-lg border border-ink/10 bg-paper p-4">
        <div className="flex items-center gap-2">
          <Route className="text-tide" size={18} aria-hidden="true" />
          <h3 className="font-semibold text-ink">Alternatives</h3>
        </div>
        <div className="mt-3 grid gap-3 md:grid-cols-2">
          {plan.alternatives.map((alternative) => (
            <div key={alternative.label} className="rounded-md bg-white p-3">
              <p className="font-semibold text-ink">{alternative.label}</p>
              <p className="mt-1 text-sm text-ink/65">{alternative.summary}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Fact({
  icon: Icon,
  label,
  value,
}: {
  icon: LucideIcon;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-lg bg-paper p-3">
      <Icon className="text-tide" size={18} aria-hidden="true" />
      <p className="mt-2 text-xs font-semibold uppercase tracking-[0.14em] text-ink/55">{label}</p>
      <p className="mt-1 text-sm font-semibold text-ink">{value}</p>
    </div>
  );
}

function InfoList({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="rounded-lg border border-ink/10 bg-paper p-4">
      <h3 className="font-semibold text-ink">{title}</h3>
      <ul className="mt-2 space-y-1 text-sm leading-6 text-ink/68">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
