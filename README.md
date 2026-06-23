# TravelAgenticAI

![CI](https://github.com/Rajtiwari0202/ai_travel_planner/actions/workflows/ci.yml/badge.svg)
![Release](https://img.shields.io/github/v/release/Rajtiwari0202/ai_travel_planner?include_prereleases)
![License](https://img.shields.io/badge/license-MIT-green)

TravelAgenticAI is a local-first, explainable multi-agent travel planning and itinerary optimization platform. It coordinates specialized research, weather, geospatial, budgeting, optimization, narrative, validation, and revision stages to produce transparent day-by-day itineraries. It is an itinerary decision-support system, not a booking engine.

## Public Demo

Public deployment is being prepared for the `v1.1.0` public research demo. Public URLs will be added only after the frontend, backend, persistence, SSE, revision, and export flow are verified end to end.

## Preview

![System architecture](docs/architecture/diagrams/rendered/15_public_render_neon_deployment.svg)

## Key Capabilities

- Multi-agent planning workflow with streamed Server-Sent Events.
- OR-Tools CP-SAT itinerary optimization with deterministic fallback.
- Budget reconciliation across transport, lodging, activities, food, local transport, fees, and contingency.
- Anonymous session-scoped saved trips for the public demo.
- SQLite local persistence and PostgreSQL-ready public persistence.
- Leaflet map, budget chart, revision assistant, JSON export, provider transparency, and research pages.
- Reproducible synthetic benchmark and ablation pipeline.

## Workflow

```text
Trip request
  -> intent and data validation
  -> destination, transport, accommodation, weather, geospatial providers
  -> CP-SAT or deterministic fallback optimization
  -> budget reconciliation and validation
  -> grounded itinerary narrative
  -> persisted plan with replayable SSE events
```

## Architecture

Local:

```text
Browser -> Nginx frontend container -> FastAPI backend container -> SQLite volume
```

Public target:

```text
Browser -> Render Static Site -> Render FastAPI Web Service -> Neon PostgreSQL
```

More diagrams are available in `docs/architecture/diagrams/`.

## Tech Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS, React Router, Leaflet, Recharts.
- Backend: FastAPI, Pydantic, SQLAlchemy, Alembic, OR-Tools.
- Persistence: SQLite for local development, PostgreSQL for public deployment.
- Testing: Pytest, Ruff, mypy, Vitest, Playwright.
- Deployment: Docker Compose locally; Render plus Neon for the public research demo.

## Quick Start With Docker

```powershell
cd F:\travelAgenticAi
docker compose up -d --build
```

Open the local app:

```text
http://127.0.0.1:18080
```

Health checks:

```powershell
curl.exe http://127.0.0.1:18080/healthz
curl.exe http://127.0.0.1:18080/api/v1/health/ready
```

## Manual Development

Backend:

```powershell
cd F:\travelAgenticAi\backend
..\venv\Scripts\python.exe -m pip install -r requirements.txt
..\venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Frontend:

```powershell
cd F:\travelAgenticAi\frontend
npm ci
$env:VITE_API_BASE_URL = "http://127.0.0.1:8000/api/v1"
npm run dev
```

## Public Deployment Summary

The repository includes `render.yaml` for:

- Render FastAPI web service
- Render static frontend
- Neon PostgreSQL via `DATABASE_URL`
- Render health checks
- build-time frontend API configuration

See `docs/deployment/RENDER_DEPLOYMENT.md`, `docs/deployment/NEON_SETUP.md`, and `docs/deployment/PUBLIC_ENVIRONMENT_VARIABLES.md`.

## Research Contribution

The research draft evaluates a multi-agent itinerary optimizer over synthetic benchmark cases with deterministic baselines and ablations. The current paper is a draft, not peer reviewed, and does not include fabricated citations or user-study data.

## Reproducibility

```powershell
cd F:\travelAgenticAi
.\venv\Scripts\python.exe research\experiments\run_all.py
```

Outputs:

- `research/results/benchmark_results.csv`
- `research/results/ablation_summary.csv`
- `research/figures/benchmark_scores.png`

## Data Transparency

Transport and accommodation prices are estimates unless explicitly labeled otherwise. The app does not provide live flight inventory, live hotel availability, payment, ticketing, or booking confirmation.

## Limitations

- No payments or commercial booking flow.
- No verified live flight or hotel inventory.
- No full user accounts; the public demo uses anonymous session-scoped access.
- Research paper still needs verified citations, deeper experiments, and human evaluation.
- Public production SaaS maturity still requires long-term monitoring, backups, abuse operations, and incident processes.

## Documentation

Start with `docs/README.md`.

Important sections:

- `docs/architecture/`
- `docs/agents/`
- `docs/api/`
- `docs/database/`
- `docs/deployment/`
- `docs/operations/`
- `docs/research/`
- `docs/security/`
- `docs/testing/`
- `docs/presentation/`

## License

MIT. See `LICENSE`.

## Maintainer

Repository: `https://github.com/Rajtiwari0202/ai_travel_planner`
