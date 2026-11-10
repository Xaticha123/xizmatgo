from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Master:                      # участник паттерна: данные контекста
    name: str
    rating: float                  # 1..5
    distance_km: float
    price: int                     # сум
    free_slots_today: int

class RankingStrategy(ABC):        # Strategy — общий интерфейс алгоритмов подбора
    @abstractmethod
    def score(self, m: Master) -> float: ...

class BalancedRanking(RankingStrategy):      # ConcreteStrategy: обычный заказ
    def score(self, m):
        return 0.5 * m.rating / 5 + 0.3 * (1 - min(m.distance_km, 10) / 10) + 0.2 * min(m.free_slots_today, 4) / 4

class UrgentRanking(RankingStrategy):        # ConcreteStrategy: «Срочно» — важнее близость
    def score(self, m):
        return 0.25 * m.rating / 5 + 0.75 * (1 - min(m.distance_km, 10) / 10)

class BudgetRanking(RankingStrategy):        # ConcreteStrategy: «Дешевле» — важнее цена
    def score(self, m):
        return 0.4 * m.rating / 5 + 0.6 * (1 - m.price / 150_000)

class MatchingService:             # Context — подсистема SS-4 «Умный подбор»
    def __init__(self, strategy: RankingStrategy):
        self._strategy = strategy
    def set_strategy(self, strategy: RankingStrategy):
        self._strategy = strategy  # стратегию можно сменить во время работы
    def rank(self, masters, top=3):
        verified = [m for m in masters if m.rating >= 4.0]   # общее правило для всех стратегий
        return sorted(verified, key=self._strategy.score, reverse=True)[:top]

def choose_strategy(urgent: bool, budget: bool) -> RankingStrategy:
    if urgent:
        return UrgentRanking()
    return BudgetRanking() if budget else BalancedRanking()

if __name__ == "__main__":
    masters = [
        Master("Алишер Т.", 4.9, 1.8, 95_000, 2),
        Master("Бахром Р.", 4.8, 3.2, 90_000, 4),
        Master("Сардор К.", 4.7, 0.6, 110_000, 1),
        Master("Жасур М.", 4.5, 5.5, 70_000, 3),
        Master("Отабек Н.", 3.6, 0.9, 60_000, 4),   # рейтинг < 4 — не попадёт в выдачу
    ]
    service = MatchingService(BalancedRanking())
    for title, urgent, budget in [("Обычный заказ", False, False), ("Срочно (+30 %)", True, False), ("Подешевле", False, True)]:
        service.set_strategy(choose_strategy(urgent, budget))
        print(f"{title} — {type(service._strategy).__name__}:")
        for i, m in enumerate(service.rank(masters), 1):
            print(f"  {i}. {m.name:<10} ★{m.rating}  {m.distance_km} км  {m.price:,} сум  score={service._strategy.score(m):.3f}".replace(",", " "))
