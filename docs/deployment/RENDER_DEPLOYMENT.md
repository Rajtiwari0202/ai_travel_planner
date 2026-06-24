# Render Deployment

`render.yaml` defines:

- `travelagenticai-api`: FastAPI web service on the free plan.
- `travelagenticai-web`: React static site on the free static hosting path.

Backend:

- build: `python -m pip install -r requirements.txt`
- pre-deploy: `python scripts/migrate.py`
- start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- health: `/api/v1/health/ready`

Frontend:

- build: `npm ci && npm run build`
- publish: `dist`
- SPA rewrite: `/* -> /index.html`

Set secrets in Render, not in Git.
