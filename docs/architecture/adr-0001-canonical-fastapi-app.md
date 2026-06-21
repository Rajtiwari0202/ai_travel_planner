# ADR 0001: Canonical FastAPI Application Under `backend/app`

## Status

Accepted

## Context

The repository had an older backend with direct modules under `backend/` and a newer partial schema layer under `backend/app`. The older backend had broken imports and a narrower mock response model.

## Decision

Use `backend/app` as the canonical backend package. Keep older prototype files available during migration, but point `backend/main.py` at `app.main`.

## Consequences

- API paths become versioned under `/api/v1`.
- New code can use package-relative imports consistently.
- Tests and research scripts can import the same planning services used by the API.
