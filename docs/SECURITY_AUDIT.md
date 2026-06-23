# Security Audit

Last updated: 2026-06-23

## Dependency Audits

| Area | Command | Result |
| --- | --- | --- |
| Backend Python requirements | `..\venv\Scripts\python.exe -m pip_audit -r requirements.txt` from `backend` | No known vulnerabilities found. |
| Frontend npm dependencies | `npm audit` from `frontend` | 0 vulnerabilities. |

Security-driven upgrades made in this phase:

- `fastapi` upgraded to `0.138.0`.
- `starlette` pinned to `1.3.1`.
- `python-dotenv` upgraded to `1.2.2`.
- `pytest` upgraded to `9.1.1`.
- `pytest-asyncio` upgraded to `1.4.0`.
- Frontend test/build tooling upgraded, including `vitest`, `vite`, `postcss`, `tailwindcss`, `autoprefixer`, and `@playwright/test`.

## Secret Scan

The high-confidence scan checks for populated private-key, bearer-token, OpenAI-style key, GitHub-token, Slack-token, and env-secret patterns. Local scan returned no matches.

The same scan is configured in `.github/workflows/ci.yml`.

## Runtime Hardening

- Backend Docker image creates and runs as an unprivileged `app` user.
- Frontend Docker image runs as the bundled unprivileged `node` user.
- `.dockerignore` keeps local virtualenvs, dependency folders, test output, databases, logs, and env files out of Docker build contexts.
- `.env` files remain ignored; examples contain placeholders only.
- Optional live/weather/model providers are disabled or local by default.

## Remaining Security Work

- Add authentication and authorization before any hosted deployment.
- Add request body size limits and stronger rate limiting for public exposure.
- Lock down production CORS to exact deployment origins.
- Add hosted secrets management and database backup/retention policy.
- Run Docker image vulnerability scanning in a live CI environment after Docker builds are available.
