# Deployment Checklist

Use this checklist before publishing or updating a demo instance.

- [ ] Confirm branch and commit to deploy.
- [ ] Run `npm audit` in `frontend`.
- [ ] Run `python -m pip_audit -r requirements.txt` in `backend`.
- [ ] Run backend tests, Ruff, mypy, frontend lint/typecheck/test/build, E2E, and research smoke.
- [ ] Run `docker compose config`.
- [ ] Run `docker compose up -d --build`.
- [ ] Confirm `http://HOST:PORT/healthz` returns `ok`.
- [ ] Confirm `http://HOST:PORT/api/v1/health/ready` returns database ready locally.
- [ ] Create one test trip through the deployed app.
- [ ] Confirm the SQLite volume location and backup plan.
- [ ] For Render, confirm `https://travelagenticai-api.onrender.com/api/v1/health/ready`.
- [ ] For Render, confirm `https://travelagenticai-web.onrender.com`.
- [ ] Restrict CORS to the public frontend origin.
- [ ] Verify anonymous ownership isolation with two browser sessions or two session headers.
- [ ] Do not enter real payment, passport, or private booking credentials; this app is not a booking system.
