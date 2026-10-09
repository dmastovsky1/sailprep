# sailprep

Race-day prep for sailors. Tell it where you're racing and what you sail, and it builds a race brief: forecast for the race window, conditions summary, and boat-specific notes.

Built for inshore racing across dinghies, foilers and keelboats, with offshore support on the roadmap.

## Quick start

```bash
pip install -e ".[dev]"

# List built-in boat classes
sailprep boats

# Brief for a J/70 regatta in Newport, venue looked up by name
sailprep brief --venue "Newport" --boat j70 --date 2026-07-18 --start 11:00 --end 16:00

# Use exact coordinates and save to a file
sailprep brief --venue "Narragansett Bay" --lat 41.49 --lon -71.33 --boat waszp -o brief.md
```

See [`examples/newport-j70.md`](examples/newport-j70.md) for sample output (generated from test fixture data).

## What's in a brief

- **Conditions at a glance:** wind range and mean, max gust and gust factor, mean direction and spread, temperature, rain.
- **Key notes:** generated from the boat's wind range, for example postponement or cancellation risk, heavy-air depower, marginal foiling, gustiness, shiftiness, persistent shifts, and building or dropping breeze.
- **Hour by hour** table for the race window.

## How it works

```
src/sailprep/
  models.py    Venue, Boat, HourlyForecast, RaceDay
  boats.py     Built-in boat class profiles (wind ranges, crew, foiling threshold)
  forecast.py  Open-Meteo geocoding and hourly forecast client (stdlib only)
  analysis.py  Race-window summary and boat-specific notes
  brief.py     Markdown renderer
  cli.py       `sailprep` command
```

Forecast data comes from [Open-Meteo](https://open-meteo.com), which is free and needs no API key. The network call is injected, so the test suite runs entirely offline against fixtures.

## Development

```bash
pip install -e ".[dev]"
ruff check . && ruff format --check .
pytest
```

CI runs lint and tests on Python 3.11 to 3.13 for every push and pull request.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## Disclaimer

sailprep is a planning aid. Always check official marine forecasts and follow race committee instructions.
