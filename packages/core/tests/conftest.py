import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


@pytest.fixture
def fake_fetch():
    """Stand-in for http_get_json that serves fixtures and records requested URLs."""
    calls: list[str] = []

    def fetch(url: str) -> dict:
        calls.append(url)
        if "geocoding" in url:
            return load("newport_geocode.json")
        return load("newport_forecast.json")

    fetch.calls = calls
    return fetch
