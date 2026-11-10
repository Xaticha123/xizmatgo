"""Тесты OrderStateMachine: допустимые и недопустимые переходы статусов."""
import pytest
from xizmatgo.states import can_change, OrderStatus as S


@pytest.mark.parametrize("tc, old, new, role, ok", [
    ("TC-S01", S.NEW, S.ACCEPTED, "master", True),
    ("TC-S02", S.IN_PROGRESS, S.COMPLETED, "master", True),
    ("TC-S03", S.COMPLETED, S.PAID, "system", True),
    ("TC-S04", S.ON_THE_WAY, S.CANCELLED, "client", True),
    ("TC-S05", S.NEW, S.ACCEPTED, "client", False),      # клиент не может «принять» заказ
    ("TC-S06", S.COMPLETED, S.PAID, "master", False),    # мастер не может отметить оплату сам
    ("TC-S07", S.IN_PROGRESS, S.CANCELLED, "client", False),  # отмена во время работы запрещена
    ("TC-S08", S.PAID, S.NEW, "moderator", False),       # возврат из конечного статуса
])
def test_transitions(tc, old, new, role, ok):
    assert can_change(old, new, role) is ok
