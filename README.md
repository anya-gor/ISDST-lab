# Задача 7: Аренда самокатов (учёт поездок)

**Студент:** Гордеенко А.В.

> API поездок + Redis (активные аренды). Compose: `api` и `redis`. Старт/стоп аренды, список активных. Явная проверка через `curl` в README.

Полная постановка — в ветке `main`, файл `tasks/lab-7.md`.

## Что внутри

```
app/main.py            # Flask API (старт/стоп/список аренд)
app/requirements.txt   # зависимости контейнера (flask, redis, gunicorn)
Dockerfile             # образ api
compose.yaml           # api + redis
.env.example           # пример переменных окружения
tests/test_api.py      # тесты API на fakeredis (без Docker)
```

| Сервис | Образ | Роль |
|--------|-------|------|
| `api` | собирается из `Dockerfile` (python:3.12-slim, gunicorn, пользователь не root) | REST API, порт `8000` |
| `redis` | `redis:7-alpine` | хранит активные аренды (hash `rentals:active`), том `redis-data` + AOF — данные переживают перезапуск |

Compose: общая сеть `backend`; `api` обращается к Redis по имени `redis`; `depends_on` с `condition: service_healthy` — `api` стартует, когда Redis ответил на `redis-cli ping`; у образа `api` есть `HEALTHCHECK` на `/health` (проверяет и связь с Redis).

## Запуск

```bash
cp .env.example .env          # Windows: copy .env.example .env
docker compose up --build -d
docker compose ps             # у обоих сервисов статус healthy
```

Остановить: `docker compose down` (данные Redis остаются в томе; полностью очистить: `docker compose down -v`).

## Проверка (curl)

```bash
# 0. Состояние (проверяет и связь с Redis)
curl -s http://localhost:8000/health
# {"status":"ok"}

# 1. Старт аренды
curl -s -X POST http://localhost:8000/rentals \
  -H "Content-Type: application/json" \
  -d '{"scooter_id":"S-1","user_id":"u1"}'
# 201 {"scooter_id":"S-1","started_at":1731830000,"user_id":"u1"}

# 2. Тот же самокат второй раз — отказ
curl -s -i -X POST http://localhost:8000/rentals \
  -H "Content-Type: application/json" \
  -d '{"scooter_id":"S-1","user_id":"u2"}'
# HTTP 409 {"error":"самокат S-1 уже арендован"}

# 3. Список активных аренд
curl -s http://localhost:8000/rentals/active
# {"count":1,"rentals":[{"scooter_id":"S-1", ...}]}

# 4. Завершение аренды
curl -s -X POST http://localhost:8000/rentals/S-1/stop
# {"duration_seconds":42,"finished_at":...,"scooter_id":"S-1","started_at":...,"user_id":"u1"}

# 5. Список снова пуст
curl -s http://localhost:8000/rentals/active
# {"count":0,"rentals":[]}
```

Проверка «данные в Redis, а не в памяти приложения»:

```bash
curl -s -X POST http://localhost:8000/rentals -H "Content-Type: application/json" \
  -d '{"scooter_id":"S-7","user_id":"u7"}'
docker compose restart api
curl -s http://localhost:8000/rentals/active          # S-7 по-прежнему в списке
docker compose exec redis redis-cli HGETALL rentals:active
```

## API

| Метод и путь | Что делает | Коды |
|--------------|-----------|------|
| `GET /health` | проверка API и Redis | 200 / 503 |
| `POST /rentals` | старт аренды: `{scooter_id, user_id}` | 201 / 400 / 409 |
| `POST /rentals/{scooter_id}/stop` | завершение, возвращает `duration_seconds` | 200 / 404 |
| `GET /rentals/active` | активные аренды, по времени старта | 200 |

Старт использует `HSETNX` — атомарную операцию Redis: два одновременных запроса на один самокат не создадут две аренды.

## Тесты без Docker

```bash
pip install -r requirements-dev.txt
pytest
```

Используется `fakeredis` (подмена Redis в памяти) и управляемые часы; ожидаемо `8 passed`.

## Как проверялось

- `pytest` — 8 тестов API проходят;
- `docker compose config -q` — конфигурация Compose валидна.
- **Не проверено:** фактическая сборка образа и запуск контейнеров — на машине, где готовилась работа, был недоступен демон Docker (Docker Desktop не запущен). Перед сдачей выполните блок «Запуск» и «Проверка» выше.
