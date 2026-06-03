from fastapi import FastAPI

from app.api.words import router as words_router

app = FastAPI(title="Vokabeltrainer Backend")
app.include_router(words_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
