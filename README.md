# Задача 7: Учебное расписание дня

**Студент:** Гордеенко А.В.

Постановка: написать тесты и измерить покрытие для модуля `main.py` ниже.

```python
# main.py
from typing import Dict, List, Optional


def add_lesson(schedule: List[dict], subject: str, start: str, room: str) -> None:
    schedule.append({"subject": subject, "start": start, "room": room})


def remove_by_subject(schedule: List[dict], subject: str) -> bool:
    for i, lesson in enumerate(schedule):
        if lesson["subject"] == subject:
            schedule.pop(i)
            return True
    return False


def find_at_time(schedule: List[dict], start: str) -> Optional[dict]:
    for lesson in schedule:
        if lesson["start"] == start:
            return lesson
    return None


def sorted_by_time(schedule: List[dict]) -> List[dict]:
    return sorted(schedule, key=lambda x: x["start"])


def rooms_used(schedule: List[dict]) -> List[str]:
    return sorted({lesson["room"] for lesson in schedule})
```

`main.py` в репозитории такой же, как в задании, поведение функций не менялось.

## Что в репозитории

- `main.py` - модуль из задания
- `tests/test_main.py` - тесты (22 штуки, pytest)
- `pytest.ini` - чтобы pytest находил `main.py`
- `requirements.txt` - pytest и pytest-cov

## Как запустить тесты

```bash
pip install -r requirements.txt
pytest
```

## Как получить отчёт о покрытии

```bash
pytest --cov=main --cov-report=term-missing
```

HTML-отчёт: `pytest --cov=main --cov-report=html`, потом открыть `htmlcov/index.html`.

Результат запуска:

```
Name      Stmts   Miss  Cover   Missing
---------------------------------------
main.py      18      0   100%
---------------------------------------
22 passed
```

## Что проверяют тесты

- `add_lesson`: добавление в пустой список, функция ничего не возвращает и меняет сам список, порядок добавления сохраняется, можно добавить одинаковые занятия.
- `remove_by_subject`: удаление есть/нет (True/False), пустое расписание, если предмет встречается два раза, удаляется только первый, регистр букв важен.
- `find_at_time`: нашли / не нашли, пустой список, если два занятия в одно время - возвращается первое.
- `sorted_by_time`: сортировка, исходный список не меняется, пустой список, при одинаковом времени порядок не меняется.
- `rooms_used`: аудитории без повторов и по порядку, пустой список, одна аудитория на несколько пар.

Интересный момент: время и аудитории сравниваются как строки. Поэтому `"9:00"` оказывается позже `"10:00"`, а аудитория `"10"` идёт раньше `"9"`. Менять код по заданию нельзя, поэтому есть два теста, которые просто фиксируют это поведение (`test_sorted_by_time_is_lexicographic` и `test_rooms_used_sorts_as_strings`). Если писать время с нулём (`09:00`), сортировка работает правильно.
