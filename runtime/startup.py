"""
Application startup manager.
"""

import logging

from brokers.clients.dhan_client import DhanClient
from brokers.dhan_broker import DhanBroker
from brokers.paper_broker import PaperBroker
from execution.execution_engine import ExecutionEngine
from execution.order_repository import OrderRepository
from execution.order_service import OrderService
from engines.risk_engine import RiskEngine
from engines.strategy_engine import StrategyEngine
from services.order_execution_adapter import OrderExecutionAdapter
from services.paper_trade_runner import PaperTradeRunner
from services.paper_trading_service import PaperTradingService

LOGGER = logging.getLogger("tos")


class Startup:
    """Handles application startup."""

    def __init__(self) -> None:
        self.broker = None
        self.portfolio = None
        self.services = {}
        self.services_initialized = False

    def load_broker(self, broker: str) -> None:
        self.broker = broker

    def load_portfolio(self, portfolio: str) -> None:
        self.portfolio = portfolio

    def initialize_services(self) -> None:
        """Initialize trading services."""

        if self.broker == "dhan":
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

        execution_engine = ExecutionEngine(
            order_service,
        )

        strategy_engine = StrategyEngine()

        risk_engine = RiskEngine()

        paper_service = PaperTradingService()

        paper_trade_runner = PaperTradeRunner(
            strategy_engine=strategy_engine,
            broker=broker,
            order_execution_adapter=execution_adapter,
        )

        self.services = {
            "broker": broker,
            "order_repository": repository,
            "order_service": order_service,
            "order_execution_adapter": execution_adapter,
            "execution_engine": execution_engine,
            "strategy_engine": strategy_engine,
            "risk_engine": risk_engine,
            "paper_trading_service": paper_service,
            "paper_trade_runner": paper_trade_runner,
        }

        if self.broker == "dhan":
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

        LOGGER.info("Trading Runtime READY")
        LOGGER.info("========================================")