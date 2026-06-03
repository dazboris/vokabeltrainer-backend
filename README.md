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
