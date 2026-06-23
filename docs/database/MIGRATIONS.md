# Migrations

Alembic is configured under `backend/alembic`.

Run migrations:

```powershell
cd F:\travelAgenticAi\backend
..\venv\Scripts\python.exe scripts\migrate.py
```

Render runs the same script before deployment through `render.yaml`.

Local SQLite compatibility is preserved. Production should use a Neon PostgreSQL `DATABASE_URL`.
