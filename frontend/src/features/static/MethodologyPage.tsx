import { FlaskConical } from "lucide-react";

export function MethodologyPage() {
  return (
    <main className="mx-auto max-w-5xl px-4 py-10 sm:px-6">
      <div className="rounded-lg border border-ink/10 bg-white p-6 shadow-soft">
        <FlaskConical className="text-tide" aria-hidden="true" />
        <h1 className="mt-4 text-3xl font-semibold text-ink">Methodology and explainability</h1>
        <p className="mt-3 leading-7 text-ink/70">
          The planner uses a typed backend orchestration flow: validate intent, load deterministic providers, align
          weather guidance, compute distances, optimize a budget-feasible activity schedule, reconcile costs, and run a
          critic validation pass. Narrative text is generated after deterministic planning and cannot alter prices,
          dates, coordinates, or selected activities.
        </p>
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          {[
            ["Hard constraints", "Budget cap, trip dates, duplicate avoidance, coordinates, room-count assumptions."],
            ["Soft objectives", "Preference match, lower cost, lower distance, weather fit, diversity, stay quality."],
            ["Data honesty", "Estimated, fallback, synthetic, live, and open-data labels are preserved in responses."],
            ["Research limitation", "Benchmarks are deterministic synthetic cases, not user-satisfaction studies."],
          ].map(([title, text]) => (
            <section key={title} className="rounded-lg bg-paper p-4">
              <h2 className="font-semibold text-ink">{title}</h2>
              <p className="mt-2 text-sm leading-6 text-ink/68">{text}</p>
            </section>
          ))}
        </div>
      </div>
    </main>
  );
}
