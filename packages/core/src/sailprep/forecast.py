"""Weather data from Open-Meteo (free, no API key).

https://open-meteo.com/en/docs
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from collections.abc import Callable
from datetime import date, datetime
from typing import Any

from .models import HourlyForecast, Venue

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

HOURLY_VARS = [
    "wind_speed_10m",
    "wind_gusts_10m",
    "wind_direction_10m",
    "temperature_2m",
    "precipitation",
]

# Injected in tests so nothing touches the network.
JSON = dict[str, Any]
Fetcher = Callable[[str], JSON]


def http_get_json(url: str) -> JSON:
    req = urllib.request.Request(url, headers={"User-Agent": "sailprep/0.1"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data: JSON = json.load(resp)
        return data


def geocode(name: str, fetch: Fetcher = http_get_json) -> Venue:
    """Resolve a place name to a Venue using Open-Meteo's geocoder."""
    url = f"{GEOCODE_URL}?{urllib.parse.urlencode({'name': name, 'count': 1})}"
    results = fetch(url).get("results") or []
    if not results:
        raise ValueError(f"Could not find a location named '{name}'")
    r = results[0]
    label = ", ".join(p for p in (r.get("name"), r.get("admin1"), r.get("country")) if p)
    return Venue(label, r["latitude"], r["longitude"], r.get("timezone", "auto"))


def build_forecast_url(venue: Venue, day: date) -> str:
    params = {
        "latitude": venue.latitude,
        "longitude": venue.longitude,
        "hourly": ",".join(HOURLY_VARS),
        "wind_speed_unit": "kn",
        "timezone": venue.timezone,
        "start_date": day.isoformat(),
        "end_date": day.isoformat(),
    }
    return f"{FORECAST_URL}?{urllib.parse.urlencode(params)}"


def parse_hourly(payload: JSON) -> list[HourlyForecast]:
    h = payload["hourly"]
    return [
        HourlyForecast(
            time=datetime.fromisoformat(t),
            wind_speed_kt=h["wind_speed_10m"][i],
            wind_gust_kt=h["wind_gusts_10m"][i],
            wind_direction_deg=h["wind_direction_10m"][i],
            temperature_c=h["temperature_2m"][i],
            precipitation_mm=h["precipitation"][i],
        )
        for i, t in enumerate(h["time"])
        if h["wind_speed_10m"][i] is not None
    ]


def get_hourly(venue: Venue, day: date, fetch: Fetcher = http_get_json) -> list[HourlyForecast]:
    return parse_hourly(fetch(build_forecast_url(venue, day)))
