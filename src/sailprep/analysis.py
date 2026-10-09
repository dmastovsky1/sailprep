"""Turn hourly forecast data into race-relevant conditions and boat-specific notes."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .models import Boat, BoatType, HourlyForecast, RaceDay

COMPASS = [
    "N",
    "NNE",
    "NE",
    "ENE",
    "E",
    "ESE",
    "SE",
    "SSE",
    "S",
    "SSW",
    "SW",
    "WSW",
    "W",
    "WNW",
    "NW",
    "NNW",
]


def compass(deg: float) -> str:
    return COMPASS[round((deg % 360) / 22.5) % 16]


def circular_mean(degrees: list[float]) -> float:
    s = sum(math.sin(math.radians(d)) for d in degrees)
    c = sum(math.cos(math.radians(d)) for d in degrees)
    return math.degrees(math.atan2(s, c)) % 360


def angle_diff(a: float, b: float) -> float:
    """Signed smallest difference b - a in degrees, in (-180, 180]."""
    d = (b - a + 180) % 360 - 180
    return 180.0 if d == -180 else d


@dataclass
class Conditions:
    hours: int
    wind_mean_kt: float
    wind_min_kt: float
    wind_max_kt: float
    gust_max_kt: float
    gust_factor: float
    direction_mean_deg: float
    direction_spread_deg: float
    direction_trend_deg: float
    wind_trend_kt: float
    precipitation_mm: float
    temp_min_c: float
    temp_max_c: float
    notes: list[str] = field(default_factory=list)

    @property
    def direction_label(self) -> str:
        return compass(self.direction_mean_deg)


def window(race: RaceDay) -> list[HourlyForecast]:
    return [h for h in race.hours if race.start <= h.time <= race.end]


def summarize(race: RaceDay) -> Conditions:
    hrs = window(race)
    if not hrs:
        raise ValueError("No forecast hours fall inside the race window")
    speeds = [h.wind_speed_kt for h in hrs]
    gusts = [h.wind_gust_kt for h in hrs]
    dirs = [h.wind_direction_deg for h in hrs]
    mean_dir = circular_mean(dirs)
    offsets = [angle_diff(mean_dir, d) for d in dirs]
    mean = sum(speeds) / len(speeds)
    c = Conditions(
        hours=len(hrs),
        wind_mean_kt=mean,
        wind_min_kt=min(speeds),
        wind_max_kt=max(speeds),
        gust_max_kt=max(gusts),
        gust_factor=(max(gusts) / mean) if mean > 0 else 0.0,
        direction_mean_deg=mean_dir,
        direction_spread_deg=max(offsets) - min(offsets),
        direction_trend_deg=angle_diff(dirs[0], dirs[-1]),
        wind_trend_kt=speeds[-1] - speeds[0],
        precipitation_mm=sum(h.precipitation_mm for h in hrs),
        temp_min_c=min(h.temperature_c for h in hrs),
        temp_max_c=max(h.temperature_c for h in hrs),
    )
    c.notes = boat_notes(race.boat, c)
    return c


def boat_notes(boat: Boat, c: Conditions) -> list[str]:
    notes: list[str] = []
    if c.wind_max_kt < boat.min_wind_kt:
        notes.append(
            f"Wind may stay below {boat.min_wind_kt:g} kt: expect postponement or abandoned races."
        )
    elif c.wind_min_kt < boat.min_wind_kt:
        notes.append("Light patches below racing minimum possible; watch for postponements.")
    if c.gust_max_kt > boat.max_wind_kt:
        notes.append(
            f"Gusts to {c.gust_max_kt:.0f} kt exceed the {boat.max_wind_kt:g} kt "
            "upper limit: racing may be cancelled."
        )
    elif c.wind_max_kt >= boat.heavy_air_kt or c.gust_max_kt >= boat.heavy_air_kt + 5:
        notes.append("Heavy air expected: rig for depower, check gear and safety kit.")
    if boat.type is BoatType.FOILER and boat.foiling_kt is not None:
        if c.wind_mean_kt < boat.foiling_kt:
            notes.append(
                f"Mean wind under ~{boat.foiling_kt:g} kt: marginal foiling, "
                "prioritise early take-off and light-air foil setup."
            )
        else:
            notes.append("Foiling conditions likely for most of the window.")
    if boat.type is BoatType.DINGHY and c.wind_mean_kt >= 15:
        notes.append("Sustained hiking breeze: hydrate and plan for physical endurance.")
    if boat.type is BoatType.KEELBOAT and c.wind_max_kt >= boat.heavy_air_kt:
        notes.append("Check crew weight and headsail choice for the top of the range.")
    if c.gust_factor >= 1.4:
        notes.append(
            f"Gusty (gust factor {c.gust_factor:.1f}): keep heads out of the boat "
            "and play the pressure."
        )
    if c.direction_spread_deg >= 20:
        notes.append(
            f"Shifty: direction varies ~{c.direction_spread_deg:.0f} deg over the "
            "window. Track shifts on a compass before the start."
        )
    if abs(c.direction_trend_deg) >= 15:
        side = "right (veering)" if c.direction_trend_deg > 0 else "left (backing)"
        notes.append(
            f"Persistent shift to the {side} of ~{abs(c.direction_trend_deg):.0f} "
            "deg forecast: favour that side on longer beats."
        )
    if abs(c.wind_trend_kt) >= 4:
        word = "building" if c.wind_trend_kt > 0 else "dropping"
        notes.append(f"Breeze {word} by ~{abs(c.wind_trend_kt):.0f} kt through the day.")
    if c.precipitation_mm >= 1:
        notes.append("Rain forecast: pack wet-weather gear and expect patchy, unstable breeze.")
    return notes
