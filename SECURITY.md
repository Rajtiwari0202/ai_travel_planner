# Security

Last reviewed: 2026-06-22

## Supported Model

This local demo is not a hosted service. Security reports should focus on repository code, local API behavior, dependency risks, and accidental data exposure.

## Secrets

- Do not commit `.env` files.
- `.env.example` contains placeholders only.
- Optional paid or local model providers must be disabled by default.
- Logs should not include secret values.

## Local Data

Trip requests and generated plans are stored in SQLite by default. Treat that database as local user data and do not commit it.

## Network Calls

Live weather is disabled by default. When enabled, provider calls use timeouts and transparent source labels.

## Current Audit Status

- Backend `pip-audit` reports no known vulnerabilities for `backend/requirements.txt`.
- Frontend `npm audit` reports 0 vulnerabilities.
- CI includes a high-confidence secret scan.
- Backend and frontend Dockerfiles run as non-root users.

See `docs/SECURITY_AUDIT.md` for the latest audit notes and remaining production security work.
