"""Race briefs, built live from the forecast for a venue, boat and race window."""

from datetime import UTC, date, datetime, time
from typing import Annotated
from urllib.error import URLError

from fastapi import APIRouter, Depends, HTTPException, Query
from sailprep.analysis import compass, summarize
from sailprep.boats import get_boat
from sailprep.forecast import Fetcher, geocode, get_hourly
from sailprep.models import RaceDay, Venue

from ..deps import get_fetcher
from ..schemas import BriefOut, ConditionsOut, HourOut, SourceOut, VenueOut
from .boats import boat_out

router = APIRouter(prefix="/api/v1", tags=["briefs"])


@router.get("/brief", responses={404: {}, 422: {}, 502: {}})
def get_brief(
    fetch: Annotated[Fetcher, Depends(get_fetcher)],
    venue: Annotated[str, Query(min_length=2, max_length=100, description="Venue name")],
    boat: Annotated[str, Query(description="Boat class key, see /api/v1/boat-classes")],
    day: Annotated[date, Query(alias="date", description="Race day, YYYY-MM-DD")],
    start: Annotated[time, Query(description="First warning signal, HH:MM local")] = time(11),
    end: Annotated[time, Query(description="Last finish, HH:MM local")] = time(16),
    lat: Annotated[float | None, Query(ge=-90, le=90)] = None,
    lon: Annotated[float | None, Query(ge=-180, le=180)] = None,
) -> BriefOut:
    """Forecast brief for one race day. Give lat and lon to skip looking up the venue by name.

    Stateless and safe to cache, so the same query string doubles as a share link.
    """
    if end <= start:
        raise HTTPException(422, "The race window must end after it starts")
    try:
        boat_class = get_boat(boat)
    except ValueError as e:
        raise HTTPException(404, str(e)) from e

    try:
        place = Venue(venue, lat, lon) if lat is not None and lon is not None else None
        if place is None:
            place = geocode(venue, fetch)
        hours = get_hourly(place, day, fetch)
    except ValueError as e:
        raise HTTPException(404, str(e)) from e
    except (URLError, TimeoutError) as e:
        raise HTTPException(502, "The forecast provider is unavailable right now") from e

    race = RaceDay(
        place, boat_class, datetime.combine(day, start), datetime.combine(day, end), hours=hours
    )
    try:
        c = summarize(race)
    except ValueError as e:
        raise HTTPException(404, "No forecast is available for that date yet") from e

    return BriefOut(
        venue=VenueOut(**place.__dict__),
        boat=boat_out(boat_class),
        date=day,
        start=start,
        end=end,
        discipline=race.discipline.value,
        conditions=ConditionsOut(
            wind_mean_kt=c.wind_mean_kt,
            wind_min_kt=c.wind_min_kt,
            wind_max_kt=c.wind_max_kt,
            gust_max_kt=c.gust_max_kt,
            gust_factor=c.gust_factor,
            direction_mean_deg=c.direction_mean_deg,
            direction_label=c.direction_label,
            direction_spread_deg=c.direction_spread_deg,
            temp_min_c=c.temp_min_c,
            temp_max_c=c.temp_max_c,
            precipitation_mm=c.precipitation_mm,
        ),
        heads_ups=c.notes,
        hours=[
            HourOut(
                time=h.time,
                in_race_window=race.start <= h.time <= race.end,
                wind_speed_kt=h.wind_speed_kt,
                wind_gust_kt=h.wind_gust_kt,
                wind_direction_deg=h.wind_direction_deg,
                direction_label=compass(h.wind_direction_deg),
                temperature_c=h.temperature_c,
                precipitation_mm=h.precipitation_mm,
            )
            for h in hours
        ],
        source=SourceOut(provider="Open-Meteo", fetched_at=datetime.now(UTC)),
    )
