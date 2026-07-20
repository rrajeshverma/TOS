from dataclasses import dataclass, field


@dataclass
class PerformanceModel:
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0

    gross_profit: float = 0.0
    gross_loss: float = 0.0
    net_profit: float = 0.0

    win_rate: float = 0.0
    profit_factor: float = 0.0

    average_win: float = 0.0
    average_loss: float = 0.0

    largest_win: float = 0.0
    largest_loss: float = 0.0

    expectancy: float = 0.0
    equity_curve: list[float] = field(default_factory=list)

    max_drawdown: float = 0.0
    max_drawdown_percent: float = 0.0

    peak_equity: float = 0.0

    recovery_factor: float = 0.0

    max_consecutive_wins: int = 0
    max_consecutive_losses: int = 0
