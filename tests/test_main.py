import pytest

from main import (
    add_lesson,
    find_at_time,
    remove_by_subject,
    rooms_used,
    sorted_by_time,
)


@pytest.fixture
def schedule():
    """Расписание из трёх занятий, добавленных не по порядку времени."""
    s = []
    add_lesson(s, "Физика", "11:00", "201")
    add_lesson(s, "Математика", "09:00", "105")
    add_lesson(s, "История", "10:00", "105")
    return s


# ---------- add_lesson ----------

def test_add_lesson_appends_to_empty_schedule():
    s = []
    add_lesson(s, "Математика", "09:00", "105")
    assert s == [{"subject": "Математика", "start": "09:00", "room": "105"}]


def test_add_lesson_returns_none_and_mutates_in_place():
    s = []
    assert add_lesson(s, "Физика", "10:00", "1") is None
    assert len(s) == 1


def test_add_lesson_keeps_insertion_order():
    s = []
    add_lesson(s, "Б", "11:00", "2")
    add_lesson(s, "А", "09:00", "1")
    assert [x["subject"] for x in s] == ["Б", "А"]


def test_add_lesson_allows_duplicates():
    s = []
    add_lesson(s, "Физика", "10:00", "1")
    add_lesson(s, "Физика", "10:00", "1")
    assert len(s) == 2


# ---------- remove_by_subject ----------

def test_remove_existing_subject(schedule):
    assert remove_by_subject(schedule, "История") is True
    assert [x["subject"] for x in schedule] == ["Физика", "Математика"]


def test_remove_missing_subject_returns_false_and_keeps_schedule(schedule):
    assert remove_by_subject(schedule, "Химия") is False
    assert len(schedule) == 3


def test_remove_from_empty_schedule():
    assert remove_by_subject([], "Физика") is False


def test_remove_deletes_only_first_match():
    s = [
        {"subject": "Физика", "start": "09:00", "room": "1"},
        {"subject": "Физика", "start": "12:00", "room": "2"},
    ]
    assert remove_by_subject(s, "Физика") is True
    assert s == [{"subject": "Физика", "start": "12:00", "room": "2"}]


def test_remove_is_case_sensitive(schedule):
    assert remove_by_subject(schedule, "физика") is False


# ---------- find_at_time ----------

def test_find_at_time_found(schedule):
    assert find_at_time(schedule, "09:00")["subject"] == "Математика"


def test_find_at_time_not_found(schedule):
    assert find_at_time(schedule, "15:30") is None


def test_find_at_time_in_empty_schedule():
    assert find_at_time([], "09:00") is None


def test_find_at_time_returns_first_of_equal_starts():
    s = [
        {"subject": "А", "start": "09:00", "room": "1"},
        {"subject": "Б", "start": "09:00", "room": "2"},
    ]
    assert find_at_time(s, "09:00")["subject"] == "А"


# ---------- sorted_by_time ----------

def test_sorted_by_time_orders_lessons(schedule):
    assert [x["start"] for x in sorted_by_time(schedule)] == ["09:00", "10:00", "11:00"]


def test_sorted_by_time_does_not_mutate_input(schedule):
    before = list(schedule)
    sorted_by_time(schedule)
    assert schedule == before


def test_sorted_by_time_empty():
    assert sorted_by_time([]) == []


def test_sorted_by_time_is_stable_for_equal_starts():
    s = [
        {"subject": "А", "start": "09:00", "room": "1"},
        {"subject": "Б", "start": "09:00", "room": "2"},
    ]
    assert [x["subject"] for x in sorted_by_time(s)] == ["А", "Б"]


def test_sorted_by_time_is_lexicographic():
    # Известная особенность: время сравнивается как строка, поэтому
    # без ведущего нуля "9:00" окажется позже "10:00".
    s = [
        {"subject": "А", "start": "9:00", "room": "1"},
        {"subject": "Б", "start": "10:00", "room": "1"},
    ]
    assert [x["subject"] for x in sorted_by_time(s)] == ["Б", "А"]


# ---------- rooms_used ----------

def test_rooms_used_unique_and_sorted(schedule):
    assert rooms_used(schedule) == ["105", "201"]


def test_rooms_used_empty():
    assert rooms_used([]) == []


def test_rooms_used_single_room_many_lessons():
    s = []
    for hour in ("09:00", "10:00", "11:00"):
        add_lesson(s, "X", hour, "A1")
    assert rooms_used(s) == ["A1"]


def test_rooms_used_sorts_as_strings():
    s = []
    add_lesson(s, "X", "09:00", "10")
    add_lesson(s, "Y", "10:00", "9")
    assert rooms_used(s) == ["10", "9"]
