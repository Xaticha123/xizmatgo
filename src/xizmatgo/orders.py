"""Компонент OrderService (SS-3): принятие заказа мастером, UC-08 / FR-08."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Protocol
from .states import OrderStatus


class OrderNotFound(Exception): ...
class OrderAlreadyTaken(Exception): ...
class MasterNotVerified(Exception): ...
class SlotBusy(Exception): ...
class OrderNotRepeatable(Exception): ...


@dataclass
class Order:
    id: str
    scheduled_at: datetime
    status: OrderStatus = OrderStatus.NEW
    master_id: Optional[str] = None


class IOrderRepository(Protocol):
    def find_by_id(self, order_id: str) -> Optional[Order]: ...
    def save(self, order: Order) -> None: ...


class OrderService:
    def __init__(self, repo, masters, schedule, bus):
        self.repo, self.masters, self.schedule, self.bus = repo, masters, schedule, bus

    def accept_order(self, order_id: str, master_id: str) -> Order:
        order = self.repo.find_by_id(order_id)                      # 1
        if order is None:                                           # 2
            raise OrderNotFound(order_id)                           # 3
        if order.status != OrderStatus.NEW:                         # 4
            raise OrderAlreadyTaken(order_id)                       # 5
        if not self.masters.is_verified(master_id):                 # 6
            raise MasterNotVerified(master_id)                      # 7
        if self.schedule.is_busy(master_id, order.scheduled_at):    # 8
            raise SlotBusy(master_id)                               # 9
        order.master_id = master_id                                 # 10
        order.status = OrderStatus.ACCEPTED
        self.schedule.reserve(master_id, order.scheduled_at)
        self.repo.save(order)
        self.bus.publish({"type": "OrderAccepted", "order_id": order.id, "master_id": master_id})
        return order                                                # 11

    def repeat_order(self, order_id: str, client_id: str, new_time: datetime, new_id: str) -> Order:
        """US-15: создать новый заказ по завершённому заказу клиента на новое время."""
        old = self.repo.find_by_id(order_id)
        if old is None or getattr(old, "client_id", client_id) != client_id:
            raise OrderNotFound(order_id)
        if old.status not in (OrderStatus.COMPLETED, OrderStatus.PAID):
            raise OrderNotRepeatable(order_id)
        new = Order(new_id, new_time)
        self.repo.save(new)
        self.bus.publish({"type": "OrderCreated", "order_id": new_id, "repeat_of": order_id})
        return new
