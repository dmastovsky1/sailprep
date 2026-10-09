"""Venue search, backed by Open-Meteo geocoding until venues live in the database."""

from typing import Annotated
from urllib.error import URLError

from fastapi import APIRouter, Depends, HTTPException, Query
from sailprep.forecast import Fetcher, search_places

from ..deps import get_fetcher
from ..schemas import VenueOut

router = APIRouter(prefix="/api/v1", tags=["venues"])


@router.get("/venues/search")
def search_venues(
    q: Annotated[str, Query(min_length=2, max_length=100, description="Place name")],
    fetch: Annotated[Fetcher, Depends(get_fetcher)],
) -> list[VenueOut]:
    """Places matching a name, best match first (up to 5)."""
    try:
        venues = search_places(q, count=5, fetch=fetch)
    except (URLError, TimeoutError) as e:
        raise HTTPException(502, "Place search is unavailable right now") from e
    return [VenueOut(**v.__dict__) for v in venues]
