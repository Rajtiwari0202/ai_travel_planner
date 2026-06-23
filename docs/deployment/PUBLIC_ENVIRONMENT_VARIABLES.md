# Public Environment Variables

Backend:

- `APP_ENV=production`
- `DATABASE_URL=<redacted Neon pooled URL>`
- `CORS_ORIGINS=<public frontend URL>`
- `ENABLE_API_DOCS=false`
- `DEMO_MODE=true`
- `ANONYMOUS_TRIP_TTL_DAYS=7`
- `RATE_LIMIT_ENABLED=true`
- `RATE_LIMIT_REQUESTS=90`
- `RATE_LIMIT_WINDOW_SECONDS=60`
- `MAX_REQUEST_BYTES=1048576`

Frontend:

- `VITE_API_BASE_URL=<public backend URL>/api/v1`
- `VITE_APP_ENV=production`
- `VITE_DEMO_MODE=true`
- `VITE_ENABLE_RESEARCH_PAGE=true`
