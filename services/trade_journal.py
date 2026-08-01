"""
Trade journal.
"""

from __future__ import annotations

import csv
from pathlib import Path

from domain.trade_journal_entry import TradeJournalEntry


class TradeJournal:
    """Writes completed trades to a CSV journal."""

    def __init__(
        self,
        filename: str = "trade_journal.csv",
    ) -> None:
        self._path = Path(filename)

        if not self._path.exists():
            with self._path.open(
                "w",
                newline="",
            ) as file:
                writer = csv.writer(file)

                writer.writerow(
                    [
                        "timestamp",
                        "symbol",
                        "side",
                        "quantity",
                        "entry_price",
                        "exit_price",
                        "pnl",
                        "strategy",
                        "status",
                    ]
                )

    def record(
        self,
        entry: TradeJournalEntry,
    ) -> None:
        with self._path.open(
            "a",
            newline="",
        ) as file:
            writer = csv.writer(file)

            writer.writerow(
                [
                    entry.timestamp.isoformat(),
                    entry.symbol,
                    entry.side,
                    entry.quantity,
                    entry.entry_price,
                    entry.exit_price,
                    entry.pnl,
                    entry.strategy,
                    entry.status,
                ]
            )
