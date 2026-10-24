"""The FastAPI static mount: CSP header, MIME types, SPA fallback (apps/web/dist stand-in)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.runtime import Runtime
from app.web import DEFAULT_CSP

REPO = Path(__file__).resolve().parents[3]


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "pyodide").mkdir()
    (dist / "index.html").write_text("<!doctype html><title>app</title>")
    (dist / "assets" / "app-1.js").write_text("export {}")
    (dist / "pyodide" / "pyodide.asm.wasm").write_bytes(b"\0asm\1\0\0\0")
    (dist / "pyodide" / "pyodide.mjs").write_text("export {}")
    monkeypatch.setenv("WEB_DIST", str(dist))
    settings = Settings(
        data_dir=tmp_path / "data", content_dir=REPO / "content", backups_enabled=False
    )
    with TestClient(create_app(settings, Runtime(settings))) as c:
        yield c


def test_csp_matches_vite_config() -> None:
    src = (REPO / "apps/web/vite.config.ts").read_text()
    block = re.search(r"export const CSP = \[(.*?)\]\.join", src, re.S)
    assert block
    assert "; ".join(re.findall(r'"([^"]+)"', block.group(1))) == DEFAULT_CSP


def test_static_headers_and_mime(client: TestClient) -> None:
    for path in ("/", "/assets/app-1.js", "/pyodide/pyodide.asm.wasm"):
        assert client.get(path).headers["content-security-policy"] == DEFAULT_CSP
    assert client.get("/pyodide/pyodide.asm.wasm").headers["content-type"] == "application/wasm"
    assert client.get("/pyodide/pyodide.mjs").headers["content-type"].startswith("text/javascript")
    assert "immutable" in client.get("/assets/app-1.js").headers["cache-control"]


@pytest.mark.parametrize("path", ["/s/py.datastructs.dict", "/p/ransom-note", "/map", "/nope/deep"])
def test_spa_fallback(client: TestClient, path: str) -> None:
    r = client.get(path)
    assert r.status_code == 200 and "<title>app</title>" in r.text
    assert r.headers["content-security-policy"] == DEFAULT_CSP


def test_api_not_shadowed(client: TestClient) -> None:
    assert client.get("/api/health").json()["status"] == "ok"
    r = client.get("/api/nope")
    assert r.status_code == 404 and r.json()["error"]["code"] == "http_404"
    assert client.get("/missing.js").status_code == 404
