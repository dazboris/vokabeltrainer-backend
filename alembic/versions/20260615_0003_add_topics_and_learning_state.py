"""Add topics and learning state to vocabulary words.

Revision ID: 20260615_0003
Revises: 20260615_0002
Create Date: 2026-06-15
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260615_0003"
down_revision: Union[str, Sequence[str], None] = "20260615_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "vocabulary_words",
        sa.Column("topic", sa.String(), nullable=False, server_default="General"),
    )
    op.add_column(
        "vocabulary_words",
        sa.Column("is_learned", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_column("vocabulary_words", "is_learned")
    op.drop_column("vocabulary_words", "topic")
