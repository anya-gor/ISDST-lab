# Задача 7: Сервис аренды самокатов

**Студент:** Гордеенко А.В.

> Старт и завершение поездки. User: как начать аренду, тарификация в двух абзацах. Tech: статусы самоката/поездки. OpenAPI: список доступных, старт, финиш, история поездок.

Полная постановка — в ветке `main`, файл `tasks/lab-8.md`.

## Документация

- [Руководство пользователя](docs/user.md) — как начать аренду, тарификация (два абзаца), FAQ и типичные ошибки
- [Техническая документация](docs/tech.md) — архитектура, статусы самоката и поездки, формула стоимости, договорённости по API, конфигурация
- OpenAPI: [`openapi.yaml`](openapi.yaml) (OpenAPI 3.0.3, 6 операций)
- Swagger UI: [`docs/swagger.html`](docs/swagger.html)

## Операции API

| Операция | Метод и путь | Требование постановки |
|----------|--------------|-----------------------|
| `listAvailableScooters` | `GET /scooters` | список доступных |
| `getScooter` | `GET /scooters/{scooterId}` | — |
| `startTrip` | `POST /trips` | старт поездки |
| `finishTrip` | `POST /trips/{tripId}/finish` | завершение поездки |
| `listTrips` | `GET /trips` | история поездок |
| `getTrip` | `GET /trips/{tripId}` | — |

Термины единые во всех документах: самокат (`Scooter`) со статусами `AVAILABLE / IN_USE / CHARGING / MAINTENANCE`, поездка (`Trip`) со статусами `ACTIVE / FINISHED / CANCELED`, тариф **50 ₽ за старт + 8 ₽ за минуту** с округлением минут вверх (пример: 17 мин 10 с → 18 мин → 194 ₽ — совпадает в user.md, tech.md и в примере `Trip` в спецификации).

## Как открыть и проверить спецификацию

```bash
pip install pyyaml openapi-spec-validator
python scripts/validate_openapi.py
```

Ожидаемый вывод: `OpenAPI 3.0.3 валидна, операций: 6`.

Просмотр в Swagger UI:

```bash
python -m http.server 8080
# http://localhost:8080/docs/swagger.html   (нужен доступ в интернет к unpkg.com за скриптами UI)
```

Либо вставьте `openapi.yaml` на <https://editor.swagger.io>.

Реализация API в работе не требуется: это документация + контракт (stub-сервера нет).
