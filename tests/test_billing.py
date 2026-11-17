import math
from decimal import Decimal

import pytest

from billing import DEFAULT_TARIFF, Tariff, billable_minutes, calculate_cost, tariff_from_env


# ---------- основные сценарии из постановки ----------

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


# ---------- округление: границы ----------

@pytest.mark.parametrize(
    "seconds,minutes",
    [(0, 0), (1, 1), (59, 1), (60, 1), (61, 2), (119, 2), (120, 2), (121, 3)],
)
def test_billable_minutes_boundaries(seconds, minutes):
    assert billable_minutes(seconds) == minutes


def test_fractional_seconds_are_supported():
    assert billable_minutes(60.0) == 1
    assert billable_minutes(60.5) == 2


# ---------- результат: деньги ----------

def test_cost_is_decimal_with_two_places():
    cost = calculate_cost(60)
    assert isinstance(cost, Decimal)
    assert str(cost) == "58.00"


# ---------- тариф ----------

def test_default_tariff_values():
    assert DEFAULT_TARIFF.start_fee == 50
    assert DEFAULT_TARIFF.per_minute == 8


def test_custom_tariff_with_kopecks():
    tariff = Tariff(start_fee=Decimal("30"), per_minute=Decimal("7.5"))
    assert calculate_cost(3 * 60, tariff) == Decimal("52.50")


def test_negative_tariff_is_rejected():
    with pytest.raises(ValueError):
        Tariff(start_fee=Decimal("-1"))
    with pytest.raises(ValueError):
        Tariff(per_minute=Decimal("-0.5"))


def test_tariff_from_env_uses_defaults_when_empty():
    assert tariff_from_env({}) == DEFAULT_TARIFF


def test_tariff_from_env_reads_values():
    tariff = tariff_from_env({"START_FEE": "20", "PER_MINUTE": "6.5"})
    assert tariff == Tariff(Decimal("20"), Decimal("6.5"))


# ---------- некорректный ввод ----------

@pytest.mark.parametrize("bad", [-1, -0.001, math.nan, math.inf, -math.inf])
def test_invalid_numeric_duration_is_rejected(bad):
    with pytest.raises(ValueError):
        calculate_cost(bad)


@pytest.mark.parametrize("bad", ["60", None, True, [60]])
def test_non_numeric_duration_is_rejected(bad):
    with pytest.raises(TypeError):
        calculate_cost(bad)
