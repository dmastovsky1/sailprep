from datetime import date, datetime

import pytest

from sailprep.forecast import build_forecast_url, geocode, get_hourly
from sailprep.models import Venue


def test_geocode_builds_label(fake_fetch):
    v = geocode("Newport", fake_fetch)
    assert v.name == "Newport, Rhode Island, United States"
    assert v.timezone == "America/New_York"
    assert v.latitude == pytest.approx(41.49, abs=0.01)


def test_geocode_unknown_place():
    with pytest.raises(ValueError, match="Could not find"):
        geocode("Nowhere", lambda url: {})


def test_forecast_url_requests_knots_for_one_day():
    url = build_forecast_url(Venue("X", 1.5, 2.5, "UTC"), date(2026, 7, 18))
    assert "wind_speed_unit=kn" in url
    assert "start_date=2026-07-18" in url and "end_date=2026-07-18" in url
    assert "wind_gusts_10m" in url


def test_get_hourly_parses_payload(fake_fetch):
    hours = get_hourly(Venue("X", 0, 0), date(2026, 7, 18), fake_fetch)
    assert len(hours) == 24
    assert hours[12].time == datetime(2026, 7, 18, 12)
    assert hours[12].wind_speed_kt == 12
