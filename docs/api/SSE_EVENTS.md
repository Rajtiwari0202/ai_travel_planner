# SSE Events

Endpoint:

```text
GET /api/v1/trips/{trip_id}/events
```

The stream sends `id`, `event`, and JSON `data`. Persisted events are replayed before live events.

Common event names:

- `plan.started`
- `agent.started`
- `agent.completed`
- `optimization.completed`
- `validation.completed`
- `plan.completed`
- `plan.failed`
