"""Bounded retry for read-then-write endpoints that can hit SQLite's stale-snapshot BUSY.

With deferred `BEGIN` (see db.py), a request that reads (taking a snapshot) then writes can get
`OperationalError: database is locked` if another request commits in between — busy_timeout does not
retry that case. `write_tx` rolls back and re-runs the whole unit of work (service call + commit) on
a fresh transaction; after the rollback the retry reads a fresh snapshot and succeeds. Single-user
contention is rare, so retries are near-zero in practice.
"""

from __future__ import annotations

import time
from collections.abc import Callable

from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session


def write_tx[T](
    db: Session, fn: Callable[[], T], *, attempts: int = 4, base_delay: float = 0.02
) -> T:
    """Run `fn` (which does the writes and commits), retrying on a 'database is locked' error.

    `fn` must be re-runnable: on failure nothing has been committed, so `db.rollback()` drops the
    partial transaction before the next attempt.
    """
    for i in range(attempts):
        try:
            return fn()
        except OperationalError as e:
            if "database is locked" not in str(e) or i == attempts - 1:
                raise
            db.rollback()
            time.sleep(base_delay * (i + 1))
    raise AssertionError("unreachable")  # pragma: no cover
