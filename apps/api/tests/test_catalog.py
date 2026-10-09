from fastapi.testclient import TestClient


def test_boat_classes_cover_every_type_in_order(client: TestClient) -> None:
    boats = client.get("/api/v1/boat-classes").json()
    assert len(boats) == 12
    types = [b["type"] for b in boats]
    assert types == sorted(types, key=["dinghy", "foiler", "keelboat"].index)
    waszp = next(b for b in boats if b["key"] == "waszp")
    assert waszp["foiling_kt"] == 8


def test_venue_search(client: TestClient) -> None:
    venues = client.get("/api/v1/venues/search?q=Newport").json()
    assert venues[0]["name"] == "Newport, Rhode Island, United States"


def test_venue_search_needs_two_characters(client: TestClient) -> None:
    assert client.get("/api/v1/venues/search?q=N").status_code == 422


def test_cors_allows_the_web_app(client: TestClient) -> None:
    resp = client.get("/api/v1/boat-classes", headers={"Origin": "http://localhost:3000"})
    assert resp.headers["access-control-allow-origin"] == "http://localhost:3000"
