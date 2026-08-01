"""
Trade journal entry.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class TradeJournalEntry:
    """Represents one completed trade."""

    timestamp: datetime
    symbol: str
    side: str
    quantity: int
    entry_price: float
    exit_price: float
    pnl: float
    strategy: str
    status: str
