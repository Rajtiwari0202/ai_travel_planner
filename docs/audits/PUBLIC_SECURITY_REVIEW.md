# Public Security Review

Date: 2026-06-24
Branch: `codex/public-deployment-v1.1`

## Scope

This review covers the public research demo hardening added for v1.1.0. It is not a penetration test.

## Implemented Controls

- Anonymous browser ownership token is generated client-side.
- Only a SHA-256 hash of the anonymous token is stored.
- Trip listing is scoped to the anonymous session.
- Reading, revising, deleting, and SSE access require ownership.
- Trip IDs are UUIDs.
- Production API docs can be disabled with `ENABLE_API_DOCS=false`.
- Request body size limit uses `MAX_REQUEST_BYTES`.
- Lightweight IP-based rate limit uses `RATE_LIMIT_ENABLED`, `RATE_LIMIT_REQUESTS`, and `RATE_LIMIT_WINDOW_SECONDS`.
- Readiness checks verify database connectivity.
- CORS origins are environment-driven and explicit.
- Public demo data retention uses `ANONYMOUS_TRIP_TTL_DAYS`.
- Staged secret scan found no high-confidence private keys or provider tokens.

## Verified Commands

- `python -m pip_audit -r requirements.txt`: no known vulnerabilities found.
- `npm audit`: found 0 vulnerabilities.
- `python -m ruff check .`: all checks passed.
- `python -m mypy app`: success.
- Backend tests include anonymous ownership isolation.

## Remaining Risks

- Rate limiting is in-memory and per-instance; a production SaaS would use edge or shared-store rate limits.
- No full user accounts; this is anonymous demo access, not authentication.
- No WAF or managed abuse protection is configured.
- Backups and long-term monitoring still depend on the public provider setup.
- Security headers are baseline only.

## Data Honesty

The app still does not claim live booking inventory, payments, or verified hotel/flight availability. Transport and accommodation prices remain estimates unless labeled otherwise.
