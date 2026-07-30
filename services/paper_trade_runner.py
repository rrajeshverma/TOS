"""
Paper trade orchestration service.
"""

from __future__ import annotations

from decimal import Decimal

from engines.trade_planner import TradePlanner
from domain.indicator_set import IndicatorSet
from domain.market import Market
from engines.order_factory import OrderFactory
from engines.trade_factory import TradeFactory
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
    ) -> None:
        self.strategy_engine = strategy_engine
        self.risk_engine = risk_engine
        self.trade_planner = TradePlanner()
        self.trade_factory = TradeFactory()
        self.order_factory = OrderFactory()
        self.position_manager = PositionManager()
        self.adapter = order_execution_adapter

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
            daily_loss=Decimal("0"),
        )

        if not risk.is_approved:
            return {
                "status": "REJECTED",
                "reason": risk.reasons,
            }

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