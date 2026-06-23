# Deployment Notes

The repository includes Dockerfiles and `docker-compose.yml` for local execution. Production deployment requires adding authentication, HTTPS termination, backups, and environment-specific CORS restrictions.

Do not assume any free hosting or API tier will remain available.

The backend and frontend Dockerfiles run as non-root users. Local image build verification passed after adding `.dockerignore`; GitHub Actions is configured to build both images.
