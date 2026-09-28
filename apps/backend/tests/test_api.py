"""HTTP layer tests (require fastapi + httpx: `uv pip install -e ".[dev]"`)."""
from fastapi.testclient import TestClient

from dice_api.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_roll_with_seed_is_replayable():
    a = client.get("/roll", params={"expr": "4d6kh3+1", "seed": 123}).json()
    b = client.get("/roll", params={"expr": "4d6kh3+1", "seed": 123}).json()
    assert a == b
    assert len(a["rolls"]) == 4 and len(a["kept"]) == 3 and len(a["dropped"]) == 1
    assert a["total"] == sum(a["kept"]) + 1


def test_roll_without_seed_returns_a_seed():
    a = client.get("/roll", params={"expr": "d20"}).json()
    b = client.get("/roll", params={"expr": "d20", "seed": a["seed"]}).json()
    assert a == b


def test_invalid_expression_is_422_with_message():
    r = client.get("/roll", params={"expr": "4d6kh5"})
    assert r.status_code == 422
    assert "between 1 and 4" in r.json()["detail"]


def test_parse_endpoint():
    r = client.get("/parse", params={"expr": "2d20kl1-1"}).json()
    assert r == {
        "expression": "2d20kl1-1", "count": 2, "sides": 20, "modifier": -1,
        "keep": ["low", 1], "min_total": 0, "max_total": 19,
    }


def test_limits():
    assert client.get("/limits").json() == {"max_count": 1000, "max_sides": 10000}
