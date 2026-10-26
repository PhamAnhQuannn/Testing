"""Tables of SPEC 6.3 needed up to M1 (plus the few that scoring/review read)."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    TypeDecorator,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class UTCDateTime(TypeDecorator):
    """Timezone-aware UTC datetimes; SQLite keeps them naive, so normalise on the way in/out."""

    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value: datetime | None, dialect: Any) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError("naive datetime; use timezone-aware UTC")
        return value.astimezone(UTC).replace(tzinfo=None)

    def process_result_value(self, value: datetime | None, dialect: Any) -> datetime | None:
        return None if value is None else value.replace(tzinfo=UTC)


class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON, list[Any]: JSON, datetime: UTCDateTime}


def uid() -> Mapped[int]:
    return mapped_column(ForeignKey("users.id"), primary_key=True)


# ---- content (loaded from files at startup; lessons/problems are served from the files) ----


class Subtopic(Base):
    __tablename__ = "subtopics"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name_vi: Mapped[str] = mapped_column(String)
    section: Mapped[str] = mapped_column(String)
    module: Mapped[str] = mapped_column(String)
    ord: Mapped[int] = mapped_column(Integer)
    prereqs: Mapped[list[Any]] = mapped_column(JSON)
    target_intern: Mapped[int] = mapped_column(Integer)
    target_ai: Mapped[int] = mapped_column(Integer)
    targets: Mapped[dict[str, Any]] = mapped_column(JSON)
    est_hours: Mapped[float] = mapped_column(Float)
    summary_vi: Mapped[str] = mapped_column(Text)
    mastery_bar_vi: Mapped[str] = mapped_column(Text)
    content_status: Mapped[str] = mapped_column(String, default="none")


class Lesson(Base):
    __tablename__ = "lessons"
    subtopic_id: Mapped[str] = mapped_column(ForeignKey("subtopics.id"), primary_key=True)
    version: Mapped[int] = mapped_column(Integer)
    path: Mapped[str] = mapped_column(String)
    content_hash: Mapped[str] = mapped_column(String)
    est_minutes: Mapped[int] = mapped_column(Integer)


class Problem(Base):
    __tablename__ = "problems"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    subtopic_id: Mapped[str] = mapped_column(ForeignKey("subtopics.id"))
    kind: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    difficulty: Mapped[str] = mapped_column(String)
    source_type: Mapped[str] = mapped_column(String)
    lc: Mapped[int | None] = mapped_column(Integer)
    time_target_min: Mapped[int] = mapped_column(Integer)
    path: Mapped[str] = mapped_column(String)
    content_hash: Mapped[str] = mapped_column(String)
    version: Mapped[int] = mapped_column(Integer)  # bumped by the loader when content_hash changes


class QuizItem(Base):
    __tablename__ = "quiz_items"
    id: Mapped[str] = mapped_column(String, primary_key=True)  # "<lesson>#<block>"
    subtopic_id: Mapped[str] = mapped_column(ForeignKey("subtopics.id"))
    source: Mapped[str] = mapped_column(String)  # lesson | assessment
    level: Mapped[int | None] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String)
    graded: Mapped[bool] = mapped_column(Boolean)


# ---- user and progress ----


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime)


class UserSettings(Base):
    __tablename__ = "settings"
    user_id: Mapped[int] = uid()
    tz: Mapped[str] = mapped_column(String, default="Asia/Ho_Chi_Minh")
    review_preset: Mapped[int | None] = mapped_column(Integer, default=6)
    backlog_warn: Mapped[int] = mapped_column(Integer, default=20)
    target_role: Mapped[str | None] = mapped_column(String)
    track: Mapped[str | None] = mapped_column(String)
    language: Mapped[str | None] = mapped_column(String)
    experience: Mapped[str | None] = mapped_column(String)
    display_name: Mapped[str | None] = mapped_column(String)
    onboarded_at: Mapped[datetime | None] = mapped_column(UTCDateTime)
    placement_choice: Mapped[str | None] = mapped_column(String)  # "skipped" (S1 "Bắt đầu từ đầu")
    backup_every_hours: Mapped[int] = mapped_column(Integer, default=6)
    backup_keep: Mapped[int] = mapped_column(Integer, default=20)
    ui_prefs: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class UserSubtopic(Base):
    __tablename__ = "user_subtopic"
    user_id: Mapped[int] = uid()
    subtopic_id: Mapped[str] = mapped_column(ForeignKey("subtopics.id"), primary_key=True)
    score: Mapped[int] = mapped_column(Integer, default=0)  # cache of scoring(events)
    lesson_done_at: Mapped[datetime | None] = mapped_column(UTCDateTime)
    quiz_best: Mapped[float | None] = mapped_column(Float)
    tested_out: Mapped[bool] = mapped_column(Boolean, default=False)
    unlocked_at: Mapped[datetime | None] = mapped_column(UTCDateTime)  # one-way
    status: Mapped[str] = mapped_column(String, default="locked")
    updated_at: Mapped[datetime | None] = mapped_column(UTCDateTime)
    known_basic: Mapped[bool] = mapped_column(Boolean, default=False)
    placement_hint: Mapped[str | None] = mapped_column(String)
    placement_session_id: Mapped[int | None] = mapped_column(Integer)


class LessonRun(Base):
    """One pass through a lesson (SPEC 5.1 `run_no`). Run 1 is created lazily."""

    __tablename__ = "lesson_runs"
    user_id: Mapped[int] = uid()
    subtopic_id: Mapped[str] = mapped_column(ForeignKey("subtopics.id"), primary_key=True)
    run_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    started_at: Mapped[datetime] = mapped_column(UTCDateTime)


class QuizAnswer(Base):
    __tablename__ = "quiz_answers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    quiz_item_id: Mapped[str] = mapped_column(String)
    run_no: Mapped[int] = mapped_column(Integer)
    attempt_no: Mapped[int] = mapped_column(Integer)
    answer: Mapped[Any] = mapped_column(JSON)
    correct: Mapped[bool] = mapped_column(Boolean)
    answered_at: Mapped[datetime] = mapped_column(UTCDateTime)
    __table_args__ = (Index("ix_quiz_answers_user_item_run", "user_id", "quiz_item_id", "run_no"),)


class ProblemState(Base):
    """Per-problem facts the server owns: hints opened, solution viewed (deviation: not in 6.3)."""

    __tablename__ = "problem_state"
    user_id: Mapped[int] = uid()
    problem_id: Mapped[str] = mapped_column(String, primary_key=True)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)
    solution_viewed: Mapped[bool] = mapped_column(Boolean, default=False)
    first_opened_at: Mapped[datetime | None] = mapped_column(UTCDateTime)


class Attempt(Base):
    __tablename__ = "attempts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    problem_id: Mapped[str] = mapped_column(String)
    mode: Mapped[str] = mapped_column(String)  # run | submit
    language: Mapped[str] = mapped_column(String)
    code: Mapped[str] = mapped_column(Text)
    verdict: Mapped[str] = mapped_column(String)
    passed: Mapped[int] = mapped_column(Integer)
    total: Mapped[int] = mapped_column(Integer)
    elapsed_ms: Mapped[int] = mapped_column(Integer, default=0)
    runtime_ms: Mapped[int | None] = mapped_column(Integer)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)
    solution_viewed: Mapped[bool] = mapped_column(Boolean, default=False)
    clean: Mapped[bool] = mapped_column(Boolean, default=False)
    started_at: Mapped[datetime | None] = mapped_column(UTCDateTime)
    submitted_at: Mapped[datetime] = mapped_column(UTCDateTime)
    problem_version: Mapped[int] = mapped_column(Integer, default=1)
    __table_args__ = (
        Index("ix_attempts_user_problem_submitted", "user_id", "problem_id", "submitted_at"),
    )


class CheckResult(Base):
    __tablename__ = "check_results"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subtopic_id: Mapped[str] = mapped_column(ForeignKey("subtopics.id"))
    item_id: Mapped[str] = mapped_column(String)
    level: Mapped[int] = mapped_column(Integer)
    attempt_no: Mapped[int] = mapped_column(Integer, default=1)
    passed: Mapped[bool] = mapped_column(Boolean)
    clean: Mapped[bool] = mapped_column(Boolean, default=False)
    minutes_used: Mapped[float | None] = mapped_column(Float)
    taken_at: Mapped[datetime] = mapped_column(UTCDateTime)
    session_id: Mapped[int | None] = mapped_column(Integer)
    context: Mapped[str] = mapped_column(String, default="mastery")
    gave_up: Mapped[bool] = mapped_column(Boolean, default=False)
    item_type: Mapped[str] = mapped_column(String, default="write_code")  # deviation: for level3_ok
    __table_args__ = (
        Index("ix_check_results_user_sub_level", "user_id", "subtopic_id", "level", "taken_at"),
    )


class CheckSession(Base):
    """One attempt at a mastery check / test out (SPEC 6.3 `check_sessions`, flows C and D).

    `ladder` holds the steps (item, level, result); results are also appended to `check_results`,
    which is what scoring reads. `expired` = no activity for 24 h; it is not a failure.
    """

    __tablename__ = "check_sessions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subtopic_id: Mapped[str] = mapped_column(ForeignKey("subtopics.id"))
    context: Mapped[str] = mapped_column(String, default="mastery")  # mastery | test_out
    placement_session_id: Mapped[int | None] = mapped_column(Integer)
    order_no: Mapped[int] = mapped_column(Integer, default=0)
    attempt_no: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String, default="in_progress")  # in_progress|done|expired
    ladder: Mapped[dict[str, Any]] = mapped_column(JSON)
    current_item_id: Mapped[str | None] = mapped_column(String)
    elapsed_ms: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime] = mapped_column(UTCDateTime)
    last_active_at: Mapped[datetime] = mapped_column(UTCDateTime)
    __table_args__ = (
        Index("ix_check_sessions_user_sub_status", "user_id", "subtopic_id", "status"),
    )


class PlacementSession(Base):
    """One sitting of the placement assessment (SPEC 5.6, UI_SPEC 2). Evidence is only ever
    `check_results` (context=placement); `state` holds the gate ladder and the current pointer.

    status: in_progress | finished | skipped ("start from scratch": writes nothing) | abandoned.
    """

    __tablename__ = "placement_sessions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    kind: Mapped[str] = mapped_column(String, default="initial")
    scope: Mapped[str] = mapped_column(String, default="all")
    status: Mapped[str] = mapped_column(String, default="in_progress")
    experience: Mapped[str] = mapped_column(String, default="none")
    state: Mapped[dict[str, Any]] = mapped_column(JSON)
    active_ms: Mapped[int] = mapped_column(Integer, default=0)
    stop_reason: Mapped[str | None] = mapped_column(String)
    started_at: Mapped[datetime] = mapped_column(UTCDateTime)
    last_active_at: Mapped[datetime] = mapped_column(UTCDateTime)
    finished_at: Mapped[datetime | None] = mapped_column(UTCDateTime)
    __table_args__ = (Index("ix_placement_sessions_user_status", "user_id", "status"),)


class ReviewCard(Base):
    __tablename__ = "review_cards"
    user_id: Mapped[int] = uid()
    subtopic_id: Mapped[str] = mapped_column(ForeignKey("subtopics.id"), primary_key=True)
    box: Mapped[int] = mapped_column(Integer, default=1)
    due_on: Mapped[date] = mapped_column(Date)
    last_reviewed_at: Mapped[datetime | None] = mapped_column(UTCDateTime)
    lapses: Mapped[int] = mapped_column(Integer, default=0)
    consecutive_passes: Mapped[int] = mapped_column(Integer, default=0)
    suspended: Mapped[bool] = mapped_column(Boolean, default=False)
    current_item_ref: Mapped[str | None] = mapped_column(String)
    current_item_opened_at: Mapped[datetime | None] = mapped_column(UTCDateTime)
    __table_args__ = (Index("ix_review_cards_user_due", "user_id", "due_on"),)


class ReviewLog(Base):
    __tablename__ = "review_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subtopic_id: Mapped[str] = mapped_column(ForeignKey("subtopics.id"))
    item_ref: Mapped[str] = mapped_column(String)
    item_kind: Mapped[str] = mapped_column(String)  # code | recall
    box_before: Mapped[int] = mapped_column(Integer)
    box_after: Mapped[int] = mapped_column(Integer)
    success: Mapped[bool] = mapped_column(Boolean)
    reviewed_at: Mapped[datetime] = mapped_column(UTCDateTime)


class Draft(Base):
    __tablename__ = "drafts"
    user_id: Mapped[int] = uid()
    problem_id: Mapped[str] = mapped_column(String, primary_key=True)
    language: Mapped[str] = mapped_column(String, primary_key=True)
    code: Mapped[str] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(UTCDateTime)
    cursor: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    elapsed_ms: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime | None] = mapped_column(UTCDateTime)
    rev: Mapped[int] = mapped_column(
        Integer, default=1
    )  # M3 (409); server-issued, bumped on change


class Event(Base):
    """Append-only log (SPEC 6.3)."""

    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[str] = mapped_column(String)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    ts: Mapped[datetime] = mapped_column(UTCDateTime)
    occurred_at: Mapped[datetime] = mapped_column(UTCDateTime)
    received_at: Mapped[datetime] = mapped_column(UTCDateTime)
    idem_key: Mapped[str | None] = mapped_column(String)
    __table_args__ = (
        Index("ix_events_user_type", "user_id", "type"),
        UniqueConstraint("user_id", "idem_key", "type", name="uq_events_idem"),
    )


class ResumeState(Base):
    __tablename__ = "resume_state"
    user_id: Mapped[int] = uid()
    mode: Mapped[str] = mapped_column(String)
    route: Mapped[str] = mapped_column(String)
    ref: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    context: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    updated_at: Mapped[datetime] = mapped_column(UTCDateTime)
    device_id: Mapped[str | None] = mapped_column(String)


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"
    key: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    method: Mapped[str] = mapped_column(String)
    path: Mapped[str] = mapped_column(String)
    status: Mapped[int] = mapped_column(Integer)  # 0 while the first request is still running
    response: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime)


class StudyTime(Base):
    """Real interaction time per local day (SPEC 6.3); view-only, no goals."""

    __tablename__ = "study_time"
    user_id: Mapped[int] = uid()
    day: Mapped[date] = mapped_column(Date, primary_key=True)
    seconds: Mapped[int] = mapped_column(Integer, default=0)


class ActivityState(Base):
    """`last_ping` per user, so several tabs never double count (SPEC 6.4 `/activity/ping`)."""

    __tablename__ = "activity_state"
    user_id: Mapped[int] = uid()
    last_ping_at: Mapped[datetime] = mapped_column(UTCDateTime)
