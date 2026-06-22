# Gap Audit

Last updated: 2026-06-21

Branch: `codex/research-production-completion`

## Baseline Commands

- `git status`: branch `main` before branch creation, with obsolete untracked scaffold under `backend/agents`, `backend/core`, `backend/models`, `backend/services`, `frontend/src/components`, and root `package-lock.json`.
- `git branch --show-current`: `main`
- `git remote -v`: `https://github.com/Rajtiwari0202/ai_travel_planner.git`
- `git log --oneline -10`: latest `e81899b Clean generated files from repository`

## Baseline Verification

Passed:

- Backend `..\venv\Scripts\python.exe -m pytest`: 7 passed.
- Backend `..\venv\Scripts\python.exe -m mypy app`: success.
- Frontend `npm run typecheck`: passed.
- Frontend `npm test -- --run`: 1 test passed; npm warned `--run` is an unknown npm config.
- Frontend `npm run build`: passed with large chunk and stale browser-data warnings.
- Frontend `npm run e2e`: 1 Playwright test passed.
- Research `.\venv\Scripts\python.exe research\experiments\run_benchmarks.py`: generated CSV and PNG.
- Research `.\venv\Scripts\python.exe research\experiments\run_ablations.py`: generated CSV.

Failed:

- Backend `..\venv\Scripts\python.exe -m ruff check .`: failed because obsolete untracked prototype modules under `backend/agents`, `backend/core`, `backend/models`, and `backend/services` are still present in the workspace.
- Frontend `npm run lint`: failed because no `lint` script exists.

## Major Gaps

### Optimizer

Status: partial.

The active optimizer in `backend/app/services/optimization/planner.py` is deterministic and budget-aware, but it is still a greedy weighted ranker. It does not provide a CP-SAT formulation, configurable baseline implementations, binding constraints, rejected-candidate explanations, or full hard-constraint reporting.

### Cost Modeling

Status: partial.

The planner correctly avoids multiplying hotel nightly price by traveler count and uses room count, nights, taxes, food, local transport, and contingency. The calculation is embedded inside the optimizer and uses floats. A canonical Decimal-safe money service and reconciliation tests are missing.

### Provider Architecture

Status: partial.

The bundled providers are transparent and free by default, and the curated destination dataset now covers ten Indian destinations. Provider metadata has been expanded, but caching, retry metadata, concurrency controls, geocoding adapters, and routing adapters remain incomplete.

### Agent Orchestration

Status: partial.

The backend emits real persisted SSE events and has named stages for the major agents. It does not yet persist full agent input/output schemas, duration, retry count, timeout status, cancellation state, or one automatic revision cycle after critic failure.

### Revision

Status: partial.

The revision endpoint updates a stored trip and appends revision history, but only supports budget changes, adventure, and indoor/rain hints. It does not yet report previous/new version IDs, cost delta, score delta, affected days, or structured actual changes.

### Frontend

Status: partial.

The Vite React workspace supports planning, streamed progress, results, budget, map, saved trips, methodology, revision, and JSON export. Missing items include React Hook Form/Zod form validation, route-level lazy loading, dedicated research/provider/error pages, strict full response validation, print view, score chart, stronger map empty/error handling, and accessibility test coverage.

### Tests

Status: partial.

Backend tests cover core happy/infeasible paths and API persistence. Frontend and E2E coverage are minimal. The required edge-case suite, coverage reports, provider outage cases, revision matrix, and accessibility checks are missing.

### Security

Status: partial.

Secrets are ignored and no paid API is required. Missing: automated secret scan report, npm/pip audit report, rate limiting, request-size limits, Docker non-root users, and expanded CORS/error leakage review.

### Research

Status: partial.

Research scripts run on a 12-case, 10-destination synthetic benchmark with five optimizer/baseline modes. Citation verification remains incomplete because no scholarly references have been inserted yet.

### Fresh Clone

Status: missing.

Fresh-clone verification has not been run for this branch.

### CI

Status: partial.

GitHub Actions runs backend and frontend basic gates, but does not run frontend lint, E2E, research smoke tests, coverage, audit/secret scan, or paper validation.
