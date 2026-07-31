"""
Trading runtime orchestrator.
"""

from __future__ import annotations

from shared.logger import get_logger


LOGGER = get_logger(__name__)

REQUIRED_SERVICES = (
    "indicator_engine",
    "strategy_engine",
    "risk_engine",
    "execution_manager",
    "market_data_service",
    "trading_pipeline",
)


class TradingRuntime:
    """
    Coordinates the trading lifecycle.
    """

    def __init__(self, services: dict) -> None:
        self.services = services
        self.running = False

    @property
    def indicator_engine(self):
        return self.services.get("indicator_engine")

    @property
    def strategy_engine(self):
        return self.services.get("strategy_engine")

    @property
    def risk_engine(self):
        return self.services.get("risk_engine")

    @property
    def execution_manager(self):
        return self.services.get("execution_manager")

    def validate(self) -> list[str]:
        """
        Validate that all required runtime services exist.

        Returns
        -------
        list[str]
            Names of missing services.
        """
        return [
            service
            for service in REQUIRED_SERVICES
            if self.services.get(service) is None
        ]

    def start(self) -> None:
        self.running = True

        market_data = self.services.get("market_data_service")
        trading_pipeline = self.services.get("trading_pipeline")

        if market_data is not None:
            if trading_pipeline is not None:
                market_data.register_tick_callback(
                    trading_pipeline.on_tick,
                )

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
        indicator_engine = self.indicator_engine
        strategy_engine = self.strategy_engine
        risk_engine = self.risk_engine

        indicators = indicator_engine.calculate(history)

        decision = strategy_engine.decide(
            market,
            indicators,
        )

        risk = risk_engine.evaluate(
            decision,
            trades_today=0,
            daily_loss=0,
        )

        execution_manager = self.execution_manager

        if execution_manager is None:
            return risk

        return execution_manager.execute(risk)

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
