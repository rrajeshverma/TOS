"""
Application startup manager.
"""

import logging
from dataclasses import replace

from brokers.clients.dhan_client import DhanClient
from brokers.dhan.websocket import WebSocketClient
from brokers.dhan_broker import DhanBroker
from brokers.paper_broker import PaperBroker
from config.runtime_config import RuntimeConfig
from config.version import APP_NAME, BUILD, MODE, VERSION
from engines.indicator_engine import IndicatorEngine
from engines.market_engine import MarketEngine
from engines.risk_engine import RiskEngine
from engines.strategy_engine import StrategyEngine
from execution.execution_engine import ExecutionEngine
from execution.execution_manager import ExecutionManager
from execution.order_repository import OrderRepository
from execution.order_service import OrderService
from integration.pipeline import TradingPipeline
from market.candle_builder import CandleBuilder
from runtime.trading_runtime import TradingRuntime
from services.market_data_service import MarketDataService
from services.order_execution_adapter import OrderExecutionAdapter
from services.paper_trade_runner import PaperTradeRunner
from services.paper_trading_service import PaperTradingService
from runtime.safety_factory import SafetyFactory

LOGGER = logging.getLogger("tos")


class Startup:
    """Handles application startup."""

    def __init__(self, config: RuntimeConfig | None = None) -> None:
        """Initialize startup manager."""

        self.config = config or RuntimeConfig()
        self.services: dict[str, object] = {}
        self.services_initialized = False

    def load_broker(self, broker: str) -> None:
        self.config = replace(self.config, broker=broker)

    def load_portfolio(self, portfolio: str) -> None:
        self.config = replace(self.config, portfolio=portfolio)

    def initialize_services(self) -> None:
        """Initialize trading services."""

        self.config.validate()

        self.log_banner()

        if self.config.broker == "dhan":
            client = DhanClient()

            broker = DhanBroker(
                client=client,
                instrument_mapper={},
            )

            broker.connect()

        else:
            broker = PaperBroker()
            broker.connect()

        repository = OrderRepository()

        order_service = OrderService(
            broker=broker,
            repository=repository,
        )

        execution_adapter = OrderExecutionAdapter(
            broker=broker,
            order_service=order_service,
        )

        execution_guard = SafetyFactory.create()

        execution_engine = ExecutionEngine(
            order_service,
            execution_guard=execution_guard,
        )

        execution_manager = ExecutionManager(
            execution_engine,
        )

        market_engine = MarketEngine()

        indicator_engine = IndicatorEngine()

        candle_builder = CandleBuilder()

        strategy_engine = StrategyEngine()

        risk_engine = RiskEngine()

        runtime = TradingRuntime({})

        paper_service = PaperTradingService()

        paper_trade_runner = PaperTradeRunner(
            strategy_engine=strategy_engine,
            risk_engine=risk_engine,
            order_execution_adapter=execution_adapter,
            execution_manager=execution_manager,
        )

        trading_pipeline = TradingPipeline(
            candle_builder=candle_builder,
            market_engine=market_engine,
            indicator_engine=indicator_engine,
            runtime=runtime,
        )

        market_data_service = MarketDataService(
            websocket=WebSocketClient(),
        )

        self.services = {
            "broker": broker,
            "order_repository": repository,
            "order_service": order_service,
            "order_execution_adapter": execution_adapter,
            "execution_engine": execution_engine,
            "execution_manager": execution_manager,
            "market_engine": market_engine,
            "indicator_engine": indicator_engine,
            "candle_builder": candle_builder,
            "strategy_engine": strategy_engine,
            "risk_engine": risk_engine,
            "paper_trading_service": paper_service,
            "paper_trade_runner": paper_trade_runner,
            "market_data_service": market_data_service,
            "trading_runtime": runtime,
            "trading_pipeline": trading_pipeline,
        }

        runtime.services = self.services

        if self.config.broker == "dhan":
            self.services["dhan_client"] = client

        self.services_initialized = True

        self.log_health()

    def log_health(self) -> None:
        """Log runtime service health."""

        LOGGER.info("========== TOS RUNTIME HEALTH ==========")

        broker = self.services.get("broker")

        LOGGER.info(
            "Broker              : %s",
            "CONNECTED" if broker and broker.is_connected() else "NOT CONNECTED",
        )

        LOGGER.info("Order Repository    : READY")
        LOGGER.info("Order Service       : READY")
        LOGGER.info("Execution Adapter   : READY")
        LOGGER.info("Execution Engine    : READY")
        LOGGER.info("Strategy Engine     : READY")
        LOGGER.info("Risk Engine         : READY")
        LOGGER.info("Paper Trading       : READY")
        LOGGER.info("Paper Trade Runner  : READY")
        LOGGER.info("Trading Runtime     : READY")
        LOGGER.info("========================================")

    def log_banner(self) -> None:
        """Log startup banner."""

        LOGGER.info("=" * 56)
        LOGGER.info("%s", APP_NAME)
        LOGGER.info("=" * 56)
        LOGGER.info("Version             : %s", VERSION)
        LOGGER.info("Build               : %s", BUILD)
        LOGGER.info("Mode                : %s", MODE)
        LOGGER.info("=" * 56)
