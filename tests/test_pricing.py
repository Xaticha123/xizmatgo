"""Тесты «чёрного ящика» PriceCalculator: классы эквивалентности и граничные значения."""
import pytest
from xizmatgo.pricing import calculate, PriceError, PriceRange

BASE = 80_000


@pytest.mark.parametrize("tc, qty, hour, urgent, expected", [
    ("TC-P01", 1, 8, False, PriceRange(95_000, 143_000)),     # нижняя граница объёма и часа
    ("TC-P02", 2, 12, False, PriceRange(175_000, 263_000)),   # типичное значение
    ("TC-P03", 4, 20, False, PriceRange(335_000, 503_000)),   # перед порогом скидки, верхняя граница часа
    ("TC-P04", 5, 12, False, PriceRange(375_000, 563_000)),   # порог скидки 10 %
    ("TC-P05", 10, 12, False, PriceRange(735_000, 1_103_000)),  # верхняя граница объёма
    ("TC-P06", 1, 12, True, PriceRange(119_000, 179_000)),    # срочно +30 %
    ("TC-P07", 5, 12, True, PriceRange(483_000, 725_000)),    # скидка и срочность вместе
])
def test_valid_classes(tc, qty, hour, urgent, expected):
    assert calculate(BASE, qty, hour, urgent) == expected


@pytest.mark.parametrize("tc, base, qty, hour", [
    ("TC-P08", BASE, 0, 12),      # объём ниже минимума
    ("TC-P09", BASE, 11, 12),     # объём выше максимума
    ("TC-P10", BASE, 2.5, 12),    # объём не целый
    ("TC-P11", BASE, 1, 7),       # час до 08:00
    ("TC-P12", BASE, 1, 21),      # час с 21:00
    ("TC-P13", 0, 1, 12),         # базовая цена не положительная
])
def test_invalid_classes(tc, base, qty, hour):
    with pytest.raises(PriceError):
        calculate(base, qty, hour, False)
