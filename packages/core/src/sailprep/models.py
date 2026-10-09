"""Core data types shared across the app."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class BoatType(StrEnum):
    DINGHY = "dinghy"
    FOILER = "foiler"
    KEELBOAT = "keelboat"


class Discipline(StrEnum):
    INSHORE = "inshore"
    # OFFSHORE is planned; adding it here should not require changes elsewhere
    # beyond a new analysis profile and brief sections.


@dataclass(frozen=True)
class Venue:
    name: str
    latitude: float
    longitude: float
    timezone: str = "auto"


@dataclass(frozen=True)
class Boat:
    """A boat class and the wind range it races well in (knots)."""

    key: str
    name: str
    type: BoatType
    min_wind_kt: float
    max_wind_kt: float
    crew: int
    # Wind above which the boat is in survival / depowered mode.
    heavy_air_kt: float
    # Foilers only: rough wind speed needed to foil reliably.
    foiling_kt: float | None = None


@dataclass(frozen=True)
class HourlyForecast:
    time: datetime
    wind_speed_kt: float
    wind_gust_kt: float
    wind_direction_deg: float
    temperature_c: float
    precipitation_mm: float


@dataclass
class RaceDay:
    venue: Venue
    boat: Boat
    start: datetime
    end: datetime
    discipline: Discipline = Discipline.INSHORE
    hours: list[HourlyForecast] = field(default_factory=list)
