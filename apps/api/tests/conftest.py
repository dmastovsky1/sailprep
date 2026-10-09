from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from sailprep_api.config import get_settings
from sailprep_api.db import get_engine
from sailprep_api.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    get_settings.cache_clear()
    get_engine.cache_clear()
    with TestClient(create_app()) as c:
        yield c
    get_engine.cache_clear()
    get_settings.cache_clear()
