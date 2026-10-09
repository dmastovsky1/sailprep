"""Turn hourly forecast data into race-relevant conditions and timed heads-ups."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime

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
    c.notes = heads_ups(race.boat, hrs, c)
    return c


def clock(t: datetime) -> str:
    """Format an hour the way sailors say it: '2 pm', '11 am'."""
    return f"{t.hour % 12 or 12} {'am' if t.hour < 12 else 'pm'}"


def first(hrs: list[HourlyForecast], test) -> HourlyForecast | None:
    return next((h for h in hrs if test(h)), None)


def heads_ups(boat: Boat, hrs: list[HourlyForecast], c: Conditions) -> list[str]:
    """Time-stamped, gently worded heads-ups about the forecast.

    Sailprep is a forecaster, not a coach: these describe what the weather is
    expected to do and when, and only ever suggest preparation (rig, gear,
    clothing). They never give tactical or boat-handling advice.
    """
    notes: list[str] = []

    if c.wind_max_kt < boat.min_wind_kt:
        notes.append(
            f"Under {boat.min_wind_kt:g} kt is forecast for the whole window, "
            "so a postponement is possible."
        )
    elif light := first(hrs, lambda h: h.wind_speed_kt < boat.min_wind_kt):
        notes.append(
            f"Around {clock(light.time)} the breeze is forecast to drop to "
            f"{light.wind_speed_kt:.0f} kt, under the usual racing minimum, "
            "so there could be a delay."
        )

    if over := first(hrs, lambda h: h.wind_gust_kt > boat.max_wind_kt):
        notes.append(
            f"From {clock(over.time)} gusts near {over.wind_gust_kt:.0f} kt are forecast, "
            f"above the {boat.name}'s usual {boat.max_wind_kt:g} kt racing limit, "
            "so racing could be cut short."
        )
    elif heavy := first(hrs, lambda h: h.wind_speed_kt >= boat.heavy_air_kt):
        notes.append(
            f"At {clock(heavy.time)} the breeze is forecast at {heavy.wind_speed_kt:.0f}+ kt "
            f"(gusts {heavy.wind_gust_kt:.0f}), so you might want to start thinking "
            "about depowering."
        )

    if boat.type is BoatType.FOILER and boat.foiling_kt is not None:
        marginal = [h for h in hrs if h.wind_speed_kt < boat.foiling_kt]
        if marginal:
            lo = min(h.wind_speed_kt for h in marginal)
            hi = max(h.wind_speed_kt for h in marginal)
            span = f"{lo:.0f} kt" if round(lo) == round(hi) else f"{lo:.0f} to {hi:.0f} kt"
            notes.append(
                f"From {clock(marginal[0].time)} to {clock(marginal[-1].time)} the forecast is "
                f"{span}, which is marginal for foiling a {boat.name}. "
                "Worth thinking about your light-air setup."
            )

    if abs(c.direction_trend_deg) >= 15:
        side = "right" if c.direction_trend_deg > 0 else "left"
        notes.append(
            f"The wind is forecast to swing about {abs(c.direction_trend_deg):.0f} degrees "
            f"to the {side} between {clock(hrs[0].time)} and {clock(hrs[-1].time)}."
        )
    elif c.direction_spread_deg >= 20:
        notes.append(
            f"The forecast direction varies by about {c.direction_spread_deg:.0f} degrees "
            "across the window."
        )

    if c.gust_factor >= 1.4:
        notes.append(
            f"Gusts are forecast up to {c.gust_factor:.1f} times the mean wind, "
            "so expect a puffy day."
        )

    if abs(c.wind_trend_kt) >= 4:
        word = "build" if c.wind_trend_kt > 0 else "ease"
        notes.append(
            f"The breeze is forecast to {word} from {hrs[0].wind_speed_kt:.0f} kt at "
            f"{clock(hrs[0].time)} to {hrs[-1].wind_speed_kt:.0f} kt by {clock(hrs[-1].time)}."
        )

    if rain := first(hrs, lambda h: h.precipitation_mm >= 0.5):
        notes.append(
            f"Rain is forecast from {clock(rain.time)}, so you might want to pack wet-weather gear."
        )
    return notes
