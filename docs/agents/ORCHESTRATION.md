# Orchestration

`TripOrchestrator` coordinates planning in ordered stages and emits persisted SSE events:

1. plan started
2. intent
3. destination
4. transport
5. accommodation
6. weather
7. optimization
8. writer
9. validation
10. plan completed

Failures are caught, the trip status becomes `failed`, and a sanitized event is emitted.
