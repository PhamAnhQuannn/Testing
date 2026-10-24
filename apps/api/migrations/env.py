from __future__ import annotations

from alembic import context
from sqlalchemy import create_engine

from app.config import Settings
from app.models import Base

config = context.config
target_metadata = Base.metadata


def _engine():
    engine = config.attributes.get("engine")
    if engine is not None:
        return engine
    url = context.get_x_argument(as_dictionary=True).get("url")
    return create_engine(url or f"sqlite:///{Settings().db_path}")


def run_migrations_online() -> None:
    engine = _engine()
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
