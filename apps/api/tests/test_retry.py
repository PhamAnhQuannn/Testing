import pytest
from sqlalchemy.exc import OperationalError

from app.retry import write_tx


class FakeDB:
    def __init__(self):
        self.rollbacks = 0

    def rollback(self):
        self.rollbacks += 1


def _locked():
    return OperationalError("BEGIN", {}, Exception("database is locked"))


def test_retries_then_succeeds():
    db = FakeDB()
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        if calls["n"] < 3:
            raise _locked()
        return "ok"

    assert write_tx(db, fn, base_delay=0) == "ok"
    assert calls["n"] == 3
    assert db.rollbacks == 2  # rolled back before each retry, not after the success


def test_gives_up_after_attempts():
    db = FakeDB()

    def fn():
        raise _locked()

    with pytest.raises(OperationalError):
        write_tx(db, fn, attempts=4, base_delay=0)
    assert db.rollbacks == 3  # attempts-1 rollbacks; the last failure re-raises


def test_other_operational_error_is_not_retried():
    db = FakeDB()
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        raise OperationalError("SELECT", {}, Exception("no such table: x"))

    with pytest.raises(OperationalError):
        write_tx(db, fn, base_delay=0)
    assert calls["n"] == 1
    assert db.rollbacks == 0
