"""
Trading runtime orchestrator.
"""

from __future__ import annotations

from runtime.market_clock import MarketClock
from runtime.runtime_metrics import RuntimeMetrics
from runtime.runtime_mode import RuntimeMode
from runtime.trading_session import TradingSession
from shared.event_bus import EventBus
from shared.events import Event
from shared.logger import get_logger
from shared.runtime_status import RuntimeStatus

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

    def __init__(
        self,
        services: dict,
        mode: RuntimeMode = RuntimeMode.PAPER,
    ) -> None:
        self.services = services
        self.mode = mode
        self.running = False
        self.runtime_status = RuntimeStatus.INITIALIZING
        self.metrics = RuntimeMetrics()
        self.event_bus = EventBus()

        self.trading_session = TradingSession()
        self.market_clock = MarketClock()

    @property
    def indicator_engine(self):
        return self.services.get("indicator_engine")

    @property
    def trading_pipeline(self):
        """
        Return the configured trading pipeline.
        """
        return self.services.get("trading_pipeline")

    @property
    def strategy_engine(self):
        return self.services.get("strategy_engine")

    @property
    def risk_engine(self):
        return self.services.get("risk_engine")

    @property
    def execution_manager(self):
        return self.services.get("execution_manager")

    @property
    def bus(self) -> EventBus:
        """Return runtime event bus."""
        return self.event_bus

    @property
    def is_running(self) -> bool:
        """Return True when runtime is active."""
        return self.runtime_status == RuntimeStatus.RUNNING

    @property
    def state(self) -> RuntimeStatus:
        """Current runtime state."""
        return self.runtime_status

    def validate(self) -> list[str]:
        """
        Validate that all required runtime services exist.

        Returns
        -------
        list[str]
            Names of missing services.
        """
        return [service for service in REQUIRED_SERVICES if self.services.get(service) is None]

    def start(self) -> None:
        self.runtime_status = RuntimeStatus.STARTING
        self.running = True

        market_data = self.services.get("market_data_service")
        trading_pipeline = self.services.get("trading_pipeline")

        if market_data is not None:
            if trading_pipeline is not None:
                market_data.register_tick_callback(
                    trading_pipeline.on_tick,
                )

            market_data.connect()

        self.runtime_status = RuntimeStatus.RUNNING

        LOGGER.info(
            "Trading runtime started [%s]",
            self.runtime_status,
        )

    def stop(self) -> None:
        market_data = self.services.get("market_data_service")

        if market_data is not None:
            market_data.disconnect()

        self.runtime_status = RuntimeStatus.STOPPING
        self.running = False
        self.runtime_status = RuntimeStatus.STOPPED
        self.bus.unsubscribe(
            Event.MARKET_TICK.value,
            self._handle_market_tick,
        )

        LOGGER.info(
            "Trading runtime stopped [%s]",
            self.runtime_status,
        )

    def pause(self) -> None:
        """Pause the runtime."""

        self.runtime_status = RuntimeStatus.PAUSED

        LOGGER.info(
            "Trading runtime paused [%s]",
            self.runtime_status,
        )

    def fail(self) -> None:
        """Move runtime into FAILED state."""

        self.running = False
        self.runtime_status = RuntimeStatus.FAILED

        LOGGER.exception(
            "Trading runtime entered FAILED state",
        )

    def health(self) -> dict:
        """Return runtime health."""

        market_data = self.services.get("market_data_service")

        return {
            "running": self.running,
            "runtime_status": self.runtime_status,
            "session_state": self.trading_session.state,
            "market_data_connected": market_data is not None,
            "trading_allowed": self.trading_session.is_trading_allowed(),
            "services": list(self.services.keys()),
        }

    def run_cycle(
        self,
        market,
        history,
    ):
        if self.trading_pipeline is not None:
            (
                _market,
                _indicators,
                _decision,
                _quality,
                risk,
                position_size,
                _trade_plan,
                _trade_management,
            ) = self.trading_pipeline.run(history)

            if self.mode == RuntimeMode.BACKTEST:
                return risk

            if self.execution_manager is None:
                return risk

            return self.execution_manager.execute(
                risk,
                quantity=position_size.quantity,
            )

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

        if self.mode == RuntimeMode.BACKTEST:
            return risk

        if self.execution_manager is None:
            return risk

        return self.execution_manager.execute(risk)

    def _handle_market_tick(
        self,
        payload: dict,
    ) -> None:
        """Handle MARKET_TICK events."""

        self.run_cycle(
            payload["market"],
            payload["history"],
        )

    def on_market_tick(
        self,
        market,
        history,
    ):
        if self.mode != RuntimeMode.BACKTEST:
            session = self.market_clock.current_session()

            self.trading_session.set_state(
                session,
            )

            if not self.trading_session.is_trading_allowed():
                LOGGER.debug(
                    "Ignoring market tick because session is %s",
                    self.trading_session.state,
                )
                return None

        self.publish(
            Event.MARKET_TICK,
            {
                "market": market,
                "history": history,
            },
        )

        return self.run_cycle(
            market,
            history,
        )

    def status(self) -> dict:
        """Return runtime status."""

        return {
            "status": self.runtime_status,
            "running": self.running,
            "metrics": self.metrics.snapshot(),
        }

    def publish(
        self,
        event: Event,
        payload,
    ) -> None:
        """Publish a runtime event."""

        self.event_bus.publish(
            event.value,
            payload,
        )
