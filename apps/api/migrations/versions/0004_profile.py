"""settings.placement_choice (S1 "Bắt đầu từ đầu" flag, PUT /profile)

Revision ID: 0004
Revises: 0003
Create Date: 2026-10-25 14:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("settings") as batch:
        batch.add_column(sa.Column("placement_choice", sa.String(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("settings") as batch:
        batch.drop_column("placement_choice")
