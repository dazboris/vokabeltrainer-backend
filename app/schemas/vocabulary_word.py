from pydantic import BaseModel, ConfigDict


class VocabularyWordCreate(BaseModel):
    german_word: str
    translation: str


class VocabularyWordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    german_word: str
    translation: str
