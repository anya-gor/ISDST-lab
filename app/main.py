"""API учёта поездок на самокатах. Активные аренды хранятся в Redis."""

import json
import os
import time

import redis
from flask import Flask, jsonify, request

ACTIVE_KEY = "rentals:active"  # Redis hash: scooter_id -> JSON аренды


def create_app(client: "redis.Redis | None" = None, clock=time.time) -> Flask:
    app = Flask(__name__)
    if client is None:
        client = redis.Redis.from_url(
            os.environ.get("REDIS_URL", "redis://redis:6379/0"), decode_responses=True
        )

    def error(message: str, status: int):
        return jsonify({"error": message}), status

    @app.get("/health")
    def health():
        try:
            client.ping()
        except redis.RedisError:
            return error("redis недоступен", 503)
        return jsonify({"status": "ok"})

    @app.post("/rentals")
    def start_rental():
        data = request.get_json(silent=True) or {}
        scooter_id, user_id = data.get("scooter_id"), data.get("user_id")
        if not scooter_id or not user_id:
            return error("нужны поля scooter_id и user_id", 400)
        rental = {
            "scooter_id": str(scooter_id),
            "user_id": str(user_id),
            "started_at": int(clock()),
        }
        # HSETNX атомарно: второй запрос на тот же самокат вернёт 0
        if not client.hsetnx(ACTIVE_KEY, rental["scooter_id"], json.dumps(rental)):
            return error(f"самокат {scooter_id} уже арендован", 409)
        return jsonify(rental), 201

    @app.post("/rentals/<scooter_id>/stop")
    def stop_rental(scooter_id: str):
        raw = client.hget(ACTIVE_KEY, scooter_id)
        if raw is None:
            return error(f"активной аренды самоката {scooter_id} нет", 404)
        client.hdel(ACTIVE_KEY, scooter_id)
        rental = json.loads(raw)
        rental["finished_at"] = int(clock())
        rental["duration_seconds"] = rental["finished_at"] - rental["started_at"]
        return jsonify(rental)

    @app.get("/rentals/active")
    def active_rentals():
        rentals = [json.loads(v) for v in client.hvals(ACTIVE_KEY)]
        rentals.sort(key=lambda r: r["started_at"])
        return jsonify({"count": len(rentals), "rentals": rentals})

    return app


def get_app() -> Flask:
    """Фабрика для gunicorn: gunicorn 'app.main:get_app()'."""
    return create_app()
