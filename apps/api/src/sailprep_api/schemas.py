"""Response models: the API's public contract, independent of core internals."""

from datetime import date, datetime, time

from pydantic import BaseModel


class VenueOut(BaseModel):
    name: str
    latitude: float
    longitude: float
    timezone: str


class BoatClassOut(BaseModel):
    key: str
    name: str
    type: str
    crew: int
    min_wind_kt: float
    max_wind_kt: float
    heavy_air_kt: float
    foiling_kt: float | None


class ConditionsOut(BaseModel):
    wind_mean_kt: float
    wind_min_kt: float
    wind_max_kt: float
    gust_max_kt: float
    gust_factor: float
    direction_mean_deg: float
    direction_label: str
    direction_spread_deg: float
    temp_min_c: float
    temp_max_c: float
    precipitation_mm: float


class HourOut(BaseModel):
    time: datetime
    in_race_window: bool
    wind_speed_kt: float
    wind_gust_kt: float
    wind_direction_deg: float
    direction_label: str
    temperature_c: float
    precipitation_mm: float


class SourceOut(BaseModel):
    provider: str
    fetched_at: datetime


class BriefOut(BaseModel):
    venue: VenueOut
    boat: BoatClassOut
    date: date
    start: time
    end: time
    discipline: str
    conditions: ConditionsOut
    heads_ups: list[str]
    hours: list[HourOut]
    source: SourceOut
