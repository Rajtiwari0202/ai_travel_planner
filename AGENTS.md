# TravelAgenticAI Agent Guide

This repository is a local-first, explainable multi-agent travel planning and itinerary optimization platform. Keep changes scoped, tested, and honest about data sources.

## Repository Layout

- `backend/`: FastAPI application, agents, providers, persistence, and tests.
- `frontend/`: Vite React TypeScript client and Playwright tests.
- `research/`: reproducible benchmark datasets, scripts, figures, and paper draft.
- `docs/`: architecture, API, deployment, operations, research, security, testing, audits, and presentation material.
- `docker-compose.yml`: local/single-host demo deployment.

Historical project prompts are archived under `docs/codex/`.

## Canonical Commands

Backend:

```powershell
cd F:\travelAgenticAi\backend
..\venv\Scripts\python.exe -m pytest
..\venv\Scripts\python.exe -m ruff check .
..\venv\Scripts\python.exe -m mypy app
..\venv\Scripts\python.exe -m pip_audit -r requirements.txt
```

Frontend:

```powershell
cd F:\travelAgenticAi\frontend
npm ci
npm run lint
npm run typecheck
npm test
npm run build
npm run e2e
```

Research:

```powershell
cd F:\travelAgenticAi
.\venv\Scripts\python.exe research\experiments\run_all.py
```

Docker:

```powershell
cd F:\travelAgenticAi
docker compose up -d --build
docker compose -p travelagenticai-deploy ps
```

## Engineering Rules

- Preserve `v1.0.0`; do not move or replace that tag.
- Work on feature branches and use small conventional commits.
- Prefer existing patterns over broad rewrites.
- Do not add paid-service requirements.
- Do not present estimated prices as live booking inventory.
- Do not commit secrets, local databases, virtual environments, caches, or build outputs.
- Keep `DATABASE_URL` environment-driven; SQLite is local default, PostgreSQL is production target.
- Keep CORS explicit in production.

## Testing Requirements

Run the relevant local checks before committing. For deployment changes, verify:

- backend health and readiness
- frontend production build
- Docker Compose path
- public-style API URL configuration
- trip creation, SSE progress, saved trips, revision, and export

## Security Rules

- Never log full database URLs, tokens, passwords, or provider secrets.
- Validate UUIDs and user input boundaries.
- Keep anonymous trip access owner-scoped.
- Use safe error envelopes in production.
- Do not expose all trips through public endpoints.

## Definition of Done

A change is done when it is implemented, documented, tested, and does not weaken the honest release scope:

- local/single-host research demo: deployable
- research paper: draft, not peer reviewed
- public SaaS: not claimed complete
- booking platform: out of scope until verified inventory and payments exist
