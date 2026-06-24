# Deployment Gap Analysis

Date: 2026-06-24
Branch: `main`

## Current State

The repository has a verified local/single-host Docker Compose deployment:

- frontend: Nginx serving Vite build on host port `18080`
- backend: FastAPI internal to Compose network
- persistence: SQLite volume
- health checks: frontend `/healthz`, backend `/api/v1/health/ready`

The repository also has a verified public research demo:

- frontend: `https://travelagenticai-web.onrender.com`
- backend: `https://travelagenticai-api.onrender.com`
- persistence: Neon PostgreSQL
- public verification: health, readiness, create/get/list/revise, anonymous ownership isolation, CORS negative check, desktop and mobile screenshots

## Public Demo Architecture

Preferred zero-cost public architecture:

```text
Browser
  -> Render Static Site
  -> Render Free FastAPI Web Service
  -> Neon Free PostgreSQL
```

## Completed Public Deployment Work

- PostgreSQL support and migrations were added while preserving SQLite locally.
- Anonymous ownership protects saved public demo trips.
- Production settings include CORS, docs, rate limits, request limits, and demo retention controls.
- Render Blueprint infrastructure was added.
- Neon and Render resources were created and verified.
- Public URLs were committed only after verification.
- Frontend handles free-service cold starts.
- Docs validation and Mermaid render inventory are included.

## Remaining Production Gaps

- Authenticated user accounts are not implemented.
- Long-term monitoring, alerting, backup, restore, and abuse operations are not complete.
- The app does not integrate verified live flight/hotel inventory.
- The app does not support payment, ticketing, or booking confirmation.

## Non-Goals

- No payments.
- No commercial booking.
- No verified live flight or hotel inventory.
- No paid hosting plan or payment method.
