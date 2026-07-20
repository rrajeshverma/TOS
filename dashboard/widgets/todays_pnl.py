from dataclasses import dataclass


@dataclass
class TodaysPnLWidget:
    realized_pnl: float = 0.0
    trade_count: int = 0
