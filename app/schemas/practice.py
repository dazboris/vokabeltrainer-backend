from pydantic import BaseModel, Field

from app.schemas.vocabulary_word import LanguageCode


class PracticeSessionCreate(BaseModel):
    topic: str
    source_language: LanguageCode
    target_language: LanguageCode
    number_of_words: int = Field(ge=1, le=100)


class PracticeCardRead(BaseModel):
    word_id: int
    position: int
    total: int
    front_text: str
    back_text: str


class PracticeSessionRead(BaseModel):
    topic: str
    source_language: LanguageCode
    target_language: LanguageCode
    cards: list[PracticeCardRead]


class PracticeResultCreate(BaseModel):
    learned_word_ids: list[int] = Field(default_factory=list)
    repeat_word_ids: list[int] = Field(default_factory=list)


class PracticeResultRead(BaseModel):
    topic: str
    learned: int
    repeat: int
