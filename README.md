# vokabeltrainer-backend

Backend API for a vocabulary trainer.

## Requirements

- Python 3.12
- Docker

## Run With Docker Compose

```bash
docker compose up --build
```

The API runs on http://localhost:8000.

## Run With Docker

```bash
docker build -t vokabeltrainer-backend .
docker run --rm -p 8000:8000 --env-file .env.example vokabeltrainer-backend
```

## Health Check

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## API Docs

FastAPI exposes interactive API documentation at:

- http://localhost:8000/docs
- http://localhost:8000/redoc

## Vocabulary Words API

Vocabulary words support German to English and English to German pairs. Use ISO language codes:

- `de` for German
- `en` for English

### Create Word

```bash
curl -X POST http://localhost:8000/words \
  -H "Content-Type: application/json" \
  -d '{"source_text":"Haus","target_text":"house","source_language":"de","target_language":"en"}'
```

Response:

```json
{
  "id": 1,
  "source_text": "Haus",
  "target_text": "house",
  "source_language": "de",
  "target_language": "en",
  "created_at": "2026-06-15T10:00:00"
}
```

### List Words

```bash
curl http://localhost:8000/words
```

### Get Word

```bash
curl http://localhost:8000/words/1
```

### Update Word

```bash
curl -X PUT http://localhost:8000/words/1 \
  -H "Content-Type: application/json" \
  -d '{"source_text":"house","target_text":"Haus","source_language":"en","target_language":"de"}'
```

### Delete Word

```bash
curl -X DELETE http://localhost:8000/words/1
```
