# Acceptance Matrix

Last updated: 2026-06-23

| Requirement | Status | Implementation File | Relevant Test | Verification Command | Evidence / Gap |
| --- | --- | --- | --- | --- | --- |
| Correct Git remote | complete | `.git/config` | n/a | `git remote -v` | Remote is `https://github.com/Rajtiwari0202/ai_travel_planner.git`. |
| Work on continuation branch | complete | git branch | n/a | `git branch --show-current` | Branch is `codex/research-production-completion`. |
| Versioned API | complete | `backend/app/api/v1/routes.py` | `backend/tests/test_api.py` | `pytest` | `/api/v1` endpoints exist and smoke tests pass. |
| Trip persistence | complete | `backend/app/repositories/trips.py` | `backend/tests/test_api.py` | `pytest` | Trip request, plan, and events persist in SQLite. |
| Real SSE events | partial | `backend/app/services/events.py` | `backend/tests/test_api.py` | `pytest`, `npm run e2e` | Events are persisted and streamed; terminal-state and reconnection tests are still thin. |
| Free default operation | complete | `backend/app/services/providers/catalog.py`, `backend/app/services/weather/service.py` | `backend/tests/test_planner.py` | `pytest` | No paid API or LLM needed. Live weather is disabled by default. |
| Data-status labels | complete | `backend/app/schemas/trip.py`, `frontend/src/features/itinerary/ItineraryResults.tsx` | `backend/tests/test_planner.py` | `pytest`, `npm run build` | Provider metadata includes source, kind, provider, source URL/id fields, warnings, error, confidence, and currency. |
| Backend-only coordinates | complete | `backend/app/services/providers/catalog.py`, `frontend/src/features/map/ItineraryMap.tsx` | `backend/tests/test_planner.py` | `pytest`, `npm run e2e` | Scheduled activities include backend coordinates; browser does not geocode. |
| Weather date alignment | complete | `backend/app/services/weather/service.py`, `backend/tests/test_planner.py` | `backend/tests/test_planner.py` | `pytest` | Forecast dates align with trip days; rainy outdoor conflicts are rejected in weather-aware mode. |
| Canonical money model | complete | `backend/app/services/budgeting/money.py` | `backend/tests/test_planner.py` | `pytest` | Decimal-safe budget service reconciles transport, accommodation, activities, local transport, food, fees, contingency, total, and remaining. |
| Room-count hotel costing | complete | `backend/app/services/budgeting/money.py`, `backend/app/services/optimization/planner.py` | `backend/tests/test_planner.py` | `pytest` | Uses `assumed_rooms * nights`, not traveler count. |
| CP-SAT optimizer | partial | `backend/app/services/optimization/planner.py` | `backend/tests/test_planner.py` | `pytest`, `run_all.py` | OR-Tools CP-SAT is used when installed and returns optimizer metadata; verified opening hours, arrival windows, and OSRM route matrices remain deeper-modeling gaps. |
| Heuristic fallback optimizer | complete | `backend/app/services/optimization/planner.py` | `backend/tests/test_planner.py` | `pytest` | Deterministic cheapest-first and weighted-ranker modes share the same candidate and budget model. |
| Required baselines | complete | `research/experiments/run_benchmarks.py` | research script | `run_all.py` | Runs cheapest-first, weighted ranker, CP-SAT, CP-SAT no-weather, and CP-SAT no-geospatial systems. |
| Agent typed state and timing | partial | `backend/app/agents/orchestrator.py` | `backend/tests/test_api.py` | `pytest` | Named stages emit events; full input/output schemas, duration, retry, and timeout metadata remain limited. |
| Revision endpoint | partial | `backend/app/agents/orchestrator.py` | `backend/tests/test_api.py` | `pytest` | Revision persists structured delta metadata, but supported instruction types remain narrow. |
| Frontend planner | partial | `frontend/src/features/planner/PlannerWorkspace.tsx` | `frontend/src/app/App.test.tsx`, E2E | `npm test`, `npm run e2e` | Planner works; React Hook Form and stricter field-level validation are not yet adopted. |
| Frontend map | complete | `frontend/src/features/map/ItineraryMap.tsx` | E2E smoke | `npm run e2e` | Markers render, single-point bounds are handled, and accessible text summary exists. |
| Saved trips | complete | `frontend/src/features/trips/SavedTripsPage.tsx` | E2E smoke | `npm run e2e` | Basic saved-trip page exists. |
| Provider status page | complete | `frontend/src/features/providers/ProviderStatusPage.tsx` | build/typecheck | `npm run build`, `npm run typecheck` | Dedicated provider-status route exists and handles loading/error states. |
| Research page | complete | `frontend/src/features/research/ResearchPage.tsx` | build/typecheck | `npm run build`, `npm run typecheck` | Dedicated research route summarizes current benchmark and ablation evidence. |
| Route-level chunking | partial | `frontend/src/app/App.tsx` | build | `npm run build` | Routes are lazy-loaded; planner chunk remains above 500 kB due map/chart dependencies. |
| Frontend lint | complete | `frontend/package.json`, `frontend/eslint.config.js` | n/a | `npm run lint` | ESLint passes for TypeScript frontend sources. |
| Backend Ruff gate | complete | `backend/pyproject.toml` | n/a | `ruff check .` | Whole-backend Ruff passes. |
| Dependency audits | complete | `backend/requirements.txt`, `frontend/package-lock.json` | n/a | `pip_audit`, `npm audit` | Both backend and frontend dependency audits report no known vulnerabilities. |
| Docker non-root users | complete | `backend/Dockerfile`, `frontend/Dockerfile`, `.dockerignore` | CI Docker job | `docker build` locally and in CI | Dockerfiles run as unprivileged users; backend and frontend image builds pass locally. |
| Docker Compose deployment | complete | `docker-compose.yml`, `frontend/nginx.conf`, `docs/deployment/README.md` | deploy smoke | `docker compose up -d --build`, `curl /healthz`, `curl /api/v1/health` | Frontend serves on host port `18080`, proxies `/api` to internal backend, and trip creation completes through proxy. |
| E2E coverage | partial | `frontend/e2e/planner.spec.ts` | Playwright | `npm run e2e` | One happy-path scenario only. |
| Research dataset breadth | complete | `research/datasets/benchmark_cases.json` | research scripts | `run_all.py` | 12 synthetic benchmark cases cover 10 Indian destinations and varied constraints. |
| Paper citations | partial | `research/paper/paper.tex`, `research/paper/CITATION_VERIFICATION.md` | n/a | n/a | No fabricated citations are used; related work remains blocked on human literature verification. |
| Fresh-clone verification | complete | `docs/FRESH_CLONE_VERIFICATION.md` | full local gates | documented commands | Fresh clone passed backend, frontend, research, and E2E verification. |
| CI completeness | complete | `.github/workflows/ci.yml` | GitHub Actions | local workflow syntax not executed | CI is configured for secret scan, backend audit/coverage/lint/mypy/tests, frontend audit/lint/typecheck/test/build, E2E, research, and Docker builds. |
