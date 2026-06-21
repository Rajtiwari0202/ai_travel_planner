# Acceptance Matrix

Last updated: 2026-06-21

| Requirement | Status | Implementation File | Relevant Test | Verification Command | Evidence / Gap |
| --- | --- | --- | --- | --- | --- |
| Correct Git remote | complete | `.git/config` | n/a | `git remote -v` | Remote is `https://github.com/Rajtiwari0202/ai_travel_planner.git`. |
| Work on continuation branch | complete | git branch | n/a | `git branch --show-current` | Branch created: `codex/research-production-completion`. |
| Versioned API | complete | `backend/app/api/v1/routes.py` | `backend/tests/test_api.py` | `pytest` | `/api/v1` endpoints exist and smoke tests pass. |
| Trip persistence | complete | `backend/app/repositories/trips.py` | `backend/tests/test_api.py` | `pytest` | Trip request, plan, and events persist in SQLite. |
| Real SSE events | partial | `backend/app/services/events.py` | `backend/tests/test_api.py` | `pytest`, `npm run e2e` | Events are persisted and streamed; event ordering edge cases and terminal-state tests are thin. |
| Free default operation | complete | `backend/app/services/providers/catalog.py`, `backend/app/services/weather/service.py` | `backend/tests/test_planner.py` | `pytest` | No paid API or LLM needed. Live weather disabled by default. |
| Data-status labels | partial | `backend/app/schemas/trip.py`, `frontend/src/features/itinerary/ItineraryResults.tsx` | `backend/tests/test_planner.py` | `pytest`, `npm run build` | Labels exist; provider metadata needs provider-name, source URL/id, warnings, and error metadata. |
| Backend-only coordinates | complete | `backend/app/services/providers/catalog.py`, `frontend/src/features/map/ItineraryMap.tsx` | `backend/tests/test_planner.py` | `pytest`, `npm run e2e` | Scheduled activities include backend coordinates; browser does not geocode. |
| Weather date alignment | partial | `backend/app/services/weather/service.py` | `backend/tests/test_planner.py` | `pytest` | Dates are aligned; forecast horizon and unavailable-date tests need expansion. |
| Canonical money model | partial | `backend/app/services/optimization/planner.py` | `backend/tests/test_schemas.py` | `pytest` | Cost pieces reconcile by construction but use floats and are embedded in optimizer. |
| Room-count hotel costing | complete | `backend/app/services/optimization/planner.py` | `backend/tests/test_schemas.py` | `pytest` | Uses `assumed_rooms * nights`, not traveler count. |
| CP-SAT optimizer | missing | n/a | n/a | n/a | No OR-Tools CP-SAT implementation yet. |
| Heuristic fallback optimizer | partial | `backend/app/services/optimization/planner.py` | `backend/tests/test_planner.py` | `pytest` | Greedy fallback works but lacks formal rejected reasons and baseline API. |
| Required baselines | partial | `research/experiments/run_benchmarks.py` | research script | `run_benchmarks.py` | Baselines are preference variants, not independent algorithms. |
| Agent typed state and timing | partial | `backend/app/agents/orchestrator.py` | `backend/tests/test_api.py` | `pytest` | Named stages emit events; duration/retry/input-output schemas are incomplete. |
| Revision endpoint | partial | `backend/app/agents/orchestrator.py` | `backend/tests/test_api.py` | `pytest` | Revision persists but supports limited instructions and limited delta metadata. |
| Frontend planner | partial | `frontend/src/features/planner/PlannerForm.tsx` | `frontend/src/app/App.test.tsx` | `npm test`, `npm run typecheck` | Form works; strict React Hook Form/Zod validation and accessibility errors missing. |
| Frontend map | partial | `frontend/src/features/map/ItineraryMap.tsx` | E2E smoke | `npm run e2e` | Markers render; missing empty/error handling, day-specific routes, and accessible text summary. |
| Saved trips | complete | `frontend/src/features/trips/SavedTripsPage.tsx` | E2E smoke | `npm run e2e` | Basic saved-trip page exists. |
| Provider status page | partial | `frontend/src/features/planner/ProviderStatusPanel.tsx` | App smoke | `npm test` | Panel exists in planner, but no dedicated provider-status route. |
| Research page | missing | n/a | n/a | n/a | No dedicated research route yet. |
| Frontend lint | complete | `frontend/package.json`, `frontend/eslint.config.js` | n/a | `npm run lint` | ESLint 9 flat-config lint passes for TypeScript frontend sources. |
| Backend Ruff gate | complete | `backend/pyproject.toml` | n/a | `ruff check .` | Whole-backend Ruff passes after removing obsolete local scaffold from the workspace. |
| E2E coverage | partial | `frontend/e2e/planner.spec.ts` | Playwright | `npm run e2e` | One happy-path scenario only. |
| Research dataset breadth | partial | `research/datasets/benchmark_cases.json` | research scripts | `run_benchmarks.py` | Only four cases and four destinations. |
| Paper citations | missing | `research/paper/paper.tex` | n/a | n/a | Related work and citation verification are placeholders. |
| Fresh-clone verification | missing | n/a | n/a | n/a | Not run yet for this branch. |
| CI completeness | partial | `.github/workflows/ci.yml` | GitHub Actions | n/a locally | Lacks lint, E2E, research, coverage, audit, and paper checks. |
