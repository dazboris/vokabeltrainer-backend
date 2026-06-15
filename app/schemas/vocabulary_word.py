from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, model_validator

LanguageCode = Literal["de", "en"]


class VocabularyWordBase(BaseModel):
    source_text: str
    target_text: str
    source_language: LanguageCode
    target_language: LanguageCode

    @model_validator(mode="after")
    def validate_language_pair(self) -> "VocabularyWordBase":
        if self.source_language == self.target_language:
            raise ValueError("source_language and target_language must be different")
        return self


class VocabularyWordCreate(VocabularyWordBase):
    pass


class VocabularyWordUpdate(VocabularyWordBase):
    pass


class VocabularyWordRead(VocabularyWordBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
