# Contributing

1. Keep the app local-first by default.
2. Do not commit secrets, credentials, database files, virtual environments, build outputs, or `node_modules`.
3. Run backend and frontend tests before submitting changes.
4. Preserve data labels for estimated, fallback, synthetic, live, cached, and open-data results.
5. Do not add booking or payment behavior to this decision-support demo.

Useful commands:

```powershell
cd backend
..\venv\Scripts\python.exe -m pytest
..\venv\Scripts\python.exe -m ruff check app tests
..\venv\Scripts\python.exe -m mypy app

cd ..\frontend
npm run typecheck
npm test
npm run build
```
