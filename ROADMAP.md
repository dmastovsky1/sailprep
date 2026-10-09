# Roadmap

Each phase ships as a series of small pull requests with green CI. A phase is done when its gate is met.

## Phase 0: Foundation
- [x] Prototype: Open-Meteo forecast, boat profiles, timed heads-ups, Markdown brief
- [x] Monorepo layout with the prototype as `packages/core`
- [x] CI: ruff, mypy (strict), pytest with coverage on Python 3.11 to 3.13, path-filtered jobs
- [x] Dependabot for Python and GitHub Actions

**Gate:** CI green on `main`.

## Phase 1: API and database
- [x] FastAPI service, health check, Docker Compose with PostgreSQL
- [ ] Tables and Alembic migrations for venues, boat classes, forecast runs and points
- [ ] Worker pulling GFS, ECMWF, ICON and HRRR from Open-Meteo on a schedule
- [ ] Venue, boat class and forecast endpoints with per-model and consensus values
- [ ] Briefs without an account (`POST /briefs`, `GET /b/{id}`), integration tests on Postgres in CI

**Gate:** a brief is served by the API with integration tests passing.

## Phase 2: Web app v1
- [x] Brief API endpoints (live from Open-Meteo, stateless share links)
- [x] Plan a race, brief page with wind chart
- [ ] Model spread and venue map
- [ ] PDF export and share links (native share sheet for group chats)
- [ ] Preview deploys on every PR; production deploy on merge

**Gate:** a live URL anyone can use.

## Phase 3: Logging and learning
- [ ] Optional sign-in; saved boats and venues
- [ ] End-of-day observation log
- [ ] Hourly buoy and weather station records
- [ ] Per-venue bias correction, shown beside the raw forecast

**Gate:** corrections reduce forecast error at a test venue.

## Phase 4: Richer forecasts and local knowledge
- [ ] Tides and currents, waves
- [ ] Accuracy-weighted model blend per venue
- [ ] Venue knowledge pipeline with cited notes
- [ ] Sailor notes, private by default with a share switch

**Gate:** briefs show tides, waves and model confidence.

## Phase 5: Mobile and offshore
- [ ] Expo app with offline briefs and forecast-change alerts
- [ ] Offshore mode: multi-day forecasts, routes and waypoints, watch planning
