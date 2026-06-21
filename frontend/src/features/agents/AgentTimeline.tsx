import { CheckCircle2, CircleDashed, Radio } from "lucide-react";
import type { AgentEvent } from "../../types/api";

interface AgentTimelineProps {
  events: AgentEvent[];
  connected: boolean;
  progress: number;
  statusLabel: string;
}

export function AgentTimeline({ events, connected, progress, statusLabel }: AgentTimelineProps) {
  return (
    <section className="rounded-lg border border-ink/10 bg-white p-4 shadow-soft" aria-label="Agent progress">
      <div className="mb-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Radio className={connected ? "text-leaf" : "text-ink/50"} size={18} aria-hidden="true" />
          <h2 className="font-semibold text-ink">Agent activity</h2>
        </div>
        <span className="rounded-full bg-tide/10 px-2 py-1 text-xs font-semibold text-tide">{statusLabel}</span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-ink/10">
        <div className="h-full rounded-full bg-tide transition-all" style={{ width: `${progress}%` }} />
      </div>
      <ol className="mt-4 grid max-h-[420px] gap-2 overflow-auto pr-1">
        {events.length ? (
          events.map((event) => (
            <li key={event.event_id} className="grid grid-cols-[22px_1fr] gap-2 rounded-md bg-paper p-2">
              {event.event_type.includes("completed") ? (
                <CheckCircle2 className="mt-0.5 text-leaf" size={18} aria-hidden="true" />
              ) : (
                <CircleDashed className="mt-0.5 text-tide" size={18} aria-hidden="true" />
              )}
              <div>
                <p className="text-sm font-semibold text-ink">{event.stage.replace("_", " ")}</p>
                <p className="text-xs leading-5 text-ink/65">{event.message}</p>
              </div>
            </li>
          ))
        ) : (
          <li className="rounded-md bg-paper p-3 text-sm text-ink/65">Submit a trip to stream backend agent events.</li>
        )}
      </ol>
    </section>
  );
}
