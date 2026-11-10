"""Тесты US-15 «Повтор заказа»."""
from datetime import datetime
import pytest
from xizmatgo.orders import OrderService, Order, OrderNotFound, OrderNotRepeatable
from xizmatgo.states import OrderStatus
from conftest import FakeOrderRepository, StubMasterDirectory, StubSchedule

T1, T2 = datetime(2026, 11, 12, 15), datetime(2026, 12, 1, 10)


def svc(bus, orders):
    return OrderService(FakeOrderRepository(orders), StubMasterDirectory(), StubSchedule(), bus)


def test_repeat_completed_order(bus):
    s = svc(bus, [Order("O1", T1, OrderStatus.PAID, "M1")])
    new = s.repeat_order("O1", "C1", T2, "O2")
    assert new.status == OrderStatus.NEW and new.scheduled_at == T2
    assert bus.events[-1] == {"type": "OrderCreated", "order_id": "O2", "repeat_of": "O1"}


def test_repeat_unfinished_order_rejected(bus):
    s = svc(bus, [Order("O1", T1, OrderStatus.ACCEPTED, "M1")])
    with pytest.raises(OrderNotRepeatable):
        s.repeat_order("O1", "C1", T2, "O2")


def test_repeat_missing_order(bus):
    with pytest.raises(OrderNotFound):
        svc(bus, []).repeat_order("X", "C1", T2, "O2")
