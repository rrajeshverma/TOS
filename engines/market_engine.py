"""
Market Engine

Responsible for validating raw market data and constructing
immutable Market domain objects.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import Any

from domain.market import Market
from exceptions import (
    InvalidPriceError,
    InvalidTimestampError,
    InvalidVolumeError,
    MissingFieldError,
)
from shared.logger import get_logger


class MarketEngine:
    """Engine responsible for creating validated Market objects."""

    REQUIRED_FIELDS = (
        "symbol",
        "exchange",
        "timeframe",
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
    )

    def __init__(self) -> None:
        self._logger = get_logger(__name__)

    def build_market(self, raw_data: Mapping[str, Any]) -> Market:
        """
        Build a validated Market object from raw market data.

        Args:
            raw_data: Raw OHLCV candle.

        Returns:
            Market

        Raises:
            MissingFieldError
            InvalidTimestampError
            InvalidPriceError
            InvalidVolumeError
        """

        if raw_data is None:
            raise MissingFieldError("Market data is None")

        self._validate_required_fields(raw_data)
        self._validate_timestamp(raw_data["timestamp"])
        self._validate_prices(raw_data)
        self._validate_volume(raw_data["volume"])

        market = Market(
            symbol=str(raw_data["symbol"]),
            exchange=str(raw_data["exchange"]),
            timeframe=str(raw_data["timeframe"]),
            timestamp=raw_data["timestamp"],
            open=float(raw_data["open"]),
            high=float(raw_data["high"]),
            low=float(raw_data["low"]),
            close=float(raw_data["close"]),
            volume=int(raw_data["volume"]),
        )

        self._logger.info(
            "Validated market candle: %s",
            market.timestamp,
        )

        return market

    def _validate_required_fields(
        self,
        raw_data: Mapping[str, Any],
    ) -> None:

        for field in self.REQUIRED_FIELDS:
            if field not in raw_data:
                raise MissingFieldError(field)

    @staticmethod
    def _validate_timestamp(
        timestamp: datetime,
    ) -> None:

        if not isinstance(timestamp, datetime):
            raise InvalidTimestampError("timestamp must be datetime")

    @staticmethod
    def _validate_prices(
        raw_data: Mapping[str, Any],
    ) -> None:

        high = float(raw_data["high"])
        low = float(raw_data["low"])
        open_price = float(raw_data["open"])
        close_price = float(raw_data["close"])

        if high < low:
            raise InvalidPriceError("High cannot be less than Low")

        if not (low <= open_price <= high):
            raise InvalidPriceError("Open outside candle range")

        if not (low <= close_price <= high):
            raise InvalidPriceError("Close outside candle range")

    @staticmethod
    def _validate_volume(
        volume: int,
    ) -> None:

        if int(volume) < 0:
            raise InvalidVolumeError("Volume cannot be negative")
