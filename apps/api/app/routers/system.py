"""Health, backups, /me, settings."""

from __future__ import annotations

from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from ..db import pragma
from ..deps import DB, RT, Content, Now, User
from ..errors import ApiError
from ..models import tables as t
from ..runtime import head_revision

router = APIRouter(prefix="/api")


@router.get("/health")
def health(rt: RT):
    """Docker healthcheck: the DB opens and reports its journal mode."""
    if rt.degraded or rt.engine is None:
        latest = rt.backups.latest()
        return JSONResponse(
            status_code=503,
            content={
                "status": rt.degraded or "unavailable",
                "latest_backup": latest.name if latest else None,
            },
        )
    mode = pragma(rt.engine, "journal_mode")
    with rt.session() as db:
        db.execute(t.User.__table__.select().limit(1)).first()
    latest = rt.backups.latest()
    return {
        "status": "ok",
        "journal_mode": mode,
        "synchronous": pragma(rt.engine, "synchronous"),
        "schema_version": head_revision(),
        "last_backup_at": latest.created_at.isoformat() if latest else None,
    }


def _backup_json(b) -> dict:
    return {"name": b.name, "size": b.size, "created_at": b.created_at.isoformat()}


@router.get("/backups")
def list_backups(rt: RT):
    return {"backups": [_backup_json(b) for b in rt.backups.list()]}


@router.post("/backups", status_code=201)
def create_backup(rt: RT):
    if rt.engine is None:
        raise ApiError(503, "db_corrupt", "Cannot back up a damaged database")
    return _backup_json(rt.backups.create())


@router.get("/backups/{name}")
def download_backup(name: str, rt: RT):
    path = rt.backups.path_for(name)
    return FileResponse(path, media_type="application/octet-stream", filename=name)


@router.post("/backups/{name}/restore")
def restore_backup(name: str, rt: RT):
    info = rt.restore(name)
    return {"restored": _backup_json(info), "status": "ok"}


# ---- me / settings ----


def _settings_json(s: t.UserSettings) -> dict:
    return {
        "tz": s.tz,
        "review_preset": s.review_preset,
        "backlog_warn": s.backlog_warn,
        "target_role": s.target_role,
        "track": s.track,
        "language": s.language,
        "experience": s.experience,
        "display_name": s.display_name,
        "onboarded_at": s.onboarded_at.isoformat() if s.onboarded_at else None,
        "backup_every_hours": s.backup_every_hours,
        "backup_keep": s.backup_keep,
        "ui_prefs": s.ui_prefs or {},
        "placement_choice": s.placement_choice,
    }


def _onboarding_json(s: t.UserSettings) -> dict:
    """`placement` is none|skipped until the placement session exists (A10/A11)."""
    return {
        "profile_done": s.onboarded_at is not None,
        "placement": "skipped" if s.placement_choice == "skipped" else "none",
    }


@router.get("/me")
def me(db: DB, user: User, content: Content):
    s = db.get(t.UserSettings, user.id)
    assert s is not None
    return {
        "user": {"id": user.id, "name": user.name},
        "settings": _settings_json(s),
        "onboarding": _onboarding_json(s),
        "content": {"subtopics": len(content.subtopics), "serve_drafts": content.serve_drafts},
    }


class SettingsIn(BaseModel):
    tz: str | None = None
    review_preset: int | None = Field(default=None, ge=1, le=50)
    backlog_warn: int | None = Field(default=None, ge=1, le=1000)
    backup_every_hours: int | None = Field(default=None, ge=1, le=168)
    ui_prefs: dict | None = None


@router.put("/settings")
def put_settings(body: SettingsIn, db: DB, user: User):
    s = db.get(t.UserSettings, user.id)
    assert s is not None
    fields = body.model_fields_set
    if "tz" in fields and body.tz is not None:
        try:
            ZoneInfo(body.tz)
        except (ZoneInfoNotFoundError, ValueError) as e:
            raise ApiError(422, "invalid_tz", f"Unknown timezone {body.tz!r}") from e
        s.tz = body.tz
    if "review_preset" in fields:
        s.review_preset = body.review_preset  # null turns the "short session" button off
    if "backlog_warn" in fields and body.backlog_warn is not None:
        s.backlog_warn = body.backlog_warn
    if "backup_every_hours" in fields and body.backup_every_hours is not None:
        s.backup_every_hours = body.backup_every_hours
    if "ui_prefs" in fields and body.ui_prefs is not None:
        s.ui_prefs = body.ui_prefs
    db.commit()
    return _settings_json(s)


class ProfileIn(BaseModel):
    """S1 profile. Every field is optional so the screen can save step by step; `onboarded_at`
    is set once all four answers exist."""

    target_role: Literal["intern", "new_grad"] | None = None
    track: Literal["swe", "ai"] | None = None
    language: Literal["python"] | None = None
    experience: Literal["none", "some", "solid"] | None = None
    display_name: str | None = Field(default=None, max_length=60)
    tz: str | None = None
    placement: Literal["skipped"] | None = None  # "Bắt đầu từ đầu"; placement itself is A10/A11


@router.put("/profile")
def put_profile(body: ProfileIn, db: DB, user: User, now: Now):
    s = db.get(t.UserSettings, user.id)
    assert s is not None
    fields = body.model_fields_set
    if "tz" in fields and body.tz is not None:
        try:
            ZoneInfo(body.tz)
        except (ZoneInfoNotFoundError, ValueError) as e:
            raise ApiError(422, "invalid_tz", f"Unknown timezone {body.tz!r}") from e
        s.tz = body.tz
    for name in ("target_role", "track", "language", "experience"):
        if name in fields and getattr(body, name) is not None:
            setattr(s, name, getattr(body, name))
    if "display_name" in fields and body.display_name is not None:
        s.display_name = body.display_name.strip() or None
    if body.placement == "skipped":
        s.placement_choice = "skipped"
    if s.onboarded_at is None and all((s.target_role, s.track, s.language, s.experience)):
        s.onboarded_at = now
    db.commit()
    return {"settings": _settings_json(s), "onboarding": _onboarding_json(s)}
