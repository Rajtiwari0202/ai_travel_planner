# Deployment Checklist

Use this checklist before publishing a demo instance.

- [ ] Confirm branch and commit to deploy.
- [ ] Run `npm audit` in `frontend`.
- [ ] Run `python -m pip_audit -r requirements.txt` in `backend`.
- [ ] Run backend tests, Ruff, mypy, frontend lint/typecheck/test/build, E2E, and research smoke.
- [ ] Run `docker compose config`.
- [ ] Run `docker compose up -d --build`.
- [ ] Confirm `http://HOST:PORT/healthz` returns `ok`.
- [ ] Confirm `http://HOST:PORT/api/v1/health` returns `{"status":"ok","service":"TravelAgenticAI"}`.
- [ ] Create one test trip through the deployed app.
- [ ] Confirm the SQLite volume location and backup plan.
- [ ] Configure HTTPS/TLS if reachable outside localhost.
- [ ] Restrict CORS to the public origin.
- [ ] Do not enter real payment, passport, or private booking credentials; this app is not a booking system.
