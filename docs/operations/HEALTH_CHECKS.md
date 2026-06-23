# Health Checks

- `GET /api/v1/health/live`: process liveness.
- `GET /api/v1/health/ready`: database-backed readiness.
- `GET /api/v1/version`: service version and environment.

Render should use `/api/v1/health/ready`.
