"""
Integration test:
Live Market Tick -> Market Runtime -> Strategy -> Risk -> Trade -> Order
"""

from datetime import datetime
from decimal import Decimal

from brokers.dhan.models import BrokerTick
from engines.decision_engine import DecisionEngine
from engines.risk_engine import RiskEngine
from market.market_runtime import MarketRuntime
from market.tick_dispatcher import TickDispatcher
from market.websocket_feed import WebSocketFeed
from domain.indicator_set import IndicatorSet

def create_indicators():
    return IndicatorSet(
        ema_high=22400,
        ema_low=22350,
        vwap=22450,
        rsi=60,
        volume_average=90000,
    )

def create_tick():
    return BrokerTick(
        symbol="NIFTY",
        ltp=22500.0,
        volume=100000,
        timestamp=datetime.now(),
    )


def test_live_market_tick_reaches_runtime():

    dispatcher = TickDispatcher()

    runtime = MarketRuntime()

    runtime.start()

    dispatcher.register(
        runtime.on_tick
    )

    feed = WebSocketFeed(
        dispatcher=dispatcher.dispatch,
    )

    feed.connect()

    feed.receive_tick(
        create_tick()
    )

    market = runtime.get_market()

    assert market is not None
    assert market.symbol == "NIFTY"
    assert market.close == 22500.0


def test_market_data_can_trigger_strategy_flow():

    dispatcher = TickDispatcher()

    runtime = MarketRuntime()

    runtime.start()

    dispatcher.register(
        runtime.on_tick
    )

    feed = WebSocketFeed(
        dispatcher=dispatcher.dispatch,
    )

    feed.receive_tick(
        create_tick()
    )

    market = runtime.get_market()

    assert market is not None

    decision_engine = DecisionEngine()

    decision = decision_engine.evaluate(
        market,
        create_indicators(),
    )

    assert decision is not None


def test_risk_engine_receives_decision():

    risk_engine = RiskEngine()

    decision_engine = DecisionEngine()

    market = MarketRuntime()

    market.start()

    market.on_tick(
        create_tick()
    )

    decision = decision_engine.evaluate(
        market.get_market(),
        create_indicators(),
    )

    risk = risk_engine.evaluate(
        decision,
        trades_today=0,
        daily_loss=Decimal("0"),
    )

    assert risk is not None


def test_live_pipeline_components_exist():

    runtime = MarketRuntime()

    assert runtime is not None
    assert runtime.tick_adapter is not None
