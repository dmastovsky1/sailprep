import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from sailprep_api.config import get_settings
from sailprep_api.db import get_engine
from sailprep_api.deps import get_fetcher
from sailprep_api.main import create_app

FIXTURES = Path(__file__).parent / "fixtures"


class FakeFetch:
    """Serves recorded Open-Meteo responses and records the URLs asked for."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def __call__(self, url: str) -> dict[str, Any]:
        self.calls.append(url)
        name = "newport_geocode.json" if "geocoding" in url else "newport_forecast.json"
        data: dict[str, Any] = json.loads((FIXTURES / name).read_text())
        return data


@pytest.fixture
def fake_fetch() -> FakeFetch:
    return FakeFetch()


@pytest.fixture
def client(fake_fetch: FakeFetch) -> Iterator[TestClient]:
    get_settings.cache_clear()
    get_engine.cache_clear()
    app = create_app()
    app.dependency_overrides[get_fetcher] = lambda: fake_fetch
    with TestClient(app) as c:
        yield c
    get_engine.cache_clear()
    get_settings.cache_clear()
