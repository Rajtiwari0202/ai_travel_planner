import { Database, RadioTower } from "lucide-react";
import type { ProviderStatus } from "../../types/api";

export function ProviderStatusPanel({ providers }: { providers: ProviderStatus[] }) {
  return (
    <aside className="rounded-lg border border-ink/10 bg-white p-4 shadow-soft" aria-label="Provider status">
      <div className="mb-3 flex items-center gap-2">
        <RadioTower className="text-tide" size={20} aria-hidden="true" />
        <h2 className="font-semibold text-ink">Provider status</h2>
      </div>
      <div className="grid gap-2">
        {providers.length ? (
          providers.map((provider) => (
            <div key={provider.name} className="rounded-md border border-ink/10 bg-paper p-3">
              <div className="flex items-center justify-between gap-2">
                <p className="text-sm font-semibold text-ink">{provider.name}</p>
                <span className={statusClass(provider.status)}>{provider.status}</span>
              </div>
              <p className="mt-1 text-xs leading-5 text-ink/65">{provider.message}</p>
              <p className="mt-2 inline-flex items-center gap-1 text-xs font-semibold text-tide">
                <Database size={13} aria-hidden="true" />
                {provider.data_kind.replace("_", " ")}
              </p>
            </div>
          ))
        ) : (
          <p className="text-sm text-ink/65">Provider status loads when the backend is reachable.</p>
        )}
      </div>
    </aside>
  );
}

function statusClass(status: ProviderStatus["status"]) {
  if (status === "available") {
    return "rounded-full bg-leaf/10 px-2 py-1 text-xs font-semibold text-leaf";
  }
  if (status === "degraded") {
    return "rounded-full bg-clay/10 px-2 py-1 text-xs font-semibold text-clay";
  }
  return "rounded-full bg-ink/10 px-2 py-1 text-xs font-semibold text-ink/60";
}
