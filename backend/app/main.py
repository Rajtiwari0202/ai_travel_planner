from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import router as api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.session import SessionLocal, init_db
from app.repositories.trips import cleanup_expired_demo_trips


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        init_db()
        with SessionLocal() as db:
            cleanup_expired_demo_trips(db, settings.anonymous_trip_ttl_days)
        yield

    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="Local-first agentic AI travel planner with deterministic optimization and transparent data labels.",
        docs_url="/docs" if settings.enable_api_docs else None,
        redoc_url="/redoc" if settings.enable_api_docs else None,
        openapi_url="/openapi.json" if settings.enable_api_docs else None,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_prefix)

    @app.get("/health")
    async def legacy_health() -> dict[str, str]:
        return {"status": "ok", "service": settings.app_name}

    return app


app = create_app()
