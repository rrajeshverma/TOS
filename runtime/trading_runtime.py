"""
Trading runtime orchestrator.
"""

from __future__ import annotations

from shared.logger import get_logger


LOGGER = get_logger(__name__)


class TradingRuntime:
    """
    Coordinates the trading lifecycle.
    """

    def __init__(self, services: dict) -> None:
        self.services = services
        self.running = False

    def start(self) -> None:
        self.running = True

        market_data = self.services.get("market_data_service")

        if market_data is not None:
            market_data.connect()

        LOGGER.info("Trading runtime started")

    def stop(self) -> None:
        market_data = self.services.get("market_data_service")

        if market_data is not None:
            market_data.disconnect()

        self.running = False

        LOGGER.info("Trading runtime stopped")

    def health(self) -> dict:
        return {
            "running": self.running,
            "services": list(self.services.keys()),
        }

    def run_cycle(
        self,
        market,
        history,
    ):
        strategy_engine = self.services["strategy_engine"]
        risk_engine = self.services["risk_engine"]

        decision = strategy_engine.evaluate(
            market,
            history,
        )

        risk = risk_engine.evaluate(
            decision,
            trades_today=0,
            daily_loss=0,
        )

        return risk

    def on_market_tick(
        self,
        market,
        history,
    ):
        """
        Process a market update.

        This is the entry point used by the live
        market data service.
        """

        return self.run_cycle(
            market,
            history,
        )