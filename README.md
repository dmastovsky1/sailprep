# sailprep

Race-day prep for sailors. Tell it where you're racing and what you sail, and it builds a race brief: forecast for the race window, conditions summary, and time-stamped heads-ups for your boat.

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
- **Heads-ups:** gentle, time-stamped notes when the forecast crosses a threshold for your boat, such as "At 2 pm the breeze is forecast at 20+ kt, so you might want to start thinking about depowering." sailprep is a forecaster, not a coach: it never gives tactical advice.
- **Hour by hour** table for the race window.

## How it works

```
src/sailprep/
  models.py    Venue, Boat, HourlyForecast, RaceDay
  boats.py     Built-in boat class profiles (wind ranges, crew, foiling threshold)
  forecast.py  Open-Meteo geocoding and hourly forecast client (stdlib only)
  analysis.py  Race-window summary and timed heads-ups
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
