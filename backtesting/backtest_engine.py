"""
Simple backtest engine.

Runs a strategy over a HistoricalDataFeed.
"""

from __future__ import annotations


class BacktestEngine:
    """
    Executes a simple strategy against historical candles.
    """

    def __init__(
        self,
        feed,
        strategy=None,
    ) -> None:
        self.feed = feed
        self.strategy = strategy

    def run(self):
        """
        Replay every candle.
        """

        results = []

        for candle in self.feed:
            if self.strategy is None:
                continue

            signal = self.strategy.on_candle(candle)

            if signal is not None:
                results.append(signal)

        return results
