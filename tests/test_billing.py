import pytest

from billing import calculate_cost


def test_zero_minutes_costs_only_start_fee():
    assert calculate_cost(0) == 50


def test_exact_minutes():
    assert calculate_cost(10 * 60) == 50 + 10 * 8


def test_partial_minute_rounds_up():
    # 17 мин 10 с -> оплачиваем 18 минут
    assert calculate_cost(17 * 60 + 10) == 50 + 18 * 8


def test_one_second_is_billed_as_full_minute():
    assert calculate_cost(1) == 58


def test_just_over_a_minute():
    assert calculate_cost(61) == 50 + 2 * 8


def test_long_trip_six_hours():
    assert calculate_cost(6 * 3600) == 50 + 360 * 8


def test_negative_duration_is_rejected():
    with pytest.raises(ValueError):
        calculate_cost(-1)
