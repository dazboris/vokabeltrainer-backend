from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserWordProgress(Base):
    __tablename__ = "user_word_progress"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("vocabulary_words.id"), primary_key=True)
    is_learned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)