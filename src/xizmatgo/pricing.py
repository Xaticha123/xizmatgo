"""Компонент PriceCalculator (SS-3): расчёт предварительной стоимости, FR-04."""
from dataclasses import dataclass
import math

VISIT_FEE = 15_000          # выезд мастера, сум
URGENT_RATE = 0.30          # надбавка за срочность к стоимости работ
BULK_DISCOUNT = 0.10        # скидка на работы при объёме от 5 единиц
BULK_FROM = 5
QTY_MIN, QTY_MAX = 1, 10
HOUR_FROM, HOUR_TO = 8, 21  # начало визита: 08:00 … 20:59


class PriceError(ValueError):
    pass


@dataclass(frozen=True)
class PriceRange:
    min: int
    max: int


def calculate(base_price: int, quantity: int, hour: int, urgent: bool) -> PriceRange:
    if not isinstance(quantity, int) or isinstance(quantity, bool):
        raise PriceError("Объём должен быть целым числом")
    if quantity < QTY_MIN or quantity > QTY_MAX:
        raise PriceError(f"Объём должен быть от {QTY_MIN} до {QTY_MAX}")
    if not (HOUR_FROM <= hour < HOUR_TO):
        raise PriceError("Мастер приезжает с 08:00 до 21:00")
    if base_price <= 0:
        raise PriceError("Базовая цена должна быть больше нуля")
    work = base_price * quantity
    if quantity >= BULK_FROM:                     # скидка за объём (исправлено, DEF-01)
        work = work * (1 - BULK_DISCOUNT)
    if urgent:
        work = work * (1 + URGENT_RATE)
    total = round(work) + VISIT_FEE
    upper = math.ceil(total * 1.5 / 1000) * 1000  # верхняя граница диапазона, кратно 1000
    return PriceRange(total, upper)
