# Implementation Plan

## Baseline Audit

- Existing repository path: `F:\travelAgenticAi`
- Original baseline branch: `main`
- Continuation branch: `codex/research-production-completion`
- Current remote: `https://github.com/Rajtiwari0202/ai_travel_planner.git`
- Intended repository from user: `https://github.com/Rajtiwari0202/ai_travel_planner`

## Existing Failures Found

- Backend import fails from `backend/main.py` because `core/orchestrator.py` mixes `core.*`, `services.*`, and `backend.services.*` imports.
- Frontend production build succeeds, but `src/main.jsx` resolves `App.js`, which renders the old TaskPilot setup screen instead of the travel planner UI in `App.jsx`.
- There is no complete canonical API, persistence, SSE workflow, or test suite.
- Backend dependencies in `backend/requirements.txt` are newer than the installed virtual environment.

## Phases

Continuation note: the original canonical backend/frontend phases are now implemented. The current branch is focused on closing the stricter completion gates from `docs/ACCEPTANCE_MATRIX.md`.

### Phase 1 - Canonical Backend

Acceptance criteria:
- `/api/v1/health` starts cleanly.
- Trip creation persists request, plan, events, and provider metadata in SQLite.
- Server-Sent Events expose real recorded agent events.
- Planner returns feasible itinerary or explicit infeasibility.
- Revision endpoint updates an existing structured itinerary.

### Phase 2 - Frontend Modernization

Acceptance criteria:
- React TypeScript + Vite frontend builds.
- Planner supports structured fields and a natural language note.
- UI consumes canonical API and SSE events.
- Results show itinerary, map, weather, budget, scores, alternatives, warnings, data labels, revision, and export.

### Phase 3 - Research Artifacts

Acceptance criteria:
- Benchmark script runs deterministically.
- Results CSV and generated figure are produced from actual local planner runs.
- Paper draft describes implemented methods and avoids fabricated citations or results.
- OR-Tools CP-SAT optimizer and deterministic baseline modes run against the same benchmark dataset.

### Phase 4 - Quality, Docs, CI

Acceptance criteria:
- Backend tests pass.
- Frontend tests pass.
- Production build passes.
- Documentation accurately states implemented and remaining items.
- Docker and GitHub Actions scaffolding are present.
- Dependency audits, secret scan, coverage, E2E, research smoke, and Docker builds are configured in CI.

### Phase 5 - Fresh Clone Verification

Acceptance criteria:
- Clone the branch into a clean folder.
- Install backend and frontend dependencies from committed files.
- Run backend, frontend, research, and E2E gates from documented commands.
- Record results in `docs/FRESH_CLONE_VERIFICATION.md`.

## Out of Scope for This Local Completion Pass

- Paid booking, payment, or live availability.
- Guaranteed live weather when `ENABLE_LIVE_WEATHER=false`.
- Force-pushing `main`.
- Claiming production readiness before all completion gates pass.
