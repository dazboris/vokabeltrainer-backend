from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.vocabulary_word import VocabularyWord
from app.schemas.vocabulary_word import (
    VocabularyWordCreate,
    VocabularyWordRead,
    VocabularyWordUpdate,
)

router = APIRouter(prefix="/words", tags=["words"])


@router.post("", response_model=VocabularyWordRead, status_code=201)
def create_word(word: VocabularyWordCreate, db: Session = Depends(get_db)) -> VocabularyWord:
    vocabulary_word = VocabularyWord(
        source_text=word.source_text,
        target_text=word.target_text,
        source_language=word.source_language,
        target_language=word.target_language,
    )
    db.add(vocabulary_word)
    db.commit()
    db.refresh(vocabulary_word)
    return vocabulary_word


@router.get("", response_model=list[VocabularyWordRead])
def list_words(db: Session = Depends(get_db)) -> list[VocabularyWord]:
    return list(db.scalars(select(VocabularyWord).order_by(VocabularyWord.id)).all())


@router.get("/{word_id}", response_model=VocabularyWordRead)
def get_word(word_id: int, db: Session = Depends(get_db)) -> VocabularyWord:
    return get_vocabulary_word_or_404(word_id, db)


@router.put("/{word_id}", response_model=VocabularyWordRead)
def update_word(
    word_id: int,
    word: VocabularyWordUpdate,
    db: Session = Depends(get_db),
) -> VocabularyWord:
    vocabulary_word = get_vocabulary_word_or_404(word_id, db)
    vocabulary_word.source_text = word.source_text
    vocabulary_word.target_text = word.target_text
    vocabulary_word.source_language = word.source_language
    vocabulary_word.target_language = word.target_language
    db.commit()
    db.refresh(vocabulary_word)
    return vocabulary_word


@router.delete("/{word_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_word(word_id: int, db: Session = Depends(get_db)) -> Response:
    vocabulary_word = get_vocabulary_word_or_404(word_id, db)
    db.delete(vocabulary_word)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_vocabulary_word_or_404(word_id: int, db: Session) -> VocabularyWord:
    vocabulary_word = db.get(VocabularyWord, word_id)
    if vocabulary_word is None:
        raise HTTPException(status_code=404, detail="Vocabulary word not found")
    return vocabulary_word
