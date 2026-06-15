from fastapi import APIRouter, Depends
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.vocabulary_word import VocabularyWord
from app.schemas.practice import (
    PracticeCardRead,
    PracticeResultCreate,
    PracticeResultRead,
    PracticeSessionCreate,
    PracticeSessionRead,
)

router = APIRouter(prefix="/practice", tags=["practice"])


@router.post("/cards", response_model=PracticeSessionRead)
def create_practice_cards(
    session: PracticeSessionCreate,
    db: Session = Depends(get_db),
) -> PracticeSessionRead:
    words = list(
        db.scalars(
            select(VocabularyWord)
            .where(
                VocabularyWord.topic == session.topic,
                or_(
                    (
                        (VocabularyWord.source_language == session.source_language)
                        & (VocabularyWord.target_language == session.target_language)
                    ),
                    (
                        (VocabularyWord.source_language == session.target_language)
                        & (VocabularyWord.target_language == session.source_language)
                    ),
                ),
            )
            .order_by(VocabularyWord.is_learned, VocabularyWord.id)
            .limit(session.number_of_words)
        ).all()
    )

    total = len(words)
    cards = [
        PracticeCardRead(
            word_id=word.id,
            position=index,
            total=total,
            front_text=word.source_text
            if word.source_language == session.source_language
            else word.target_text,
            back_text=word.target_text
            if word.target_language == session.target_language
            else word.source_text,
        )
        for index, word in enumerate(words, start=1)
    ]

    return PracticeSessionRead(
        topic=session.topic,
        source_language=session.source_language,
        target_language=session.target_language,
        cards=cards,
    )


@router.post("/results", response_model=PracticeResultRead)
def save_practice_results(
    result: PracticeResultCreate,
    db: Session = Depends(get_db),
) -> PracticeResultRead:
    learned_ids = set(result.learned_word_ids)
    repeat_ids = set(result.repeat_word_ids)
    word_ids = learned_ids | repeat_ids

    words = []
    if word_ids:
        words = list(db.scalars(select(VocabularyWord).where(VocabularyWord.id.in_(word_ids))).all())

    topic = words[0].topic if words else ""
    for word in words:
        if word.id in learned_ids:
            word.is_learned = True
        if word.id in repeat_ids:
            word.is_learned = False

    db.commit()

    return PracticeResultRead(
        topic=topic,
        learned=len(learned_ids),
        repeat=len(repeat_ids),
    )
