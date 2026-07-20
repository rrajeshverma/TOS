from dataclasses import dataclass


@dataclass
class PerformanceWidget:
    win_rate: float = 0.0
    total_trades: int = 0
    average_profit: float = 0.0
    average_loss: float = 0.0
