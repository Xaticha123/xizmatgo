"""Тесты «белого ящика» OrderService.accept_order: по одному на каждый базисный путь."""
from datetime import datetime
import pytest
from xizmatgo.orders import (OrderService, Order, OrderNotFound, OrderAlreadyTaken,
                             MasterNotVerified, SlotBusy)
from xizmatgo.states import OrderStatus
from conftest import FakeOrderRepository, StubMasterDirectory, StubSchedule

WHEN = datetime(2026, 11, 12, 15, 0)


def make_service(bus, orders=(), verified=("M1",), busy=()):
    repo = FakeOrderRepository(orders)
    sched = StubSchedule(busy)
    return OrderService(repo, StubMasterDirectory(verified), sched, bus), repo, sched


def test_path1_order_not_found(bus):                       # TC-W01: 1-2-3-11
    svc, repo, _ = make_service(bus)
    with pytest.raises(OrderNotFound):
        svc.accept_order("X404", "M1")
    assert bus.events == [] and repo.saved == []


def test_path2_order_already_taken(bus):                   # TC-W02: 1-2-4-5-11
    svc, repo, _ = make_service(bus, [Order("O1", WHEN, OrderStatus.ACCEPTED, "M2")])
    with pytest.raises(OrderAlreadyTaken):
        svc.accept_order("O1", "M1")
    assert repo.data["O1"].master_id == "M2"


def test_path3_master_not_verified(bus):                   # TC-W03: 1-2-4-6-7-11
    svc, repo, _ = make_service(bus, [Order("O1", WHEN)], verified=())
    with pytest.raises(MasterNotVerified):
        svc.accept_order("O1", "M1")
    assert repo.data["O1"].status == OrderStatus.NEW


def test_path4_slot_busy(bus):                             # TC-W04: 1-2-4-6-8-9-11
    svc, repo, _ = make_service(bus, [Order("O1", WHEN)], busy={("M1", WHEN)})
    with pytest.raises(SlotBusy):
        svc.accept_order("O1", "M1")
    assert repo.saved == []


def test_path5_success(bus):                               # TC-W05: 1-2-4-6-8-10-11
    svc, repo, sched = make_service(bus, [Order("O1", WHEN)])
    order = svc.accept_order("O1", "M1")
    assert order.status == OrderStatus.ACCEPTED and order.master_id == "M1"
    assert repo.saved == ["O1"] and sched.reserved == [("M1", WHEN)]
    assert bus.events == [{"type": "OrderAccepted", "order_id": "O1", "master_id": "M1"}]
