# Sailprep API

FastAPI service that serves forecasts and race briefs to the web and mobile apps. Interactive docs are at `/docs` once it is running.

## Run it

From the repo root, with Docker:

```bash
docker compose up --build
curl localhost:8000/health/ready
```

Or directly, against a local PostgreSQL:

```bash
cd apps/api
pip install -e ../../packages/core -e ".[dev]"
export SAILPREP_DATABASE_URL=postgresql+psycopg://sailprep:sailprep@localhost:5432/sailprep
uvicorn sailprep_api.main:app --reload
```

## Endpoints so far

| Method and path | Does |
| --- | --- |
| `GET /health` | The process is up (no database call) |
| `GET /health/ready` | PostgreSQL is reachable; 503 if not |

## Checks

```bash
ruff check . && ruff format --check . && mypy && pytest
```

Tests need a PostgreSQL to talk to; CI runs one as a service container.
