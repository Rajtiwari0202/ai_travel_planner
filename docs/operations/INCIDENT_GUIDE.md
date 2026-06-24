# Incident Guide

1. Check frontend URL.
2. Check backend `/api/v1/health/live`.
3. Check backend `/api/v1/health/ready`.
4. Review Render logs for sanitized error categories.
5. Verify Neon is reachable.
6. Confirm CORS and frontend API URL settings.
7. Roll back to the previous Git release if a deployment regression is confirmed.
