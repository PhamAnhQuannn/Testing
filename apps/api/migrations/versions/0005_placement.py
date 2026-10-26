"""placement_sessions (placement assessment sittings, SPEC 5.6 / UI_SPEC 2)

`user_subtopic.known_basic/placement_hint/placement_session_id` and `check_sessions.
placement_session_id` already exist from 0001/0002.

Revision ID: 0005
Revises: 0004
Create Date: 2026-10-25 18:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "placement_sessions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(), nullable=False),
        sa.Column("scope", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("experience", sa.String(), nullable=False),
        sa.Column("state", sa.JSON(), nullable=False),
        sa.Column("active_ms", sa.Integer(), nullable=False),
        sa.Column("stop_reason", sa.String(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("last_active_at", sa.DateTime(), nullable=False),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("placement_sessions", schema=None) as batch_op:
        batch_op.create_index(
            "ix_placement_sessions_user_status", ["user_id", "status"], unique=False
        )


def downgrade() -> None:
    with op.batch_alter_table("placement_sessions", schema=None) as batch_op:
        batch_op.drop_index("ix_placement_sessions_user_status")
    op.drop_table("placement_sessions")
