# Deployment Gap Analysis

Date: 2026-06-23
Branch: `codex/public-deployment-v1.1`

## Current State

The repository has a verified local/single-host Docker Compose deployment:

- frontend: Nginx serving Vite build on host port `18080`
- backend: FastAPI internal to Compose network
- persistence: SQLite volume
- health checks: frontend `/healthz`, backend `/api/v1/health`

## Public Demo Target

Preferred zero-cost public architecture:

```text
Browser
  -> Render Static Site
  -> Render Free FastAPI Web Service
  -> Neon Free PostgreSQL
```

## Gaps Before Public Deployment

- PostgreSQL support and migrations must be added while preserving SQLite locally.
- Anonymous ownership must protect saved public demo trips.
- Production settings need typed configuration for CORS, docs, rate limits, request limits, and demo retention.
- Render Blueprint infrastructure needs to be added.
- Neon and Render resources require authenticated provider sessions.
- Public URLs must only be committed after real verification.
- Frontend needs graceful handling for free-service cold starts.
- CI should include Markdown link validation and Mermaid validation/render checks.

## Non-Goals

- No payments.
- No commercial booking.
- No verified live flight or hotel inventory.
- No paid hosting plan or payment method.
