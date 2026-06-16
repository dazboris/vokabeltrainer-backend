from fastapi import APIRouter, Depends
from sqlalchemy import Integer, cast, func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.vocabulary_word import VocabularyWord
from app.schemas.topics import TopicRead
from app.schemas.vocabulary_word import VocabularyWordRead

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("", response_model=list[TopicRead])
def list_topics(db: Session = Depends(get_db)) -> list[TopicRead]:
    rows = db.execute(
        select(
            VocabularyWord.topic,
            func.count(VocabularyWord.id),
            func.sum(cast(VocabularyWord.is_learned, Integer)),
        )
        .group_by(VocabularyWord.topic)
        .order_by(VocabularyWord.topic)
    ).all()

    return [
        TopicRead(
            name=topic,
            total_count=total_count,
            learned_count=learned_count or 0,
        )
        for topic, total_count, learned_count in rows
    ]


@router.get("/{topic}/words", response_model=list[VocabularyWordRead])
def list_topic_words(topic: str, db: Session = Depends(get_db)) -> list[VocabularyWord]:
    return list(
        db.scalars(
            select(VocabularyWord)
            .where(VocabularyWord.topic == topic)
            .order_by(VocabularyWord.id)
        ).all()
    )
