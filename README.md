# lemon.markets Orders API

Simple order placement service built with FastAPI. Orders get saved to Postgres and processed in the background via Celery workers.

## Prerequisites

- Docker
- Docker Compose

## Getting started

Clone the repo and run:

```bash
docker compose up --build
```

API runs on `http://localhost:8000`. First run will take a bit longer while it pulls the images and builds.

## Try it out

Market order:

```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"instrument": "DE000A0Q4RZ3", "type": "market", "quantity": 10, "side": "buy"}'
```

Limit order:

```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"instrument": "DE000A0Q4RZ3", "type": "limit", "quantity": 10, "side": "buy", "limit_price": 42.50}'
```

## Tests

```bash
pip install -r requirements.txt
pytest
```

Tests use an in-memory SQLite database so no running Postgres needed.
