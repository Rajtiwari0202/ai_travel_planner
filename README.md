# TravelAgenticAI

![CI](https://github.com/Rajtiwari0202/ai_travel_planner/actions/workflows/ci.yml/badge.svg)
![Release](https://img.shields.io/github/v/release/Rajtiwari0202/ai_travel_planner?include_prereleases)
![License](https://img.shields.io/badge/license-MIT-green)

TravelAgenticAI is a public, local-first research demo for explainable multi-agent travel planning and budget-constrained itinerary optimization. It coordinates specialized planning agents, deterministic providers, OR-Tools CP-SAT optimization, budget reconciliation, map rendering, revision, persistence, and research benchmarking into one deployable full-stack product.

It is an itinerary decision-support platform, not a booking engine. Prices are transparent estimates and the app does not sell tickets, process payments, or claim verified live flight/hotel inventory.

## Live Demo

| Surface | Link |
| --- | --- |
| Public frontend | https://travelagenticai-web.onrender.com |
| Backend readiness | https://travelagenticai-api.onrender.com/api/v1/health/ready |
| Backend version | https://travelagenticai-api.onrender.com/api/v1/version |
| GitHub release | https://github.com/Rajtiwari0202/ai_travel_planner/releases/tag/v1.1.0 |

The public demo runs on Render with Neon PostgreSQL. Render free services may take a short time to wake after inactivity.

## Screenshots

### Desktop Planner

![TravelAgenticAI public desktop demo](docs/assets/screenshots/public-demo-desktop.png)

### Mobile Planner

<img src="docs/assets/screenshots/public-demo-mobile.png" alt="TravelAgenticAI public mobile demo" width="360" />

## What It Does

- Builds a day-by-day itinerary from origin, destination, dates, travelers, budget, and preferences.
- Streams planning progress with Server-Sent Events so users can see each agent stage.
- Uses OR-Tools CP-SAT to search for budget-feasible schedules, with deterministic fallback strategies.
- Reconciles transport, accommodation, activities, food, local transport, taxes, fees, and contingency.
- Labels provider data as estimate, fallback, open data, cached, synthetic, or live where applicable.
- Persists trips with anonymous session ownership for the public demo.
- Supports itinerary revision, saved trips, JSON export, maps, provider status, research pages, and methodology documentation.
- Ships reproducible benchmark and ablation artifacts for the research track.

## Architecture

Public deployment:

```text
Browser
  -> Render Static Site
  -> Render FastAPI Web Service
  -> Neon PostgreSQL
```

Local Docker deployment:

```text
Browser
  -> Nginx frontend container
  -> FastAPI backend container
  -> SQLite volume
```

![Public Render and Neon architecture](docs/architecture/diagrams/rendered/15_public_render_neon_deployment.svg)

Planning workflow:

```text
Trip request
  -> intent and request validation
  -> destination, transport, accommodation, weather, and geospatial providers
  -> CP-SAT or deterministic fallback optimization
  -> budget reconciliation and critic validation
  -> itinerary narrative generation
  -> persistence with replayable SSE events
  -> revision and export
```

## Agent Pipeline

| Stage | Responsibility |
| --- | --- |
| Intent agent | Validates dates, budget, travelers, and preferences. |
| Destination research agent | Loads destination context and candidate activities. |
| Transport research agent | Estimates travel modes, durations, and costs. |
| Accommodation research agent | Selects lodging options and room-count assumptions. |
| Weather agent | Adds forecast or fallback weather guidance. |
| Geospatial agent | Scores distance and route tradeoffs. |
| Optimization agent | Builds a budget-feasible schedule with CP-SAT or deterministic fallback. |
| Budget agent | Reconciles total estimated cost and remaining budget. |
| Writer agent | Produces an explainable itinerary narrative. |
| Critic agent | Validates feasibility, assumptions, warnings, and data labels. |
| Revision agent | Re-plans from user instructions while preserving history. |

## Tech Stack

| Area | Tools |
| --- | --- |
| Frontend | React, TypeScript, Vite, Tailwind CSS, React Router, Leaflet, Recharts |
| Backend | FastAPI, Pydantic, SQLAlchemy, Alembic, OR-Tools |
| Persistence | SQLite locally, Neon PostgreSQL publicly |
| Testing | Pytest, Ruff, mypy, Vitest, Playwright |
| Deployment | Docker Compose, Nginx, Render, Neon |
| Research | Synthetic benchmark cases, ablations, generated CSVs, generated figures |

## Verification Status

Verified for the `v1.1.0` release:

- GitHub Actions CI passed on `main`.
- Public frontend returned HTTP 200.
- Public backend readiness returned `{"status":"ready","database":"ok"}`.
- Public `/api/v1/version` returned `1.1.0` in production.
- Public trip create, fetch, list, and revise flow passed against Neon persistence.
- Anonymous ownership isolation returned 404 for another session.
- Unknown-origin CORS negative check did not echo the origin.
- Desktop and mobile public browser screenshots were captured after itinerary completion.
- Local backend tests, linting, type checks, frontend tests, production build, Playwright E2E, research smoke, docs validation, and Docker Compose deployment passed.

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

## Research Track

The repository includes a reproducible research pipeline for benchmark and ablation evaluation. The current paper draft is not peer reviewed and intentionally avoids fabricated citations or user-study claims.

```powershell
cd F:\travelAgenticAi
.\venv\Scripts\python.exe research\experiments\run_all.py
```

Generated outputs:

- `research/results/benchmark_results.csv`
- `research/results/ablation_summary.csv`
- `research/figures/benchmark_scores.png`

## Deployment Notes

The public research demo uses:

- Render static site for the React frontend.
- Render Python web service for the FastAPI backend.
- Neon PostgreSQL through provider-managed secret storage.
- Render health checks on `/api/v1/health/ready`.
- Frontend build-time API configuration.

Deployment documentation:

- `docs/deployment/RENDER_DEPLOYMENT.md`
- `docs/deployment/NEON_SETUP.md`
- `docs/deployment/PUBLIC_ENVIRONMENT_VARIABLES.md`
- `docs/audits/FINAL_VERIFICATION_REPORT.md`

## Scope And Limitations

What this release is:

- A full-stack public research demo.
- A local-first portfolio project.
- An explainable multi-agent planning and optimization system.
- A reproducible benchmark and documentation package.

What this release is not:

- Not a booking platform.
- Not a payment or ticketing system.
- Not a verified live inventory provider.
- Not a production SaaS with user accounts, long-term monitoring, backups, abuse operations, and commercial SLAs.

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

Repository: https://github.com/Rajtiwari0202/ai_travel_planner
