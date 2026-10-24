"""Idempotency-Key middleware for state-changing requests (SPEC 6.4 / UI_SPEC 4.4).

The first request with a key claims it by inserting a row (unique primary key), runs, and stores its
response; a repeat returns that response without running the handler. Two concurrent requests with
the same key: the second sees the claim and gets 409 `idempotency_in_progress`.
A claim older than `idempotency_pending_stale_s` (crashed worker) is taken over.
"""

from __future__ import annotations

import json
from datetime import timedelta
from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from .models import tables as t
from .services.progress import USER_ID

WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
MAX_KEY_LEN = 200


async def _json_response(send: Send, status: int, body: Any, extra: list | None = None) -> None:
    raw = json.dumps(body).encode()
    headers = [(b"content-type", b"application/json"), (b"content-length", str(len(raw)).encode())]
    await send(
        {"type": "http.response.start", "status": status, "headers": headers + (extra or [])}
    )
    await send({"type": "http.response.body", "body": raw})


class IdempotencyMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or scope["method"] not in WRITE_METHODS:
            return await self.app(scope, receive, send)
        key = None
        for k, v in scope["headers"]:
            if k == b"idempotency-key":
                key = v.decode("latin-1").strip()
        rt = scope["app"].state.rt
        if not key or rt.engine is None or not scope["path"].startswith("/api"):
            return await self.app(scope, receive, send)
        if len(key) > MAX_KEY_LEN:
            return await _json_response(
                send, 400, {"error": {"code": "invalid_idempotency_key", "message": "Key too long"}}
            )

        method, path = scope["method"], scope["path"]
        now = rt.clock()
        stale = timedelta(seconds=rt.settings.idempotency_pending_stale_s)
        with rt.engine.begin() as conn:
            try:
                with conn.begin_nested():
                    conn.execute(
                        t.IdempotencyKey.__table__.insert().values(
                            key=key,
                            user_id=USER_ID,
                            method=method,
                            path=path,
                            status=0,
                            response=None,
                            created_at=now,
                        )
                    )
                claimed = True
                existing = None
            except IntegrityError:
                claimed = False
                existing = conn.execute(
                    select(t.IdempotencyKey).where(t.IdempotencyKey.key == key)
                ).one()
                if existing.status == 0 and now - existing.created_at > stale:
                    conn.execute(
                        update(t.IdempotencyKey)
                        .where(t.IdempotencyKey.key == key)
                        .values(created_at=now, method=method, path=path)
                    )
                    claimed = True
        if not claimed:
            assert existing is not None
            if existing.method != method or existing.path != path:
                return await _json_response(
                    send,
                    422,
                    {
                        "error": {
                            "code": "idempotency_key_reuse",
                            "message": "This Idempotency-Key was used for a different request",
                        }
                    },
                )
            if existing.status == 0:
                return await _json_response(
                    send,
                    409,
                    {
                        "error": {
                            "code": "idempotency_in_progress",
                            "message": "A request with this key is still running",
                        }
                    },
                    [(b"retry-after", b"1")],
                )
            stored = existing.response
            return await _json_response(
                send, existing.status, stored, [(b"idempotent-replay", b"true")]
            )

        # Hold the response until its copy is stored, so a client that retries right after
        # receiving it can never see the key in the "running" state.
        status = 500
        held: list[Message] = []
        ctype = b""
        chunks: list[bytes] = []

        async def capture(message: Message) -> None:
            nonlocal status, ctype
            if message["type"] == "http.response.start":
                status = message["status"]
                for k, v in message.get("headers", []):
                    if k.lower() == b"content-type":
                        ctype = v
            elif message["type"] == "http.response.body":
                chunks.append(message.get("body", b""))
            held.append(message)

        try:
            await self.app(scope, receive, capture)
        except BaseException:
            self._release(rt, key)
            raise
        if status >= 500:
            self._release(rt, key)
            for m in held:
                await send(m)
            return
        body = b"".join(chunks)
        try:
            payload: Any = json.loads(body) if body and b"json" in ctype else None
        except ValueError:
            payload = None
        with rt.engine.begin() as conn:
            conn.execute(
                update(t.IdempotencyKey)
                .where(t.IdempotencyKey.key == key)
                .values(status=status, response=payload)
            )
        for m in held:
            await send(m)

    @staticmethod
    def _release(rt: Any, key: str) -> None:
        if rt.engine is None:
            return
        with rt.engine.begin() as conn:
            conn.execute(delete(t.IdempotencyKey).where(t.IdempotencyKey.key == key))
