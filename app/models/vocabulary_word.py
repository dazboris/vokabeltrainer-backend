from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class VocabularyWord(Base):
    __tablename__ = "vocabulary_words"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_text: Mapped[str] = mapped_column(String, nullable=False)
    target_text: Mapped[str] = mapped_column(String, nullable=False)
    source_language: Mapped[str] = mapped_column(String(2), nullable=False)
    target_language: Mapped[str] = mapped_column(String(2), nullable=False)
    topic: Mapped[str] = mapped_column(String, nullable=False, default="General")
    is_learned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
