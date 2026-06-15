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

## Topics API

The vocabulary overview screen uses topics with learned/total progress.

```bash
curl http://localhost:8000/topics
```

Response:

```json
[
  {
    "name": "Travel",
    "learned_count": 18,
    "total_count": 20
  }
]
```

Topic details:

```bash
curl http://localhost:8000/topics/Travel/words
```

## Practice API

Generate cards for the learning screen:

```bash
curl -X POST http://localhost:8000/practice/cards \
  -H "Content-Type: application/json" \
  -d '{"topic":"Travel","source_language":"en","target_language":"de","number_of_words":20}'
```

Response:

```json
{
  "topic": "Travel",
  "source_language": "en",
  "target_language": "de",
  "cards": [
    {
      "word_id": 1,
      "position": 1,
      "total": 20,
      "front_text": "airport",
      "back_text": "Flughafen"
    }
  ]
}
```

Save the session result:

```bash
curl -X POST http://localhost:8000/practice/results \
  -H "Content-Type: application/json" \
  -d '{"learned_word_ids":[1,2,3],"repeat_word_ids":[4,5]}'
```

Response:

```json
{
  "topic": "Travel",
  "learned": 3,
  "repeat": 2
}
```

## AI Word Generation

The backend can generate vocabulary words with the OpenAI API and save them to the database.

Configure an API key in your local environment:

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.5
```

Generate words for a user-provided topic:

```bash
curl -X POST http://localhost:8000/ai/generate-words \
  -H "Content-Type: application/json" \
  -d '{"topic":"Travel","source_language":"en","target_language":"de","number_of_words":20}'
```

Response:

```json
{
  "topic": "Travel",
  "source_language": "en",
  "target_language": "de",
  "words": [
    {
      "id": 1,
      "source_text": "airport",
      "target_text": "Flughafen",
      "source_language": "en",
      "target_language": "de",
      "topic": "Travel",
      "is_learned": false,
      "created_at": "2026-06-15T10:00:00"
    }
  ]
}
```

Do not commit a real `OPENAI_API_KEY` to GitHub.
