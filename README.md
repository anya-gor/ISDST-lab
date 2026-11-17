# Задача 7: Аренда самокатов (учёт поездок)

**Студент:** Гордеенко А.В.

Постановка:

> API поездок + Redis (активные аренды). Compose: `api` и `redis`. Старт/стоп аренды, список активных. Явная проверка через `curl` в README.

## Что сделано

Небольшое API на Flask, которое запускает и завершает аренду самоката и показывает активные аренды. Активные аренды хранятся в Redis.

Файлы:

- `app/main.py` - код API
- `app/requirements.txt` - зависимости для контейнера (flask, redis, gunicorn)
- `Dockerfile` - сборка образа API
- `compose.yaml` - запуск двух сервисов: `api` и `redis`
- `.env.example` - пример переменных окружения
- `tests/test_api.py` - тесты API (запускаются без Docker, вместо Redis fakeredis)

Сервисы в compose:

- `api` - собирается из `Dockerfile` на основе `python:3.12-slim`, запускается через gunicorn на порту 8000 и не от root. В образе есть `HEALTHCHECK`, он дёргает `/health`.
- `redis` - официальный образ `redis:7-alpine`. Данные лежат в томе `redis-data`, включён AOF, поэтому аренды не пропадают после перезапуска.

Оба сервиса в одной сети `backend`. API подключается к Redis по имени `redis`. В `depends_on` стоит `condition: service_healthy`, то есть API стартует только после того, как Redis ответил на `redis-cli ping`.

## Запуск

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
```

В `docker compose ps` у обоих контейнеров должен быть статус `healthy`.

Остановить: `docker compose down`. Если нужно удалить и данные Redis: `docker compose down -v`.

## Проверка

```bash
# проверка, что API работает и видит Redis
curl -s http://localhost:8000/health
# {"status":"ok"}

# начать аренду
curl -s -X POST http://localhost:8000/rentals -H "Content-Type: application/json" -d '{"scooter_id":"S-1","user_id":"u1"}'
# {"scooter_id":"S-1","started_at":1794916093,"user_id":"u1"}

# попробовать взять тот же самокат ещё раз - будет 409
curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8000/rentals -H "Content-Type: application/json" -d '{"scooter_id":"S-1","user_id":"u2"}'
# 409

# список активных аренд
curl -s http://localhost:8000/rentals/active
# {"count":1,"rentals":[{"scooter_id":"S-1","started_at":1794916093,"user_id":"u1"}]}

# перезапустить API - аренда остаётся, потому что она в Redis
docker compose restart api
curl -s http://localhost:8000/rentals/active
# {"count":1,"rentals":[...]}

# завершить аренду
curl -s -X POST http://localhost:8000/rentals/S-1/stop
# {"duration_seconds":8,"finished_at":1794916101,"scooter_id":"S-1","started_at":1794916093,"user_id":"u1"}

# теперь активных нет
curl -s http://localhost:8000/rentals/active
# {"count":0,"rentals":[]}
```

Выводы в комментариях взяты из настоящего запуска. Посмотреть данные прямо в Redis можно так:

```bash
docker compose exec redis redis-cli HGETALL rentals:active
```

## Методы API

| Метод | Что делает | Ответы |
|-------|-----------|--------|
| `GET /health` | проверка API и связи с Redis | 200, 503 если Redis недоступен |
| `POST /rentals` | начать аренду, в теле `scooter_id` и `user_id` | 201, 400 если нет полей, 409 если самокат занят |
| `POST /rentals/{scooter_id}/stop` | завершить аренду, возвращает длительность | 200, 404 если аренды нет |
| `GET /rentals/active` | список активных аренд | 200 |

Аренды хранятся в hash `rentals:active` (ключ - id самоката). Для старта используется команда `HSETNX`: она записывает значение, только если такого ключа ещё нет. Поэтому даже если два запроса придут одновременно, один самокат не сдадут двум людям.

## Тесты без Docker

```bash
pip install -r requirements-dev.txt
pytest
```

8 тестов, все проходят.
