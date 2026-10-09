# Roadmap

Each milestone ships as its own small PR with tests and green CI.

## v0.1: Inshore MVP (done)
- [x] Venue lookup by name or coordinates
- [x] Hourly wind, gust, direction, temperature, rain from Open-Meteo
- [x] Built-in dinghy, foiler and keelboat profiles
- [x] Race-window summary with boat-specific notes
- [x] Markdown race brief
- [x] CI: ruff + pytest on Python 3.11 to 3.13

## Next
- [ ] Tides and currents (NOAA CO-OPS for US venues; marine API elsewhere)
- [ ] Waves and sea state from the Open-Meteo marine API
- [ ] Compare multiple forecast models side by side (GFS, ECMWF, HRRR) to show confidence
- [ ] HTML and PDF brief output
- [ ] Venue knowledge: gather local tips (geographic wind effects, current lines, sea breeze) from the web and summarise them into the brief
- [ ] Custom boat profiles from a YAML file
- [ ] Sunrise, sunset and daylight window

## Later
- [ ] Offshore mode: multi-day route forecasts, waypoints, watch planning
- [ ] Web app front end
- [ ] Release automation (tag, changelog, PyPI publish)
