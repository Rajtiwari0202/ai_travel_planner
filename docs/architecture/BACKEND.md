# Backend Architecture

The backend is FastAPI with SQLAlchemy persistence.

Key areas:

- `app/main.py`: app factory, CORS, request guards, startup cleanup.
- `app/api/v1/routes.py`: versioned API routes.
- `app/agents/orchestrator.py`: planning and revision orchestration.
- `app/services`: providers, weather, geospatial, optimization, budgeting, narrative.
- `app/repositories/trips.py`: trip persistence and anonymous ownership checks.
- `app/db/session.py`: SQLite/PostgreSQL engine setup and health checks.

Production uses `DATABASE_URL` and `pool_pre_ping=True`.
