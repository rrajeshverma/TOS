"""
Trading Pipeline.

Orchestrates the end-to-end trading flow.
"""

from __future__ import annotations

from decimal import Decimal

from config.risk import CAPITAL, RISK_PERCENT, RISK_REWARD_RATIO
from engines.stop_loss_engine import StopLossEngine


class TradingPipeline:
    """
    Coordinates the complete trading workflow.
    """

    def __init__(
        self,
        indicator_engine,
        decision_engine,
        trade_quality_engine,
        risk_engine,
        position_sizing_engine,
        trade_planning_engine,
        trade_management_engine,
        stop_loss_engine=None,
    ):
        self._indicator_engine = indicator_engine
        self._decision_engine = decision_engine
        self._trade_quality_engine = trade_quality_engine
        self._risk_engine = risk_engine
        self._position_sizing_engine = position_sizing_engine
        self._trade_planning_engine = trade_planning_engine
        self._trade_management_engine = trade_management_engine
        self._stop_loss_engine = stop_loss_engine or StopLossEngine()

    def run(self, candles):
        """
        Execute one trading cycle.
        """
        if candles is None:
            raise ValueError("candles cannot be None")

        if not candles:
            raise ValueError("candles cannot be empty")

        if len(candles) < 2:
            raise ValueError("At least 2 candles are required")

        market = candles[-1]

        indicators = self._indicator_engine.calculate(candles)

        decision = self._decision_engine.evaluate(
            market,
            indicators,
        )

        trade_quality = self._trade_quality_engine.evaluate(
            decision=decision,
            trades_today=0,
        )

        risk = self._risk_engine.evaluate(
            decision=decision,
            trades_today=0,
            daily_loss=Decimal(0),
        )

        previous_candle = candles[-2]

        entry_price = Decimal(str(market.close))

        stop = self._stop_loss_engine.calculate(
            signal=decision.signal,
            previous_high=Decimal(str(previous_candle.high)),
            previous_low=Decimal(str(previous_candle.low)),
            ema_high=Decimal(str(indicators.ema_high)),
            ema_low=Decimal(str(indicators.ema_low)),
        )

        stop_loss = stop.price

        stop_loss_distance = abs(
            entry_price - stop_loss,
        )

        position_size = self._position_sizing_engine.calculate(
            capital=CAPITAL,
            risk_percent=RISK_PERCENT,
            stop_loss_distance=stop_loss_distance,
        )

        target_price = entry_price + (stop_loss_distance * RISK_REWARD_RATIO)

        trade_plan = self._trade_planning_engine.create_plan(
            decision=decision,
            position_size=position_size,
            entry_price=entry_price,
            stop_loss=stop_loss,
            target_price=target_price,
        )

        trade_management = self._trade_management_engine.evaluate(
            entry_price=entry_price,
            stop_loss=stop_loss,
            current_price=entry_price,
        )

        return (
            market,
            indicators,
            decision,
            trade_quality,
            risk,
            position_size,
            trade_plan,
            trade_management,
        )
