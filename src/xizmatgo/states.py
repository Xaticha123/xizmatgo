"""Компонент OrderStateMachine (SS-3): допустимые переходы статусов заказа."""
from enum import Enum


class OrderStatus(str, Enum):
    NEW = "NEW"; ACCEPTED = "ACCEPTED"; ON_THE_WAY = "ON_THE_WAY"
    IN_PROGRESS = "IN_PROGRESS"; COMPLETED = "COMPLETED"; PAID = "PAID"; CANCELLED = "CANCELLED"


S = OrderStatus
TRANSITIONS = {   # (из, в): роли, которым разрешён переход
    (S.NEW, S.ACCEPTED): {"master"},
    (S.ACCEPTED, S.ON_THE_WAY): {"master"},
    (S.ON_THE_WAY, S.IN_PROGRESS): {"master"},
    (S.IN_PROGRESS, S.COMPLETED): {"master"},
    (S.COMPLETED, S.PAID): {"system"},
    (S.NEW, S.CANCELLED): {"client", "moderator"},
    (S.ACCEPTED, S.CANCELLED): {"client", "master", "moderator"},
    (S.ON_THE_WAY, S.CANCELLED): {"client", "moderator"},
}


def can_change(old: OrderStatus, new: OrderStatus, role: str) -> bool:
    return role in TRANSITIONS.get((old, new), set())
