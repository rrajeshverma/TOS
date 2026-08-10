"""
=========================================================
Trading Operating System (TOS)
Module      : Trade Journal
Version     : 1.0.0
Author      : Rajesh Varma
Description : Records completed paper trades.
=========================================================
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import ClassVar

from domain.trade import Trade
from shared.logger import get_logger


class TradeJournal:
    HEADER: ClassVar[list[str]] = [
        "Trade ID",
        "Entry Time",
        "Entry Price",
        "Exit Time",
        "Exit Price",
        "Quantity",
        "PnL",
        "Status",
    ]

    def __init__(
        self,
        file_path: str = "journal/trade_journal.csv",
    ) -> None:
        self._logger = get_logger(__name__)

        self.file_path = Path(file_path)

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.file_path.exists():
            with open(
                self.file_path,
                "w",
                newline="",
                encoding="utf-8",
            ) as file:
                writer = csv.writer(file)
                writer.writerow(self.HEADER)

    def record(
        self,
        trade: Trade,
    ) -> None:
        """
        Record a completed trade.
        """

        with open(
            self.file_path,
            "a",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.writer(file)

            writer.writerow(
                [
                    trade.trade_id,
                    trade.entry_time,
                    trade.entry_price,
                    trade.exit_time,
                    trade.exit_price,
                    trade.quantity,
                    trade.pnl,
                    trade.status.value,
                ]
            )

        self._logger.info(
            "Trade recorded: %s",
            trade.trade_id,
        )

    def exists(self) -> bool:
        """
        Returns True if the journal file exists.
        """
        return self.file_path.exists()

    def count(self) -> int:
        """
        Returns the number of recorded trades.
        Excludes the CSV header.
        """

        if not self.file_path.exists():
            return 0

        with open(
            self.file_path,
            newline="",
            encoding="utf-8",
        ) as file:
            return max(sum(1 for _ in file) - 1, 0)
