from pydantic import BaseModel, Field

from app.schemas.vocabulary_word import LanguageCode, VocabularyWordRead


class AIGenerateWordsRequest(BaseModel):
    topic: str
    source_language: LanguageCode
    target_language: LanguageCode
    number_of_words: int = Field(ge=1, le=50)


class AIGeneratedWord(BaseModel):
    source_text: str
    target_text: str


class AIGeneratedWords(BaseModel):
    words: list[AIGeneratedWord]


class AIGenerateWordsResponse(BaseModel):
    topic: str
    source_language: LanguageCode
    target_language: LanguageCode
    words: list[VocabularyWordRead]
