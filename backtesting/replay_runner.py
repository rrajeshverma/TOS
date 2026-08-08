"""
Historical replay runner.

Feeds historical Market objects into the TradingRuntime.
"""

from __future__ import annotations

from backtesting.backtest_context import BacktestContext
from shared.logger import get_logger

LOGGER = get_logger(__name__)


class ReplayRunner:
    def __init__(
        self,
        runtime,
        feed,
        context: BacktestContext | None = None,
    ):
        self._runtime = runtime
        self._feed = feed
        self.context = context or BacktestContext()

    def run(self) -> int:
        """
        Replay the complete historical feed.
        """

        history = []

        processed = 0
        skipped = 0
        last_market = None

        for market in self._feed:
            last_market = market
            history.append(market)

            try:
                risk = self._runtime.on_market_tick(
                    market,
                    history,
                )

                LOGGER.debug(
                    "Runtime returned: %s",
                    type(risk).__name__,
                )

                if risk is not None:
                    self.context.on_risk(
                        risk=risk,
                        market=market,
                    )

                processed += 1

                if processed % 100 == 0:
                    LOGGER.info(
                        "Processed %d candles",
                        processed,
                    )

            except ValueError as exc:
                skipped += 1

                LOGGER.debug(
                    "Skipping candle: %s",
                    exc,
                )

        if last_market is not None:
            self.context.finalize(last_market)

        LOGGER.info(
            "Replay completed. Processed=%d Skipped=%d",
            processed,
            skipped,
        )

        return processed
