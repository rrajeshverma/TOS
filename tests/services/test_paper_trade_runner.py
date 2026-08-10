from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

from domain.indicator_set import IndicatorSet
from domain.market import Market
from services.paper_trade_runner import PaperTradeRunner
from shared.enums import Signal


class FakeDecision:
    def __init__(self):
        self.signal = Signal.BUY_CE


class FakeRisk:
    def __init__(self, approved=True):
        self.is_approved = approved
        self.reasons = ("Risk rejected",)


class FakeTrade:
    def __init__(self):
        self.trade_id = "TRADE001"
        self.entry_price = Decimal(100)


class FakeOrder:
    def __init__(self):
        self.order_id = "ORDER001"
        self.quantity = 65


class FakePosition:
    def __init__(self):
        self.position_id = "POSITION001"


def create_runner():
    strategy = Mock()
    risk_engine = Mock()
    adapter = Mock()

    runner = PaperTradeRunner(
        strategy_engine=strategy,
        risk_engine=risk_engine,
        order_execution_adapter=adapter,
    )

    return runner, strategy, risk_engine, adapter


def create_market_and_indicators():
    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime.now(),
        open=22500,
        high=22550,
        low=22490,
        close=22540,
        volume=100000,
    )

    indicators = IndicatorSet(
        ema_high=22520,
        ema_low=22480,
        vwap=22510,
        rsi=60,
        volume_average=90000,
    )

    return market, indicators


def test_run_returns_rejected_when_risk_not_approved():
    runner, strategy, _, _adapter = create_runner()

    strategy.decide.return_value = FakeDecision()

    runner.risk_engine = Mock()
    runner.risk_engine.evaluate.return_value = FakeRisk(False)

    market, indicators = create_market_and_indicators()

    result = runner.run(
        market,
        indicators,
    )

    assert result["status"] == "REJECTED"
    assert result["reason"] == ("Risk rejected",)


def test_strategy_engine_called_once():
    runner, strategy, _, adapter = create_runner()

    strategy.decide.return_value = FakeDecision()

    runner.risk_engine = Mock()
    runner.risk_engine.evaluate.return_value = FakeRisk()

    runner.trade_factory = Mock()
    runner.trade_factory.create.return_value = FakeTrade()

    runner.order_factory = Mock()
    runner.order_factory.create.return_value = FakeOrder()

    runner.position_manager = Mock()
    runner.position_manager.open_position.return_value = FakePosition()

    adapter.to_execution_order.return_value = object()
    adapter.execute.return_value = "OK"

    market, indicators = create_market_and_indicators()

    runner.run(
        market,
        indicators,
    )

    strategy.decide.assert_called_once()


def test_adapter_execute_called_once():
    runner, strategy, _, adapter = create_runner()

    strategy.decide.return_value = FakeDecision()

    runner.risk_engine = Mock()
    runner.risk_engine.evaluate.return_value = FakeRisk()

    runner.trade_factory = Mock()
    runner.trade_factory.create.return_value = FakeTrade()

    runner.order_factory = Mock()
    runner.order_factory.create.return_value = FakeOrder()

    runner.position_manager = Mock()
    runner.position_manager.open_position.return_value = FakePosition()

    adapter.to_execution_order.return_value = object()
    adapter.execute.return_value = "BROKER_OK"

    market, indicators = create_market_and_indicators()

    runner.run(
        market,
        indicators,
    )

    adapter.execute.assert_called_once()


def test_run_returns_expected_fields():
    runner, strategy, _, adapter = create_runner()

    strategy.decide.return_value = FakeDecision()

    runner.risk_engine = Mock()
    runner.risk_engine.evaluate.return_value = FakeRisk()

    runner.trade_factory = Mock()
    runner.trade_factory.create.return_value = FakeTrade()

    runner.order_factory = Mock()
    runner.order_factory.create.return_value = FakeOrder()

    runner.position_manager = Mock()
    runner.position_manager.open_position.return_value = FakePosition()

    adapter.to_execution_order.return_value = object()
    adapter.execute.return_value = "SUCCESS"

    market, indicators = create_market_and_indicators()

    result = runner.run(
        market,
        indicators,
    )

    assert result["signal"] == Signal.BUY_CE
    assert result["trade_id"] == "TRADE001"
    assert result["order_id"] == "ORDER001"
    assert result["broker_result"] == "SUCCESS"
    assert result["position_id"] == "POSITION001"


def test_position_manager_called_once():
    runner, strategy, _, adapter = create_runner()

    strategy.decide.return_value = FakeDecision()

    runner.risk_engine = Mock()
    runner.risk_engine.evaluate.return_value = FakeRisk()

    trade = FakeTrade()
    order = FakeOrder()

    runner.trade_factory = Mock()
    runner.trade_factory.create.return_value = trade

    runner.order_factory = Mock()
    runner.order_factory.create.return_value = order

    runner.position_manager = Mock()
    runner.position_manager.open_position.return_value = FakePosition()

    adapter.to_execution_order.return_value = object()
    adapter.execute.return_value = "OK"

    market, indicators = create_market_and_indicators()

    runner.run(
        market,
        indicators,
    )

    runner.position_manager.open_position.assert_called_once_with(
        order,
        order.quantity,
        100,
    )


def test_execution_manager_called_when_available():
    strategy = Mock()
    risk_engine = Mock()
    adapter = Mock()
    execution_manager = Mock()

    runner = PaperTradeRunner(
        strategy_engine=strategy,
        risk_engine=risk_engine,
        order_execution_adapter=adapter,
        execution_manager=execution_manager,
    )

    strategy.decide.return_value = FakeDecision()

    risk = FakeRisk()
    risk_engine.evaluate.return_value = risk

    execution_manager.execute.return_value = {
        "status": "EXECUTED",
    }

    market, indicators = create_market_and_indicators()

    result = runner.run(
        market,
        indicators,
    )

    execution_manager.execute.assert_called_once_with(risk)

    assert result == {
        "status": "EXECUTED",
    }


def test_runner_uses_execution_manager_when_configured():
    strategy = Mock()
    risk_engine = Mock()
    execution_manager = Mock()

    decision = Mock()
    risk = Mock()
    risk.is_approved = True

    strategy.decide.return_value = decision
    risk_engine.evaluate.return_value = risk
    execution_manager.execute.return_value = {"status": "OK"}

    runner = PaperTradeRunner(
        strategy_engine=strategy,
        risk_engine=risk_engine,
        order_execution_adapter=Mock(),
        execution_manager=execution_manager,
    )

    result = runner.run(Mock(), Mock())

    execution_manager.execute.assert_called_once_with(risk)
    assert result == {"status": "OK"}
