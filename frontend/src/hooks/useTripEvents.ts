import { useEffect, useMemo, useState } from "react";
import { eventSourceUrl, parseAgentEvent } from "../services/api";
import type { AgentEvent, EventType } from "../types/api";

const EVENT_TYPES: EventType[] = [
  "plan.started",
  "agent.started",
  "agent.progress",
  "agent.completed",
  "agent.failed",
  "optimization.completed",
  "validation.completed",
  "plan.completed",
  "plan.failed",
];

export function useTripEvents(tripId: string | null) {
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setEvents([]);
    setError(null);
    if (!tripId) {
      setConnected(false);
      return undefined;
    }

    const source = new EventSource(eventSourceUrl(tripId));
    setConnected(true);

    const handleEvent = (message: MessageEvent<string>) => {
      const event = parseAgentEvent(message);
      setEvents((current) => {
        if (current.some((item) => item.event_id === event.event_id)) {
          return current;
        }
        return [...current, event];
      });
      if (event.event_type === "plan.completed" || event.event_type === "plan.failed") {
        source.close();
        setConnected(false);
      }
    };

    EVENT_TYPES.forEach((type) => source.addEventListener(type, handleEvent));
    source.onerror = () => {
      setError("Event stream disconnected.");
      source.close();
      setConnected(false);
    };

    return () => {
      EVENT_TYPES.forEach((type) => source.removeEventListener(type, handleEvent));
      source.close();
      setConnected(false);
    };
  }, [tripId]);

  const latestProgress = useMemo(() => {
    const progressEvents = events.filter((event) => typeof event.progress === "number");
    return progressEvents[progressEvents.length - 1]?.progress ?? 0;
  }, [events]);

  const completed = events.some((event) => event.event_type === "plan.completed");

  return { events, connected, error, latestProgress, completed };
}
