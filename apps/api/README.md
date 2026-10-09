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
| `GET /api/v1/boat-classes` | Built-in boat class profiles |
| `GET /api/v1/venues/search?q=newport` | Places matching a name, best first |
| `GET /api/v1/brief?venue=Newport&boat=j70&date=2026-07-18&start=11:00&end=16:00` | Race brief: conditions, timed heads-ups and the day's hourly forecast (add `lat` and `lon` to skip the place lookup) |

Briefs are built live from Open-Meteo for now and are stateless, so the query string doubles as a share link. Stored briefs, forecast history and multiple models arrive with the database work.

## Checks

```bash
ruff check . && ruff format --check . && mypy && pytest
```

Tests need a PostgreSQL to talk to; CI runs one as a service container.
