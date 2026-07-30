from datetime import datetime
from unittest.mock import Mock

from domain.decision import Decision
from domain.indicator_set import IndicatorSet
from domain.market import Market
from engines.strategy_engine import StrategyEngine
from shared.enums import DecisionStatus, Signal


def create_market() -> Market:
    return Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="1m",
        timestamp=datetime.now(),
        open=100.0,
        high=105.0,
        low=99.0,
        close=104.0,
        volume=1000,
    )


def create_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        ema_high=103.0,
        ema_low=100.0,
        vwap=102.0,
        rsi=60.0,
        volume_average=1000.0,
    )


def create_decision(
    market: Market,
    indicators: IndicatorSet,
) -> Decision:
    return Decision(
        decision_id="DEC001",
        timestamp=market.timestamp,
        market=market,
        indicator_set=indicators,
        signal=Signal.BUY_CE,
        status=DecisionStatus.VALID,
        reasons=("test",),
    )


def test_evaluate_uses_all_engines():
    market = create_market()
    indicators = create_indicator_set()
    decision = create_decision(market, indicators)

    market_engine = Mock()
    indicator_engine = Mock()
    decision_engine = Mock()

    market_engine.build_market.return_value = market
    indicator_engine.calculate.return_value = indicators
    decision_engine.evaluate.return_value = decision

    engine = StrategyEngine(
        market_engine=market_engine,
        indicator_engine=indicator_engine,
        decision_engine=decision_engine,
    )

    raw_market = {"dummy": "value"}
    history = [market]

    result = engine.evaluate(raw_market, history)

    market_engine.build_market.assert_called_once_with(raw_market)
    indicator_engine.calculate.assert_called_once_with(history)
    decision_engine.evaluate.assert_called_once_with(
        market,
        indicators,
    )

    assert result is decision


def test_decide_delegates_to_decision_engine():
    market = create_market()
    indicators = create_indicator_set()
    decision = create_decision(market, indicators)

    decision_engine = Mock()
    decision_engine.evaluate.return_value = decision

    engine = StrategyEngine(
        decision_engine=decision_engine,
    )

    result = engine.decide(
        market,
        indicators,
    )

    decision_engine.evaluate.assert_called_once_with(
        market,
        indicators,
    )

    assert result is decision
