# Задача 7: Мини-сервис коротких ссылок (in-memory)

**Студент:** Гордеенко А.В.

Постановка:

> API или модуль: создать короткую ссылку, получить исходный URL. Тесты основных сценариев. CI; CD — mock-deploy скрипт, пишущий «версию» в `deployed/VERSION`.

[![CI/CD](https://github.com/anya-gor/ISDST-lab/actions/workflows/ci.yml/badge.svg?branch=lab-6)](https://github.com/anya-gor/ISDST-lab/actions/workflows/ci.yml)

## Структура проекта

- `shortener/service.py` - сам сервис, класс `UrlShortener`, ссылки хранятся в словаре в памяти
- `tests/test_shortener.py` - тесты сервиса
- `tests/test_deploy.py` - тесты скрипта деплоя
- `scripts/deploy.py` - mock-деплой, пишет версию в `deployed/VERSION`
- `VERSION` - номер версии (0.1.0)
- `.github/workflows/ci.yml` - пайплайн для GitHub Actions

## Как работает сервис

```python
from shortener import UrlShortener

s = UrlShortener()
code = s.create("https://example.com/page")   # 'g8'
s.short_url("https://example.com/page")       # 'http://sho.rt/g8'
s.resolve(code)                               # 'https://example.com/page'
```

- Код ссылки - это номер по счётчику, записанный в base62 (цифры и латинские буквы). Так коды короткие и не повторяются.
- Если одну и ту же ссылку сократить два раза, код будет одинаковый.
- Принимаются только ссылки `http://` и `https://`, иначе ошибка `InvalidUrlError`.
- Если такого кода нет, `resolve` выдаёт `UnknownCodeError`.

## Как запустить тесты локально

```bash
pip install -r requirements.txt
pytest --cov=shortener --cov-report=term-missing --cov-fail-under=90
```

Должно быть `21 passed`, покрытие 100%.

## Как устроен CI/CD

В пайплайне два задания.

**test** запускается на каждый push и pull request. Ставит зависимости и гоняет pytest на Python 3.11 и 3.12. Если хоть один тест упал или покрытие меньше 90%, задание красное и дальше ничего не идёт.

**deploy** запускается только если test прошёл, и только при push в `main` или при push тега вида `v*` (например `v0.1.0`). На других ветках деплоя нет. Что делает:

1. запускает `python scripts/deploy.py`;
2. скрипт копирует пакет `shortener` в папку `deployed/` и пишет в `deployed/VERSION` версию вида `0.1.0+abc1234` (номер из файла `VERSION` и начало хеша коммита);
3. выводит `deployed/VERSION` в лог;
4. сохраняет папку `deployed/` как артефакт.

Это не настоящий деплой на сервер, а имитация, как и сказано в задании. Деплой считается успешным, если задание deploy зелёное, в логе есть `[deploy] готово`, а в артефакте `deployed` лежит файл `VERSION`.

Так как в этом репозитории каждая лаба лежит в своей ветке, а в `main` только описания заданий, деплой этой работы запускается через тег:

```bash
git tag v0.1.0
git push origin v0.1.0
```

Проверить деплой локально:

```bash
python scripts/deploy.py
cat deployed/VERSION
```

## Как проверить статус CI

- На GitHub открыть вкладку Actions, workflow "CI/CD": https://github.com/anya-gor/ISDST-lab/actions
- Там видно запуски для ветки `lab-6` (только тесты) и для тега `v0.1.0` (тесты + деплой, у него есть артефакт `deployed`).
- Бейдж в начале README показывает статус последнего запуска на ветке `lab-6`.
- Чтобы проверить, что пайплайн правда падает, можно сломать любой тест и сделать push - задание test станет красным.
