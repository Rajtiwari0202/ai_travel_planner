from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from time import monotonic
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api.v1.routes import router as api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.session import SessionLocal, init_db
from app.repositories.trips import cleanup_expired_demo_trips

_rate_limits: dict[str, list[float]] = {}


def _client_key(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


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
        version="1.1.0",
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

    @app.middleware("http")
    async def public_demo_guards(request: Request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid4())
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > settings.max_request_bytes:
            return JSONResponse(
                status_code=413,
                content={"detail": "Request body too large", "request_id": request_id},
                headers={"x-request-id": request_id},
            )
        if settings.rate_limit_enabled:
            now = monotonic()
            key = _client_key(request)
            window_start = now - settings.rate_limit_window_seconds
            bucket = [seen for seen in _rate_limits.get(key, []) if seen >= window_start]
            if len(bucket) >= settings.rate_limit_requests:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded", "request_id": request_id},
                    headers={"x-request-id": request_id},
                )
            bucket.append(now)
            _rate_limits[key] = bucket
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        response.headers["x-content-type-options"] = "nosniff"
        response.headers["referrer-policy"] = "strict-origin-when-cross-origin"
        return response

    app.include_router(api_router, prefix=settings.api_prefix)

    @app.get("/health")
    async def legacy_health() -> dict[str, str]:
        return {"status": "ok", "service": settings.app_name}

    return app


app = create_app()
