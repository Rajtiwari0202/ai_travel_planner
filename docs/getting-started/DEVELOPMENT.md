# Development

Use Python 3.12 and Node 22.

Backend checks:

```powershell
cd F:\travelAgenticAi\backend
..\venv\Scripts\python.exe -m pytest
..\venv\Scripts\python.exe -m ruff check .
..\venv\Scripts\python.exe -m mypy app
```

Frontend checks:

```powershell
cd F:\travelAgenticAi\frontend
npm run lint
npm run typecheck
npm test
npm run build
```

The active frontend entry is `frontend/src/main.tsx`. The active backend entry is `backend/main.py`.
