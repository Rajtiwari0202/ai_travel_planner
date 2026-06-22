# Project Status

Last updated: 2026-06-21

## Summary

TravelAgenticAI has been upgraded from a mock prototype into a local-first, full-stack, explainable agentic travel-planning demo. It now works without paid APIs or an LLM, persists trips locally, streams real backend agent events, and includes reproducible research artifacts.

This is not claimed as fully production-ready because authentication, real booking inventory, a CP-SAT optimizer, and a verified user study are not implemented.

## Repository Target

- Working folder: `F:\travelAgenticAi`
- User-designated GitHub repo: `https://github.com/Rajtiwari0202/ai_travel_planner`
- Current remote: `https://github.com/Rajtiwari0202/ai_travel_planner.git`
- Continuation branch: `codex/research-production-completion`

## Implemented

- `AGENTS.md` contains the provided master prompt.
- Canonical FastAPI app under `backend/app`.
- Versioned API under `/api/v1`.
- SQLite persistence for trips and agent events.
- Server-Sent Events for real backend planning progress.
- Deterministic local providers for destination, activity, transport, accommodation, weather fallback, geospatial scoring, budget reconciliation, itinerary writing, validation, and revision.
- Vite React TypeScript frontend with planner, event timeline, itinerary results, budget chart, Leaflet map, revision assistant, saved trips page, methodology page, and JSON export.
- Research benchmark dataset, benchmark runner, ablation runner, generated CSVs, generated PNG figure, and conservative paper draft.
- Dockerfiles, `docker-compose.yml`, `.env.example`, CI workflow, and project docs.

## Verification Results

Passed:

- Backend: `python -m pytest` -> 7 passed
- Backend: `python -m ruff check app tests` -> all checks passed
- Backend: `python -m mypy app` -> success, 28 source files
- Frontend: `npm run typecheck` -> passed
- Frontend: `npm test` -> 1 test passed
- Frontend: `npm run build` -> passed
- E2E: `npm run e2e` -> 1 Chromium test passed
- Research: `run_benchmarks.py` and `run_ablations.py` -> CSV/PNG outputs generated

Failed or incomplete in the continuation audit baseline:

- Backend: `python -m ruff check .` against the whole backend failed because obsolete untracked prototype modules are present in the local workspace.
- Frontend: `npm run lint` failed because no lint script is defined.

Resolved in continuation branch:

- Removed obsolete untracked local scaffold folders from the workspace.
- Added frontend ESLint config and `npm run lint`.
- Re-ran `python -m ruff check .` in `backend`: passed.
- Re-ran `npm run lint` in `frontend`: passed.
- Added OR-Tools CP-SAT itinerary optimization with deterministic heuristic fallback.
- Added a canonical Decimal-based budget service and reconciliation tests.
- Expanded backend planner tests from 7 to 11 tests.
- Expanded research dataset to 12 synthetic cases across 10 Indian destinations and regenerated 60 benchmark rows.
- Re-ran `npm run e2e` after restarting the local backend: passed.

Warnings and notes:

- Frontend build warns that the main bundle is larger than 500 kB because map/chart libraries are bundled together.
- npm reports dependency vulnerabilities after install; a careful dependency audit is still needed before any public deployment.
- Current audit files: `docs/GAP_AUDIT.md`, `docs/ACCEPTANCE_MATRIX.md`, and `docs/VERIFICATION_REPORT.md`.

## Research Outputs

- `research/results/benchmark_results.csv`
- `research/results/ablation_summary.csv`
- `research/figures/benchmark_scores.png`
- `research/paper/paper.tex`

## Remaining Limitations

- No live booking, payment, or real-time flight/hotel availability.
- Current optimizer uses OR-Tools CP-SAT when installed and falls back to deterministic heuristics otherwise. It still does not model every production constraint such as verified opening hours, OSRM route matrices, or arrival/departure windows.
- Live weather is optional and disabled by default.
- No production auth, user accounts, or cloud deployment hardening.
- Paper related work remains intentionally uncited until scholarly sources are verified; `research/paper/CITATION_VERIFICATION.md` records this limitation.
