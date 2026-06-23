# Project Explanation

TravelAgenticAI helps plan trips by coordinating specialized backend agents and a deterministic optimizer. The problem is that travel planning combines preferences, budget, time, weather, distance, and feasibility. A single chat response can sound useful while hiding unsupported assumptions; this project keeps those assumptions visible.

Architecture: the React frontend sends a structured request to FastAPI. FastAPI stores the trip, streams agent progress through SSE, calls provider services, runs the optimizer, persists the final plan, and serves saved trips scoped to an anonymous browser session.

Agents: intent validates the request; destination loads context; transport and accommodation produce estimates; weather aligns forecast or fallback guidance; geospatial scoring helps route efficiency; optimization schedules activities; budgeting reconciles costs; writer creates narrative text; critic records validation; revision replans after follow-up instructions.

Data model: `trip_records` stores the request, plan JSON, status, timestamps, and anonymous owner hash. `agent_event_records` stores replayable event history.

Optimizer: OR-Tools CP-SAT is used when available. Deterministic heuristic fallbacks keep the demo usable.

Frontend flow: submit planner form, watch progress, review itinerary, inspect budget and map, revise, export JSON, and revisit saved trips from the same browser session.

Local execution: use Docker Compose for the single-host demo or run backend/frontend separately for development.

Deployment: public target is Render Static Site, Render FastAPI Web Service, and Neon PostgreSQL.

Testing: backend pytest/Ruff/mypy, frontend lint/typecheck/Vitest/build/E2E, research `run_all.py`, Docker build, and deployment smoke checks.

Research: scripts generate benchmark and ablation CSVs plus figures from committed synthetic cases. The paper is a draft, not peer reviewed.

Common modifications: add destinations in provider catalog, tune optimizer weights in `planner.py`, add UI views under `frontend/src/features`, add API routes under `backend/app/api/v1/routes.py`.

Debugging workflow: check health endpoints, request IDs, trip status, event records, frontend console, CORS settings, and database readiness.
