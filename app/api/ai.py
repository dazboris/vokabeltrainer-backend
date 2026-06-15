from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.vocabulary_word import VocabularyWord
from app.schemas.ai import AIGenerateWordsRequest, AIGenerateWordsResponse
from app.services.openai_vocabulary import generate_vocabulary_words

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/generate-words", response_model=AIGenerateWordsResponse)
def generate_words(
    request: AIGenerateWordsRequest,
    db: Session = Depends(get_db),
) -> AIGenerateWordsResponse:
    generated = generate_vocabulary_words(request)

    vocabulary_words = [
        VocabularyWord(
            source_text=word.source_text,
            target_text=word.target_text,
            source_language=request.source_language,
            target_language=request.target_language,
            topic=request.topic,
        )
        for word in generated.words
    ]

    db.add_all(vocabulary_words)
    db.commit()
    for vocabulary_word in vocabulary_words:
        db.refresh(vocabulary_word)

    return AIGenerateWordsResponse(
        topic=request.topic,
        source_language=request.source_language,
        target_language=request.target_language,
        words=vocabulary_words,
    )
