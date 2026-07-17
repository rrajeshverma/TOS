from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class OptimizationResult:
    parameters: dict[str, Any]

    trades: int = 0
    wins: int = 0
    losses: int = 0

    net_profit: float = 0.0
    max_drawdown: float = 0.0
    profit_factor: float = 0.0
    expectancy: float = 0.0
    sharpe_ratio: float = 0.0
    sortino_ratio: float = 0.0
    calmar_ratio: float = 0.0

    @property
    def win_rate(self) -> float:
        if self.trades == 0:
            return 0.0
        return (self.wins / self.trades) * 100

    @property
    def is_profitable(self) -> bool:
        return self.net_profit > 0

    @property
    def score(self) -> float:
        """
        Simple composite score.
        This can be refined later by StrategyRanker.
        """
        return (
            self.net_profit
            + (self.profit_factor * 100)
            + (self.sharpe_ratio * 100)
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)