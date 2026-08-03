"""
Backtest configuration.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class BacktestConfig:
    """
    Immutable backtest configuration.
    """

    symbol: str

    timeframe: str

    start_date: datetime

    end_date: datetime

    initial_capital: float = 100000.0

    max_trades_per_day: int = 2

    risk_reward: float = 2.0

    commission: float = 0.0

    slippage: float = 0.0

    def __post_init__(self) -> None:
        if not self.symbol:
            raise ValueError("Symbol cannot be empty.")

        if not self.timeframe:
            raise ValueError("Timeframe cannot be empty.")

        if self.start_date >= self.end_date:
            raise ValueError("Start date must be before end date.")

        if self.initial_capital <= 0:
            raise ValueError("Initial capital must be greater than zero.")

        if self.max_trades_per_day <= 0:
            raise ValueError("Maximum trades per day must be greater than zero.")

        if self.risk_reward <= 0:
            raise ValueError("Risk reward must be greater than zero.")

        if self.commission < 0:
            raise ValueError("Commission cannot be negative.")

        if self.slippage < 0:
            raise ValueError("Slippage cannot be negative.")
