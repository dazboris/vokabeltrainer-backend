import os

from fastapi import HTTPException, status
from openai import OpenAI, OpenAIError

from app.schemas.ai import AIGenerateWordsRequest, AIGeneratedWords


def generate_vocabulary_words(request: AIGenerateWordsRequest) -> AIGeneratedWords:
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OPENAI_API_KEY is not configured",
        )

    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-5.5")

    try:
        response = client.responses.parse(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You generate vocabulary for a German-English learning app. "
                        "Return only useful beginner to intermediate vocabulary. "
                        "Do not include duplicates, proper names, offensive words, "
                        "or words outside the requested topic. Keep entries concise."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Generate {request.number_of_words} vocabulary words for topic "
                        f"'{request.topic}'. Source language: {request.source_language}. "
                        f"Target language: {request.target_language}."
                    ),
                },
            ],
            text_format=AIGeneratedWords,
        )
    except OpenAIError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="OpenAI word generation failed",
        ) from exc

    generated_words = response.output_parsed
    if generated_words is None:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="OpenAI returned an empty generation result",
        )

    return generated_words
