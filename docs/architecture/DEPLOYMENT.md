# Deployment Architecture

Local deployment uses Docker Compose:

- Nginx frontend container on port `18080`
- FastAPI backend container on the internal Compose network
- SQLite volume for persistence

Public target:

- Render Static Site for React build
- Render Free Web Service for FastAPI
- Neon Free PostgreSQL for durable persistence

The fallback is a single Render Docker service if split static/backend deployment is blocked by provider constraints.
