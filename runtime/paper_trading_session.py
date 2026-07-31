"""
Paper Trading Session Runtime

Handles simulated trading lifecycle.

Flow:

START
    |
    ▼
Market Data
    |
    ▼
Strategy Processing
    |
    ▼
Paper Execution
    |
    ▼
Journal Update
"""

from datetime import datetime


class PaperTradingSession:
    """
    Controls paper trading runtime lifecycle.
    """

    def __init__(
        self,
        market_feed=None,
        strategy=None,
        executor=None,
        journal=None,
    ) -> None:
        self.market_feed = market_feed
        self.strategy = strategy
        self.executor = executor
        self.journal = journal

        self.running = False

        self.trades = []

    def start(self) -> None:
        """
        Start paper trading session.
        """

        self.running = True

    def stop(self) -> None:
        """
        Stop paper trading session.
        """

        self.running = False

    def is_running(self) -> bool:
        """
        Runtime status.
        """

        return self.running

    def process_tick(
        self,
        tick,
    ):
        """
        Process incoming market tick.
        """

        if not self.running:
            raise RuntimeError("Paper trading session is not running.")

        if self.strategy is None:
            return None

        decision = self.strategy.evaluate(tick)

        if decision is None:
            return None

        if self.executor is None:
            return None

        trade = self.executor.execute(decision)

        if trade is not None:
            self.trades.append(trade)

            if self.journal:
                self.journal.record(trade)

        return trade

    def summary(self) -> dict:
        return {
            "running": self.running,
            "trades": len(self.trades),
            "timestamp": datetime.now(),
        }
