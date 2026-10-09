# sailprep core

The Python package behind Sailprep: forecast fetching, race-window analysis, timed heads-ups and brief rendering. The API and background worker (coming in Phase 1) import it, so this logic is written and tested once.

```bash
pip install -e ".[dev]"
sailprep boats
sailprep brief --venue "Newport" --boat j70 --date 2026-07-18
pytest
```

See [`examples/newport-j70.md`](examples/newport-j70.md) for sample output (generated from test fixture data).
