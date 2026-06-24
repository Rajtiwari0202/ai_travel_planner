# Final Verification Report

Date: 2026-06-24
Branch: `main`

## Local Verification

Backend:

- `python -m coverage run -m pytest`: 12 passed, 1 Starlette TestClient warning.
- `python -m coverage report --show-missing --fail-under=70`: 90% total coverage.
- `python -m ruff check .`: passed.
- `python -m mypy app`: passed.
- `python -m pip_audit -r requirements.txt`: no known vulnerabilities found.
- `python scripts/check_database.py`: `database=ok`.
- SQLite migration smoke with `DATABASE_URL=sqlite:///./tmp_migration_smoke.sqlite3` and `python scripts/migrate.py`: passed.

Frontend:

- `npm prune`: passed.
- `npm dedupe`: passed; updated one transitive lockfile entry.
- `npm audit`: 0 vulnerabilities.
- `npm run lint`: passed.
- `npm run typecheck`: passed.
- `npm test`: 1 test passed.
- `npm run build`: passed with known large planner chunk warning from map/chart libraries.
- `npm run e2e`: 1 Chromium test passed.

Research and docs:

- `python research/experiments/run_all.py`: regenerated benchmark CSV, ablation CSV, and benchmark PNG.
- `python scripts/check_docs.py`: `docs=ok`.
- Mermaid render inventory: 18 sources, 18 SVG files, 18 PNG files.

Docker:

- `docker compose config`: passed.
- `docker compose -p travelagenticai-v11-check build backend frontend`: passed.
- `docker compose -p travelagenticai-deploy up -d --build`: passed.
- `curl.exe http://127.0.0.1:18080/healthz`: `ok`.
- `curl.exe http://127.0.0.1:18080/api/v1/health/ready`: `{"status":"ready","database":"ok"}`.
- Proxied trip creation through `http://127.0.0.1:18080/api/v1/trips`: completed.
- Proxied revision through `/api/v1/trips/{trip_id}/revise`: completed and revision history count was `1`.

Docker cleanup:

- `docker image prune -f`: completed without removing volumes.
- `docker builder prune -f`: reclaimed build cache without removing volumes.

## Current Local Demo URL

- `http://127.0.0.1:18080`

## Public Deployment Status

Complete for the `v1.1.0` public research demo.

Verified public URLs:

- Frontend: `https://travelagenticai-web.onrender.com`
- Backend readiness: `https://travelagenticai-api.onrender.com/api/v1/health/ready`
- Backend version: `https://travelagenticai-api.onrender.com/api/v1/version`

Public verification:

- Render backend service deployed live after pinning backend Python runtime to `3.12.8`.
- Render frontend static service deployed live.
- Neon PostgreSQL migration completed successfully.
- `GET /api/v1/health/live`: 200.
- `GET /api/v1/health/ready`: 200 with database ok.
- `GET /api/v1/version`: 200 with production environment.
- `POST /api/v1/trips`: 202 with a trip id.
- `GET /api/v1/trips/{trip_id}`: 200 and status `complete`.
- `GET /api/v1/trips`: 200 and included the anonymous-session-owned trip.
- `POST /api/v1/trips/{trip_id}/revise`: 200 with one revision history entry.
- Anonymous ownership isolation: another session received 404 for the same trip.
- CORS negative check: an unknown origin was not echoed in `access-control-allow-origin`.
- Public browser screenshot pass captured desktop and mobile itinerary renders:
  - `docs/assets/screenshots/public-demo-desktop.png`
  - `docs/assets/screenshots/public-demo-mobile.png`

## Known Warnings

- Frontend planner chunk remains above 500 kB because Leaflet and Recharts are used in the planner route.
- FastAPI/Starlette TestClient emits a deprecation warning from the installed dependency stack.
