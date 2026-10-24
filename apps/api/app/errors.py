from __future__ import annotations


class ApiError(Exception):
    """Rendered as {"error": {"code", "message", ...extra}} (SPEC 6.4)."""

    def __init__(self, status: int, code: str, message: str, **extra: object) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.extra = extra


class StartupError(RuntimeError):
    """The app refuses to start (unsafe data dir, journal_mode != wal, ...)."""
