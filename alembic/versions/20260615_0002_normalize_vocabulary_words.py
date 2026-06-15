"""Normalize vocabulary words for German-English pairs.

Revision ID: 20260615_0002
Revises: 20260603_0001
Create Date: 2026-06-15
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260615_0002"
down_revision: Union[str, Sequence[str], None] = "20260603_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("vocabulary_words", "german_word", new_column_name="source_text")
    op.alter_column("vocabulary_words", "translation", new_column_name="target_text")
    op.add_column(
        "vocabulary_words",
        sa.Column("source_language", sa.String(length=2), nullable=False, server_default="de"),
    )
    op.add_column(
        "vocabulary_words",
        sa.Column("target_language", sa.String(length=2), nullable=False, server_default="en"),
    )


def downgrade() -> None:
    op.drop_column("vocabulary_words", "target_language")
    op.drop_column("vocabulary_words", "source_language")
    op.alter_column("vocabulary_words", "target_text", new_column_name="translation")
    op.alter_column("vocabulary_words", "source_text", new_column_name="german_word")
