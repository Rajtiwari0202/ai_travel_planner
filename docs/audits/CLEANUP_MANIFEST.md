# Cleanup Manifest

Date: 2026-06-23
Branch: `codex/public-deployment-v1.1`

## Removed Tracked Files

| File | Classification | Evidence | Reason |
| --- | --- | --- | --- |
| `backend/agent_stub.py` | obsolete prototype | Only referenced by file name search. | Replaced by canonical `backend/app/agents/orchestrator.py`. |
| `backend/notion_helper_stub.py` | obsolete prototype | Only referenced by file name search. | Not part of product or deployment path. |
| `frontend/public/index.html` | duplicate scaffold | Vite uses root `frontend/index.html`. | Prevents confusion with CRA layout. |
| `frontend/src/App.css` | obsolete scaffold | Not imported by active `frontend/src/main.tsx` path. | Old CRA styling. |
| `frontend/src/App.js` | obsolete scaffold | Not imported by active TypeScript app. | Old TaskPilot/CRA entry. |
| `frontend/src/App.jsx` | obsolete scaffold | Not imported by active TypeScript app. | Duplicate app implementation. |
| `frontend/src/index.js` | obsolete scaffold | Vite uses `frontend/src/main.tsx`. | Duplicate entry point. |
| `frontend/src/logo.svg` | obsolete scaffold | Not imported by active app. | Old CRA asset. |
| `frontend/src/reportWebVitals.js` | obsolete scaffold | Only referenced by removed `index.js`. | CRA-only performance helper. |
| `frontend/src/setupTests.js` | obsolete scaffold | Vitest uses `frontend/src/test/setup.ts`. | Duplicate test setup. |

## Moved Files

| Source | Destination | Reason |
| --- | --- | --- |
| `AGENTS.md` | `docs/codex/MASTER_PROMPT_V1.md` | Preserve historical mission prompt while keeping root instructions concise. |

## Safe Local Cleanup

The following commands are safe after verification because they do not remove volumes:

```powershell
docker image prune -f
docker builder prune -f
```

Do not run `docker system prune --volumes` unless intentionally deleting local persisted data.
