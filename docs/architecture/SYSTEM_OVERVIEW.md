# System Overview

TravelAgenticAI accepts a structured trip request, coordinates deterministic research agents, optimizes a day-by-day schedule, persists the plan, and streams explainable progress to the browser.

Primary boundaries:

- Browser: React planner, timeline, map, budget chart, saved trips, revision UI.
- API: FastAPI `/api/v1`.
- Agents: destination, transport, accommodation, weather, geospatial, optimization, budget, writer, critic, revision.
- Persistence: SQLite locally, PostgreSQL for public deployment.
- Research: reproducible synthetic benchmark and ablation pipeline.

See `diagrams/source/` and `diagrams/rendered/` for editable and rendered diagrams.
