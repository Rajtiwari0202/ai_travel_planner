# Deployment Notes

Last updated: 2026-06-24

TravelAgenticAI has two verified deployment paths:

- Local/single-host Docker Compose deployment.
- Public research demo deployment on Render with Neon PostgreSQL.

This is suitable for a research and portfolio release. It is not a production SaaS or booking platform release.

## Production-Style Local Deploy

```powershell
cd F:\travelAgenticAi
docker compose up -d --build
```

Open:

- App: `http://127.0.0.1:18080`
- Frontend health: `http://127.0.0.1:18080/healthz`
- API health through Nginx: `http://127.0.0.1:18080/api/v1/health`

The default host port is `18080` to avoid common local conflicts on `8080`. Override it with:

```powershell
$env:FRONTEND_PORT = "8081"
docker compose up -d --build
```

Stop:

```powershell
docker compose down
```

## Architecture

- `frontend/Dockerfile` builds the Vite app and serves static assets with unprivileged Nginx.
- `frontend/nginx.conf` serves the SPA, exposes `/healthz`, adds baseline security headers, and proxies `/api/` to the backend service.
- `backend/Dockerfile` runs FastAPI/Uvicorn as an unprivileged `app` user and includes a container healthcheck.
- `docker-compose.yml` exposes only the frontend by default; the backend stays on the internal Compose network.
- SQLite data persists in the `travelagenticai-data` volume.

## Verified Commands

These were verified locally on 2026-06-23:

```powershell
docker compose config
docker build -f backend/Dockerfile -t travelagenticai-backend:deploy .
docker build -f frontend/Dockerfile -t travelagenticai-frontend:deploy .
docker compose -p travelagenticai-deploy up -d --build
curl.exe -i http://127.0.0.1:18080/healthz
curl.exe -i http://127.0.0.1:18080/api/v1/health
```

A proxied trip creation request through `http://127.0.0.1:18080/api/v1/trips` completed successfully.

## Public Research Demo

Verified public URLs:

- Frontend: `https://travelagenticai-web.onrender.com`
- Backend readiness: `https://travelagenticai-api.onrender.com/api/v1/health/ready`
- Backend version: `https://travelagenticai-api.onrender.com/api/v1/version`

The public demo uses Render HTTPS, a Render static frontend, a Render FastAPI web service, and Neon PostgreSQL. It was verified for health checks, database readiness, trip creation, persisted fetch/list, revision, anonymous ownership isolation, CORS negative behavior, and browser screenshots.

## Production SaaS Requirements

Before treating this as production SaaS:

- Add authentication before storing real user trip data.
- Add backup and restore procedures for managed PostgreSQL.
- Add long-term monitoring, alerting, abuse operations, and incident response ownership.
- Add external vulnerability scanning in the deployment registry or CI platform.
- Add production data contracts for any live provider integrations.
- Do not enter real payment, passport, or private booking credentials; this app is not a booking system.

## Release Scope

- Local/single-host research demo: about 95% complete.
- Public research demo: about 90% complete.
- Research-paper submission: about 70-80% complete.
- Public production SaaS: about 60-65% complete.
- Actual booking platform: not applicable until verified inventory and payments are added.
