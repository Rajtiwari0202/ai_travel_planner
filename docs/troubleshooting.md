# Troubleshooting

## Backend import fails

Run commands from `F:\travelAgenticAi\backend` and use:

```powershell
..\venv\Scripts\python.exe -m uvicorn main:app --reload
```

## Frontend cannot reach backend

Confirm the backend is running on `http://localhost:8000` and that `VITE_API_BASE_URL` points to `http://localhost:8000/api/v1`.

## Map tiles do not load

The map uses public OpenStreetMap tiles. Check network access and retry. Itinerary coordinates still come from the backend.

## Weather is not live

Live weather is disabled by default. Set `ENABLE_LIVE_WEATHER=true` to use Open-Meteo; fallback labels remain visible when unavailable.
