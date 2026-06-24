# Quickstart

## Docker

```powershell
cd F:\travelAgenticAi
docker compose up -d --build
```

Open `http://127.0.0.1:18080` for the local single-host demo.

## Development

Backend:

```powershell
cd F:\travelAgenticAi\backend
..\venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Frontend:

```powershell
cd F:\travelAgenticAi\frontend
npm ci
npm run dev
```

For local development set `VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1`.
