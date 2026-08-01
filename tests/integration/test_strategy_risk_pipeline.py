"""
Strategy → Risk integration.
"""

from decimal import Decimal

from tests.helpers.domain_factory import (
    make_indicator_set,
    make_market,
)

from engines.strategy_engine import StrategyEngine
from engines.risk_engine import RiskEngine

from shared.enums import (
    DecisionStatus,
    Signal,
)


def test_strategy_risk_pipeline():
    market = make_market(
        close=Decimal("111"),
    )

    indicators = make_indicator_set(
        ema_high=Decimal("105"),
        ema_low=Decimal("95"),
        vwap=Decimal("104"),
        rsi=60,
    )

    strategy = StrategyEngine()

    decision = strategy.decide(
        market,
        indicators,
    )

    assert decision.signal == Signal.BUY_CE

    risk = RiskEngine().evaluate(
        decision,
        trades_today=0,
        daily_loss=Decimal("0"),
    )

    assert risk.is_approved
    assert decision.status == DecisionStatus.VALID
