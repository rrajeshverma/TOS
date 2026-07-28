"""
TOS Market Tick Domain Model

Represents a single market price update.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Tick:
    """
    Immutable market tick.
    """

    symbol: str
    price: float
    volume: int
    timestamp: datetime
    exchange: str

    def __post_init__(self) -> None:

        if not self.symbol:
            raise ValueError(
                "Symbol is required"
            )

        if self.price <= 0:
            raise ValueError(
                "Price must be positive"
            )

        if self.volume <= 0:
            raise ValueError(
                "Volume must be positive"
            )

        if not self.exchange:
            raise ValueError(
                "Exchange is required"
            )
