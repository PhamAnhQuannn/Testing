"""FastAPI app factory. `app` (module level) is what uvicorn runs: `uvicorn app.main:app`."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import Settings
from .errors import ApiError
from .idempotency import IdempotencyMiddleware
from .routers import content, learning, problems, resume, system
from .runtime import Runtime


def _err(status: int, code: str, message: str, **extra: object) -> JSONResponse:
    return JSONResponse(
        status_code=status, content={"error": {"code": code, "message": message, **extra}}
    )


def create_app(settings: Settings | None = None, runtime: Runtime | None = None) -> FastAPI:
    rt = runtime or Runtime(settings or Settings())

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        rt.start()  # raises StartupError: unsafe data dir, journal_mode != wal, ...
        rt.start_scheduler()
        try:
            yield
        finally:
            await rt.stop_scheduler()
            rt.stop()

    app = FastAPI(title="Prep App API", lifespan=lifespan)
    app.state.rt = rt

    @app.exception_handler(ApiError)
    async def _api_error(_: Request, exc: ApiError) -> JSONResponse:
        return _err(exc.status, exc.code, exc.message, **exc.extra)

    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        details = [
            {"loc": list(e["loc"]), "msg": e["msg"], "type": e["type"]} for e in exc.errors()
        ]
        return _err(422, "validation_error", "Invalid request", details=details)

    @app.exception_handler(StarletteHTTPException)
    async def _http(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        return _err(exc.status_code, f"http_{exc.status_code}", str(exc.detail))

    app.add_middleware(IdempotencyMiddleware)
    for r in (system.router, content.router, learning.router, problems.router, resume.router):
        app.include_router(r)

    web_dist = os.environ.get("WEB_DIST")
    if web_dist and Path(web_dist).is_dir():
        app.mount("/", StaticFiles(directory=web_dist, html=True), name="web")
    return app


app = create_app()
