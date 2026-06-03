from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.vocabulary_word import VocabularyWord
from app.schemas.vocabulary_word import VocabularyWordCreate, VocabularyWordRead

router = APIRouter(prefix="/words", tags=["words"])


@router.post("", response_model=VocabularyWordRead, status_code=201)
def create_word(word: VocabularyWordCreate, db: Session = Depends(get_db)) -> VocabularyWord:
    vocabulary_word = VocabularyWord(
        german_word=word.german_word,
        translation=word.translation,
    )
    db.add(vocabulary_word)
    db.commit()
    db.refresh(vocabulary_word)
    return vocabulary_word


@router.get("", response_model=list[VocabularyWordRead])
def list_words(db: Session = Depends(get_db)) -> list[VocabularyWord]:
    return list(db.scalars(select(VocabularyWord).order_by(VocabularyWord.id)).all())
