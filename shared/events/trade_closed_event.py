"""
Trade Closed Event.
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class TradeClosedEvent:
    """Trade closed."""

    trade_id: str
    pnl: Decimal
