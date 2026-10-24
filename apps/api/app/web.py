"""Serving the built web app (apps/web/dist) from FastAPI.

* CSP: worker scripts only honour the Content-Security-Policy *header*, so every static response
  carries it. The string is the one `apps/web/vite.config.ts` exports; the build also writes it to
  `dist/csp.txt` (read here), `DEFAULT_CSP` is the fallback and a test keeps both in sync.
* MIME: `.wasm` must be `application/wasm`, `.mjs`/`.js` a JavaScript type (module workers).
* SPA fallback: a path with no file extension that is not under /api gets index.html, so client
  routes (/s/:id, /p/:id, /map) survive a reload. /api/* keeps its JSON 404.
"""

from __future__ import annotations

import mimetypes
from pathlib import Path

from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.types import Scope

DEFAULT_CSP = "; ".join(
    [
        "default-src 'self'",
        "script-src 'self' 'wasm-unsafe-eval'",
        "worker-src 'self'",
        "connect-src 'self'",
        "font-src 'self'",
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' data:",
    ]
)

for _ext, _type in {
    ".wasm": "application/wasm",
    ".mjs": "text/javascript",
    ".js": "text/javascript",
    ".json": "application/json",
    ".woff2": "font/woff2",
}.items():
    mimetypes.add_type(_type, _ext)


ASSET_EXTS = {
    ".js", ".mjs", ".css", ".wasm", ".map", ".json", ".zip", ".txt", ".png", ".svg", ".ico",
    ".woff", ".woff2", ".jpg", ".webp", ".webmanifest",
}  # fmt: skip


class SpaStaticFiles(StaticFiles):
    def __init__(self, directory: str | Path, **kwargs) -> None:
        super().__init__(directory=directory, html=True, **kwargs)
        csp_file = Path(directory) / "csp.txt"
        self.csp = csp_file.read_text().strip() if csp_file.is_file() else DEFAULT_CSP

    async def get_response(self, path: str, scope: Scope) -> Response:
        try:
            response = await super().get_response(path, scope)
        except HTTPException as exc:
            if exc.status_code != 404 or not self._is_client_route(path):
                raise
            response = await super().get_response("index.html", scope)
        response.headers["Content-Security-Policy"] = self.csp
        response.headers["X-Content-Type-Options"] = "nosniff"
        if path.startswith("assets/"):  # hashed file names
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        elif Path(path).suffix.lower() not in ASSET_EXTS:
            response.headers["Cache-Control"] = "no-cache"
        return response

    @staticmethod
    def _is_client_route(path: str) -> bool:
        first = path.split("/", 1)[0]
        # ids contain dots (/s/py.datastructs.dict), so judge by known asset extensions only
        return first != "api" and Path(path).suffix.lower() not in ASSET_EXTS
