import { useEffect, useState } from "react";
import { AlertTriangle, CheckCircle2, CircleSlash, Database, RadioTower } from "lucide-react";
import { providerStatus } from "../../services/api";
import type { ProviderStatus } from "../../types/api";

export function ProviderStatusPage() {
  const [providers, setProviders] = useState<ProviderStatus[]>([]);
  const [state, setState] = useState<"loading" | "ready" | "error">("loading");

  useEffect(() => {
    let active = true;
    providerStatus()
      .then((items) => {
        if (active) {
          setProviders(items);
          setState("ready");
        }
      })
      .catch(() => {
        if (active) {
          setState("error");
        }
      });
    return () => {
      active = false;
    };
  }, []);

  return (
    <main className="mx-auto max-w-7xl px-4 py-10 sm:px-6">
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <div className="inline-flex items-center gap-2 rounded-md bg-white px-3 py-2 text-sm font-semibold text-tide shadow-soft">
            <RadioTower size={16} aria-hidden="true" />
            Data pipeline
          </div>
          <h1 className="mt-4 text-3xl font-semibold text-ink">Provider status</h1>
        </div>
        <p className="max-w-2xl text-sm leading-6 text-ink/65">
          Live integrations are optional; deterministic providers keep the planner usable without paid services.
        </p>
      </div>

      {state === "loading" && <p className="text-sm text-ink/65">Checking providers...</p>}
      {state === "error" && (
        <div className="rounded-lg border border-clay/20 bg-white p-4 text-sm text-clay" role="alert">
          Provider status is unavailable because the backend is not reachable.
        </div>
      )}
      {state === "ready" && (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {providers.map((provider) => {
            const Icon = statusIcon(provider.status);
            return (
              <article key={provider.name} className="rounded-lg border border-ink/10 bg-white p-4 shadow-soft">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h2 className="font-semibold text-ink">{provider.name}</h2>
                    <p className="mt-2 text-sm leading-6 text-ink/65">{provider.message}</p>
                  </div>
                  <span className={statusClass(provider.status)}>
                    <Icon size={16} aria-hidden="true" />
                    {provider.status}
                  </span>
                </div>
                <p className="mt-4 inline-flex items-center gap-2 rounded-md bg-paper px-3 py-2 text-xs font-semibold text-tide">
                  <Database size={14} aria-hidden="true" />
                  {provider.data_kind.replace("_", " ")}
                </p>
              </article>
            );
          })}
        </div>
      )}
    </main>
  );
}

function statusIcon(status: ProviderStatus["status"]) {
  if (status === "available") {
    return CheckCircle2;
  }
  if (status === "degraded") {
    return AlertTriangle;
  }
  return CircleSlash;
}

function statusClass(status: ProviderStatus["status"]) {
  const base = "inline-flex shrink-0 items-center gap-1 rounded-full px-2 py-1 text-xs font-semibold";
  if (status === "available") {
    return `${base} bg-leaf/10 text-leaf`;
  }
  if (status === "degraded") {
    return `${base} bg-clay/10 text-clay`;
  }
  return `${base} bg-ink/10 text-ink/60`;
}
