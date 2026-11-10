"""Заглушки (stubs) и шпионы (spies) зависимостей OrderService."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import pytest


class FakeOrderRepository:               # заглушка IOrderRepository (в памяти вместо PostgreSQL)
    def __init__(self, orders=()):
        self.data = {o.id: o for o in orders}
        self.saved = []
    def find_by_id(self, order_id):
        return self.data.get(order_id)
    def save(self, order):
        self.data[order.id] = order
        self.saved.append(order.id)


class StubMasterDirectory:               # заглушка подсистемы SS-1 / SS-6 (статус верификации)
    def __init__(self, verified=()):
        self.verified = set(verified)
    def is_verified(self, master_id):
        return master_id in self.verified


class StubSchedule:                      # заглушка графика мастера (СлотГрафика)
    def __init__(self, busy=()):
        self.busy = set(busy)
        self.reserved = []
    def is_busy(self, master_id, when):
        return (master_id, when) in self.busy
    def reserve(self, master_id, when):
        self.reserved.append((master_id, when))


class SpyEventBus:                       # шпион IEventBus (INF-4): запоминает события
    def __init__(self):
        self.events = []
    def publish(self, event):
        self.events.append(event)


@pytest.fixture
def bus():
    return SpyEventBus()
