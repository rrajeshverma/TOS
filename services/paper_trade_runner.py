"""
Paper trade orchestration service.
"""

from __future__ import annotations

from decimal import Decimal

from domain.indicator_set import IndicatorSet
from domain.market import Market
from engines.order_factory import OrderFactory
from engines.trade_factory import TradeFactory
from engines.trade_planner import TradePlanner
from services.position_manager import PositionManager
from shared.enums import (
    Broker,
    OrderSide,
)


class PaperTradeRunner:
    """
    Executes one complete paper trading cycle.
    """

    def __init__(
        self,
        strategy_engine,
        risk_engine,
        order_execution_adapter,
        trade_planner=None,
        trade_factory=None,
        order_factory=None,
        position_manager=None,
        execution_manager=None,
    ) -> None:
        self.strategy_engine = strategy_engine
        self.risk_engine = risk_engine
        self.trade_planner = trade_planner or TradePlanner()
        self.trade_factory = trade_factory or TradeFactory()
        self.order_factory = order_factory or OrderFactory()
        self.position_manager = position_manager or PositionManager()
        self.adapter = order_execution_adapter
        self.execution_manager = execution_manager

    def run(
        self,
        market: Market,
        indicators: IndicatorSet,
    ):
        decision = self.strategy_engine.decide(
            market,
            indicators,
        )

        risk = self.risk_engine.evaluate(
            decision,
            trades_today=0,
            daily_loss=Decimal(0),
        )

        if not risk.is_approved:
            return {
                "status": "REJECTED",
                "reason": risk.reasons,
            }

        if self.execution_manager is not None:
            return self.execution_manager.execute(
                risk,
            )

        plan = self.trade_planner.plan(
            market,
            risk,
        )

        trade = self.trade_factory.create(
            risk,
            entry_price=plan.entry_price,
            stop_loss=plan.stop_loss,
        )

        order = self.order_factory.create(
            trade,
            Broker.DHAN,
            OrderSide.BUY,
            trade.entry_price,
        )

        execution = self.adapter.to_execution_order(order)

        broker_result = self.adapter.execute(
            execution,
        )

        position = self.position_manager.open_position(
            order,
            order.quantity,
            trade.entry_price,
        )

        return {
            "signal": decision.signal,
            "trade_id": trade.trade_id,
            "order_id": order.order_id,
            "broker_result": broker_result,
            "position_id": position.position_id,
        }
