import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from alembic import command
from alembic.config import Config

from app.api.auth import router as auth_router
from app.api.practice import router as practice_router
from app.api.topics import router as topics_router
from app.api.words import router as words_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Uygulama başlarken veritabanı güncellemelerini (migrations) otomatik uygular
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    yield

app = FastAPI(title="Vokabeltrainer Backend", lifespan=lifespan)

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

app.include_router(auth_router)
app.include_router(words_router)
app.include_router(topics_router)
app.include_router(practice_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
