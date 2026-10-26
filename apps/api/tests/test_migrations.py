from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, inspect

from app.models import Base
from app.runtime import alembic_config, head_revision


def test_migrations_match_models(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'm.db'}")
    command.upgrade(alembic_config(engine), "head")
    with engine.connect() as conn:
        diff = compare_metadata(MigrationContext.configure(conn), Base.metadata)
    assert diff == [], f"models and migrations differ, add a migration: {diff}"


def test_m1_tables_exist(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'm.db'}")
    command.upgrade(alembic_config(engine), "head")
    tables = set(inspect(engine).get_table_names())
    assert {
        "users", "settings", "subtopics", "lessons", "problems", "user_subtopic", "quiz_answers",
        "lesson_runs", "attempts", "drafts", "events", "resume_state", "idempotency_keys",
        "check_results", "review_cards", "review_log", "alembic_version", "check_sessions",
    } <= tables  # fmt: skip
    cols = {c["name"] for c in inspect(engine).get_columns("events")}
    assert {"idem_key", "occurred_at", "received_at"} <= cols
    cols = {c["name"] for c in inspect(engine).get_columns("drafts")}
    assert {"elapsed_ms", "started_at"} <= cols
    cols = {c["name"] for c in inspect(engine).get_columns("user_subtopic")}
    assert {"unlocked_at", "known_basic"} <= cols
    assert head_revision() == "0002"
