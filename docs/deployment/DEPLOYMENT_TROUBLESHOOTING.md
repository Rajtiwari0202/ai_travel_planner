# Deployment Troubleshooting

- Backend readiness fails: verify `DATABASE_URL`, Neon status, and migration logs.
- CORS errors: ensure `CORS_ORIGINS` exactly matches the public frontend origin.
- Frontend cannot submit: verify `VITE_API_BASE_URL` points to the backend `/api/v1`.
- SSE does not stream: verify the service allows long-lived HTTP responses and the trip session token matches.
- Free service sleeps: the frontend wake-up banner should retry readiness before submitting.
