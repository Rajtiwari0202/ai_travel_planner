# TravelAgenticAI

TravelAgenticAI is a local-first agentic travel planning and itinerary optimization platform. It is an itinerary decision-support system, not a booking engine.

The default demo uses free/open-source software, curated local datasets, deterministic estimates, SQLite persistence, and a template narrative provider. No paid API or LLM is required.

## Release Readiness

- Local/single-host research demo: about 90-95% complete.
- Research-paper submission: about 70-80% complete; verified citations, deeper experiments, statistical treatment, and human evaluation remain.
- Public production SaaS: about 55-65% complete; authentication, HTTPS, backups, hosted secrets, monitoring, abuse protection, and production operations remain.
- Actual booking platform: not applicable yet; payments and verified flight/hotel inventory are intentionally absent.

Suggested release title: **TravelAgenticAI v1.0.0 - Local-First Research Release**.

## Current Feature Status

Implemented:

- Versioned FastAPI API under `/api/v1`
- SQLite trip persistence
- Backend-generated agent events via Server-Sent Events
- Deterministic destination, transport, accommodation, weather fallback, geospatial, optimization, budget, writer, critic, and revision flow
- Budget-feasible plan generation or explicit infeasibility result
- Backend-supplied coordinates for all scheduled activities
- Vite React TypeScript frontend
- Planner form, real event timeline, itinerary results, budget chart, Leaflet map, revision assistant, saved trips page, provider status page, research page, methodology page, JSON export
- Backend tests, frontend tests, frontend build, Ruff, mypy, dependency audits, coverage, E2E, and CI configuration
- OR-Tools CP-SAT optimizer with deterministic heuristic fallback
- Reproducible benchmark scripts and paper draft

Not implemented:

- Live booking or payment
- Real-time flight/hotel inventory
- Verified user-satisfaction study
- Production authentication
- Fully modeled booking-grade constraints such as verified opening hours, OSRM route matrices, and arrival/departure windows

## Architecture

```text
frontend/                 Vite React TypeScript client
backend/app/              Canonical FastAPI backend
backend/app/agents/       Typed orchestration flow
backend/app/services/     Providers, weather, geospatial, optimization, narrative
backend/app/repositories/ SQLite persistence access
research/                 Benchmarks, figures, and paper draft
docs/                     Architecture and API notes
```

See `docs/architecture/` for diagrams and ADRs.

## Data Honesty

The UI and API distinguish:

- Estimated transport price
- Estimated accommodation price
- Public/open-data inspired attraction coordinates
- Live weather when explicitly enabled
- Fallback weather guidance when live weather is disabled or unavailable
- Synthetic fallback destination data

No synthetic or estimated data is presented as live booking availability.

## Quickstart - Windows PowerShell

```powershell
cd F:\travelAgenticAi

# Backend
.\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
cd backend
..\venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Frontend in another terminal
cd F:\travelAgenticAi\frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Docker Deploy

```powershell
cd F:\travelAgenticAi
docker compose up -d --build
```

Open `http://127.0.0.1:18080`. The frontend container serves static assets with Nginx and proxies `/api` to the internal backend container.

## Test Commands

```powershell
cd F:\travelAgenticAi\backend
..\venv\Scripts\python.exe -m pip install pip-audit coverage
..\venv\Scripts\python.exe -m pytest
..\venv\Scripts\python.exe -m ruff check .
..\venv\Scripts\python.exe -m mypy app
..\venv\Scripts\python.exe -m coverage run -m pytest
..\venv\Scripts\python.exe -m coverage report --fail-under=70
..\venv\Scripts\python.exe -m pip_audit -r requirements.txt

cd F:\travelAgenticAi\frontend
npm audit
npm run lint
npm run typecheck
npm test
npm run build
npm run e2e
```

## Research

```powershell
cd F:\travelAgenticAi
.\venv\Scripts\python.exe research\experiments\run_benchmarks.py
.\venv\Scripts\python.exe research\experiments\run_ablations.py
.\venv\Scripts\python.exe research\experiments\run_all.py
```

Outputs are written to `research/results/` and `research/figures/`.

## API

Core endpoints:

- `GET /api/v1/health`
- `POST /api/v1/trips`
- `GET /api/v1/trips`
- `GET /api/v1/trips/{trip_id}`
- `POST /api/v1/trips/{trip_id}/revise`
- `GET /api/v1/trips/{trip_id}/events`
- `DELETE /api/v1/trips/{trip_id}`
- `GET /api/v1/providers/status`
- `GET /api/v1/destinations/search`

OpenAPI docs are available at `http://localhost:8000/docs`.

For Docker Compose deployment, API routes are proxied under the same host, for example `http://127.0.0.1:18080/api/v1/health`.

## Intended GitHub Repository

User-designated repo: `https://github.com/Rajtiwari0202/ai_travel_planner`

The local Git remote was not changed automatically because `AGENTS.md` explicitly says not to change Git remotes.

## License

MIT. See `LICENSE`.
