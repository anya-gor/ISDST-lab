import json

import pytest
from pytest_bdd import given, parsers, scenarios, then

from main import in_bounds, only_positive, unique_sorted

scenarios("../features/number_filters.feature")


def _numbers(text: str) -> list[float]:
    """Разбирает '[1, 2.5, -3]' в список чисел."""
    return json.loads(text)


@pytest.fixture
def context():
    return {}


@given(parsers.parse("список чисел {text}"))
def given_numbers(context, text):
    context["nums"] = _numbers(text)


@then(parsers.parse("only_positive возвращает {expected}"))
def then_only_positive(context, expected):
    assert only_positive(context["nums"]) == _numbers(expected)


@then(parsers.parse("in_bounds от {low:g} до {high:g} возвращает {expected}"))
def then_in_bounds(context, low, high, expected):
    assert in_bounds(context["nums"], low, high) == _numbers(expected)


@then(parsers.parse("unique_sorted возвращает {expected}"))
def then_unique_sorted(context, expected):
    assert unique_sorted(context["nums"]) == _numbers(expected)
