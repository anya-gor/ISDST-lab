import fakeredis
import pytest

from app.main import create_app


@pytest.fixture
def client():
    clock = iter(range(1000, 2000, 60))  # каждый вызов clock() = +60 с
    app = create_app(fakeredis.FakeRedis(decode_responses=True), clock=lambda: next(clock))
    return app.test_client()


def test_health_ok(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_start_rental(client):
    r = client.post("/rentals", json={"scooter_id": "S-1", "user_id": "u1"})
    assert r.status_code == 201
    assert r.get_json()["scooter_id"] == "S-1"


def test_start_requires_fields(client):
    assert client.post("/rentals", json={"scooter_id": "S-1"}).status_code == 400
    assert client.post("/rentals", data="не json").status_code == 400


def test_cannot_start_same_scooter_twice(client):
    client.post("/rentals", json={"scooter_id": "S-1", "user_id": "u1"})
    r = client.post("/rentals", json={"scooter_id": "S-1", "user_id": "u2"})
    assert r.status_code == 409


def test_active_list_contains_started_rentals(client):
    client.post("/rentals", json={"scooter_id": "S-1", "user_id": "u1"})
    client.post("/rentals", json={"scooter_id": "S-2", "user_id": "u2"})
    body = client.get("/rentals/active").get_json()
    assert body["count"] == 2
    assert [r["scooter_id"] for r in body["rentals"]] == ["S-1", "S-2"]


def test_stop_returns_duration_and_removes_from_active(client):
    client.post("/rentals", json={"scooter_id": "S-1", "user_id": "u1"})  # t=1000
    r = client.post("/rentals/S-1/stop")                                  # t=1060
    assert r.status_code == 200
    assert r.get_json()["duration_seconds"] == 60
    assert client.get("/rentals/active").get_json()["count"] == 0


def test_stop_without_active_rental_is_404(client):
    assert client.post("/rentals/S-9/stop").status_code == 404


def test_scooter_can_be_rented_again_after_stop(client):
    client.post("/rentals", json={"scooter_id": "S-1", "user_id": "u1"})
    client.post("/rentals/S-1/stop")
    assert client.post("/rentals", json={"scooter_id": "S-1", "user_id": "u2"}).status_code == 201
