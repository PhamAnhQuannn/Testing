"""check_sessions (mastery check / test out sessions, SPEC 6.3)

`check_results` already has attempt_no, session_id, context and gave_up from 0001.

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-25 09:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "check_sessions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("subtopic_id", sa.String(), nullable=False),
        sa.Column("context", sa.String(), nullable=False),
        sa.Column("placement_session_id", sa.Integer(), nullable=True),
        sa.Column("order_no", sa.Integer(), nullable=False),
        sa.Column("attempt_no", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("ladder", sa.JSON(), nullable=False),
        sa.Column("current_item_id", sa.String(), nullable=True),
        sa.Column("elapsed_ms", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("last_active_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["subtopic_id"], ["subtopics.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("check_sessions", schema=None) as batch_op:
        batch_op.create_index(
            "ix_check_sessions_user_sub_status",
            ["user_id", "subtopic_id", "status"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("check_sessions", schema=None) as batch_op:
        batch_op.drop_index("ix_check_sessions_user_sub_status")

    op.drop_table("check_sessions")
