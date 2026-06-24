# Configuration

Backend configuration is read from environment variables in `backend/app/core/config.py`.

Important variables:

- `APP_ENV`
- `DATABASE_URL`
- `CORS_ORIGINS`
- `ENABLE_API_DOCS`
- `ANONYMOUS_TRIP_TTL_DAYS`
- `RATE_LIMIT_ENABLED`
- `RATE_LIMIT_REQUESTS`
- `RATE_LIMIT_WINDOW_SECONDS`
- `MAX_REQUEST_BYTES`
- `PROVIDER_TIMEOUT_SECONDS`

Frontend configuration:

- `VITE_API_BASE_URL`
- `VITE_APP_ENV`
- `VITE_DEMO_MODE`
- `VITE_ENABLE_RESEARCH_PAGE`

Do not commit secrets. Public deployments should store database URLs only in provider secret storage.
