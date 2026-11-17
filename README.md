# Задача 7: Мини-сервис коротких ссылок (in-memory)

**Студент:** Гордеенко А.В.

> API или модуль: создать короткую ссылку, получить исходный URL. Тесты основных сценариев. CI; CD — mock-deploy скрипт, пишущий «версию» в `deployed/VERSION`.

Полная постановка — в ветке `main`, файл `tasks/lab-6.md`.

[![CI/CD](../../actions/workflows/ci.yml/badge.svg)](../../actions/workflows/ci.yml)
<!-- После публикации на GitHub замените ссылку на: https://github.com/<user>/<repo>/actions/workflows/ci.yml -->

## Структура проекта

```
shortener/service.py     # класс UrlShortener (хранилище в памяти)
shortener/__init__.py
tests/test_shortener.py  # тесты сервиса (в т. ч. параметризованные)
tests/test_deploy.py     # тесты mock-деплоя
scripts/deploy.py        # CD: пишет deployed/VERSION
VERSION                  # базовая версия (0.1.0)
.github/workflows/ci.yml # пайплайн GitHub Actions
```

## Сервис

```python
from shortener import UrlShortener

s = UrlShortener(base_url="http://sho.rt/")
code = s.create("https://example.com/page")   # 'g8'
s.short_url("https://example.com/page")       # 'http://sho.rt/g8'
s.resolve(code)                               # 'https://example.com/page'
```

- код — число-счётчик в base62 (детерминированно, без коллизий); один URL → один код;
- принимаются только `http`/`https` ссылки с хостом (иначе `InvalidUrlError`);
- неизвестный код → `UnknownCodeError`.

## Как запустить тесты локально

```bash
python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
pytest --cov=shortener --cov-report=term-missing --cov-fail-under=90
```

Ожидаемо: `21 passed`, покрытие `shortener` — 100 %.

## Как устроен CI/CD

Файл `.github/workflows/ci.yml`, два задания:

| Стадия | Когда | Что делает |
|--------|-------|-----------|
| **test** | каждый `push` и Pull Request, на Python 3.11 и 3.12 | ставит зависимости, запускает `pytest --cov-fail-under=90`. Любой упавший тест или покрытие < 90 % → задание **красное**, пайплайн останавливается |
| **deploy** | **только `push` в ветку `main`** и только если `test` успешен (`needs: test`) | запускает `python scripts/deploy.py`: копирует пакет `shortener/` в `deployed/`, пишет `deployed/VERSION` вида `0.1.0+<короткий SHA>`, показывает файл в логе и сохраняет `deployed/` как **artifact** |

Деплой — упрощённый (mock): никаких серверов и секретов. «Успешный деплой» = задание `deploy` зелёное, в логе строка `[deploy] готово`, в artifact `deployed` лежит файл `VERSION`.

Проверка деплоя локально:

```bash
python scripts/deploy.py
cat deployed/VERSION      # 0.1.0
```

(в CI версия содержит SHA коммита из переменной `GITHUB_SHA`; каталог `deployed/` в git не хранится).

## Как проверить статус CI

1. Опубликуйте репозиторий на GitHub (`git remote add origin <URL>`, `git push -u origin --all`).
2. Вкладка **Actions** → workflow «CI/CD» → последний запуск; зелёная галочка — тесты прошли; у запуска на `main` дополнительно виден artifact `deployed`.
3. Badge в начале README показывает статус последнего прогона (замените путь на `https://github.com/<user>/<repo>/...`).
4. Чтобы убедиться, что пайплайн «краснеет»: сломайте любой assert, сделайте push — задание `test` упадёт, `deploy` не запустится.

> Примечание: локально пайплайн в GitHub Actions не запускался (репозиторий пока не опубликован); логика тестов и деплоя проверена запуском `pytest` и `scripts/deploy.py`, а YAML — загрузкой парсером.
> Ветка `lab-6` — рабочая ветка учебного репозитория: деплой-задание срабатывает на `main` того репозитория, куда публикуется проект.
