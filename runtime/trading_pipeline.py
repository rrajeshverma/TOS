"""
=========================================================
Trading Operating System (TOS)

Module      : Trading Pipeline
Version     : 1.0.0
Author      : Rajesh Varma
Description : Orchestrates the end-to-end trading flow.
=========================================================
"""

from __future__ import annotations


class TradingPipeline:
    """
    Coordinates the complete trading workflow.
    """

    def __init__(
        self,
        market_engine,
        indicator_engine,
        decision_engine,
        trade_quality_engine,
        risk_engine,
        position_sizing_engine,
        trade_planning_engine,
        trade_management_engine,
    ):
        self._market_engine = market_engine
        self._indicator_engine = indicator_engine
        self._decision_engine = decision_engine
        self._trade_quality_engine = trade_quality_engine
        self._risk_engine = risk_engine
        self._position_sizing_engine = position_sizing_engine
        self._trade_planning_engine = trade_planning_engine
        self._trade_management_engine = trade_management_engine

    def run(self, candles):
        """
        Execute one trading cycle.

        Returns:
            tuple[Market, IndicatorSet]
        """
        if candles is None:
            raise ValueError("candles cannot be None")

        if not candles:
            raise ValueError("candles cannot be empty")

        market = self._market_engine.build_market(candles[-1])

        indicators = self._indicator_engine.calculate(candles)

        decision = self._decision_engine.decide(indicators)

        trade_quality = self._trade_quality_engine.evaluate(
            decision=decision,
            trades_today=0,
        )

        risk = self._risk_engine.evaluate(
            decision=decision,
            trades_today=0,
            daily_loss=0,
        )

        position_size = self._position_sizing_engine.calculate(
            capital=100000,
            risk_percent=2,
            stop_loss_distance=100,
        )

        trade_plan = self._trade_planning_engine.create_plan(
            decision=decision,
            position_size=position_size,
            entry_price=250,
            stop_loss=240,
            target_price=270,
        )

        return (
            market,
            indicators,
            decision,
            trade_quality,
            risk,
            position_size,
            trade_plan,
        )


class FakePositionSizingEngine:
    def __init__(self):
        self.called = False

    def calculate(
        self,
        capital,
        risk_percent,
        stop_loss_distance,
        lot_size=1,
    ):
        self.called = True
        return "POSITION_SIZE"
