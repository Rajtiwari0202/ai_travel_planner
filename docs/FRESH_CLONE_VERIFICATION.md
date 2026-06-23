# Fresh Clone Verification

Last updated: 2026-06-23

## Clone

- Source: `https://github.com/Rajtiwari0202/ai_travel_planner.git`
- Branch: `codex/research-production-completion`
- Fresh folder: `F:\travelAgenticAi-fresh-verify-20260622-195819`
- Clone command: `git clone --branch codex/research-production-completion https://github.com/Rajtiwari0202/ai_travel_planner.git F:\travelAgenticAi-fresh-verify-20260622-195819`

## Setup

| Area | Command | Result |
| --- | --- | --- |
| Backend venv | `python -m venv venv` | passed |
| Backend dependencies | `.\venv\Scripts\python.exe -m pip install -r backend\requirements.txt` | passed |
| Backend audit tools | `.\venv\Scripts\python.exe -m pip install pip-audit coverage` | passed |
| Frontend dependencies | `npm ci` in `frontend` | passed with 0 vulnerabilities |

## Verification Results

| Command | Result | Notes |
| --- | --- | --- |
| `..\venv\Scripts\python.exe -m pytest` in `backend` | passed | 11 passed, 1 Starlette `TestClient` deprecation warning. |
| `..\venv\Scripts\python.exe -m ruff check .` in `backend` | passed | All checks passed. |
| `..\venv\Scripts\python.exe -m mypy app` in `backend` | passed | Success, 30 source files. |
| `..\venv\Scripts\python.exe -m pip_audit -r requirements.txt` in `backend` | passed | No known vulnerabilities found. |
| `..\venv\Scripts\python.exe -m coverage run -m pytest` plus `coverage report --fail-under=70` | passed | 91% coverage. |
| `npm audit` in `frontend` | passed | 0 vulnerabilities. |
| `npm run lint` in `frontend` | passed | ESLint passed. |
| `npm run typecheck` in `frontend` | passed | TypeScript passed. |
| `npm test` in `frontend` | passed | 1 Vitest test passed. |
| `npm run build` in `frontend` | passed with warning | Planner route chunk remains over 500 kB. |
| `npm run e2e` in `frontend` | passed on rerun | Initial cold run timed out waiting for the lazy planner route; E2E timeout was increased afterward. |
| `.\venv\Scripts\python.exe research\experiments\run_all.py` | passed | Regenerated benchmark CSV, ablation CSV, and PNG; working tree stayed clean. |

## Docker Verification

After adding `.dockerignore`, both local image builds passed from `F:\travelAgenticAi`:

- `docker build -f backend/Dockerfile -t travelagenticai-backend:test .`
- `docker build -f frontend/Dockerfile -t travelagenticai-frontend:test .`

The `.dockerignore` reduced frontend build context to about 1.5 MB and backend build context to about 29 MB in the observed local run.

## Notes

- The fresh clone remained clean after research regeneration.
- Docker verification was run in the main working tree after Docker Desktop became available and `.dockerignore` was added.
- The project is verified as a local-first demo/research prototype, not as a hosted production booking service.
