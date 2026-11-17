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
