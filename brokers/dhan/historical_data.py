"""
Dhan historical market-data adapter.
"""

from __future__ import annotations

from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from dhanhq import DhanContext, dhanhq

from domain.market import Market

IST = ZoneInfo("Asia/Kolkata")


class DhanHistoricalData:
    """Fetch completed historical candles from Dhan."""

    def __init__(
        self,
        client_id: str,
        access_token: str,
    ) -> None:
        self._client = dhanhq(
            DhanContext(
                client_id,
                access_token,
            )
        )

    def load_nifty_5m(
        self,
        from_date: str,
        to_date: str,
        limit: int = 50,
        now: datetime | None = None,
    ) -> list[Market]:
        response = self._client.intraday_minute_data(
            security_id="13",
            exchange_segment="IDX_I",
            instrument_type="INDEX",
            from_date=from_date,
            to_date=to_date,
            interval=5,
        )

        if not isinstance(response, dict):
            raise RuntimeError("Invalid Dhan historical-data response.")

        data = response.get("data") or {}

        required = (
            "open",
            "high",
            "low",
            "close",
            "volume",
            "timestamp",
        )

        if any(key not in data for key in required):
            raise RuntimeError("Dhan historical response is missing candle fields.")

        lengths = {len(data[key]) for key in required}

        if len(lengths) != 1:
            raise RuntimeError("Dhan historical candle arrays have mismatched lengths.")

        markets: list[Market] = []

        for open_, high, low, close, volume, timestamp in zip(
            data["open"],
            data["high"],
            data["low"],
            data["close"],
            data["volume"],
            data["timestamp"],
            strict=True,
        ):
            candle_time = datetime.fromtimestamp(
                float(timestamp),
                tz=UTC,
            ).astimezone(IST)

            markets.append(
                Market(
                    symbol="NIFTY",
                    exchange="NSE",
                    timeframe="5m",
                    timestamp=candle_time,
                    open=float(open_),
                    high=float(high),
                    low=float(low),
                    close=float(close),
                    volume=int(volume),
                )
            )

        markets.sort(key=lambda market: market.timestamp)

        current_time = now.astimezone(IST) if now is not None else datetime.now(IST)

        current_bucket = current_time.replace(
            minute=(current_time.minute // 5) * 5,
            second=0,
            microsecond=0,
        )

        # Exclude the currently forming 5-minute candle.
        markets = [market for market in markets if market.timestamp < current_bucket]

        # Keep only the newest completed candles.
        if limit > 0:
            markets = markets[-limit:]

        return markets
