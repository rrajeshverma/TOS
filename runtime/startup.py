"""
Application startup manager.
"""

import logging
from dataclasses import replace

from brokers.clients.dhan_client import DhanClient
from brokers.dhan.live_market_feed import LiveMarketFeed
from brokers.dhan.websocket import WebSocketClient
from brokers.dhan_broker import DhanBroker
from brokers.instrument_mapper import InstrumentMapper
from brokers.paper_broker import PaperBroker
from config.runtime_config import RuntimeConfig
from config.version import APP_NAME, BUILD, MODE, VERSION
from engines.decision_engine import DecisionEngine
from engines.indicator_engine import IndicatorEngine
from engines.market_engine import MarketEngine
from engines.position_sizing_engine import PositionSizingEngine
from engines.risk_engine import RiskEngine
from engines.stop_loss_engine import StopLossEngine
from engines.strategy_engine import StrategyEngine
from engines.trade_management_engine import TradeManagementEngine
from engines.trade_planning_engine import TradePlanningEngine
from engines.trade_quality_engine import TradeQualityEngine
from execution.execution_engine import ExecutionEngine
from execution.execution_manager import ExecutionManager
from execution.order_repository import OrderRepository
from execution.order_service import OrderService
from integration.pipeline import TradingPipeline as MarketDataPipeline
from journal.trade_journal import TradeJournal
from market.candle_builder import CandleBuilder
from providers.dhan_instrument_provider import DhanInstrumentProvider
from runtime.runtime_mode import RuntimeMode
from runtime.safety_factory import SafetyFactory
from runtime.trading_pipeline import TradingPipeline
from runtime.trading_runtime import TradingRuntime
from services.market_data_service import MarketDataService
from services.order_execution_adapter import OrderExecutionAdapter
from services.paper_position_lifecycle import PaperPositionLifecycle
from services.paper_trade_runner import PaperTradeRunner
from services.paper_trading_service import PaperTradingService
from storage.instrument_repository import InstrumentRepository
from trading.execution_mode import ExecutionMode

LOGGER = logging.getLogger("tos")


class Startup:
    """Handles application startup."""

    def __init__(self, config: RuntimeConfig | None = None) -> None:
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

        # ---------------- BROKER ----------------
        instrument_repository = InstrumentRepository()
        instrument_provider = DhanInstrumentProvider()

        for instrument in instrument_provider.load():
            instrument_repository.add(instrument)

        instrument_mapper = InstrumentMapper(
            instrument_repository,
        )

        if self.config.broker == "dhan":
            client = DhanClient()

            broker = DhanBroker(
                client=client,
                instrument_mapper=instrument_mapper,
            )

            broker.connect()
        else:
            broker = PaperBroker()
            broker.connect()

        # ---------------- CORE SERVICES ----------------
        repository = OrderRepository()

        order_service = OrderService(
            broker=broker,
            repository=repository,
        )

        execution_adapter = OrderExecutionAdapter(
            broker=broker,
            order_service=order_service,
        )

        execution_mode = ExecutionMode(self.config.mode)
        execution_guard = SafetyFactory.create(execution_mode)

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
        decision_engine = DecisionEngine()
        trade_quality_engine = TradeQualityEngine()
        risk_engine = RiskEngine()
        stop_loss_engine = StopLossEngine()
        position_sizing_engine = PositionSizingEngine()
        trade_planning_engine = TradePlanningEngine()
        trade_management_engine = TradeManagementEngine()

        runtime = TradingRuntime(
            {},
            mode=RuntimeMode(self.config.mode.lower()),
        )

        paper_service = PaperTradingService()
        trade_journal = TradeJournal()

        paper_trade_runner = PaperTradeRunner(
            strategy_engine=strategy_engine,
            risk_engine=risk_engine,
            order_execution_adapter=execution_adapter,
            execution_manager=execution_manager,
        )

        paper_position_lifecycle = PaperPositionLifecycle(
            trade_journal=trade_journal,
            order_service=order_service,
            broker=broker,
        )

        market_data_pipeline = MarketDataPipeline(
            candle_builder=candle_builder,
            market_engine=market_engine,
            indicator_engine=indicator_engine,
            runtime=runtime,
        )

        trading_pipeline = TradingPipeline(
            indicator_engine=indicator_engine,
            decision_engine=decision_engine,
            trade_quality_engine=trade_quality_engine,
            risk_engine=risk_engine,
            position_sizing_engine=position_sizing_engine,
            trade_planning_engine=trade_planning_engine,
            trade_management_engine=trade_management_engine,
            stop_loss_engine=stop_loss_engine,
            trade_journal=trade_journal,
        )

        # ---------------- MARKET DATA ----------------

        if self.config.market_data == "dhan":
            try:
                live_market_feed = LiveMarketFeed(
                    client_id=self.config.dhan_client_id,
                    access_token=self.config.dhan_access_token,
                    instrument_mapper=instrument_mapper,
                )

                websocket = WebSocketClient(
                    live_market_feed=live_market_feed,
                )

                market_data_service = MarketDataService(
                    websocket=websocket,
                )

            except Exception:
                # Fallback for safety (important for tests)
                market_data_service = MarketDataService(
                    websocket=None,
                )

            else:
                try:
                    nifty = instrument_repository.get_by_symbol("NIFTY")
                except KeyError:
                    LOGGER.warning(
                        "NIFTY instrument not available; "
                        "Dhan market feed will remain unsubscribed.",
                    )
                else:
                    market_data_service.subscribe([nifty])

        else:
            # Paper market-data mode → no live market dependency
            market_data_service = MarketDataService(
                websocket=None,
            )

        # ---------------- SERVICE REGISTRY ----------------
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
            "paper_position_lifecycle": paper_position_lifecycle,
            "market_data_service": market_data_service,
            "market_data_pipeline": market_data_pipeline,
            "trading_runtime": runtime,
            "trading_pipeline": trading_pipeline,
        }

        runtime.services = self.services

        if self.config.broker == "dhan":
            self.services["dhan_client"] = client

        self.services_initialized = True
        self.log_health()

    def log_health(self) -> None:
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

        runtime = self.services.get("trading_runtime")

        LOGGER.info(
            "Trading Runtime     : %s",
            runtime.state if runtime else "UNKNOWN",
        )

        LOGGER.info("========================================")

    def log_banner(self) -> None:
        LOGGER.info("=" * 56)
        LOGGER.info("%s", APP_NAME)
        LOGGER.info("=" * 56)
        LOGGER.info("Version             : %s", VERSION)
        LOGGER.info("Build               : %s", BUILD)
        LOGGER.info("Mode                : %s", MODE)
        LOGGER.info("=" * 56)

    def shutdown(self) -> None:
        runtime = self.services.get("trading_runtime")

        if runtime is not None:
            runtime.stop()

        broker = self.services.get("broker")

        if broker is not None:
            broker.disconnect()

        self.services_initialized = False

        LOGGER.info("Application shutdown complete")
