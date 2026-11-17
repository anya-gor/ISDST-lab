"""Биллинг поездки на самокате: плата за старт + оплата за минуты.

Минуты округляются вверх: любая начатая минута оплачивается полностью.
Деньги считаются в Decimal, чтобы не накапливать ошибки float.
"""

import math
import os
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from typing import Mapping, Union

SECONDS_IN_MINUTE = 60
CENT = Decimal("0.01")

Number = Union[int, float]


@dataclass(frozen=True)
class Tariff:
    """Тариф: плата за старт и цена за минуту (в рублях)."""

    start_fee: Decimal = Decimal("50")
    per_minute: Decimal = Decimal("8")

    def __post_init__(self) -> None:
        if self.start_fee < 0 or self.per_minute < 0:
            raise ValueError("Тариф не может содержать отрицательные значения")


DEFAULT_TARIFF = Tariff()


def tariff_from_env(env: Mapping[str, str] = os.environ) -> Tariff:
    """Читает START_FEE и PER_MINUTE из окружения; не заданные берёт по умолчанию."""
    return Tariff(
        start_fee=Decimal(env.get("START_FEE", DEFAULT_TARIFF.start_fee)),
        per_minute=Decimal(env.get("PER_MINUTE", DEFAULT_TARIFF.per_minute)),
    )


def billable_minutes(duration_seconds: Number) -> int:
    """Количество оплачиваемых минут (округление вверх)."""
    if isinstance(duration_seconds, bool) or not isinstance(duration_seconds, (int, float)):
        raise TypeError("duration_seconds должен быть числом (int или float)")
    if not math.isfinite(duration_seconds) or duration_seconds < 0:
        raise ValueError("duration_seconds должен быть конечным числом >= 0")
    # Fraction вместо float-деления: нет ошибок вида 3.0000000000000004
    return math.ceil(Fraction(duration_seconds) / SECONDS_IN_MINUTE)


def calculate_cost(duration_seconds: Number, tariff: Tariff = DEFAULT_TARIFF) -> Decimal:
    """Стоимость поездки: старт + оплачиваемые минуты × цена минуты."""
    minutes = billable_minutes(duration_seconds)
    return (tariff.start_fee + minutes * tariff.per_minute).quantize(CENT)
