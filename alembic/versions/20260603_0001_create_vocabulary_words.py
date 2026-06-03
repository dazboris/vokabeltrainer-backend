"""Create vocabulary words table.

Revision ID: 20260603_0001
Revises:
Create Date: 2026-06-03
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260603_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "vocabulary_words",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("german_word", sa.String(), nullable=False),
        sa.Column("translation", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("vocabulary_words")
