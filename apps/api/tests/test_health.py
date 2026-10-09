import pytest
from fastapi.testclient import TestClient

from sailprep_api import __version__


def test_health_does_not_need_the_database(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "version": __version__}


def test_ready_when_database_is_reachable(client: TestClient) -> None:
    resp = client.get("/health/ready")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "database": "ok"}


@pytest.fixture
def unreachable_db(monkeypatch: pytest.MonkeyPatch) -> None:
    # Port 1 refuses connections immediately, so this fails fast.
    monkeypatch.setenv(
        "SAILPREP_DATABASE_URL", "postgresql+psycopg://sailprep:x@127.0.0.1:1/sailprep"
    )


def test_not_ready_when_database_is_down(unreachable_db: None, client: TestClient) -> None:
    resp = client.get("/health/ready")
    assert resp.status_code == 503
    assert resp.json() == {"status": "unavailable", "database": "unreachable"}


def test_openapi_spec_is_published(client: TestClient) -> None:
    spec = client.get("/openapi.json").json()
    assert spec["info"]["title"] == "Sailprep API"
    assert "/health/ready" in spec["paths"]
