import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.words import router as words_router

app = FastAPI(title="Vokabeltrainer Backend")

frontend_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(words_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
