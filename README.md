# Sailprep

[![CI](https://github.com/dmastovsky1/sailprep/actions/workflows/ci.yml/badge.svg)](https://github.com/dmastovsky1/sailprep/actions/workflows/ci.yml)

A sailing forecaster for racers. Pick a venue, a boat and a race window, and Sailprep builds a race-day weather brief: wind, gusts and direction across several forecast models, tides, local conditions notes, and gentle time-stamped heads-ups such as *"At 2 pm the breeze is forecast at 20+ kt, so you might want to start thinking about depowering."* Briefs can be shared as a PDF straight into a crew group chat.

After sailing, you can log what you actually saw. Sailprep compares those logs (plus nearby buoys and weather stations) with what was forecast, and learns a correction for venues you sail often.

Sailprep is a forecaster, not a coach: it describes the weather and never gives tactical advice.

Built first for inshore racing in dinghies, foilers and keelboats, with offshore and native mobile on the roadmap.

## Repository layout

```
packages/core/   Python package: forecast fetching, analysis, heads-ups, brief rendering (working today)
apps/api/        FastAPI backend (Phase 1, in progress) and scheduled worker
apps/web/        Next.js web app (Phase 2, in progress)
apps/mobile/     React Native app (Phase 5)
docs/            Architecture and design notes
```

## Try it today

The core package already works as a command-line tool:

```bash
cd packages/core
pip install -e ".[dev]"
sailprep boats
sailprep brief --venue "Newport" --boat j70 --date 2026-07-18 --start 11:00 --end 16:00
```

Sample output: [`packages/core/examples/newport-j70.md`](packages/core/examples/newport-j70.md).

## Run it

```bash
docker compose up --build
```

Then open http://localhost:3000 for the web app, or http://localhost:8000/docs for the API. See [apps/web](apps/web/README.md) and [apps/api](apps/api/README.md).

## Architecture

See [docs/architecture.md](docs/architecture.md) for the system design and [ROADMAP.md](ROADMAP.md) for the build plan.

## Development

Every pull request runs lint (ruff), strict type checks (mypy) and tests (pytest, Python 3.11 to 3.13) in GitHub Actions. Jobs only run for the parts of the repo a change touches.

## Disclaimer

Sailprep is a planning aid. Always check official marine forecasts and follow race committee instructions.

## License

MIT
