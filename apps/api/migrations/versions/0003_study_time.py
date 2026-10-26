"""study_time + activity_state (POST /activity/ping, SPEC 6.4)

Revision ID: 0003
Revises: 0002
Create Date: 2026-10-25 12:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "study_time",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("day", sa.Date(), nullable=False),
        sa.Column("seconds", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("user_id", "day"),
    )
    op.create_table(
        "activity_state",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("last_ping_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("user_id"),
    )


def downgrade() -> None:
    op.drop_table("activity_state")
    op.drop_table("study_time")
