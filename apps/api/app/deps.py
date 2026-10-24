from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime
from typing import Annotated

from fastapi import Depends, Header, Request
from sqlalchemy.orm import Session

from .models import tables as t
from .runtime import Runtime
from .services import progress
from .services.content_loader import ContentStore


def get_rt(request: Request) -> Runtime:
    return request.app.state.rt


def get_db(request: Request) -> Iterator[Session]:
    """One session per request. Handlers that write call `db.commit()` themselves, before the
    response is built, so a 2xx always means the transaction is durable."""
    session = request.app.state.rt.session()
    try:
        yield session
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()


def current_user(db: Annotated[Session, Depends(get_db)]) -> t.User:
    """MVP: the fixed user. Multi-user (M7) changes only this function (SPEC 6.4)."""
    user = db.get(t.User, progress.USER_ID)
    assert user is not None
    return user


def get_content(rt: Annotated[Runtime, Depends(get_rt)]) -> ContentStore:
    assert rt.content is not None
    return rt.content


def get_now(rt: Annotated[Runtime, Depends(get_rt)]) -> datetime:
    return rt.clock()


def idem_key(
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> str | None:
    return idempotency_key


DB = Annotated[Session, Depends(get_db)]
User = Annotated[t.User, Depends(current_user)]
Content = Annotated[ContentStore, Depends(get_content)]
Now = Annotated[datetime, Depends(get_now)]
RT = Annotated[Runtime, Depends(get_rt)]
IdemKey = Annotated[str | None, Depends(idem_key)]
