# Deployment Notes

Last updated: 2026-06-23

TravelAgenticAI now has a verified Docker Compose deployment path for a local or single-host demo deployment.

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

## Hosted Deployment Requirements

Before exposing this outside a trusted demo environment:

- Put HTTPS/TLS in front of the frontend service.
- Set `FRONTEND_PORT`, `CORS_ORIGINS`, and any public origin values for the target host.
- Add authentication before storing real user trip data.
- Configure host-level backups for the SQLite volume or migrate persistence to a managed database.
- Add request-size/rate-limit enforcement at the edge proxy.
- Run image vulnerability scanning in the deployment registry or CI platform.

This is deployment-ready as a local/single-host demo. It is not a live booking, payment, or authenticated SaaS system.
