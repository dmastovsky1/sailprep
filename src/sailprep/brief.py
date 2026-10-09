"""Render a race brief as Markdown."""

from __future__ import annotations

from .analysis import Conditions, compass, window
from .models import RaceDay


def render_markdown(race: RaceDay, c: Conditions) -> str:
    v, b = race.venue, race.boat
    lines = [
        f"# Race Brief: {v.name}",
        "",
        f"**Boat:** {b.name} ({b.type.value}, crew of {b.crew})  ",
        f"**Date:** {race.start:%A %d %B %Y}  ",
        f"**Race window:** {race.start:%H:%M} to {race.end:%H:%M} (local)  ",
        f"**Discipline:** {race.discipline.value}  ",
        f"**Position:** {v.latitude:.4f}, {v.longitude:.4f}",
        "",
        "## Conditions at a glance",
        "",
        "| | |",
        "|---|---|",
        f"| Wind | {c.wind_min_kt:.0f} to {c.wind_max_kt:.0f} kt (mean {c.wind_mean_kt:.0f} kt) |",
        f"| Gusts | up to {c.gust_max_kt:.0f} kt (factor {c.gust_factor:.1f}) |",
        f"| Direction | {c.direction_label} ({c.direction_mean_deg:.0f} deg), "
        f"spread {c.direction_spread_deg:.0f} deg |",
        f"| Air temp | {c.temp_min_c:.0f} to {c.temp_max_c:.0f} C |",
        f"| Rain | {c.precipitation_mm:.1f} mm |",
        "",
        "## Key notes",
        "",
    ]
    lines += [f"- {n}" for n in c.notes] or ["- Nothing unusual in the forecast."]
    lines += [
        "",
        "## Hour by hour",
        "",
        "| Time | Wind (kt) | Gust (kt) | Dir | Temp (C) | Rain (mm) |",
        "|---|---|---|---|---|---|",
    ]
    for h in window(race):
        lines.append(
            f"| {h.time:%H:%M} | {h.wind_speed_kt:.0f} | {h.wind_gust_kt:.0f} | "
            f"{compass(h.wind_direction_deg)} {h.wind_direction_deg:.0f} | "
            f"{h.temperature_c:.0f} | {h.precipitation_mm:.1f} |"
        )
    lines += [
        "",
        "---",
        "_Forecast data: [Open-Meteo](https://open-meteo.com). "
        "Always check official marine forecasts and race committee instructions._",
        "",
    ]
    return "\n".join(lines)
