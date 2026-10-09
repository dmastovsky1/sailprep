from typing import Any
from urllib.error import URLError

from fastapi.testclient import TestClient

from sailprep_api.deps import get_fetcher

from .conftest import FakeFetch

BRIEF = "/api/v1/brief?venue=Newport&boat=j70&date=2026-07-18&start=11:00&end=16:00"


def test_brief_geocodes_the_venue_and_summarises_the_window(
    client: TestClient, fake_fetch: FakeFetch
) -> None:
    resp = client.get(BRIEF)
    assert resp.status_code == 200
    body = resp.json()
    assert body["venue"]["name"] == "Newport, Rhode Island, United States"
    assert body["boat"]["name"] == "J/70"
    assert body["conditions"]["wind_min_kt"] == 11
    assert body["conditions"]["wind_max_kt"] == 15
    assert (
        "The breeze is forecast to build from 11 kt at 11 am to 15 kt by 4 pm."
        in (body["heads_ups"])
    )
    assert len(body["hours"]) == 24
    assert sum(h["in_race_window"] for h in body["hours"]) == 6
    assert body["source"]["provider"] == "Open-Meteo"
    assert len(fake_fetch.calls) == 2


def test_coordinates_skip_the_venue_lookup(client: TestClient, fake_fetch: FakeFetch) -> None:
    resp = client.get(BRIEF.replace("venue=Newport", "venue=Narragansett+Bay&lat=41.49&lon=-71.33"))
    assert resp.status_code == 200
    assert resp.json()["venue"]["name"] == "Narragansett Bay"
    assert len(fake_fetch.calls) == 1


def test_unknown_boat_is_404(client: TestClient) -> None:
    resp = client.get(BRIEF.replace("boat=j70", "boat=bathtub"))
    assert resp.status_code == 404
    assert "Unknown boat" in resp.json()["detail"]


def test_window_must_end_after_it_starts(client: TestClient) -> None:
    resp = client.get(BRIEF.replace("end=16:00", "end=10:00"))
    assert resp.status_code == 422


def test_unknown_place_is_404(client: TestClient) -> None:
    client.app.dependency_overrides[get_fetcher] = lambda: lambda url: {}  # type: ignore[attr-defined]
    resp = client.get(BRIEF)
    assert resp.status_code == 404
    assert "Could not find" in resp.json()["detail"]


def test_provider_outage_is_502(client: TestClient) -> None:
    def down(url: str) -> dict[str, Any]:
        raise URLError("connection refused")

    client.app.dependency_overrides[get_fetcher] = lambda: down  # type: ignore[attr-defined]
    resp = client.get(BRIEF)
    assert resp.status_code == 502


def test_brief_is_in_the_openapi_spec(client: TestClient) -> None:
    paths = client.get("/openapi.json").json()["paths"]
    assert {"/api/v1/brief", "/api/v1/boat-classes", "/api/v1/venues/search"} <= set(paths)
