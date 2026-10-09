from datetime import date, datetime

import pytest

from sailprep.analysis import angle_diff, circular_mean, compass, summarize
from sailprep.boats import get_boat
from sailprep.forecast import get_hourly
from sailprep.models import HourlyForecast, RaceDay, Venue

VENUE = Venue("Test", 0, 0)


def race_for(boat_key, hours, start=11, end=16):
    return RaceDay(
        VENUE,
        get_boat(boat_key),
        datetime(2026, 7, 18, start),
        datetime(2026, 7, 18, end),
        hours=hours,
    )


def flat_hours(speed, gust=None, direction=180.0):
    return [
        HourlyForecast(datetime(2026, 7, 18, h), speed, gust or speed, direction, 20, 0)
        for h in range(24)
    ]


def test_compass():
    assert compass(0) == "N"
    assert compass(359) == "N"
    assert compass(225) == "SW"


def test_circular_mean_wraps_north():
    assert angle_diff(0, circular_mean([350, 10])) == pytest.approx(0, abs=1e-6)


def test_angle_diff_signed_and_wrapping():
    assert angle_diff(350, 10) == 20
    assert angle_diff(10, 350) == -20


def test_summary_uses_race_window_only(fake_fetch):
    hours = get_hourly(VENUE, date(2026, 7, 18), fake_fetch)
    c = summarize(race_for("ilca7", hours))
    assert c.hours == 6
    assert c.wind_min_kt == 11 and c.wind_max_kt == 15
    assert c.direction_label in {"SSW", "SW"}
    assert c.wind_trend_kt == 4
    assert any("building" in n for n in c.notes)


def test_empty_window_raises():
    with pytest.raises(ValueError):
        summarize(
            RaceDay(
                VENUE,
                get_boat("ilca7"),
                datetime(2027, 1, 1),
                datetime(2027, 1, 1, 1),
                hours=flat_hours(10),
            )
        )


def test_light_air_foiler_note():
    c = summarize(race_for("waszp", flat_hours(6)))
    assert any("marginal foiling" in n for n in c.notes)


def test_foiling_conditions_note():
    c = summarize(race_for("moth", flat_hours(12)))
    assert any("Foiling conditions likely" in n for n in c.notes)


def test_over_limit_gusts_flag_cancellation():
    c = summarize(race_for("j70", flat_hours(22, gust=30)))
    assert any("cancelled" in n for n in c.notes)


def test_below_minimum_flags_postponement():
    c = summarize(race_for("etchells", flat_hours(1.5)))
    assert any("postponement" in n for n in c.notes)


def test_shifty_and_persistent_shift():
    hours = [
        HourlyForecast(datetime(2026, 7, 18, h), 10, 12, 180 + h * 6, 20, 0) for h in range(24)
    ]
    c = summarize(race_for("420", hours))
    assert any("Shifty" in n for n in c.notes)
    assert any("veering" in n for n in c.notes)


def test_unknown_boat():
    with pytest.raises(ValueError, match="Known boats"):
        get_boat("optimist-xl")
