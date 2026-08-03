"""
CSV historical data source.
"""

from __future__ import annotations

import csv
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path

from backtesting.historical_data_source import HistoricalDataSource
from domain.market import Market


class CSVDataSource(HistoricalDataSource):
    """
    Loads historical market data from CSV.
    """

    def __init__(
        self,
        symbol: str,
        exchange: str,
        timeframe: str,
    ) -> None:
        self._symbol = symbol
        self._exchange = exchange
        self._timeframe = timeframe

    def load(
        self,
        source: Path | str,
    ) -> Iterator[Market]:
        """
        Load Market objects from CSV.
        """

        with open(source, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                yield Market(
                    symbol=self._symbol,
                    exchange=self._exchange,
                    timeframe=self._timeframe,
                    timestamp=datetime.fromisoformat(
                        row["timestamp"],
                    ),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=int(float(row["volume"])),
                )
