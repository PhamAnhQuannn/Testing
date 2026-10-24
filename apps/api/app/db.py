"""SQLite engine with the durability PRAGMAs of SPEC 6.7."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from sqlalchemy import Engine, create_engine, event

from .errors import StartupError


def apply_pragmas(dbapi_conn: sqlite3.Connection) -> str:
    cur = dbapi_conn.cursor()
    mode = cur.execute("PRAGMA journal_mode=WAL").fetchone()[0]
    cur.execute("PRAGMA synchronous=FULL")
    cur.execute("PRAGMA foreign_keys=ON")
    cur.execute("PRAGMA busy_timeout=5000")
    cur.close()
    return str(mode).lower()


def make_engine(db_path: Path) -> Engine:
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False, "isolation_level": None, "timeout": 5},
    )

    @event.listens_for(engine, "connect")
    def _on_connect(dbapi_conn, _record):  # noqa: ANN001
        mode = apply_pragmas(dbapi_conn)
        if mode != "wal":
            raise StartupError(
                f"SQLite journal_mode is {mode!r}, not 'wal'; refusing to run with weaker "
                "durability (is the data directory on a filesystem without shared memory support?)"
            )

    @event.listens_for(engine, "begin")
    def _on_begin(conn):  # noqa: ANN001
        # pysqlite's own transaction handling is disabled above (isolation_level=None), so emit
        # BEGIN ourselves: every request is one real transaction.
        conn.exec_driver_sql("BEGIN")

    return engine


def pragma(engine: Engine, name: str) -> str:
    with engine.connect() as c:
        return str(c.exec_driver_sql(f"PRAGMA {name}").scalar())
