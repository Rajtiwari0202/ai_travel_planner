# Render Deployment

Verified public services:

- Frontend: `https://travelagenticai-web.onrender.com`
- Backend: `https://travelagenticai-api.onrender.com`
- Readiness: `https://travelagenticai-api.onrender.com/api/v1/health/ready`

`render.yaml` defines:

- `travelagenticai-api`: FastAPI web service on the free plan.
- `travelagenticai-web`: React static site on the free static hosting path.

Backend:

- build: `python -m pip install -r requirements.txt`
- pre-deploy: `python scripts/migrate.py`
- start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- health: `/api/v1/health/ready`
- runtime: Python `3.12.8` from `backend/.python-version`

Frontend:

- build: `npm ci && npm run build`
- publish: `dist`
- SPA rewrite: `/* -> /index.html`

Set secrets in Render, not in Git.

Public verification on 2026-06-24 confirmed backend readiness, frontend rendering, Neon persistence, anonymous session isolation, and revision flow.
