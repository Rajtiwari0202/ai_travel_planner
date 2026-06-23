# Gap Audit

Last updated: 2026-06-23

Branch: `codex/research-production-completion`

## Baseline Commands

- `git status`: branch `main` before branch creation, with obsolete untracked scaffold under `backend/agents`, `backend/core`, `backend/models`, `backend/services`, `frontend/src/components`, and root `package-lock.json`.
- `git branch --show-current`: `main`
- `git remote -v`: `https://github.com/Rajtiwari0202/ai_travel_planner.git`
- `git log --oneline -10`: latest `e81899b Clean generated files from repository`

## Resolved Since Baseline

- Removed obsolete local scaffold directories that broke whole-backend Ruff checks.
- Added frontend ESLint and `npm run lint`.
- Added OR-Tools CP-SAT optimization with deterministic fallback modes.
- Added canonical Decimal-safe budget reconciliation.
- Expanded provider metadata and bundled Indian destination coverage.
- Expanded benchmark dataset to 12 synthetic cases across 10 Indian destinations.
- Added benchmark, ablation, and run-all research workflows.
- Added provider-status and research frontend routes.
- Added route-level lazy loading.
- Cleared backend and frontend dependency audits.
- Added CI jobs for secret scan, backend audit/coverage/lint/mypy/tests, frontend audit/lint/typecheck/test/build, E2E, research, and Docker builds.
- Updated Dockerfiles to run as non-root users and added `.dockerignore` for practical build contexts.
- Completed fresh-clone verification.
- Added production-style Docker Compose deploy path with Nginx static frontend, `/api` proxy, healthchecks, internal backend, and verified trip-creation smoke.

## Remaining Gaps

### Optimizer

Status: partial.

The implemented optimizer uses OR-Tools CP-SAT when available and deterministic heuristic fallbacks otherwise. Remaining gaps are production-grade constraints: verified opening hours, arrival/departure windows, live inventory, and OSRM-style route matrices.

### Provider Architecture

Status: partial.

The bundled providers are transparent and free by default. Remaining gaps are retry metadata, cache invalidation policy, real geocoding/routing adapters, and stronger provider outage simulation.

### Agent Orchestration

Status: partial.

The backend emits real persisted SSE events and named stages. It does not yet persist full agent input/output schemas, duration, retry count, timeout status, cancellation state, or an automatic revision cycle after critic failure.

### Revision

Status: partial.

The revision endpoint updates a stored trip and reports structured delta metadata. It still supports a narrow set of instructions.

### Frontend

Status: partial.

The Vite React workspace supports planning, streamed progress, results, budget, map, saved trips, providers, research, methodology, revision, and JSON export. Remaining gaps include React Hook Form/Zod form validation, stricter full-response parsing, print view, score chart, broader accessibility checks, and more E2E flows.

### Tests

Status: partial.

Backend coverage is healthy for the local demo, but frontend and E2E coverage remain thin. Provider outage, revision matrix, accessibility, and browser compatibility tests should be expanded before public deployment.

### Security

Status: partial.

Dependency audits are currently clean, high-confidence secret scanning is configured, and Dockerfiles run as non-root users. Hosted production still needs auth, request-size limits, stronger rate limiting, exact-origin CORS, secret management, image scanning, and backup policy.

### Research

Status: partial.

Research scripts run on a 12-case, 10-destination synthetic benchmark with five optimizer/baseline modes. Citation verification remains incomplete because no scholarly references have been inserted yet, and no user study has been run.

### Fresh Clone

Status: complete for local demo gates.

Fresh-clone verification passed for backend, frontend, research, and E2E commands. See `docs/FRESH_CLONE_VERIFICATION.md`.

### Docker

Status: complete for local image builds.

Dockerfiles and CI Docker build jobs are present. Backend and frontend images build locally after adding `.dockerignore`.

### Hosted Production

Status: partial.

The repository is ready for local or single-host demo deployment. Public hosted production still needs HTTPS termination, authentication, backup policy, hosted secret management, stricter rate limiting, and image vulnerability scanning.
