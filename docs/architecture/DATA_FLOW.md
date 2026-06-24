# Data Flow

1. Browser submits a trip request with an anonymous session token.
2. API stores a trip record and queues background planning.
3. Orchestrator emits agent events and persists them.
4. Providers return transparent estimated or fallback data.
5. Optimizer schedules activities under budget and feasibility constraints.
6. Budget service reconciles total cost.
7. Writer creates a grounded narrative summary.
8. Browser receives SSE progress and polls the persisted trip.
9. Revision updates the structured request and creates a new plan version.
